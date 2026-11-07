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

## Usage
```
uv run bench models                                    # list models in models.yaml
uv run bench new 2026-11-baseline --models gemma4-12b,qwen3.5-9b --repeats 5
uv run bench add 2026-11-baseline --models gpt-oss-20b # tests only the new model, adds it to the table
uv run bench run 2026-11-baseline                      # resume after Ctrl+C / retry API errors
uv run bench report 2026-11-baseline                   # rebuild leaderboard.md
uv run bench list                                      # all benchmarks and their progress
```
`new` options: `--profile final_answer`, `--temperature 0.7`, `--max-tokens N`,
`--questions 1,2,3`, `--no-run`.

Each question attempt is a separate request with no shared history. A new benchmark never touches
existing ones. To change the prompt, repeats or temperature, create a new benchmark.
