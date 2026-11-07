"""Leaderboard computation and Markdown rendering."""
from __future__ import annotations

import statistics
from collections import Counter

from .store import REPORT, Run, now_iso
from .task import Question


def model_stats(run: Run, alias: str, questions: list[Question], latest: dict) -> dict:
    repeats = run.config["repeats"]
    expected = len(questions) * repeats
    recs = [latest[k] for q in questions for a in range(1, repeats + 1)
            if (k := (alias, q.id, a)) in latest]
    scored = [r for r in recs if r["status"] != "error"]
    points = sum(1 for r in scored if r["correct"])
    status = Counter(r["status"] for r in recs)

    # points per repeat round (only rounds where every question was scored)
    rounds = []
    for a in range(1, repeats + 1):
        rr = [latest.get((alias, q.id, a)) for q in questions]
        if all(r is not None and r["status"] != "error" for r in rr):
            rounds.append(sum(1 for r in rr if r["correct"]))

    # majority vote: a question counts if the correct letter is the unique most common answer
    majority = 0
    per_q = {}
    for q in questions:
        qr = [r for r in scored if r["question_id"] == q.id]
        per_q[q.id] = (sum(1 for r in qr if r["correct"]), len(qr))
        votes = Counter(r["extracted"] for r in qr).most_common()
        if votes and votes[0][0] == q.answer and (len(votes) == 1 or votes[1][1] < votes[0][1]):
            majority += 1

    durations = [r["duration_s"] for r in scored if r.get("duration_s") is not None]
    tokens = [r["completion_tokens"] for r in scored if r.get("completion_tokens")]
    costs = [r["cost"] for r in recs if r.get("cost") is not None]
    return {
        "alias": alias,
        "points": points,
        "scored": len(scored),
        "expected": expected,
        "pct": 100 * points / len(scored) if scored else 0.0,
        "rounds": rounds,
        "majority": majority,
        "per_q": per_q,
        "unparsed": status["unparsed"],
        "truncated": status["truncated"],
        "errors": status["error"],
        "avg_s": statistics.mean(durations) if durations else None,
        "avg_tok": statistics.mean(tokens) if tokens else None,
        "cost": sum(costs) if costs else None,
    }


def _fmt_rounds(rounds: list[int], n: int) -> str:
    if not rounds:
        return "–"
    if len(rounds) == 1:
        return f"{rounds[0]}/{n}"
    return f"{statistics.mean(rounds):.1f} ± {statistics.stdev(rounds):.1f}"


def render(run: Run, questions: list[Question]) -> str:
    latest = run.latest()
    nq = len(questions)
    cfg = run.config
    stats = [model_stats(run, a, questions, latest) for a in run.models]
    stats.sort(key=lambda s: (-s["pct"], -s["points"], s["alias"]))

    out = [f"# {cfg['task']} — {cfg['name']}", ""]
    gen = cfg.get("generation") or {}
    out += [
        f"- Created: {cfg['created']} · Updated: {now_iso()}",
        f"- Dataset: `{cfg['dataset']}` ({nq} questions) · Repeats: {cfg['repeats']} "
        f"· Max points per model: {nq * cfg['repeats']}",
        f"- Prompt profile: `{cfg['prompt_profile']}` · Temperature: {gen.get('temperature')} "
        f"· Max tokens: {gen.get('max_tokens')}",
        "",
        "| # | Model | Points | Score | Per round (of "
        f"{nq}) | Majority vote | Unparsed | Truncated | Errors | Avg time | Avg out tok | Cost |",
        "|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for i, s in enumerate(stats, 1):
        pts = f"{s['points']}/{s['scored']}"
        if s["scored"] < s["expected"]:
            pts += f" (of {s['expected']})"
        out.append("| " + " | ".join([
            str(i), s["alias"], pts, f"{s['pct']:.1f}%", _fmt_rounds(s["rounds"], nq),
            f"{s['majority']}/{nq}", str(s["unparsed"]), str(s["truncated"]), str(s["errors"]),
            f"{s['avg_s']:.1f}s" if s["avg_s"] is not None else "–",
            f"{s['avg_tok']:.0f}" if s["avg_tok"] is not None else "–",
            f"${s['cost']:.4f}" if s["cost"] is not None else "–",
        ]) + " |")

    out += ["", "## Per question (correct / attempts)", "",
            "| Model | " + " | ".join(f"Q{q.id} ({q.answer})" for q in questions) + " |",
            "|---|" + "--:|" * nq]
    for s in stats:
        cells = [f"{c}/{n}" if n else "–" for c, n in (s["per_q"][q.id] for q in questions)]
        out.append(f"| {s['alias']} | " + " | ".join(cells) + " |")

    out += ["", "## Models", "", "| Model | Provider | Model id | Settings |", "|---|---|---|---|"]
    for s in stats:
        m = run.models[s["alias"]]
        skip = {"provider", "model", "added"}
        settings = ", ".join(f"{k}={v}" for k, v in m.items() if k not in skip) or "–"
        out.append(f"| {s['alias']} | {m['provider']} | `{m['model']}` | {settings} |")

    out += [
        "",
        "_Score = points / scored attempts. Errors (API failures) are not scored and are retried "
        "by `bench run`; unparsed and truncated replies count as wrong. Per round = mean ± SD of "
        "points per full pass over the questions. Majority vote = questions where the correct "
        "letter was the single most common answer._",
        "",
    ]
    return "\n".join(out)


def write_report(run: Run, questions: list[Question], quiet: bool = False) -> str:
    text = render(run, questions)
    (run.path / REPORT).write_text(text, encoding="utf-8")
    if not quiet:
        print(text)
        print(f"Saved to {run.path / REPORT}")
    return text
