# simplebench — 2026-11-08_ollama

- Created: 2026-11-08T10:00:45+01:00 · Updated: 2026-11-08T17:59:35+01:00
- Dataset: `SimpleBench/simple_bench_public.json` (10 questions) · Repeats: 1 · Max points per model: 10
- Prompt profile: `one_letter` · Temperature: None · Max tokens: None
- Run time: 7h 47m over 1 session (wall time, pauses between sessions excluded)

| # | Model | Points | Score | Per round (of 10) | Majority vote | Unparsed | Truncated | Errors | Avg time | Avg out tok | Cost |
|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | ollama-gemma4-26b | 7/10 | 70.0% | 7/10 | 7/10 | 0 | 0 | 0 | 170.4s | 4405 | – |
| 2 | ollama-bonsai-2-27b | 6/10 | 60.0% | 6/10 | 6/10 | 0 | 0 | 0 | 225.6s | 1248 | – |
| 3 | ollama-qwen3.8 | 5/10 | 50.0% | 5/10 | 5/10 | 0 | 0 | 0 | 206.2s | 788 | – |
| 4 | ollama-bonsai-2-9b | 4/10 | 40.0% | 4/10 | 4/10 | 0 | 0 | 0 | 70.7s | 5399 | – |
| 5 | ollama-lfm2.5-8b | 4/10 | 40.0% | 4/10 | 4/10 | 0 | 0 | 0 | 23.5s | 3704 | – |
| 6 | ollama-mimo-v2.6 | 4/10 | 40.0% | 4/10 | 4/10 | 0 | 2 | 0 | 497.0s | 7044 | – |
| 7 | ollama-nemotron-3.5-lightning | 4/10 | 40.0% | 4/10 | 4/10 | 0 | 0 | 0 | 433.6s | 9300 | – |
| 8 | ollama-bonsai-2-2b | 2/10 | 20.0% | 2/10 | 2/10 | 0 | 0 | 0 | 58.1s | 10313 | – |
| 9 | ollama-flint | 2/10 | 20.0% | 2/10 | 2/10 | 0 | 0 | 0 | 97.1s | 3003 | – |
| 10 | ollama-gemma4-e4b | 2/10 | 20.0% | 2/10 | 2/10 | 0 | 0 | 0 | 12.2s | 1038 | – |
| 11 | ollama-ornith-1.5-9b | 2/10 | 20.0% | 2/10 | 2/10 | 0 | 1 | 0 | 541.2s | 7500 | – |
| 12 | ollama-gpt-oss-20b | 1/10 | 10.0% | 1/10 | 1/10 | 0 | 0 | 0 | 311.5s | 7645 | – |
| 13 | ollama-lfm2.5-24b | 1/10 | 10.0% | 1/10 | 1/10 | 0 | 0 | 0 | 154.4s | 5509 | – |

## Per question (correct / attempts)

| Model | Q1 (B) | Q2 (A) | Q3 (A) | Q4 (C) | Q5 (B) | Q6 (A) | Q7 (C) | Q8 (F) | Q9 (A) | Q10 (B) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ollama-gemma4-26b | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 |
| ollama-bonsai-2-27b | 1/1 | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 |
| ollama-qwen3.8 | 1/1 | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 1/1 | 1/1 | 0/1 |
| ollama-bonsai-2-9b | 1/1 | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 1/1 | 0/1 |
| ollama-lfm2.5-8b | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 0/1 |
| ollama-mimo-v2.6 | 1/1 | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 |
| ollama-nemotron-3.5-lightning | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 1/1 | 1/1 | 0/1 |
| ollama-bonsai-2-2b | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 |
| ollama-flint | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 |
| ollama-gemma4-e4b | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 |
| ollama-ornith-1.5-9b | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| ollama-gpt-oss-20b | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 |
| ollama-lfm2.5-24b | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 |

## Models

| Model | Provider | Model id | Settings |
|---|---|---|---|
| ollama-gemma4-26b | ollama | `gemma4:26b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-27b | ollama | `bonsai-2:27b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-qwen3.8 | ollama | `qwen3.8:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-9b | ollama | `bonsai-2:9b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-lfm2.5-8b | ollama | `lfm2.5:8b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-mimo-v2.6 | ollama | `mimo-v2.6:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-nemotron-3.5-lightning | ollama | `nemotron-3.5-lightning:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-2b | ollama | `bonsai-2:2b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-flint | ollama | `flint:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-gemma4-e4b | ollama | `gemma4:e4b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-ornith-1.5-9b | ollama | `ornith-1.5:9b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-gpt-oss-20b | ollama | `gpt-oss:20b` | think=high, timeout=3600, options={'num_ctx': 32768} |
| ollama-lfm2.5-24b | ollama | `lfm2.5:24b` | think=True, timeout=3600, options={'num_ctx': 32768} |

_Score = points / scored attempts. Errors (API failures) are not scored and are retried by `bench run`; unparsed and truncated replies (output token limit or `max_duration` reached) count as wrong. Per round = mean ± SD of points per full pass over the questions. Majority vote = questions where the correct letter was the single most common answer._
