"""Command-line interface: `uv run bench <command> ...`"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .registry import load_registry, resolve
from .report import write_report
from .control import STOP_FILE
from .runner import ORDERS, load_run_questions, run_benchmark
from .store import CONFIG, Run, is_error
from .task import all_tasks, get_task
from .util import ROOT, load_env


def _csv(s: str | None) -> list[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def cmd_new(a) -> None:
    task = get_task(a.task)
    default_profile, profiles = task.profiles()
    profile_name = a.profile or default_profile
    if profile_name not in profiles:
        raise SystemExit(f"Unknown prompt profile '{profile_name}'. Known: {', '.join(profiles)}")
    dataset = Path(a.dataset) if a.dataset else task.dir / task.default_dataset
    qids = None
    if a.questions:
        all_ids = {q.id for q in task.load_questions(dataset)}
        qids = [int(x) if x.isdigit() else x for x in _csv(a.questions)]
        if bad := [x for x in qids if x not in all_ids]:
            raise SystemExit(f"Question ids not in dataset: {bad}")
    models = resolve(_csv(a.models))
    run = Run.create(task, a.name, dataset=dataset, profile_name=profile_name,
                     profile=profiles[profile_name], repeats=a.repeats,
                     temperature=a.temperature, max_tokens=a.max_tokens,
                     question_ids=qids, models=models)
    print(f"Created benchmark '{a.name}' at {run.path}")
    if not a.no_run:
        run_benchmark(run, concurrency=a.concurrency, order=a.order)


def cmd_add(a) -> None:
    run = Run.find(a.name, a.task)
    added = run.add_models(resolve(_csv(a.models)))
    print(f"Added to '{run.name}': {', '.join(added) or '(nothing new)'}")
    if added and not a.no_run:
        run_benchmark(run, only_models=added, concurrency=a.concurrency, order=a.order)


def cmd_run(a) -> None:
    run = Run.find(a.name, a.task)
    run_benchmark(run, only_models=_csv(a.models) or None, concurrency=a.concurrency,
                  order=a.order)


def cmd_extend(a) -> None:
    run = Run.find(a.name, a.task)
    before = run.config["repeats"]
    run.set_repeats(a.repeats)
    if a.repeats == before:
        print(f"'{run.name}' already has {before} repeats")
    else:
        print(f"'{run.name}': repeats {before} -> {a.repeats}")
    if not a.no_run:
        run_benchmark(run, concurrency=a.concurrency, order=a.order)


def cmd_report(a) -> None:
    run = Run.find(a.name, a.task)
    write_report(run, load_run_questions(run, get_task(run.config["task"])))


def cmd_stop(a) -> None:
    run = Run.find(a.name, a.task)
    (run.path / STOP_FILE).touch()
    print(f"Stop requested for '{run.name}'. It stops once the current attempt(s) finish "
          f"(only if it's running now; the request is cleared on the next start).")


def cmd_list(a) -> None:
    found = False
    for task in all_tasks():
        if not task.runs_dir.exists():
            continue
        for p in sorted(task.runs_dir.iterdir()):
            if not (p / CONFIG).exists():
                continue
            found = True
            run = Run(p)
            c = run.config
            nq = len(c.get("question_ids") or task.load_questions(run.dataset_path))
            expected = nq * c["repeats"] * len(run.models)
            done = sum(1 for r in run.latest().values() if not is_error(r))
            print(f"{task.name:12} {c['name']:28} {len(run.models):2} models  "
                  f"repeats={c['repeats']}  profile={c['prompt_profile']:12} "
                  f"progress {done}/{expected}  created {c['created'][:16]}")
    if not found:
        print("No benchmarks yet. Create one with 'bench new <name> --models ...'.")


def cmd_models(a) -> None:
    for alias, m in load_registry().items():
        print(f"{alias:28} {m['provider']:11} {m['model']}")


def main(argv: list[str] | None = None) -> None:
    load_env()
    p = argparse.ArgumentParser(prog="bench", description="Run personal LLM benchmarks.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("new", help="create a new benchmark and run it")
    s.add_argument("name", help="benchmark name (folder under <Task>/runs/)")
    s.add_argument("--models", required=True, help="comma-separated aliases from models.yaml")
    s.add_argument("--task", default="simplebench")
    s.add_argument("--repeats", type=int, default=1, help="times each question is asked")
    s.add_argument("--profile", help="prompt profile from <Task>/prompts.yaml")
    s.add_argument("--temperature", type=float, help="default: provider/model default")
    s.add_argument("--max-tokens", type=int, help="default: no explicit limit")
    s.add_argument("--questions", help="comma-separated question ids (default: all)")
    s.add_argument("--dataset", help="dataset file (default: the task's bundled one)")
    s.add_argument("--no-run", action="store_true", help="only create, don't run yet")
    s.add_argument("--concurrency", type=int, help="parallel requests per OpenRouter model (default 4; a model's own lower value wins; Ollama unaffected)")
    s.add_argument("--order", choices=ORDERS, help="rounds: all models per repeat, leaderboard after each round; models: one model at a time (default: rounds if any Ollama model, else models)")
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("add", help="add models to an existing benchmark and run only them")
    s.add_argument("name")
    s.add_argument("--models", required=True)
    s.add_argument("--task")
    s.add_argument("--no-run", action="store_true")
    s.add_argument("--concurrency", type=int, help="parallel requests per OpenRouter model (default 4; a model's own lower value wins; Ollama unaffected)")
    s.add_argument("--order", choices=ORDERS, help="rounds: all models per repeat, leaderboard after each round; models: one model at a time (default: rounds if any Ollama model, else models)")
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("run", help="run/resume pending attempts (also retries errors)")
    s.add_argument("name")
    s.add_argument("--models", help="limit to these aliases")
    s.add_argument("--task")
    s.add_argument("--concurrency", type=int, help="parallel requests per OpenRouter model (default 4; a model's own lower value wins; Ollama unaffected)")
    s.add_argument("--order", choices=ORDERS, help="rounds: all models per repeat, leaderboard after each round; models: one model at a time (default: rounds if any Ollama model, else models)")
    s.set_defaults(fn=cmd_run)

    s = sub.add_parser("extend", help="raise the number of repeats and run the new rounds")
    s.add_argument("name")
    s.add_argument("--repeats", type=int, required=True, help="new total number of repeats")
    s.add_argument("--task")
    s.add_argument("--no-run", action="store_true")
    s.add_argument("--concurrency", type=int, help="parallel requests per OpenRouter model (default 4; a model's own lower value wins; Ollama unaffected)")
    s.add_argument("--order", choices=ORDERS, help="rounds: all models per repeat, leaderboard after each round; models: one model at a time (default: rounds if any Ollama model, else models)")
    s.set_defaults(fn=cmd_extend)

    s = sub.add_parser("report", help="rebuild and print the leaderboard")
    s.add_argument("name")
    s.add_argument("--task")
    s.set_defaults(fn=cmd_report)

    s = sub.add_parser("stop", help="stop a running benchmark after its current attempt(s)")
    s.add_argument("name")
    s.add_argument("--task")
    s.set_defaults(fn=cmd_stop)

    sub.add_parser("list", help="list benchmarks").set_defaults(fn=cmd_list)
    sub.add_parser("models", help="list models in models.yaml").set_defaults(fn=cmd_models)

    args = p.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args.fn(args)


if __name__ == "__main__":
    main()
