# simplebench — 2026-11-08_ollama

- Created: 2026-11-08T10:00:45+01:00 · Updated: 2026-11-14T12:04:30+01:00
- Dataset: `SimpleBench/simple_bench_public.json` (10 questions) · Repeats: 3 · Max points per model: 30
- Prompt profile: `one_letter` · Temperature: None · Max tokens: None
- Run time: 31h 56m over 6 sessions (wall time, pauses between sessions excluded)

| # | Model | Points | Score | Per round (of 10) | Majority vote | Unparsed | Truncated | Errors | Avg time | Avg out tok | Cost |
|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | ollama-gemma4-26b | 18/30 | 60.0% | 6.0 ± 1.0 | 6/10 | 0 | 0 | 0 | 261.6s | 4534 | – |
| 2 | ollama-bonsai-2-27b | 16/30 | 53.3% | 5.3 ± 1.2 | 5/10 | 0 | 0 | 0 | 286.1s | 1266 | – |
| 3 | ollama-qwen3.8-27b | 10/20 (of 30) | 50.0% | 5.0 ± 0.0 | 5/10 | 0 | 0 | 0 | 214.6s | 752 | – |
| 4 | ollama-bonsai-2-9b | 13/30 | 43.3% | 4.3 ± 0.6 | 4/10 | 0 | 0 | 0 | 226.5s | 5188 | – |
| 5 | ollama-gemma4-e4b | 12/30 | 40.0% | 4.0 ± 2.0 | 4/10 | 0 | 0 | 0 | 36.4s | 984 | – |
| 6 | ollama-mimo-v2.6 | 12/30 | 40.0% | 4.0 ± 0.0 | 4/10 | 0 | 7 | 0 | 605.2s | 8454 | – |
| 7 | ollama-lfm2.5-8b | 9/30 | 30.0% | 3.0 ± 1.0 | 3/10 | 0 | 0 | 0 | 84.8s | 4455 | – |
| 8 | ollama-nemotron-3.5-lightning | 9/30 | 30.0% | 3.0 ± 1.0 | 3/10 | 0 | 0 | 0 | 427.9s | 9301 | – |
| 9 | ollama-ornith-1.5-9b | 7/25 (of 30) | 28.0% | 3.0 ± 1.4 | 1/10 | 0 | 3 | 0 | 463.0s | 6724 | – |
| 10 | ollama-bonsai-2-2b | 6/30 | 20.0% | 2.0 ± 0.0 | 2/10 | 0 | 0 | 0 | 70.5s | 10919 | – |
| 11 | ollama-lfm2.5-24b | 6/30 | 20.0% | 2.0 ± 1.0 | 2/10 | 0 | 0 | 0 | 202.4s | 5703 | – |
| 12 | ollama-flint | 5/30 | 16.7% | 1.7 ± 0.6 | 1/10 | 0 | 0 | 0 | 244.8s | 4239 | – |
| 13 | ollama-gpt-oss-20b | 5/30 | 16.7% | 1.7 ± 0.6 | 1/10 | 0 | 0 | 0 | 644.1s | 9488 | – |

## Per question (correct / attempts)

| Model | Q1 (B) | Q2 (A) | Q3 (A) | Q4 (C) | Q5 (B) | Q6 (A) | Q7 (C) | Q8 (F) | Q9 (A) | Q10 (B) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ollama-gemma4-26b | 3/3 | 3/3 | 2/3 | 0/3 | 3/3 | 1/3 | 0/3 | 3/3 | 2/3 | 1/3 |
| ollama-bonsai-2-27b | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | 0/3 | 1/3 | 3/3 | 2/3 | 1/3 |
| ollama-qwen3.8-27b | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | 0/2 | 0/2 | 2/2 | 2/2 | 0/2 |
| ollama-bonsai-2-9b | 3/3 | 3/3 | 0/3 | 1/3 | 1/3 | 0/3 | 0/3 | 2/3 | 3/3 | 0/3 |
| ollama-gemma4-e4b | 2/3 | 2/3 | 1/3 | 1/3 | 2/3 | 0/3 | 0/3 | 3/3 | 1/3 | 0/3 |
| ollama-mimo-v2.6 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | 0/3 | 0/3 | 3/3 | 0/3 | 0/3 |
| ollama-lfm2.5-8b | 0/3 | 0/3 | 1/3 | 0/3 | 0/3 | 3/3 | 0/3 | 2/3 | 3/3 | 0/3 |
| ollama-nemotron-3.5-lightning | 1/3 | 2/3 | 0/3 | 2/3 | 0/3 | 0/3 | 0/3 | 3/3 | 1/3 | 0/3 |
| ollama-ornith-1.5-9b | 3/3 | 0/3 | 1/3 | 1/3 | 1/3 | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 |
| ollama-bonsai-2-2b | 0/3 | 0/3 | 0/3 | 1/3 | 0/3 | 0/3 | 0/3 | 3/3 | 2/3 | 0/3 |
| ollama-lfm2.5-24b | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 2/3 | 0/3 | 3/3 | 1/3 | 0/3 |
| ollama-flint | 0/3 | 0/3 | 0/3 | 0/3 | 1/3 | 0/3 | 0/3 | 3/3 | 1/3 | 0/3 |
| ollama-gpt-oss-20b | 0/3 | 0/3 | 0/3 | 0/3 | 1/3 | 0/3 | 0/3 | 3/3 | 1/3 | 0/3 |

## Models

| Model | Provider | Model id | Settings |
|---|---|---|---|
| ollama-gemma4-26b | ollama | `gemma4:26b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-27b | ollama | `bonsai-2:27b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-qwen3.8-27b | ollama | `qwen3.8:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-9b | ollama | `bonsai-2:9b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-gemma4-e4b | ollama | `gemma4:e4b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-mimo-v2.6 | ollama | `mimo-v2.6:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-lfm2.5-8b | ollama | `lfm2.5:8b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-nemotron-3.5-lightning | ollama | `nemotron-3.5-lightning:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-ornith-1.5-9b | ollama | `ornith-1.5:9b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-2b | ollama | `bonsai-2:2b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-lfm2.5-24b | ollama | `lfm2.5:24b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-flint | ollama | `flint:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-gpt-oss-20b | ollama | `gpt-oss:20b` | think=high, timeout=3600, options={'num_ctx': 32768} |

_Score = points / scored attempts. Errors (API failures) are not scored and are retried by `bench run`; unparsed and truncated replies (output token limit or `max_duration` reached) count as wrong. Per round = mean ± SD of points per full pass over the questions. Majority vote = questions where the correct letter was the single most common answer._
