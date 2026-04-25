from __future__ import annotations

import os
from typing import Optional

import jwt
from fastapi import Header, HTTPException
from pydantic import BaseModel


AUTH_MODE = (os.getenv("WALLET_AUTH_MODE", "hybrid").strip().lower() or "hybrid")
GATE_JWKS_URL = os.getenv(
    "WALLET_GATE_JWKS_URL",
    "http://localhost:45001/api/v1/oidc/jwks",
).strip()
GATE_ISSUER = os.getenv("WALLET_GATE_ISSUER", "").strip()
GATE_AUDIENCE = os.getenv("WALLET_GATE_AUDIENCE", "").strip()
GATE_JWT_ALGORITHM = os.getenv("WALLET_GATE_JWT_ALGORITHM", "RS256").strip() or "RS256"

_jwks_client: jwt.PyJWKClient | None = None
_jwks_client_url: str | None = None


class Actor(BaseModel):
    org_id: str
    user_id: str
    role: str


def _normalize(value: object) -> str:
    return str(value or "").strip()


def _resolve_role_from_claims(payload: dict) -> str:
    org_role = _normalize(payload.get("org_role")).lower()
    if org_role:
        return org_role

    roles = payload.get("roles")
    if isinstance(roles, list):
        for candidate in roles:
            value = _normalize(candidate).lower()
            if value:
                return value

    return "member"


def _get_jwks_client() -> jwt.PyJWKClient:
    global _jwks_client, _jwks_client_url
    if not GATE_JWKS_URL:
        raise HTTPException(status_code=503, detail="Wallet Gate JWKS URL is not configured")

    if _jwks_client is None or _jwks_client_url != GATE_JWKS_URL:
        _jwks_client = jwt.PyJWKClient(GATE_JWKS_URL, cache_keys=True)
        _jwks_client_url = GATE_JWKS_URL

    return _jwks_client


def _resolve_actor_from_headers(
    x_org_id: Optional[str],
    x_user_id: Optional[str],
    x_user_role: Optional[str],
) -> Actor:
    org_id = _normalize(x_org_id)
    user_id = _normalize(x_user_id)
    role = _normalize(x_user_role).lower() or "member"

    if not org_id or not user_id:
        raise HTTPException(status_code=401, detail="Missing organization or user identity headers")

    return Actor(org_id=org_id, user_id=user_id, role=role)


def _resolve_actor_from_bearer_token(authorization: Optional[str]) -> Actor:
    token = _normalize(authorization)
    if not token.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")

    raw_token = token[7:].strip()
    if not raw_token:
        raise HTTPException(status_code=401, detail="Bearer token required")

    try:
        signing_key = _get_jwks_client().get_signing_key_from_jwt(raw_token)
        decode_kwargs = {
            "key": signing_key.key,
            "algorithms": [GATE_JWT_ALGORITHM],
        }
        options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_nbf": True,
            "verify_iat": True,
            "verify_iss": bool(GATE_ISSUER),
            "verify_aud": bool(GATE_AUDIENCE),
        }
        if GATE_ISSUER:
            decode_kwargs["issuer"] = GATE_ISSUER
        if GATE_AUDIENCE:
            decode_kwargs["audience"] = GATE_AUDIENCE

        payload = jwt.decode(raw_token, options=options, **decode_kwargs)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired access token") from exc

    org_id = _normalize(payload.get("org_id"))
    user_id = _normalize(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing subject claim")
    if not org_id:
        raise HTTPException(status_code=403, detail="Token missing organization scope")

    return Actor(
        org_id=org_id,
        user_id=user_id,
        role=_resolve_role_from_claims(payload),
    )


async def get_actor(
    x_org_id: Optional[str] = Header(default=None, alias="X-Org-Id"),
    x_user_id: Optional[str] = Header(default=None, alias="X-User-Id"),
    x_user_role: Optional[str] = Header(default=None, alias="X-User-Role"),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> Actor:
    if AUTH_MODE not in {"headers", "gate", "hybrid"}:
        raise HTTPException(status_code=500, detail="Invalid Wallet auth mode configuration")

    has_bearer = _normalize(authorization).lower().startswith("bearer ")

    if AUTH_MODE == "headers":
        return _resolve_actor_from_headers(x_org_id, x_user_id, x_user_role)

    if AUTH_MODE == "gate":
        actor = _resolve_actor_from_bearer_token(authorization)
    else:
        actor = (
            _resolve_actor_from_bearer_token(authorization)
            if has_bearer
            else _resolve_actor_from_headers(x_org_id, x_user_id, x_user_role)
        )

    if _normalize(x_org_id) and _normalize(x_org_id) != actor.org_id:
        raise HTTPException(status_code=403, detail="X-Org-Id mismatch with authenticated actor")

    return actor
