"""Executes pending (model, question, attempt) triples and records each one."""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from .control import StopControl
from .providers import ProviderError, TimeLimitExceeded, complete
from .report import write_report
from .store import Run, is_error, now_iso
from .task import Question, Task, get_task
from .util import fmt_duration, sha256_file

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
    t0 = time.monotonic()
    try:
        c = complete(model, task.build_messages(q, run.prompt), run.config["generation"],
                     log=lambda m: print(f"{_ts()}  [{alias}] Q{q.id} #{attempt}{m}", flush=True))
    except TimeLimitExceeded as e:  # a runaway reply: counts as wrong, like hitting max tokens
        rec.update(status="truncated", extracted=None, correct=False, content="",
                   finish_reason="time_limit", error=str(e),
                   duration_s=round(time.monotonic() - t0, 2))
        return rec
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


def _ts() -> str:
    """Clock time prefix for progress lines, so the gap since the previous line is visible."""
    return datetime.now().strftime("%H:%M:%S")


def _line(rec: dict, done: int, total: int) -> str:
    head = f"{_ts()}  [{rec['model']}] {done}/{total}  Q{rec['question_id']} #{rec['attempt']}: "
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


ORDERS = ("rounds", "models")


def choose_order(run: Run, aliases: list[str], override: str | None) -> str:
    """rounds: repeat-major (every model answers every question, then the next repeat), so the
    leaderboard is meaningful after each round; best for slow sequential local models.
    models: model-major, each model's parallel pool draws from all its pending attempts, so one
    slow reply never leaves the other workers idle; best for cloud models."""
    if override:
        return override
    return "rounds" if any(run.models[a]["provider"] == "ollama" for a in aliases) else "models"


def run_benchmark(run: Run, only_models: list[str] | None = None,
                  concurrency: int | None = None, order: str | None = None,
                  max_duration: float | None = None) -> None:
    task = get_task(run.config["task"])
    questions = load_run_questions(run, task)
    aliases = only_models or list(run.models)
    unknown = [a for a in aliases if a not in run.models]
    if unknown:
        raise SystemExit(f"Not in benchmark '{run.name}': {', '.join(unknown)}")

    finished = {k for k, r in run.latest().items() if not is_error(r)}
    order = choose_order(run, aliases, order)
    session = None
    try:
        with StopControl(run.path) as stop:
            session = _Session(run, task, questions, stop, concurrency, max_duration)
            print(f"Order: {order} ({run.config['repeats']} repeats, {len(aliases)} models)",
                  flush=True)
            if order == "rounds":
                stopped = session.by_rounds(aliases, finished)
            else:
                stopped = session.by_models(aliases, finished)
    except KeyboardInterrupt:
        print("\nInterrupted. Finished attempts are saved; 'bench run "
              f"{run.name}' resumes the rest.", flush=True)
        if session:
            session.save("interrupted")
        write_report(run, questions, quiet=True)
        sys.stdout.flush()
        os._exit(130)  # don't wait for in-flight HTTP requests
    if stopped:
        print(f"\nStopped. Finished attempts are saved; 'bench run {run.name}' resumes the rest.")
    print()
    session.save("stopped" if stopped else "completed")
    write_report(run, questions)
    session.print_summary()


