"""
HermesAI — LLM inference for RM Orbit services.

Routes to Ollama (local, free) first; escalates to OpenRouter (cloud) if local
is unavailable. Designed for FastAPI services — all methods are async.

Env vars:
  OLLAMA_URL          Local Ollama base URL (default: http://localhost:11434)
  OPENROUTER_API_KEY  Enable cloud escalation (optional)
  ORBIT_DEFAULT_MODEL Default local model tag (default: gemma3:4b)
  ORBIT_CLOUD_MODEL   Cloud model via OpenRouter (default: nous/hermes-3-llama-3.1-70b)
"""

import logging
import os
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OPENROUTER_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
DEFAULT_LOCAL_MODEL = os.getenv("ORBIT_DEFAULT_MODEL", "gemma3:4b")
DEFAULT_CLOUD_MODEL = os.getenv("ORBIT_CLOUD_MODEL", "nous/hermes-3-llama-3.1-70b")


@dataclass
class AIResponse:
    text: str
    model: str
    provider: str   # "ollama" | "openrouter" | "stub"
    tokens: int = 0


class HermesAI:
    """
    Async LLM client for RM Orbit services.

    Use a single instance per service (or per-request — it's lightweight).
    """

    def __init__(self, timeout: float = 120.0):
        self._client = httpx.AsyncClient(timeout=timeout)

    async def complete(self, prompt: str, system: str = "",
                       model: str = "auto", max_tokens: int = 1024,
                       temperature: float = 0.3) -> AIResponse:
        """Run a completion. Tries Ollama first, then OpenRouter."""
        try:
            return await self._ollama(prompt, system, model, max_tokens, temperature)
        except Exception as e:
            logger.warning(f"Ollama unavailable: {e}")

        if OPENROUTER_API_KEY:
            try:
                return await self._openrouter(prompt, system, model, max_tokens, temperature)
            except Exception as e:
                logger.warning(f"OpenRouter failed: {e}")

        return AIResponse(text=f"[AI offline] {prompt[:60]}", model="stub", provider="stub")

    async def _ollama(self, prompt: str, system: str, model: str,
                      max_tokens: int, temperature: float) -> AIResponse:
        m = DEFAULT_LOCAL_MODEL if model == "auto" else model
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        resp = await self._client.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": m, "messages": messages, "stream": False,
                  "options": {"temperature": temperature, "num_predict": max_tokens}},
        )
        resp.raise_for_status()
        data = resp.json()
        return AIResponse(
            text=data["message"]["content"],
            model=m,
            provider="ollama",
            tokens=data.get("eval_count", 0),
        )

    async def _openrouter(self, prompt: str, system: str, model: str,
                          max_tokens: int, temperature: float) -> AIResponse:
        m = DEFAULT_CLOUD_MODEL if model == "auto" else model
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        resp = await self._client.post(
            f"{OPENROUTER_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://rmorbit.com",
                "X-Title": "RM Orbit",
            },
            json={"model": m, "messages": messages,
                  "max_tokens": max_tokens, "temperature": temperature},
        )
        resp.raise_for_status()
        data = resp.json()
        return AIResponse(
            text=data["choices"][0]["message"]["content"],
            model=m,
            provider="openrouter",
            tokens=data.get("usage", {}).get("total_tokens", 0),
        )

    # ── Orbit-specific helpers ─────────────────────────────────────────────────

    async def triage_email(self, subject: str, body: str, sender: str) -> dict:
        """
        AI-powered email triage for RM Mail.
        Returns: {priority, category, summary, suggested_reply, needs_action}
        """
        prompt = f"""Analyse this email and respond in valid JSON only.

From: {sender}
Subject: {subject}
Body:
{body[:2000]}

Return exactly this JSON structure:
{{
  "priority": "critical|high|normal|low",
  "category": "work|personal|finance|marketing|notification|support|other",
  "summary": "one sentence summary",
  "needs_action": true|false,
  "suggested_reply": "brief reply draft or empty string if no reply needed"
}}"""

        resp = await self.complete(
            prompt,
            system="You are an intelligent email assistant. Always respond with valid JSON only.",
            temperature=0.1,
            max_tokens=512,
        )
        import json
        try:
            # Extract JSON even if there's surrounding text
            text = resp.text.strip()
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except Exception:
            return {
                "priority": "normal",
                "category": "other",
                "summary": resp.text[:200],
                "needs_action": False,
                "suggested_reply": "",
            }

    async def summarise_thread(self, messages: list[dict]) -> str:
        """Summarise an email thread for RM Mail thread view."""
        thread_text = "\n---\n".join(
            f"From: {m.get('sender', 'unknown')}\n{m.get('body', '')[:500]}"
            for m in messages[-10:]  # Last 10 messages
        )
        resp = await self.complete(
            f"Summarise this email thread in 3 bullet points:\n\n{thread_text}",
            system="You are a concise email assistant.",
            max_tokens=256,
            temperature=0.2,
        )
        return resp.text

    async def smart_compose(self, context: str, instruction: str) -> str:
        """Generate or complete email text for RM Writer and RM Mail compose."""
        resp = await self.complete(
            instruction,
            system=f"You are a professional writing assistant. Context: {context[:500]}",
            max_tokens=512,
            temperature=0.4,
        )
        return resp.text

    async def suggest_meeting_slots(self, request: str, existing_events: list[dict]) -> str:
        """Suggest meeting times for RM Calendar based on existing schedule."""
        events_str = "\n".join(
            f"- {e.get('title', 'Event')}: {e.get('start')} → {e.get('end')}"
            for e in existing_events[:20]
        )
        resp = await self.complete(
            f"Existing schedule:\n{events_str}\n\nRequest: {request}\n\nSuggest 3 available time slots.",
            system="You are a smart calendar assistant. Be concise.",
            max_tokens=256,
            temperature=0.2,
        )
        return resp.text

    async def close(self) -> None:
        await self._client.aclose()
