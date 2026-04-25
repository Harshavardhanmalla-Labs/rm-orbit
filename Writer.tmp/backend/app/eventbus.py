from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


_redis_client = None
_redis_module = None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_org_id(event: dict[str, Any]) -> str | None:
    org_id = event.get("org_id") or event.get("orgId")
    if org_id:
        return str(org_id)

    data = event.get("data")
    if isinstance(data, dict):
        nested = data.get("org_id") or data.get("orgId")
        if nested:
            return str(nested)
    return None


def _resolve_user_id(event: dict[str, Any]) -> str | None:
    user_id = event.get("user_id") or event.get("userId")
    if user_id:
        return str(user_id)

    data = event.get("data")
    if isinstance(data, dict):
        nested = data.get("user_id") or data.get("userId")
        if nested:
            return str(nested)
    return None


def build_writer_event_envelope(event_type: str, event: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(event or {})
    envelope: dict[str, Any] = {
        "timestamp": _now_iso(),
        "source": "writer",
        "event_type": payload.get("event_type") or payload.get("eventType") or event_type,
        "schema_version": payload.get("schema_version")
        or payload.get("schemaVersion")
        or 1,
        **payload,
    }

    org_id = _resolve_org_id(envelope)
    if org_id:
        envelope["org_id"] = org_id

    user_id = _resolve_user_id(envelope)
    if user_id:
        envelope["user_id"] = user_id
    elif "user_id" not in envelope:
        envelope["user_id"] = None

    if not envelope.get("event_id"):
        envelope["event_id"] = (
            payload.get("event_id")
            or payload.get("eventId")
            or (payload.get("data") or {}).get("event_id")
            or (payload.get("data") or {}).get("eventId")
            or str(uuid4())
        )

    return envelope


def _get_redis_module():
    global _redis_module
    if _redis_module is not None:
        return _redis_module

    try:
        import redis  # type: ignore
    except Exception:
        _redis_module = None
        return None

    _redis_module = redis
    return _redis_module


def get_redis_client():
    global _redis_client
    if _redis_client is not None:
        return _redis_client

    redis = _get_redis_module()
    if redis is None:
        return None

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    try:
        client = redis.from_url(redis_url, decode_responses=True)
        client.ping()
        _redis_client = client
    except Exception:
        _redis_client = None
    return _redis_client


def publish_writer_event(event_type: str, event: dict[str, Any] | None = None) -> dict[str, Any]:
    envelope = build_writer_event_envelope(event_type, event)
    if not envelope.get("org_id"):
        return envelope

    client = get_redis_client()
    if client is None:
        return envelope

    try:
        payload = json.dumps(envelope)
        client.publish(event_type, payload)
        client.publish("writer.activity", payload)
    except Exception:
        # Event publishing must never block primary writer mutations.
        pass

    return envelope
