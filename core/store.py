"""A benchmark run on disk: frozen config.yaml + append-only results.jsonl."""
from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path

from .task import Task, all_tasks
from .util import ROOT, fmt_duration, read_yaml, sha256_file, write_yaml

CONFIG = "config.yaml"
RESULTS = "results.jsonl"
REPORT = "leaderboard.md"
SESSIONS = "sessions.jsonl"  # one line per `bench new/add/run/extend` session that did work


def is_error(rec: dict) -> bool:
    """An attempt that produced no usable reply: not scored, retried by `bench run`.

    Also covers replies recorded before these cases became errors: host aborts
    (finish_reason "error") and OpenRouter replies that "stop" with reasoning but no answer.
    """
    if rec["status"] == "error" or rec.get("finish_reason") == "error":
        return True
    return (rec.get("finish_reason") == "stop" and rec.get("served_by") != "ollama"
            and bool(rec.get("reasoning")) and not (rec.get("content") or "").strip())


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


class Run:
    def __init__(self, path: Path):
        self.path = path
        self.config: dict = read_yaml(path / CONFIG)
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- creation / lookup
    @classmethod
    def create(cls, task: Task, name: str, *, dataset: Path, profile_name: str, profile: dict,
               repeats: int, temperature, max_tokens, question_ids, models: dict) -> "Run":
        path = task.runs_dir / name
        if path.exists():
            raise SystemExit(f"Benchmark '{name}' already exists at {path}. "
                             f"Use 'bench add' to add models, or pick another name.")
        path.mkdir(parents=True)
        try:
            rel = dataset.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            rel = str(dataset.resolve())
        config = {
            "task": task.name,
            "name": name,
            "created": now_iso(),
            "dataset": rel,
            "dataset_sha256": sha256_file(dataset),
            "question_ids": question_ids,  # null = all questions
            "repeats": repeats,
            "prompt_profile": profile_name,
            "system_prompt": profile.get("system"),
            "user_suffix": profile.get("suffix"),
            "generation": {"temperature": temperature, "max_tokens": max_tokens},
            "models": {alias: {**d, "added": now_iso()} for alias, d in models.items()},
        }
        write_yaml(path / CONFIG, config)
        (path / RESULTS).touch()
        return cls(path)

    @classmethod
    def find(cls, name: str, task_name: str | None = None) -> "Run":
        hits = [t.runs_dir / name for t in all_tasks()
                if (task_name is None or t.name == task_name) and (t.runs_dir / name / CONFIG).exists()]
        if not hits:
            raise SystemExit(f"No benchmark named '{name}'. See 'bench list'.")
        if len(hits) > 1:
            raise SystemExit(f"'{name}' exists in several tasks; pass --task.")
        return cls(hits[0])

    # ---------------------------------------------------------------- config helpers
    @property
    def name(self) -> str:
        return self.config["name"]

    @property
    def models(self) -> dict[str, dict]:
        return self.config["models"]

    @property
    def dataset_path(self) -> Path:
        p = Path(self.config["dataset"])
        return p if p.is_absolute() else ROOT / p

    @property
    def prompt(self) -> dict:
        return {"system": self.config.get("system_prompt"), "suffix": self.config.get("user_suffix")}

    def add_models(self, models: dict[str, dict]) -> list[str]:
        added = []
        for alias, d in models.items():
            if alias in self.models:
                print(f"  '{alias}' is already in this benchmark (kept its frozen definition)")
                continue
            self.config["models"][alias] = {**d, "added": now_iso()}
            added.append(alias)
        write_yaml(self.path / CONFIG, self.config)
        return added

    def set_repeats(self, repeats: int) -> None:
        """Raise the number of repeats. More samples of the same setup keep results comparable."""
        current = self.config["repeats"]
        if repeats < current:
            raise SystemExit(f"'{self.name}' already has {current} repeats; it can only grow "
                             f"(lowering it would hide recorded attempts).")
        self.config["repeats"] = repeats
        write_yaml(self.path / CONFIG, self.config)

    # ---------------------------------------------------------------- sessions (wall time)
    def add_session(self, session: dict) -> None:
        with open(self.path / SESSIONS, "a", encoding="utf-8") as f:
            f.write(json.dumps(session, ensure_ascii=False) + "\n")

    def sessions(self) -> list[dict]:
        p = self.path / SESSIONS
        if not p.exists():
            return []
        with open(p, encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def time_summary(self, live: dict | None = None) -> str | None:
        """Total wall time over all sessions, pauses between them excluded.

        `live` is the session still running (not yet in sessions.jsonl), if any.
        """
        sessions = self.sessions() + ([live] if live and live["attempts"] else [])
        n_records = len(self.records())
        if not sessions:
            return "untracked" if n_records else None
        total = sum(s["wall_s"] for s in sessions)
        text = f"{fmt_duration(total)} over {len(sessions)} session" + ("s" if len(sessions) > 1 else "")
        if sum(s["attempts"] for s in sessions) < n_records:
            text += " (+ earlier untracked sessions)"
        return text

    # ---------------------------------------------------------------- results
    def append(self, record: dict) -> None:
        line = json.dumps(record, ensure_ascii=False)
        with self._lock, open(self.path / RESULTS, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()

    def records(self) -> list[dict]:
        out = []
        p = self.path / RESULTS
        if not p.exists():
            return out
        with open(p, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"  warning: skipping corrupt line {n} in {p.name}")
        return out

    def latest(self) -> dict[tuple, dict]:
        """Latest record per (model, question_id, attempt); later lines supersede earlier ones."""
        return {(r["model"], r["question_id"], r["attempt"]): r for r in self.records()}
