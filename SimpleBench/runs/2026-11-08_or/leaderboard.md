# simplebench — 2026-11-08_or

- Created: 2026-11-08T02:25:25+01:00 · Updated: 2026-11-08T09:05:25+01:00
- Dataset: `SimpleBench/simple_bench_public.json` (10 questions) · Repeats: 10 · Max points per model: 100
- Prompt profile: `one_letter` · Temperature: None · Max tokens: None
- Run time: untracked (benchmark created before session timing)

| # | Model | Points | Score | Per round (of 10) | Majority vote | Unparsed | Truncated | Errors | Avg time | Avg out tok | Cost |
|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | or-glm-5.3-flash | 75/100 | 75.0% | 7.5 ± 0.8 | 8/10 | 0 | 0 | 0 | 8.3s | 199 | $0.0114 |
| 2 | or-claude-haiku-5.5 | 70/100 | 70.0% | 7.0 ± 0.8 | 7/10 | 0 | 0 | 0 | 5.6s | 781 | $0.0418 |
| 3 | or-gemma-4-26b | 67/100 | 67.0% | 6.7 ± 0.8 | 7/10 | 0 | 0 | 0 | 69.8s | 4430 | $0.1345 |
| 4 | or-qwen3.8 | 60/100 | 60.0% | 6.0 ± 0.7 | 5/10 | 0 | 0 | 0 | 19.4s | 906 | $0.1728 |
| 5 | or-gpt-6-luna | 50/100 | 50.0% | 5.0 ± 0.5 | 5/10 | 0 | 0 | 0 | 9.8s | 671 | $0.0354 |
| 6 | or-bonsai-2-27b | 48/100 | 48.0% | 4.8 ± 1.0 | 5/10 | 0 | 0 | 0 | 31.0s | 1287 | $0.0658 |
| 7 | or-bonsai-2-9b | 45/100 | 45.0% | 4.5 ± 0.8 | 5/10 | 0 | 0 | 0 | 70.9s | 5757 | $0.0764 |
| 8 | or-gpt-oss-120b | 29/100 | 29.0% | 2.9 ± 0.6 | 3/10 | 0 | 6 | 0 | 314.5s | 14777 | $0.2521 |
| 9 | or-nemotron-3.5-lightning | 29/100 | 29.0% | 2.9 ± 1.3 | 2/10 | 0 | 0 | 0 | 30.6s | 8679 | $0.1750 |
| 10 | or-gpt-oss-20b | 28/100 | 28.0% | 2.8 ± 1.0 | 2/10 | 0 | 0 | 0 | 75.8s | 8862 | $0.1248 |
| 11 | or-flint | 23/100 | 23.0% | 2.3 ± 1.3 | 2/10 | 0 | 0 | 0 | 28.1s | 4278 | $0.0000 |
| 12 | or-lfm2.5-24b | 19/100 | 19.0% | 1.9 ± 0.7 | 1/10 | 0 | 21 | 0 | 15.8s | 5187 | $0.3641 |

## Per question (correct / attempts)

