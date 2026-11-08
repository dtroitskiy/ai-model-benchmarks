"""Provider adapters: one `complete()` call per question attempt, no shared history."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

import httpx


@dataclass
class Completion:
    content: str
    reasoning: str | None = None
    finish_reason: str | None = None
    truncated: bool = False
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    reasoning_tokens: int | None = None
    cost: float | None = None
    served_by: str | None = None
    duration_s: float = 0.0
    raw_usage: dict = field(default_factory=dict)


class ProviderError(Exception):
    def __init__(self, message: str, retryable: bool):
        super().__init__(message)
        self.retryable = retryable


def _gen_value(model: dict, gen: dict, key: str):
    """Model-level setting overrides the benchmark-level one."""
    return model[key] if model.get(key) is not None else gen.get(key)


def _post(url: str, body: dict, headers: dict, timeout: float) -> dict:
    try:
        r = httpx.post(url, json=body, headers=headers,
                       timeout=httpx.Timeout(timeout, connect=30))
    except (httpx.TimeoutException, httpx.TransportError) as e:
        raise ProviderError(f"{type(e).__name__}: {e}", retryable=True) from e
    if r.status_code == 429 or r.status_code >= 500:
        raise ProviderError(f"HTTP {r.status_code}: {r.text[:500]}", retryable=True)
    if r.status_code >= 400:
        raise ProviderError(f"HTTP {r.status_code}: {r.text[:500]}", retryable=False)
    try:
        return r.json()
    except ValueError as e:
        raise ProviderError(f"Invalid JSON response: {r.text[:500]}", retryable=True) from e


# --------------------------------------------------------------------------- Ollama

def _ollama_base(model: dict) -> str:
    base = model.get("base_url") or os.environ.get("OLLAMA_HOST") or "http://localhost:11434"
    if "://" not in base:
        base = "http://" + base
    return base.replace("0.0.0.0", "localhost").rstrip("/")


def _ollama(model: dict, messages: list[dict], gen: dict) -> Completion:
    body: dict = {"model": model["model"], "messages": messages, "stream": False}
    if "think" in model:
        body["think"] = model["think"]
    if "keep_alive" in model:
        body["keep_alive"] = model["keep_alive"]
    options = dict(model.get("options") or {})
    if (t := _gen_value(model, gen, "temperature")) is not None:
        options.setdefault("temperature", t)
    if (mt := _gen_value(model, gen, "max_tokens")) is not None:
        options.setdefault("num_predict", mt)
    if options:
        body["options"] = options
    body.update(model.get("extra") or {})

    t0 = time.monotonic()
    data = _post(f"{_ollama_base(model)}/api/chat", body, {}, model.get("timeout", 3600))
    dt = time.monotonic() - t0
    if "error" in data:
        raise ProviderError(f"Ollama error: {data['error']}", retryable=False)
    msg = data.get("message") or {}
    reason = data.get("done_reason")
    return Completion(
        content=msg.get("content") or "",
        reasoning=msg.get("thinking"),
        finish_reason=reason,
        truncated=reason == "length",
        prompt_tokens=data.get("prompt_eval_count"),
        completion_tokens=data.get("eval_count"),  # includes thinking tokens
        served_by="ollama",
        duration_s=round(dt, 2),
    )


# --------------------------------------------------------------------------- OpenRouter

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _openrouter(model: dict, messages: list[dict], gen: dict) -> Completion:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise ProviderError("OPENROUTER_API_KEY is not set (put it in .env)", retryable=False)
    body: dict = {"model": model["model"], "messages": messages, "usage": {"include": True}}
    if (t := _gen_value(model, gen, "temperature")) is not None:
        body["temperature"] = t
    if (mt := _gen_value(model, gen, "max_tokens")) is not None:
        body["max_tokens"] = mt
    if model.get("reasoning"):
        body["reasoning"] = model["reasoning"]
    if model.get("routing"):
        body["provider"] = model["routing"]
    body.update(model.get("extra") or {})
    headers = {"Authorization": f"Bearer {key}", "X-Title": "AI-Benchmarks"}

    t0 = time.monotonic()
    data = _post(OPENROUTER_URL, body, headers, model.get("timeout", 900))
    dt = time.monotonic() - t0
    if data.get("error"):
        err = data["error"]
        code = err.get("code") if isinstance(err, dict) else None
        retry = code in (408, 429, 502, 503, 504) or (isinstance(code, int) and code >= 500)
        raise ProviderError(f"OpenRouter error: {err}", retryable=retry)
    choices = data.get("choices") or []
    if not choices:
        raise ProviderError(f"OpenRouter returned no choices: {str(data)[:500]}", retryable=True)
    choice = choices[0]
    msg = choice.get("message") or {}
    usage = data.get("usage") or {}
    reason = choice.get("finish_reason")
    if reason == "error":  # host failed mid-generation: partial reasoning, no answer
        detail = choice.get("error") or choice.get("native_finish_reason")
        raise ProviderError(f"Host {data.get('provider')} aborted generation "
                            f"after {usage.get('completion_tokens')} tokens: {detail}",
                            retryable=True)
    if reason == "stop" and not (msg.get("content") or "").strip() and msg.get("reasoning"):
        # reported as a normal finish, but the reasoning breaks off and no answer follows
        raise ProviderError(f"Host {data.get('provider')} returned reasoning but no answer "
                            f"after {usage.get('completion_tokens')} tokens", retryable=True)
    return Completion(
        content=msg.get("content") or "",
        reasoning=msg.get("reasoning"),
        finish_reason=reason,
        truncated=reason == "length",
        prompt_tokens=usage.get("prompt_tokens"),
        completion_tokens=usage.get("completion_tokens"),
        reasoning_tokens=(usage.get("completion_tokens_details") or {}).get("reasoning_tokens"),
        cost=usage.get("cost"),
        served_by=data.get("provider"),
        duration_s=round(dt, 2),
        raw_usage=usage,
    )


_ADAPTERS = {"ollama": _ollama, "openrouter": _openrouter}

RETRY_DELAYS = (5, 20, 60)


def complete(model: dict, messages: list[dict], gen: dict, log=print) -> Completion:
    """Call the model, retrying transient failures. Raises ProviderError when giving up."""
    adapter = _ADAPTERS[model["provider"]]
    for i, delay in enumerate((*RETRY_DELAYS, None)):
        try:
            return adapter(model, messages, gen)
        except ProviderError as e:
            if not e.retryable or delay is None:
                raise
            log(f"    retry {i + 1}/{len(RETRY_DELAYS)} in {delay}s: {str(e)[:200]}")
            time.sleep(delay)
    raise AssertionError("unreachable")
