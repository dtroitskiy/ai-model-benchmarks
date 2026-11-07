"""SimpleBench task definition."""
from __future__ import annotations

import json
from pathlib import Path

from core.task import Question, Task, option_letters


class SimpleBenchTask(Task):
    name = "simplebench"
    dir = Path(__file__).resolve().parent
    default_dataset = "simple_bench_public.json"

    def load_questions(self, dataset: Path) -> list[Question]:
        data = json.loads(dataset.read_text(encoding="utf-8"))
        return [
            Question(
                id=item["question_id"],
                prompt=item["prompt"],
                answer=item["answer"].strip().upper(),
                choices=option_letters(item["prompt"]),
            )
            for item in data["eval_data"]
        ]
