"""Styled, self-contained leaderboard.html (same numbers as leaderboard.md)."""
from __future__ import annotations

import statistics
from html import escape

from .report import NOTE_BODY, _fmt_rounds
from .store import Run, now_iso
from .task import Question

CSS = """
:root {
  --bg: #f7f7f5; --panel: #ffffff; --text: #1d1d1b; --muted: #6b6b66; --line: #e4e3df;
  --accent: #2f6fdf; --accent-soft: #e6eefc; --warn: #b4530a; --bad: #b42318;
  --bar: #2f6fdf; --bar-bg: #ecebe7; --best: #0f7b45; --best-soft: #e3f4ea;
  --local: #7a4bd1; --local-soft: #efe8fb; --cloud: #0f7b9b; --cloud-soft: #e2f3f7;
  --heat-l: 88%; --heat-text: #1d1d1b;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #141413; --panel: #1d1d1b; --text: #ecebe7; --muted: #a09f99; --line: #33322f;
    --accent: #7aa7f5; --accent-soft: #1f2a3d; --warn: #f0a35e; --bad: #f2867c;
    --bar: #6f9cf0; --bar-bg: #2c2b28; --best: #5fcf94; --best-soft: #173527;
    --local: #b79af0; --local-soft: #2a2140; --cloud: #6cc7df; --cloud-soft: #15313a;
    --heat-l: 30%; --heat-text: #ecebe7;
  }
}
:root[data-theme="dark"] {
  --bg: #141413; --panel: #1d1d1b; --text: #ecebe7; --muted: #a09f99; --line: #33322f;
  --accent: #7aa7f5; --accent-soft: #1f2a3d; --warn: #f0a35e; --bad: #f2867c;
  --bar: #6f9cf0; --bar-bg: #2c2b28; --best: #5fcf94; --best-soft: #173527;
  --local: #b79af0; --local-soft: #2a2140; --cloud: #6cc7df; --cloud-soft: #15313a;
  --heat-l: 30%; --heat-text: #ecebe7;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text);
  font: 14px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
main { max-width: 1280px; margin: 0 auto; padding: 28px 16px 48px; }
h1 { font-size: 22px; margin: 0 0 6px; }
h2 { font-size: 16px; margin: 32px 0 10px; }
.meta { display: flex; flex-wrap: wrap; gap: 6px 18px; color: var(--muted); font-size: 13px; }
.meta b { color: var(--text); font-weight: 600; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 10px;
  overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; }
th, td { padding: 7px 10px; border-bottom: 1px solid var(--line); white-space: nowrap; }
tr:last-child td { border-bottom: none; }
th { font-size: 12px; font-weight: 600; color: var(--muted); text-align: right;
  background: var(--panel); position: sticky; top: 0; }
td { text-align: right; }
th.l, td.l { text-align: left; }
th.sortable { cursor: pointer; user-select: none; }
th.sortable:hover { color: var(--text); }
th.sorted::after { content: " ▾"; } th.sorted.asc::after { content: " ▴"; }
tbody tr:hover td { background: var(--accent-soft); }
.rank { color: var(--muted); width: 2em; }
.model { font-weight: 600; }
.tag { display: inline-block; font-size: 11px; font-weight: 600; padding: 1px 6px;
  border-radius: 99px; margin-left: 6px; vertical-align: 1px; }
.tag.local { color: var(--local); background: var(--local-soft); }
.tag.cloud { color: var(--cloud); background: var(--cloud-soft); }
.score { display: flex; align-items: center; gap: 8px; justify-content: flex-end; }
.bar { width: 90px; height: 8px; border-radius: 4px; background: var(--bar-bg); overflow: hidden; }
.bar i { display: block; height: 100%; background: var(--bar); border-radius: 4px; }
.best { color: var(--best); font-weight: 700; }
td.best-cell { background: var(--best-soft); }
.zero { color: var(--muted); opacity: .55; }
.warn { color: var(--warn); font-weight: 600; }
.bad { color: var(--bad); font-weight: 600; }
.sub { color: var(--muted); font-size: 12px; }
td.heat { text-align: center; color: var(--heat-text); min-width: 52px; }
td.heat.empty { color: var(--muted); }
code { font: 12px ui-monospace, "Cascadia Code", Consolas, monospace; }
.settings { white-space: normal; color: var(--muted); font-size: 12px; text-align: left;
  min-width: 320px; }
.note { color: var(--muted); font-size: 12.5px; margin-top: 18px; max-width: 900px; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
a.home { display: inline-block; font-size: 13px; margin-bottom: 10px; }
"""

