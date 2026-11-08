"""Executes pending (model, question, attempt) triples and records each one."""
from __future__ import annotations

import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from .control import StopControl
from .providers import ProviderError, complete
from .report import write_report
from .store import Run, is_error, now_iso
from .task import Question, Task, get_task
from .util import sha256_file

DEFAULT_CONCURRENCY = {"ollama": 1, "openrouter": 4}


def load_run_questions(run: Run, task: Task) -> list[Question]:
    ds = run.dataset_path
    if not ds.exists():
        raise SystemExit(f"Dataset not found: {ds}")
    if sha256_file(ds) != run.config["dataset_sha256"]:
        raise SystemExit(f"Dataset {ds} changed since benchmark '{run.name}' was created. "
                         f"Start a new benchmark instead (results would not be comparable).")
    qs = task.load_questions(ds)
    ids = run.config.get("question_ids")
    if ids:
        qs = [q for q in qs if q.id in set(ids)]
    return qs


def _attempt(run: Run, task: Task, alias: str, model: dict, q: Question, attempt: int) -> dict:
    rec = {
        "ts": now_iso(), "model": alias, "question_id": q.id, "attempt": attempt,
        "expected": q.answer,
    }
    try:
        c = complete(model, task.build_messages(q, run.prompt), run.config["generation"],
                     log=lambda m: print(f"  [{alias}] Q{q.id} #{attempt}{m}", flush=True))
    except ProviderError as e:
        rec.update(status="error", extracted=None, correct=False, error=str(e))
        return rec
    extracted = task.extract(c.content, q)
    if extracted is not None:
        status = "answered"
    else:
        status = "truncated" if c.truncated else "unparsed"
    rec.update(
        status=status, extracted=extracted, correct=extracted == q.answer,
        content=c.content, reasoning=c.reasoning, finish_reason=c.finish_reason,
        prompt_tokens=c.prompt_tokens, completion_tokens=c.completion_tokens,
        reasoning_tokens=c.reasoning_tokens, cost=c.cost, served_by=c.served_by,
        duration_s=c.duration_s,
    )
    return rec


def _line(rec: dict, done: int, total: int) -> str:
    head = f"  [{rec['model']}] {done}/{total}  Q{rec['question_id']} #{rec['attempt']}: "
    st = rec["status"]
    if st == "error":
        return head + f"ERROR {rec['error'][:150]}"
    mark = "OK " if rec["correct"] else "x  "
    got = rec["extracted"] or f"<{st}>"
    extra = f"{rec['duration_s']:.1f}s"
    if rec.get("completion_tokens"):
        extra += f", {rec['completion_tokens']} tok"
    if rec.get("cost"):
        extra += f", ${rec['cost']:.4f}"
    return head + f"{mark}{got} (expected {rec['expected']}; {extra})"


def effective_concurrency(model: dict, override: int | None) -> int:
    """--concurrency applies to OpenRouter models only; a model's own lower value still wins.

    Ollama models are excluded: a local server queues parallel requests, so they would only
    inflate measured times and risk hitting the request timeout.
    """
    own = model.get("concurrency")
    if override is None or model["provider"] != "openrouter":
        return own or DEFAULT_CONCURRENCY[model["provider"]]
    return min(own, override) if own else override


def run_benchmark(run: Run, only_models: list[str] | None = None,
                  concurrency: int | None = None) -> None:
    task = get_task(run.config["task"])
    questions = load_run_questions(run, task)
    repeats = run.config["repeats"]
    aliases = only_models or list(run.models)
    unknown = [a for a in aliases if a not in run.models]
    if unknown:
        raise SystemExit(f"Not in benchmark '{run.name}': {', '.join(unknown)}")

    finished = {k for k, r in run.latest().items() if not is_error(r)}
    with StopControl(run.path) as stop:
        stopped = _run_models(run, task, questions, repeats, aliases, finished, stop,
                              concurrency)
    if stopped:
        print(f"\nStopped. Finished attempts are saved; 'bench run {run.name}' resumes the rest.\n")
    else:
        print()
    write_report(run, questions)


def _run_models(run, task, questions, repeats, aliases, finished, stop, concurrency) -> bool:
    """Returns True if stopped early by a graceful stop request."""

    def guarded(alias, model, q, a):
        if stop.requested:  # checked when a worker picks the attempt up, not when queued
            return None
        return _attempt(run, task, alias, model, q, a)

    try:
        for idx, alias in enumerate(aliases, 1):
            if stop.requested:
                return True
            model = run.models[alias]
            # attempt-major order: a partial run still covers every question evenly
            pending = [(q, a) for a in range(1, repeats + 1) for q in questions
                       if (alias, q.id, a) not in finished]
            tag = f"Model {idx}/{len(aliases)} [{alias}]"
            if not pending:
                print(f"{tag} complete, nothing to do")
                continue
            conc = effective_concurrency(model, concurrency)
            print(f"\n{tag} {len(pending)} attempts pending "
                  f"({model['provider']}: {model['model']}, concurrency {conc})", flush=True)
            done = 0
            if conc <= 1:
                for q, a in pending:
                    if stop.requested:
                        return True
                    rec = _attempt(run, task, alias, model, q, a)
                    run.append(rec)
                    done += 1
                    print(_line(rec, done, len(pending)), flush=True)
            else:
                with ThreadPoolExecutor(conc) as ex:
                    futs = [ex.submit(guarded, alias, model, q, a) for q, a in pending]
                    for f in as_completed(futs):
                        rec = f.result()
                        if rec is None:
                            continue
                        run.append(rec)
                        done += 1
                        print(_line(rec, done, len(pending)), flush=True)
                if stop.requested:
                    return True
    except KeyboardInterrupt:
        print("\nInterrupted. Finished attempts are saved; 'bench run "
              f"{run.name}' resumes the rest.", flush=True)
        write_report(run, questions, quiet=True)
        sys.stdout.flush()
        os._exit(130)  # don't wait for in-flight HTTP requests
    return False