| Model | Q1 (B) | Q2 (A) | Q3 (A) | Q4 (C) | Q5 (B) | Q6 (A) | Q7 (C) | Q8 (F) | Q9 (A) | Q10 (B) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| or-glm-5.3-flash | 10/10 | 10/10 | 8/10 | 2/10 | 8/10 | 7/10 | 10/10 | 10/10 | 7/10 | 3/10 |
| or-claude-haiku-5.5 | 10/10 | 10/10 | 3/10 | 8/10 | 9/10 | 10/10 | 0/10 | 10/10 | 10/10 | 0/10 |
| or-gemma-4-26b | 10/10 | 10/10 | 7/10 | 4/10 | 10/10 | 9/10 | 1/10 | 10/10 | 6/10 | 0/10 |
| or-qwen3.8 | 10/10 | 10/10 | 3/10 | 5/10 | 10/10 | 0/10 | 3/10 | 10/10 | 8/10 | 1/10 |
| or-gpt-6-luna | 8/10 | 10/10 | 0/10 | 1/10 | 10/10 | 7/10 | 0/10 | 10/10 | 4/10 | 0/10 |
| or-bonsai-2-27b | 10/10 | 8/10 | 1/10 | 1/10 | 9/10 | 1/10 | 2/10 | 10/10 | 5/10 | 1/10 |
| or-bonsai-2-9b | 7/10 | 9/10 | 0/10 | 2/10 | 8/10 | 0/10 | 0/10 | 8/10 | 10/10 | 1/10 |
| or-gpt-oss-120b | 0/10 | 9/10 | 0/10 | 0/10 | 2/10 | 0/10 | 0/10 | 9/10 | 9/10 | 0/10 |
| or-nemotron-3.5-lightning | 2/10 | 3/10 | 2/10 | 4/10 | 3/10 | 0/10 | 0/10 | 10/10 | 5/10 | 0/10 |
| or-gpt-oss-20b | 1/10 | 4/10 | 0/10 | 0/10 | 9/10 | 0/10 | 0/10 | 10/10 | 4/10 | 0/10 |
| or-flint | 2/10 | 0/10 | 0/10 | 1/10 | 7/10 | 0/10 | 0/10 | 10/10 | 3/10 | 0/10 |
| or-lfm2.5-24b | 1/10 | 0/10 | 0/10 | 0/10 | 0/10 | 5/10 | 0/10 | 10/10 | 3/10 | 0/10 |

## Models

| Model | Provider | Model id | Settings |
|---|---|---|---|
| or-glm-5.3-flash | openrouter | `z-ai/glm-5.3-flash` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['z-ai/fp8', 'baseten/fp8', 'novita/fp8'], 'allow_fallbacks': False} |
| or-claude-haiku-5.5 | openrouter | `anthropic/claude-haiku-5.5` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['anthropic', 'amazon-bedrock', 'google-vertex/global'], 'allow_fallbacks': False} |
| or-gemma-4-26b | openrouter | `google/gemma-4-26b-a4b-it` | timeout=900, reasoning={'enabled': True}, routing={'order': ['coreweave/bf16', 'parasail/bf16', 'novita/bf16'], 'allow_fallbacks': False} |
| or-qwen3.8 | openrouter | `qwen/qwen3.8-27b` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['deepinfra/bf16', 'cerebras/fp16'], 'allow_fallbacks': False} |
| or-gpt-6-luna | openrouter | `openai/gpt-6-luna` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['openai', 'azure'], 'allow_fallbacks': False} |
| or-bonsai-2-27b | openrouter | `prism-ml/ternary-bonsai-2-27b` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['darkbloom/int4'], 'allow_fallbacks': False} |
| or-bonsai-2-9b | openrouter | `prism-ml/ternary-bonsai-2-9b` | timeout=900, reasoning={'enabled': True}, routing={'order': ['darkbloom/int4'], 'allow_fallbacks': False} |
| or-gpt-oss-120b | openrouter | `openai/gpt-oss-120b` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['deepinfra/bf16', 'dekallm/bf16', 'crusoe/bf16'], 'allow_fallbacks': False} |
| or-nemotron-3.5-lightning | openrouter | `nvidia/nemotron-3.5-lightning` | timeout=900, reasoning={'enabled': True}, routing={'order': ['coreweave/bf16', 'deepinfra/bf16'], 'allow_fallbacks': False} |
| or-gpt-oss-20b | openrouter | `openai/gpt-oss-20b` | timeout=900, reasoning={'effort': 'high'}, routing={'order': ['deepinfra/bf16', 'dekallm/bf16'], 'allow_fallbacks': False} |
| or-flint | openrouter | `recursive/flint-v1.0:free` | timeout=900, reasoning={'enabled': True}, concurrency=2, routing={'order': ['recursive/bf16'], 'allow_fallbacks': False} |
| or-lfm2.5-24b | openrouter | `liquid/lfm-2.5-24b-a2b` | timeout=900, reasoning={'enabled': True}, routing={'order': ['liquid/fp8'], 'allow_fallbacks': False} |

_Score = points / scored attempts. Errors (API failures) are not scored and are retried by `bench run`; unparsed and truncated replies count as wrong. Per round = mean ± SD of points per full pass over the questions. Majority vote = questions where the correct letter was the single most common answer._
