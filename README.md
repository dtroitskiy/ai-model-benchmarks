# AI Benchmarks

Personal benchmarks for local (Ollama) and cloud (OpenRouter) models.

## Setup
```
uv sync
copy .env.example .env      # then put your OPENROUTER_API_KEY in .env
```

## Layout
- `models.yaml`: all models you might benchmark, each with a short alias, plus per-provider defaults.
- `core/`: shared code (providers, runner, storage, leaderboard).
- `SimpleBench/`: the dataset, `prompts.yaml` (prompt profiles) and `runs/<benchmark>/`, which holds:
  - `config.yaml`: settings frozen at creation (prompt text, repeats, temperature, dataset hash, model definitions)
  - `results.jsonl`: one line per (model, question, attempt), including the thinking text and the final reply
  - `leaderboard.md`: generated from the results
  - `sessions.jsonl`: start, end and wall time of each session, for the total run time

## Usage
```
uv run bench models                                    # list models in models.yaml
uv run bench new 2026-11-baseline --models gemma4-12b,qwen3.5-9b --repeats 5
uv run bench add 2026-11-baseline --models gpt-oss-20b # tests only the new model, adds it to the table
uv run bench run 2026-11-baseline                      # resume after Ctrl+C / retry API errors
uv run bench extend 2026-11-baseline --repeats 4       # raise repeats to 4 total and run the new rounds
uv run bench report 2026-11-baseline                   # rebuild leaderboard.md
uv run bench list                                      # all benchmarks and their progress
uv run bench stop 2026-11-baseline                     # from another terminal: stop after current attempt(s)
```
While a benchmark runs, press `q` to stop once the attempt(s) in progress finish (press `q` again
to cancel). Ctrl+C aborts immediately and loses the attempts in progress.
`new` options: `--profile final_answer`, `--temperature 0.7`, `--max-tokens N`,
`--questions 1,2,3`, `--no-run`.

`new`, `add` and `run` accept `--concurrency N`: parallel requests per OpenRouter model for that
session (default 4). It changes only speed, not results. A model's own lower `concurrency` still
wins (e.g. free-tier Flint stays at 2). Ollama models are unaffected because a local server would
only queue the requests.

**Order.** With any Ollama model in the run, the order is `rounds`: every model answers every
question once, then the next repeat starts. `leaderboard.md` is rebuilt after each round, so you
can read partial results while it runs, then add rounds later with `bench extend`. Cloud-only runs
use `models`: one model at a time, with its parallel requests drawing from all of its pending
attempts, so a slow reply doesn't leave the other workers idle. `new`, `add`, `run` and `extend`
accept `--order rounds|models` to override this.

**Time.** After each model the run prints its duration and the time since start. Each session
that does work is logged in `sessions.jsonl`. At the end, and in the leaderboard header, the
benchmark's total wall time is the sum of its sessions, so pauses between sessions don't count.
Runs created before this was added show as untracked.

Each question attempt is a separate request with no shared history. A new benchmark never touches
existing ones. To change the prompt, repeats or temperature, create a new benchmark.
