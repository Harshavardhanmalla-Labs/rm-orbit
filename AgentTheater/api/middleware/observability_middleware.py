"""Per-request observability: request_id generation, Prometheus metrics, structured logging."""
from __future__ import annotations

import time
import logging
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from AgentTheater.observability.metrics import get_metrics

logger = logging.getLogger("agenttheatre.requests")

_SKIP_PATHS = {"/health/live", "/health", "/metrics"}


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Assign X-Request-ID, record Prometheus counters/histograms, emit one JSON log line."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        start = time.monotonic()

        response = await call_next(request)

        latency_ms = (time.monotonic() - start) * 1000
        status = str(response.status_code)
        method = request.method
        endpoint = request.url.path
        tenant_id = request.headers.get("X-Tenant-ID", "")

        if endpoint not in _SKIP_PATHS:
            m = get_metrics()
            m.api_requests_total.labels(
                method=method, endpoint=endpoint, status=status, version="v1"
            ).inc()
            m.api_request_latency_ms.labels(
                method=method, endpoint=endpoint, version="v1"
            ).observe(latency_ms)
            if response.status_code >= 400:
                m.api_errors_total.labels(
                    endpoint=endpoint,
                    error_type="http_error",
                    status=status,
                ).inc()

        logger.info(
            "http_request",
            extra={
                "request_id": request_id,
                "method": method,
                "path": endpoint,
                "status_code": response.status_code,
                "latency_ms": round(latency_ms, 2),
                "tenant_id": tenant_id,
            },
        )

        response.headers["X-Request-ID"] = request_id
        return response