class _Session:
    """One `bench` invocation: executes attempts and tracks its wall time."""

    def __init__(self, run: Run, task: Task, questions: list[Question], stop, concurrency,
                 max_duration=None):
        self.run, self.task, self.questions, self.stop = run, task, questions, stop
        self.concurrency = concurrency
        self.max_duration = max_duration  # session override of each model's max_duration
        self.started = now_iso()
        self.t0 = time.monotonic()
        self.attempts = 0
        self.saved = False

    def since_start(self) -> str:
        return fmt_duration(time.monotonic() - self.t0)

    # ------------------------------------------------------------ orders
    def by_models(self, aliases: list[str], finished: set) -> bool:
        repeats = self.run.config["repeats"]
        for idx, alias in enumerate(aliases, 1):
            if self.stop.requested:
                return True
            # attempt-major within the model: a partial run still covers every question evenly
            pending = [(q, a) for a in range(1, repeats + 1) for q in self.questions
                       if (alias, q.id, a) not in finished]
            tag = f"Model {idx}/{len(aliases)} [{alias}]"
            if not pending:
                print(f"{tag} complete, nothing to do")
                continue
            print()
            if self._batch(alias, pending, tag):
                return True
        return False

    def by_rounds(self, aliases: list[str], finished: set) -> bool:
        repeats = self.run.config["repeats"]
        for a in range(1, repeats + 1):
            work = [(alias, [(q, a) for q in self.questions if (alias, q.id, a) not in finished])
                    for alias in aliases]
            if not any(items for _, items in work):
                print(f"Round {a}/{repeats} complete, nothing to do")
                continue
            print(f"\n{_ts()} === Round {a}/{repeats} ===", flush=True)
            for idx, (alias, items) in enumerate(work, 1):
                if self.stop.requested:
                    return True
                if items and self._batch(alias, items, f"Model {idx}/{len(aliases)} [{alias}]"):
                    return True
            self.report()
            print(f"{_ts()} === Round {a}/{repeats} done · {self.since_start()} since start · "
                  f"leaderboard updated ===", flush=True)
        return False

    # ------------------------------------------------------------ execution
    def _batch(self, alias: str, items: list[tuple], header: str) -> bool:
        """Runs one model's attempts. Returns True if a stop request skipped any of them."""
        run, model = self.run, self.run.models[alias]
        if self.max_duration:
            model = {**model, "max_duration": self.max_duration}
        conc = effective_concurrency(model, self.concurrency)
        limit = f", max {fmt_duration(model['max_duration'])}" if model.get("max_duration") else ""
        print(f"{_ts()} {header} {len(items)} attempts pending "
              f"({model['provider']}: {model['model']}, concurrency {conc}{limit})", flush=True)
        t0 = time.monotonic()
        done = 0
        skipped = False

        def record(rec: dict) -> None:
            nonlocal done
            run.append(rec)
            self.attempts += 1
            done += 1
            print(_line(rec, done, len(items)), flush=True)

        def guarded(q, a):
            if self.stop.requested:  # checked when a worker picks the attempt up, not when queued
                return None
            return _attempt(run, self.task, alias, model, q, a)

        if conc <= 1:
            for q, a in items:
                if self.stop.requested:
                    skipped = True
                    break
                record(_attempt(run, self.task, alias, model, q, a))
        else:
            ex = ThreadPoolExecutor(conc)
            try:
                for f in as_completed([ex.submit(guarded, q, a) for q, a in items]):
                    if (rec := f.result()) is None:
                        skipped = True
                    else:
                        record(rec)
            finally:
                ex.shutdown(wait=False, cancel_futures=True)
        if done:
            print(f"{_ts()}  [{alias}] {done} attempts in {fmt_duration(time.monotonic() - t0)} · "
                  f"{self.since_start()} since start", flush=True)
        if not skipped:
            self.report()  # keep leaderboard.md current
        return skipped

    def info(self, status: str = "running") -> dict:
        return {"start": self.started, "end": now_iso(),
                "wall_s": round(time.monotonic() - self.t0, 1), "attempts": self.attempts,
                "status": status}

    def report(self) -> None:
        write_report(self.run, self.questions, quiet=True,
                     live=None if self.saved else self.info())

    def save(self, status: str) -> None:
        """Append this session to sessions.jsonl (only if it did any work)."""
        if self.attempts and not self.saved:
            self.run.add_session(self.info(status))
        self.saved = True

    def print_summary(self) -> None:
        wall = time.monotonic() - self.t0
        print(f"This session: {fmt_duration(wall)} ({self.attempts} attempts) · "
              f"Benchmark total: {self.run.time_summary() or '0s'}", flush=True)
