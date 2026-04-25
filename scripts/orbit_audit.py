from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_audit_record(
    *,
    service: str,
    event: str,
    request_id: str,
    method: str,
    path: str,
    status_code: int,
    duration_ms: int,
    org_id: str | None = None,
    workspace_id: str | None = None,
    user_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = {
        "timestamp": _now_iso(),
        "record_type": "audit_log",
        "service": service,
        "event": event,
        "request_id": request_id,
        "method": method,
        "path": path,
        "status_code": int(status_code),
        "duration_ms": int(duration_ms),
        "org_id": org_id,
        "workspace_id": workspace_id,
        "user_id": user_id,
    }
    if extra:
        record["extra"] = extra
    return record


def get_audit_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    return logger


def emit_audit(logger: logging.Logger, record: dict[str, Any]) -> None:
    logger.info(json.dumps(record, default=str))