SORT_JS = """
document.querySelectorAll("table.sortable-table").forEach(table => {
  const heads = table.querySelectorAll("th.sortable");
  heads.forEach((th, idx) => th.addEventListener("click", () => {
    const col = [...th.parentNode.children].indexOf(th);
    const asc = th.classList.contains("sorted") && !th.classList.contains("asc");
    heads.forEach(h => h.classList.remove("sorted", "asc"));
    th.classList.add("sorted"); if (asc) th.classList.add("asc");
    const body = table.tBodies[0];
    const rows = [...body.rows];
    const key = r => { const c = r.children[col]; const v = c.dataset.v;
      return v === undefined ? c.textContent.trim().toLowerCase() : parseFloat(v); };
    rows.sort((a, b) => { const x = key(a), y = key(b);
      if (typeof x === "number" && typeof y === "number") {
        if (isNaN(x)) return 1; if (isNaN(y)) return -1; return asc ? x - y : y - x; }
      return asc ? String(y).localeCompare(String(x)) : String(x).localeCompare(String(y)); });
    rows.forEach(r => body.appendChild(r));
  }));
});
"""


def _num(v, fmt: str, suffix: str = "") -> tuple[str, str]:
    """(display text, sort value) for an optional number."""
    if v is None:
        return "–", "NaN"
    return format(v, fmt) + suffix, repr(float(v))


def _count_cell(n: int, cls: str) -> str:
    return f'<td data-v="{n}" class="{cls if n else "zero"}">{n}</td>'


def _heat(c: int, n: int) -> str:
    if not n:
        return '<td class="heat empty">–</td>'
    frac = c / n
    hue = round(frac * 135)  # 0 red .. 135 green
    return (f'<td class="heat" data-v="{frac:.3f}" style="background: hsl({hue} 62% '
            f'var(--heat-l))" title="{c} of {n} correct">{c}/{n}</td>')


