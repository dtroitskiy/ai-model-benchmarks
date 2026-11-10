# simplebench — 2026-11-08_ollama

- Created: 2026-11-08T10:00:45+01:00 · Updated: 2026-11-10T14:06:44+01:00
- Dataset: `SimpleBench/simple_bench_public.json` (10 questions) · Repeats: 2 · Max points per model: 20
- Prompt profile: `one_letter` · Temperature: None · Max tokens: None
- Run time: 22h 25m over 4 sessions (wall time, pauses between sessions excluded)

| # | Model | Points | Score | Per round (of 10) | Majority vote | Unparsed | Truncated | Errors | Avg time | Avg out tok | Cost |
|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | ollama-gemma4-26b | 13/20 | 65.0% | 6.5 ± 0.7 | 6/10 | 0 | 0 | 0 | 254.8s | 4543 | – |
| 2 | ollama-bonsai-2-27b | 10/20 | 50.0% | 5.0 ± 1.4 | 4/10 | 0 | 0 | 0 | 304.5s | 1362 | – |
| 3 | ollama-qwen3.8 | 10/20 | 50.0% | 5.0 ± 0.0 | 5/10 | 0 | 0 | 0 | 214.6s | 752 | – |
| 4 | ollama-bonsai-2-9b | 9/20 | 45.0% | 4.5 ± 0.7 | 4/10 | 0 | 0 | 0 | 176.1s | 4984 | – |
| 5 | ollama-mimo-v2.6 | 8/20 | 40.0% | 4.0 ± 0.0 | 4/10 | 0 | 4 | 0 | 482.5s | 7109 | – |
| 6 | ollama-lfm2.5-8b | 7/20 | 35.0% | 3.5 ± 0.7 | 3/10 | 0 | 0 | 0 | 117.7s | 5267 | – |
| 7 | ollama-nemotron-3.5-lightning | 7/20 | 35.0% | 3.5 ± 0.7 | 2/10 | 0 | 0 | 0 | 471.2s | 10603 | – |
| 8 | ollama-gemma4-e4b | 6/20 | 30.0% | 3.0 ± 1.4 | 1/10 | 0 | 0 | 0 | 31.1s | 969 | – |
| 9 | ollama-ornith-1.5-9b | 6/20 | 30.0% | 3.0 ± 1.4 | 1/10 | 0 | 3 | 0 | 510.2s | 7654 | – |
| 10 | ollama-bonsai-2-2b | 4/20 | 20.0% | 2.0 ± 0.0 | 1/10 | 0 | 0 | 0 | 56.5s | 10092 | – |
| 11 | ollama-flint | 4/20 | 20.0% | 2.0 ± 0.0 | 1/10 | 0 | 0 | 0 | 199.9s | 3803 | – |
| 12 | ollama-gpt-oss-20b | 3/20 | 15.0% | 1.5 ± 0.7 | 1/10 | 0 | 0 | 0 | 683.6s | 9990 | – |
| 13 | ollama-lfm2.5-24b | 3/20 | 15.0% | 1.5 ± 0.7 | 1/10 | 0 | 0 | 0 | 217.7s | 5465 | – |

## Per question (correct / attempts)

| Model | Q1 (B) | Q2 (A) | Q3 (A) | Q4 (C) | Q5 (B) | Q6 (A) | Q7 (C) | Q8 (F) | Q9 (A) | Q10 (B) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ollama-gemma4-26b | 2/2 | 2/2 | 2/2 | 0/2 | 2/2 | 0/2 | 0/2 | 2/2 | 2/2 | 1/2 |
| ollama-bonsai-2-27b | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | 0/2 | 1/2 | 2/2 | 1/2 | 0/2 |
| ollama-qwen3.8 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | 0/2 | 0/2 | 2/2 | 2/2 | 0/2 |
| ollama-bonsai-2-9b | 2/2 | 2/2 | 0/2 | 1/2 | 0/2 | 0/2 | 0/2 | 2/2 | 2/2 | 0/2 |
| ollama-mimo-v2.6 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | 0/2 | 0/2 | 2/2 | 0/2 | 0/2 |
| ollama-lfm2.5-8b | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 | 2/2 | 0/2 | 2/2 | 2/2 | 0/2 |
| ollama-nemotron-3.5-lightning | 1/2 | 1/2 | 0/2 | 2/2 | 0/2 | 0/2 | 0/2 | 2/2 | 1/2 | 0/2 |
| ollama-gemma4-e4b | 1/2 | 1/2 | 0/2 | 1/2 | 1/2 | 0/2 | 0/2 | 2/2 | 0/2 | 0/2 |
| ollama-ornith-1.5-9b | 2/2 | 0/2 | 1/2 | 1/2 | 1/2 | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 |
| ollama-bonsai-2-2b | 0/2 | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 | 0/2 | 2/2 | 1/2 | 0/2 |
| ollama-flint | 0/2 | 0/2 | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 | 2/2 | 1/2 | 0/2 |
| ollama-gpt-oss-20b | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 2/2 | 1/2 | 0/2 |
| ollama-lfm2.5-24b | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 1/2 | 0/2 | 2/2 | 0/2 | 0/2 |

## Models

| Model | Provider | Model id | Settings |
|---|---|---|---|
| ollama-gemma4-26b | ollama | `gemma4:26b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-27b | ollama | `bonsai-2:27b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-qwen3.8 | ollama | `qwen3.8:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-9b | ollama | `bonsai-2:9b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-mimo-v2.6 | ollama | `mimo-v2.6:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-lfm2.5-8b | ollama | `lfm2.5:8b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-nemotron-3.5-lightning | ollama | `nemotron-3.5-lightning:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-gemma4-e4b | ollama | `gemma4:e4b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-ornith-1.5-9b | ollama | `ornith-1.5:9b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-bonsai-2-2b | ollama | `bonsai-2:2b` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-flint | ollama | `flint:latest` | think=True, timeout=3600, options={'num_ctx': 32768} |
| ollama-gpt-oss-20b | ollama | `gpt-oss:20b` | think=high, timeout=3600, options={'num_ctx': 32768} |
| ollama-lfm2.5-24b | ollama | `lfm2.5:24b` | think=True, timeout=3600, options={'num_ctx': 32768} |

_Score = points / scored attempts. Errors (API failures) are not scored and are retried by `bench run`; unparsed and truncated replies (output token limit or `max_duration` reached) count as wrong. Per round = mean ± SD of points per full pass over the questions. Majority vote = questions where the correct letter was the single most common answer._
