"""
HermesNotify — multi-platform notification gateway for RM Orbit.

Sends Orbit system alerts, important email notifications, calendar reminders,
and security alerts across Telegram, Discord, Slack, WhatsApp, Email, etc.

Configure in env vars (or pass config dict directly):
  ORBIT_TELEGRAM_BOT_TOKEN + ORBIT_TELEGRAM_CHAT_ID
  ORBIT_DISCORD_WEBHOOK
  ORBIT_SLACK_WEBHOOK

Usage:
    notify = HermesNotify()
    await notify.send("New critical email from CEO", title="RM Mail Alert", priority="high")
"""

import asyncio
import json
import logging
import os
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

# Platform credentials (env-var driven — no hardcoded secrets)
_TELEGRAM_TOKEN = os.getenv("ORBIT_TELEGRAM_BOT_TOKEN", "")
_TELEGRAM_CHAT = os.getenv("ORBIT_TELEGRAM_CHAT_ID", "")
_DISCORD_WEBHOOK = os.getenv("ORBIT_DISCORD_WEBHOOK", "")
_SLACK_WEBHOOK = os.getenv("ORBIT_SLACK_WEBHOOK", "")
_MATRIX_HOMESERVER = os.getenv("ORBIT_MATRIX_HOMESERVER", "https://matrix.org")
_MATRIX_TOKEN = os.getenv("ORBIT_MATRIX_TOKEN", "")
_MATRIX_ROOM = os.getenv("ORBIT_MATRIX_ROOM_ID", "")


class HermesNotify:
    """
    Multi-platform notification gateway for RM Orbit.

    Only sends to platforms that have credentials configured.
    """

    def __init__(self, extra_config: dict | None = None):
        self._cfg = extra_config or {}
        self._client = httpx.AsyncClient(timeout=20.0)

    async def send(self, message: str, title: str = "",
                   platforms: list[str] | None = None,
                   priority: str = "normal") -> dict[str, bool]:
        """
        Send notification to all configured platforms (or specified subset).
        Returns {platform: success} dict.

        Priority "critical" prefixes message with urgent emoji on supporting platforms.
        """
        prefix = "🚨 " if priority == "critical" else ("⚡ " if priority == "high" else "")
        full_msg = f"{prefix}*{title}*\n{message}" if title else f"{prefix}{message}"

        tasks = {}
        if platforms is None or "telegram" in platforms:
            if _TELEGRAM_TOKEN and _TELEGRAM_CHAT:
                tasks["telegram"] = self._telegram(full_msg)
        if platforms is None or "discord" in platforms:
            if _DISCORD_WEBHOOK:
                tasks["discord"] = self._discord(full_msg)
        if platforms is None or "slack" in platforms:
            if _SLACK_WEBHOOK:
                tasks["slack"] = self._slack(full_msg)
        if platforms is None or "matrix" in platforms:
            if _MATRIX_TOKEN and _MATRIX_ROOM:
                tasks["matrix"] = self._matrix(message)

        # Add any extra platforms from injected config
        for platform, cfg in self._cfg.items():
            if platforms is None or platform in platforms:
                tasks[platform] = self._generic(platform, full_msg, cfg)

        if not tasks:
            logger.debug("HermesNotify: no platforms configured, skipping send")
            return {}

        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        return {
            platform: not isinstance(r, Exception)
            for platform, r in zip(tasks.keys(), results)
        }

    async def _telegram(self, text: str) -> None:
        r = await self._client.post(
            f"https://api.telegram.org/bot{_TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": _TELEGRAM_CHAT, "text": text, "parse_mode": "Markdown"},
        )
        r.raise_for_status()

    async def _discord(self, text: str) -> None:
        r = await self._client.post(_DISCORD_WEBHOOK, json={"content": text[:2000]})
        r.raise_for_status()

    async def _slack(self, text: str) -> None:
        r = await self._client.post(_SLACK_WEBHOOK, json={"text": text})
        r.raise_for_status()

    async def _matrix(self, text: str) -> None:
        r = await self._client.post(
            f"{_MATRIX_HOMESERVER}/_matrix/client/v3/rooms/{_MATRIX_ROOM}/send/m.room.message",
            headers={"Authorization": f"Bearer {_MATRIX_TOKEN}"},
            json={"msgtype": "m.text", "body": text},
        )
        r.raise_for_status()

    async def _generic(self, platform: str, text: str, cfg: dict) -> None:
        webhook = cfg.get("webhook_url")
        if webhook:
            r = await self._client.post(webhook, json={"content": text, "platform": platform})
            r.raise_for_status()

    async def close(self) -> None:
        await self._client.aclose()
