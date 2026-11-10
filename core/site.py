"""Static site for GitHub Pages: a home page plus one leaderboard page per benchmark.

Layout (short URLs): <out>/index.html, <out>/<task>/<benchmark>/index.html.
Only HTML is published; results.jsonl files (full reasoning text) stay in the repository.
"""
from __future__ import annotations

import shutil
from html import escape
from pathlib import Path

from .report import compute_stats
from .report_html import CSS, render_html
from .runner import load_run_questions
from .store import CONFIG, Run, is_error, now_iso
from .task import all_tasks

HOME_CSS = """
.task { margin-top: 28px; }
td.name a { font-weight: 600; }
.prog { display: flex; align-items: center; gap: 8px; justify-content: flex-end; }
.leader { text-align: left; }
.empty-note { color: var(--muted); }
"""


def _benchmark_rows(out: Path) -> dict[str, list[dict]]:
    """Writes every benchmark page; returns summary rows per task for the home page."""
    rows: dict[str, list[dict]] = {}
    for task in all_tasks():
        if not task.runs_dir.exists():
            continue
        for path in sorted(task.runs_dir.iterdir()):
            if not (path / CONFIG).exists() or path.name.startswith("_"):
                continue  # names starting with "_" are scratch/test runs
            run = Run(path)
            questions = load_run_questions(run, task)
            stats = compute_stats(run, questions)
            records = run.records()
            updated = max((r["ts"] for r in records), default=run.config["created"])
            page = out / task.name / run.name / "index.html"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(render_html(run, questions, stats, updated=updated,
                                        home_href="../../"), encoding="utf-8")
            providers = {m["provider"] for m in run.models.values()}
            expected = len(questions) * run.config["repeats"] * len(run.models)
            done = sum(1 for r in run.latest().values() if not is_error(r))
            leader = stats[0] if stats and stats[0]["scored"] else None
            rows.setdefault(task.name, []).append({
                "href": f"{task.name}/{run.name}/", "name": run.name,
                "created": run.config["created"], "updated": updated,
                "models": len(run.models),
                "kinds": sorted("local" if p == "ollama" else "cloud" for p in providers),
                "repeats": run.config["repeats"], "done": done, "expected": expected,
                "leader": leader, "run_time": run.time_summary(),
            })
            print(f"  {task.name}/{run.name}/  ({len(run.models)} models, {done}/{expected})")
    return rows


def _home(rows: dict[str, list[dict]]) -> str:
    out = [
        "<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>AI model benchmarks</title>", f"<style>{CSS}{HOME_CSS}</style>", "</head>",
        "<body><main>", "<h1>AI model benchmarks</h1>",
        '<div class="meta"><span>Personal benchmarks of local (Ollama) and cloud (OpenRouter) '
        f"models · Site built <b>{escape(now_iso()[:16].replace('T', ' '))}</b></span></div>",
    ]
    if not rows:
        out.append('<p class="empty-note">No benchmarks yet.</p>')
    for task, items in rows.items():
        items.sort(key=lambda r: r["created"], reverse=True)
        out += [f'<h2 class="task">{escape(task)}</h2>', '<div class="card"><table><thead><tr>',
                '<th class="l">Benchmark</th><th class="l">Models</th><th>Repeats</th>',
                '<th>Progress</th><th class="l">Leader</th><th>Run time</th>',
                "<th>Updated</th></tr></thead><tbody>"]
        for r in items:
            pct = 100 * r["done"] / r["expected"] if r["expected"] else 0
            tags = "".join(f'<span class="tag {k}">{k}</span>' for k in r["kinds"])
            leader = (f'<span class="model">{escape(r["leader"]["alias"])}</span> '
                      f'<span class="sub">{r["leader"]["pct"]:.1f}%</span>'
                      if r["leader"] else '<span class="sub">–</span>')
            full = r["run_time"] or "–"
            if full == "untracked":
                short, full = "–", "untracked: benchmark created before session timing"
            else:  # "5h 34m over 3 sessions (+ earlier untracked sessions)" -> "5h 34m+"
                short = full.split(" over ")[0] + ("+" if "untracked" in full else "")
            out.append(
                "<tr>"
                f'<td class="l name"><a href="{escape(r["href"])}">{escape(r["name"])}</a></td>'
                f'<td class="l">{r["models"]}{tags}</td>'
                f'<td>{r["repeats"]}</td>'
                f'<td><div class="prog"><span>{r["done"]}/{r["expected"]}</span>'
                f'<span class="bar"><i style="width:{pct:.1f}%"></i></span></div></td>'
                f'<td class="leader">{leader}</td>'
                f'<td title="{escape(full)}">{escape(short)}</td>'
                f'<td>{escape(r["updated"][:16].replace("T", " "))}</td>'
                "</tr>")
        out += ["</tbody></table></div>"]
    out += ["</main></body></html>", ""]
    return "\n".join(out)


def build_site(out: Path) -> None:
    if out.exists():
        if any(out.iterdir()) and not (out / "index.html").exists():
            raise SystemExit(f"{out} is not empty and doesn't look like a built site; "
                             f"refusing to delete it. Pick another --out.")
        shutil.rmtree(out)
    out.mkdir(parents=True)
    print(f"Building site in {out}")
    rows = _benchmark_rows(out)
    (out / "index.html").write_text(_home(rows), encoding="utf-8")
    (out / ".nojekyll").touch()  # serve files as they are
    print(f"Done: {sum(len(v) for v in rows.values())} benchmark page(s) + index.html")
