# simplebench — 2026-11-07

- Created: 2026-11-07T18:17:38+01:00 · Updated: 2026-11-14T12:04:29+01:00
- Dataset: `SimpleBench/simple_bench_public.json` (10 questions) · Repeats: 5 · Max points per model: 50
- Prompt profile: `one_letter` · Temperature: None · Max tokens: None
- Run time: untracked (benchmark created before session timing)

| # | Model | Points | Score | Per round (of 10) | Majority vote | Unparsed | Truncated | Errors | Avg time | Avg out tok | Cost |
|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | or-gemma-4-26b | 33/50 | 66.0% | 6.6 ± 0.5 | 6/10 | 0 | 0 | 0 | 64.1s | 5147 | $0.0781 |
| 2 | or-qwen3.8-27b | 33/50 | 66.0% | 6.6 ± 0.9 | 5/10 | 0 | 0 | 0 | 19.6s | 977 | $0.0930 |
| 3 | or-bonsai-2-9b | 22/50 | 44.0% | 4.4 ± 0.9 | 5/10 | 0 | 0 | 0 | 71.5s | 5996 | $0.0397 |
| 4 | or-bonsai-2-27b | 21/50 | 42.0% | 4.2 ± 0.8 | 5/10 | 0 | 0 | 0 | 37.3s | 1151 | $0.0295 |
| 5 | or-gpt-oss-20b | 14/50 | 28.0% | 2.8 ± 0.8 | 2/10 | 0 | 0 | 0 | 77.1s | 9754 | $0.0686 |
| 6 | or-nemotron-3.5-lightning | 14/50 | 28.0% | 2.8 ± 1.3 | 3/10 | 0 | 1 | 0 | 44.3s | 11547 | $0.1162 |
| 7 | or-lfm2.5-24b | 10/50 | 20.0% | 2.0 ± 0.7 | 1/10 | 0 | 9 | 0 | 42.0s | 5675 | $0.1991 |

## Per question (correct / attempts)

| Model | Q1 (B) | Q2 (A) | Q3 (A) | Q4 (C) | Q5 (B) | Q6 (A) | Q7 (C) | Q8 (F) | Q9 (A) | Q10 (B) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| or-gemma-4-26b | 5/5 | 5/5 | 2/5 | 1/5 | 5/5 | 5/5 | 0/5 | 5/5 | 5/5 | 0/5 |
| or-qwen3.8-27b | 5/5 | 5/5 | 2/5 | 2/5 | 5/5 | 1/5 | 2/5 | 5/5 | 5/5 | 1/5 |
| or-bonsai-2-9b | 4/5 | 4/5 | 0/5 | 2/5 | 5/5 | 0/5 | 0/5 | 3/5 | 4/5 | 0/5 |
| or-bonsai-2-27b | 4/5 | 4/5 | 0/5 | 0/5 | 5/5 | 0/5 | 0/5 | 5/5 | 3/5 | 0/5 |
| or-gpt-oss-20b | 0/5 | 2/5 | 0/5 | 1/5 | 1/5 | 1/5 | 0/5 | 5/5 | 4/5 | 0/5 |
| or-nemotron-3.5-lightning | 0/5 | 3/5 | 1/5 | 2/5 | 0/5 | 0/5 | 0/5 | 5/5 | 3/5 | 0/5 |
| or-lfm2.5-24b | 0/5 | 2/5 | 0/5 | 0/5 | 0/5 | 1/5 | 0/5 | 5/5 | 2/5 | 0/5 |

## Models

| Model | Provider | Model id | Settings |
|---|---|---|---|
| or-gemma-4-26b | openrouter | `google/gemma-4-26b-a4b-it` | timeout=900, reasoning={'enabled': True}, routing={'order': ['coreweave/bf16', 'parasail/bf16', 'novita/bf16'], 'allow_fallbacks': False} |
| or-qwen3.8-27b | openrouter | `qwen/qwen3.8-27b` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['deepinfra/bf16', 'cerebras/fp16'], 'allow_fallbacks': False} |
| or-bonsai-2-9b | openrouter | `prism-ml/ternary-bonsai-2-9b` | timeout=900, reasoning={'enabled': True}, routing={'order': ['darkbloom/int4'], 'allow_fallbacks': False} |
| or-bonsai-2-27b | openrouter | `prism-ml/ternary-bonsai-2-27b` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['darkbloom/int4'], 'allow_fallbacks': False} |
| or-gpt-oss-20b | openrouter | `openai/gpt-oss-20b` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['deepinfra/bf16', 'dekallm/bf16'], 'allow_fallbacks': False} |
| or-nemotron-3.5-lightning | openrouter | `nvidia/nemotron-3.5-lightning` | timeout=900, reasoning={'enabled': True}, routing={'order': ['coreweave/bf16', 'deepinfra/bf16'], 'allow_fallbacks': False} |
| or-lfm2.5-24b | openrouter | `liquid/lfm-2.5-24b-a2b` | timeout=900, reasoning={'enabled': True}, routing={'order': ['liquid/fp8'], 'allow_fallbacks': False} |

_Score = points / scored attempts. Errors (API failures) are not scored and are retried by `bench run`; unparsed and truncated replies (output token limit or `max_duration` reached) count as wrong. Per round = mean ± SD of points per full pass over the questions. Majority vote = questions where the correct letter was the single most common answer._