def render_html(run: Run, questions: list[Question], stats: list[dict],
                live: dict | None = None, updated: str | None = None,
                home_href: str | None = None) -> str:
    """`updated` replaces the current time (the site uses the last result's time);
    `home_href` adds a link back to the site's home page."""
    cfg = run.config
    nq = len(questions)
    gen = cfg.get("generation") or {}
    best_pct = max((s["pct"] for s in stats if s["scored"]), default=None)
    best_major = max((s["majority"] for s in stats), default=None)
    best_round = max((statistics.mean(s["rounds"]) for s in stats if s["rounds"]), default=None)
    run_time = run.time_summary(live)
    if run_time == "untracked":
        run_time = "untracked (created before session timing)"
    title = f"{cfg['task']} — {cfg['name']}"

    meta = [
        ("Created", cfg["created"][:16].replace("T", " ")),
        ("Updated", (updated or now_iso())[:16].replace("T", " ")),
        ("Questions", str(nq)), ("Repeats", str(cfg["repeats"])),
        ("Max points", str(nq * cfg["repeats"])), ("Prompt", cfg["prompt_profile"]),
        ("Temperature", str(gen.get("temperature"))), ("Max tokens", str(gen.get("max_tokens"))),
        ("Run time", run_time or "–"),
    ]
    out = [
        "<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{escape(title)}</title>", f"<style>{CSS}</style>", "</head>", "<body><main>",
        (f'<a class="home" href="{escape(home_href)}">← All benchmarks</a>' if home_href else ""),
        f"<h1>{escape(title)}</h1>",
        '<div class="meta">' + "".join(f"<span>{k}: <b>{escape(v)}</b></span>" for k, v in meta)
        + "</div>",
        "<h2>Leaderboard</h2>", '<div class="card"><table class="sortable-table">', "<thead><tr>",
    ]
    heads = [("#", "l"), ("Model", "l"), ("Score", ""), ("Points", ""),
             (f"Per round (of {nq})", ""), ("Majority vote", ""), ("Unparsed", ""),
             ("Truncated", ""), ("Errors", ""), ("Avg time", ""), ("Avg out tok", ""),
             ("Cost", "")]
    out += [f'<th class="sortable {c}">{escape(h)}</th>' for h, c in heads]
    out += ["</tr></thead>", "<tbody>"]
    for i, s in enumerate(stats, 1):
        m = run.models[s["alias"]]
        kind = "local" if m["provider"] == "ollama" else "cloud"
        pts = f"{s['points']}/{s['scored']}"
        if s["scored"] < s["expected"]:
            pts += f' <span class="sub">of {s["expected"]}</span>'
        is_best = s["scored"] and s["pct"] == best_pct
        score = (f'<td data-v="{s["pct"]:.3f}"{" class=best-cell" if is_best else ""}>'
                 f'<div class="score"><span class="{"best" if is_best else ""}">'
                 f'{s["pct"]:.1f}%</span><span class="bar"><i style="width:{s["pct"]:.1f}%">'
                 f"</i></span></div></td>")
        r_mean = statistics.mean(s["rounds"]) if s["rounds"] else None
        r_cls = "best" if r_mean is not None and r_mean == best_round else ""
        rounds = (f'<td data-v="{r_mean if r_mean is not None else "NaN"}">'
                  f'<span class="{r_cls}">{escape(_fmt_rounds(s["rounds"], nq))}</span></td>')
        major_cls = "best" if s["majority"] == best_major else ""
        t_txt, t_v = _num(s["avg_s"], ".1f", "s")
        k_txt, k_v = _num(s["avg_tok"], ".0f")
        c_txt, c_v = _num(s["cost"], ".4f")
        if s["cost"] is not None:
            c_txt = "$" + c_txt
        out.append(
            "<tr>"
            f'<td class="l rank" data-v="{i}">{i}</td>'
            f'<td class="l"><span class="model">{escape(s["alias"])}</span>'
            f'<span class="tag {kind}">{kind}</span></td>'
            f"{score}"
            f'<td data-v="{s["points"]}">{pts}</td>'
            f"{rounds}"
            f'<td data-v="{s["majority"]}"><span class="{major_cls}">{s["majority"]}/{nq}'
            f"</span></td>"
            + _count_cell(s["unparsed"], "warn") + _count_cell(s["truncated"], "warn")
            + _count_cell(s["errors"], "bad")
            + f'<td data-v="{t_v}">{t_txt}</td><td data-v="{k_v}">{k_txt}</td>'
            f'<td data-v="{c_v}">{c_txt}</td>'
            "</tr>")
    out += ["</tbody></table></div>"]

    # per question heat map
    out += ["<h2>Per question <span class=sub>(correct / attempts)</span></h2>",
            '<div class="card"><table class="sortable-table"><thead><tr>',
            '<th class="sortable l">Model</th>']
    out += [f'<th class="sortable" style="text-align:center">Q{escape(str(q.id))} '
            f'<span class="sub">({escape(q.answer)})</span></th>' for q in questions]
    out += ["</tr></thead><tbody>"]
    for s in stats:
        cells = "".join(_heat(c, n) for c, n in (s["per_q"][q.id] for q in questions))
        out.append(f'<tr><td class="l model">{escape(s["alias"])}</td>{cells}</tr>')
    out += ["</tbody></table></div>"]

    # model definitions
    out += ["<h2>Models</h2>", '<div class="card"><table><thead><tr>',
            '<th class="l">Model</th><th class="l">Provider</th><th class="l">Model id</th>',
            '<th class="l">Settings</th></tr></thead><tbody>']
    for s in stats:
        m = run.models[s["alias"]]
        skip = {"provider", "model", "added"}
        settings = ", ".join(f"{k}={v}" for k, v in m.items() if k not in skip) or "–"
        out.append(f'<tr><td class="l model">{escape(s["alias"])}</td>'
                   f'<td class="l">{escape(m["provider"])}</td>'
                   f'<td class="l"><code>{escape(m["model"])}</code></td>'
                   f'<td class="settings">{escape(settings)}</td></tr>')
    out += ["</tbody></table></div>"]

    note = escape("Score = points / scored attempts. Errors (API failures) are not scored and "
                  "are retried by bench run; " + NOTE_BODY.replace("`", ""))
    out += [f'<p class="note">{note} Click a column header to sort.</p>',
            f"<script>{SORT_JS}</script>", "</main></body></html>", ""]
    return "\n".join(out)
