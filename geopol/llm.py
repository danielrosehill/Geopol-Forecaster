"""Thin async OpenRouter client used by every LLM call in the pipeline.

No direct provider SDKs. One key. Per-role model IDs come from config.py.
"""
from __future__ import annotations

import os
from typing import Any

import httpx

from .config import OPENROUTER_API_KEY, OPENROUTER_CHAT_URL, MODEL_DEFAULT


class OpenRouterError(RuntimeError):
    pass


async def chat(
    messages: list[dict[str, str]],
    *,
    model: str = MODEL_DEFAULT,
    temperature: float = 0.7,
    max_tokens: int | None = None,
    timeout: float = 180.0,
) -> str:
    """Single OpenRouter chat completion. Returns assistant content."""
    if not OPENROUTER_API_KEY:
        raise OpenRouterError("OPENROUTER_API_KEY is not set")
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/danielrosehill/Geopol-Forecaster-POC",
        "X-Title": "Geopol Forecaster",
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(OPENROUTER_CHAT_URL, json=payload, headers=headers)
        if r.status_code >= 400:
            raise OpenRouterError(f"OpenRouter {r.status_code}: {r.text[:500]}")
        data = r.json()
    return data["choices"][0]["message"]["content"] or ""


def install_openai_env_shim() -> None:
    """Make libraries that look for `OPENAI_API_KEY` / `OPENAI_BASE_URL`
    (notably llm-snowglobe, which wraps langchain-openai) talk to OpenRouter.

    Call this once at pipeline start before constructing any snowglobe LLM.
    """
    if OPENROUTER_API_KEY:
        os.environ.setdefault("OPENAI_API_KEY", OPENROUTER_API_KEY)
    os.environ.setdefault("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    os.environ.setdefault("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
