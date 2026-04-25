import json
import logging
from typing import Any

import httpx
from openai import AsyncOpenAI

from app.settings import get_llm_settings

logger = logging.getLogger(__name__)


def _settings():
    return get_llm_settings()


def _client() -> AsyncOpenAI:
    settings = _settings()
    kwargs: dict[str, Any] = {
        "api_key": settings.api_key,
        "timeout": settings.timeout_seconds,
        "max_retries": settings.max_retries,
    }
    if settings.base_url:
        kwargs["base_url"] = settings.base_url
    return AsyncOpenAI(**kwargs)


def provider_name() -> str:
    return _settings().provider


def model_name() -> str:
    return _settings().model


# Backward-compatible constant for older imports and diagnostics.
MODEL = model_name()


async def is_alive() -> bool:
    settings = _settings()
    if not settings.model:
        return False
    if settings.provider != "ollama":
        return bool(settings.api_key)

    try:
        tags_url = settings.base_url.replace("/v1", "").rstrip("/") + "/api/tags"
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(tags_url)
            if r.status_code != 200:
                return False
            models = r.json().get("models", [])
            return any((m.get("name") or m.get("model")) == settings.model for m in models)
    except Exception:
        return False


async def generate(system: str, user: str, temperature: float = 0.3, max_tokens: int = 4096) -> str:
    settings = _settings()
    try:
        resp = await _client().chat.completions.create(
            model=settings.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        logger.exception("LLM generation failed with provider=%s model=%s", settings.provider, settings.model)
        return f"[AI generation error: {e}]"


def _strip_code_fence(raw: str) -> str:
    text = raw.strip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    if len(lines) >= 2 and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return "\n".join(lines[1:]).strip()


def _extract_json(raw: str) -> dict:
    text = _strip_code_fence(raw)
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {"items": parsed}
    except json.JSONDecodeError:
        pass

    candidates = []
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        end = text.rfind(end_char)
        if start != -1 and end != -1 and end > start:
            candidates.append(text[start:end + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            return parsed if isinstance(parsed, dict) else {"items": parsed}
        except json.JSONDecodeError:
            continue

    return {}


async def generate_json(system: str, user: str, temperature: float = 0.2) -> dict:
    settings = _settings()
    prompt = (
        user
        + "\n\nRespond ONLY with valid JSON. No markdown fences, no explanation, no preamble. "
        + "Start your response with { or [."
    )

    last_raw = ""
    for attempt in range(max(1, settings.json_repair_attempts)):
        raw = await generate(system, prompt, temperature=temperature, max_tokens=3000)
        last_raw = raw
        parsed = _extract_json(raw)
        if parsed:
            return parsed

        prompt = (
            "Repair this invalid JSON response. Return only valid JSON, with no markdown fences.\n\n"
            f"Invalid response:\n{last_raw[:6000]}"
        )
        temperature = 0

    logger.warning(
        "LLM JSON generation failed after %s attempts with provider=%s model=%s raw=%r",
        settings.json_repair_attempts,
        settings.provider,
        settings.model,
        last_raw[:500],
    )
    return {}


async def generate_long(system: str, user: str, temperature: float = 0.4) -> str:
    return await generate(system, user, temperature=temperature, max_tokens=8192)
