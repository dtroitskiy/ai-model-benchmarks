"""Model registry (models.yaml at the project root)."""
from __future__ import annotations

from pathlib import Path

from .util import ROOT, deep_merge, read_yaml

PROVIDERS = ("ollama", "openrouter")


def load_registry(path: Path = ROOT / "models.yaml") -> dict[str, dict]:
    """Return {alias: fully merged model definition}."""
    data = read_yaml(path) or {}
    defaults = data.get("defaults") or {}
    models = {}
    for alias, d in (data.get("models") or {}).items():
        provider = d.get("provider")
        if provider not in PROVIDERS:
            raise ValueError(f"models.yaml: '{alias}' has unknown provider {provider!r}")
        if not d.get("model"):
            raise ValueError(f"models.yaml: '{alias}' is missing 'model'")
        models[alias] = deep_merge(defaults.get(provider) or {}, d)
    return models


def resolve(aliases: list[str]) -> dict[str, dict]:
    registry = load_registry()
    missing = [a for a in aliases if a not in registry]
    if missing:
        raise SystemExit(
            f"Unknown model alias(es): {', '.join(missing)}\n"
            f"Defined in models.yaml: {', '.join(registry) or '(none)'}"
        )
    return {a: registry[a] for a in aliases}
