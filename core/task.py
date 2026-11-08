"""Task interface + a generic multiple-choice implementation that benchmarks can reuse."""
from __future__ import annotations

import importlib
import re
from dataclasses import dataclass
from pathlib import Path

from .util import read_yaml


@dataclass
class Question:
    id: int | str
    prompt: str
    answer: str
    choices: list[str]


class Task:
    """A benchmark type (e.g. SimpleBench). Each benchmark *run* lives in <dir>/runs/<name>/."""
    name: str = ""
    dir: Path = Path()
    default_dataset: str = ""

    @property
    def runs_dir(self) -> Path:
        return self.dir / "runs"

    def load_questions(self, dataset: Path) -> list[Question]:
        raise NotImplementedError

    def profiles(self) -> tuple[str, dict]:
        """Return (default profile name, {name: {system, suffix}})."""
        data = read_yaml(self.dir / "prompts.yaml")
        return data.get("default"), data["profiles"]

    def build_messages(self, q: Question, prompt: dict) -> list[dict]:
        user = q.prompt.rstrip()
        if prompt.get("suffix"):
            user += "\n\n" + prompt["suffix"].strip()
        msgs = []
        if prompt.get("system"):
            msgs.append({"role": "system", "content": prompt["system"].strip()})
        msgs.append({"role": "user", "content": user})
        return msgs

    def extract(self, text: str, q: Question) -> str | None:
        return extract_choice(text, q.choices)


# ----------------------------------------------------------------- answer extraction

_THINK_BLOCK = re.compile(r"<think(?:ing)?>.*?</think(?:ing)?>", re.S | re.I)
_OPEN = r"[\s*_`\"'(\[]*"
_CLOSE = r"[\s*_`\"'.)\]:]*"


def option_letters(prompt: str) -> list[str]:
    return re.findall(r"^([A-Z])[.)]\s", prompt, re.M)


def extract_choice(text: str, letters: list[str]) -> str | None:
    """Pull the chosen option letter out of a model's final reply, or None if unclear."""
    if not text:
        return None
    t = _THINK_BLOCK.sub("", text)
    if re.search(r"</think(?:ing)?>", t, re.I):  # unbalanced: keep text after the last close tag
        t = re.split(r"</think(?:ing)?>", t, flags=re.I)[-1]
    t = t.strip()
    cls = "[" + "".join(letters or "ABCDEF") + "]"

    # 1. The whole reply is just the letter (possibly decorated: **B**, (B), "B.", `B`)
    if m := re.fullmatch(rf"{_OPEN}({cls}){_CLOSE}", t):
        return m[1]
    # 1b. Explanation followed by the letter alone on the last line
    last = t.splitlines()[-1] if t else ""
    if m := re.fullmatch(rf"{_OPEN}({cls}){_CLOSE}", last):
        return m[1]
    # 1c. The letter alone on the first line, followed by an explanation
    first = t.splitlines()[0] if t else ""
    if m := re.fullmatch(rf"{_OPEN}({cls}){_CLOSE}", first):
        return m[1]
    # 2. Explicit answer markers, last occurrence wins
    for pat in (
        rf"\\boxed\{{\s*(?:\\text\{{)?\s*({cls})\b",
        rf"(?i:final\s+answer)\s*(?:(?i:is))?\s*[:\-]?{_OPEN}({cls})\b",
        rf"(?i:\banswer)\s*(?:(?i:is)|:)\s*(?:(?i:option))?{_OPEN}({cls})\b",
        rf"\*\*\s*({cls})\s*[.):]?\s*\*\*",
    ):
        if found := re.findall(pat, t):
            return found[-1]
    # 3. Reply starts with the letter followed by punctuation, e.g. "B. 0" or "C) inside"
    if m := re.match(rf"{_OPEN}({cls})[.):\]]", t):
        return m[1]
    return None


# ----------------------------------------------------------------- task registry

TASKS = {
    "simplebench": "SimpleBench.task:SimpleBenchTask",
}


def get_task(name: str) -> Task:
    if name not in TASKS:
        raise SystemExit(f"Unknown task '{name}'. Known: {', '.join(TASKS)}")
    module, cls = TASKS[name].split(":")
    return getattr(importlib.import_module(module), cls)()


def all_tasks() -> list[Task]:
    return [get_task(n) for n in TASKS]
