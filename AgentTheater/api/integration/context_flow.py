"""Extract and propagate security/trace context through API → Events."""
from __future__ import annotations

import os
from uuid import UUID, uuid4
from fastapi import Request
import jwt as _jwt

from AgentTheater.events.security import EventSecurityContext

_JWT_SECRET = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-in-production-key!")
_JWT_ALGORITHM = "HS256"


def extract_security_context(request: Request) -> EventSecurityContext:
    """Extract and cryptographically verify user context from Authorization header.

    Expects:
      - Authorization: Bearer {jwt_token}  (HS256-signed, must include 'sub' + 'exp')
      - X-Tenant-ID: {tenant_uuid}         (must match token's tenant_id claim)

    Raises ValueError on: missing header, invalid/expired signature, tenant mismatch.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    token = auth_header[7:]

    try:
        payload = _jwt.decode(
            token,
            _JWT_SECRET,
            algorithms=[_JWT_ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
    except _jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except _jwt.MissingRequiredClaimError as e:
        raise ValueError(f"Token missing required claim: {e}")
    except _jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")

    user_id_str = payload.get("sub")
    try:
        user_id = UUID(user_id_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid user_id in token sub: {user_id_str}")

    # Prefer X-Tenant-ID header; fall back to token claim
    header_tenant = request.headers.get("X-Tenant-ID")
    token_tenant = payload.get("tenant_id")

    tenant_id_str = header_tenant or token_tenant
    if not tenant_id_str:
        raise ValueError("Missing X-Tenant-ID header or tenant_id in token")

    # Enforce consistency: if both supplied, they must match
    if header_tenant and token_tenant and header_tenant != token_tenant:
        raise ValueError("X-Tenant-ID header does not match token tenant_id claim")

    try:
        tenant_id = UUID(tenant_id_str)
    except ValueError:
        raise ValueError(f"Invalid tenant_id: {tenant_id_str}")

    roles = payload.get("roles", [])

    return EventSecurityContext(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=roles,
    )


def extract_correlation_id(request: Request) -> str:
    """Extract or generate correlation_id for request tracing."""
    return request.headers.get("X-Correlation-ID") or str(uuid4())


def propagate_context_to_response_headers(
    response,
    correlation_id: str,
    api_version: str = "v1",
    deprecation: str = None,
) -> None:
    """Add tracing and version headers to response."""
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-API-Version"] = api_version

    if deprecation:
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = deprecation
        response.headers["Link"] = '</api/v2/decisions>; rel="successor-version"'
