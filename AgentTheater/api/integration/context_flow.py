"""Extract and propagate security/trace context through API → Events."""
from __future__ import annotations

from uuid import UUID, uuid4
from fastapi import Request
from AgentTheater.events.security import EventSecurityContext


def extract_security_context(request: Request) -> EventSecurityContext:
    """Extract user context from Authorization header + tenant header.

    Expects:
      - Authorization: Bearer {jwt_token}
      - X-Tenant-ID: {tenant_uuid}

    Raises:
      - ValueError if token invalid or tenant missing
    """
    # Get Authorization header
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    token = auth_header.replace("Bearer ", "")

    # For testing: parse token (in production: use real JWT library)
    try:
        import json
        import base64

        # JWT format: header.payload.signature
        payload_b64 = token.split(".")[1]
        # Add padding if needed
        payload_b64 += "=" * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
    except Exception:
        raise ValueError("Invalid token")

    # Extract user_id from JWT sub claim
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise ValueError("Token missing 'sub' claim")

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise ValueError(f"Invalid user_id in token: {user_id_str}")

    # Extract tenant_id from header or JWT
    tenant_id_str = request.headers.get("X-Tenant-ID")
    if not tenant_id_str:
        tenant_id_str = payload.get("tenant_id")

    if not tenant_id_str:
        raise ValueError("Missing X-Tenant-ID header or tenant_id in token")

    try:
        tenant_id = UUID(tenant_id_str)
    except ValueError:
        raise ValueError(f"Invalid tenant_id: {tenant_id_str}")

    # Extract roles
    roles = payload.get("roles", [])

    return EventSecurityContext(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=roles,
    )


def extract_correlation_id(request: Request) -> str:
    """Extract or generate correlation_id for request tracing.

    Looks for X-Correlation-ID header.
    If missing, generates UUID.

    Used to trace request through:
      API → Event → Consumer logs
    """
    correlation_id = request.headers.get("X-Correlation-ID")

    if correlation_id:
        return correlation_id

    # Generate if not provided
    return str(uuid4())


def propagate_context_to_response_headers(
    response,
    correlation_id: str,
    api_version: str = "v1",
    deprecation: str = None,
) -> None:
    """Add context headers to response.

    Propagates:
      - X-Correlation-ID (for request tracing)
      - X-API-Version (for client to know which version responded)
      - Deprecation (RFC 7231 sunset info)
    """
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-API-Version"] = api_version

    if deprecation:
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = deprecation
        response.headers["Link"] = '</api/v2/decisions>; rel="successor-version"'
