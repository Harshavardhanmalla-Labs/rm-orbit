from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


security = HTTPBearer(auto_error=False)

_gate_public_key: Optional[str] = None
_jwks_client = None
_jwks_client_url: Optional[str] = None


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _normalize_audience(audience_claim) -> list[str]:
    if isinstance(audience_claim, str):
        value = audience_claim.strip()
        return [value] if value else []
    if isinstance(audience_claim, list):
        return [str(item).strip() for item in audience_claim if str(item).strip()]
    return []


def _validate_standard_claims(payload: dict) -> None:
    expected_issuer = os.getenv("GATE_EXPECTED_ISSUER", "").strip()
    if expected_issuer and payload.get("iss") != expected_issuer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token issuer",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expected_audience = os.getenv("GATE_EXPECTED_AUDIENCE", "").strip()
    if not expected_audience:
        return

    audiences = _normalize_audience(payload.get("aud"))
    if expected_audience in audiences:
        return

    allow_client_id_fallback = _env_bool("ALLOW_CLIENT_ID_AUDIENCE_FALLBACK", True)
    if allow_client_id_fallback and payload.get("client_id") == expected_audience:
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token audience",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _default_gate_key_path() -> Path:
    return Path(__file__).resolve().parents[3] / "Gate" / "authx" / "certs" / "public.pem"


def get_gate_public_key() -> Optional[str]:
    global _gate_public_key
    if _gate_public_key is not None:
        return _gate_public_key

    key_path_raw = os.getenv("GATE_PUBLIC_KEY_PATH", str(_default_gate_key_path()))
    key_path = Path(key_path_raw)
    try:
        if key_path.exists():
            _gate_public_key = key_path.read_text(encoding="utf-8")
    except Exception:
        _gate_public_key = None
    return _gate_public_key


def get_gate_jwks_client():
    global _jwks_client
    global _jwks_client_url

    jwks_url = os.getenv("GATE_JWKS_URL", "").strip()
    if not jwks_url:
        return None

    if _jwks_client is None or _jwks_client_url != jwks_url:
        _jwks_client = jwt.PyJWKClient(jwks_url)
        _jwks_client_url = jwks_url

    return _jwks_client


def _decode_rs256_with_jwks(token: str) -> Optional[dict]:
    jwks_client = get_gate_jwks_client()
    if not jwks_client:
        return None

    signing_key = jwks_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        options={"verify_aud": False},
    )
    _validate_standard_claims(payload)
    return payload


def _decode_rs256_with_local_key(token: str) -> Optional[dict]:
    gate_key = get_gate_public_key()
    if not gate_key:
        return None

    payload = jwt.decode(token, gate_key, algorithms=["RS256"], options={"verify_aud": False})
    _validate_standard_claims(payload)
    return payload


def _decode_hs256_local(token: str) -> dict:
    secret = os.getenv("JWT_SECRET") or os.getenv("WRITER_JWT_SECRET", "writer-secret-key")
    payload = jwt.decode(token, secret, algorithms=["HS256"], options={"verify_aud": False})
    _validate_standard_claims(payload)
    return payload


def verify_gate_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict | None:
    auth_required = _env_bool("WRITER_AUTH_REQUIRED", False)

    if credentials is None:
        if not auth_required:
            return None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload = _decode_rs256_with_jwks(token)
        if payload:
            return payload
    except HTTPException:
        raise
    except jwt.InvalidTokenError:
        pass

    try:
        payload = _decode_rs256_with_local_key(token)
        if payload:
            return payload
    except HTTPException:
        raise
    except jwt.InvalidTokenError:
        pass

    try:
        if not _env_bool("ALLOW_LOCAL_HS256_FALLBACK", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return _decode_hs256_local(token)
    except HTTPException:
        raise
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_org_header(token_payload: dict | None, x_org_id: str | None) -> None:
    if not token_payload:
        return

    org_id = (x_org_id or "").strip()
    require_org_header = _env_bool("WRITER_REQUIRE_ORG_HEADER", False)
    if require_org_header and not org_id:
        raise HTTPException(status_code=400, detail="Missing required header: X-Org-Id")

    if not org_id:
        return

    token_org_id = (
        str(token_payload.get("org_id") or token_payload.get("orgId") or "").strip()
    )
    if token_org_id and token_org_id != org_id:
        raise HTTPException(status_code=403, detail="Token/header org mismatch")


def validate_workspace_claim(token_payload: dict | None, workspace_id: str) -> None:
    if not token_payload:
        return
    if not _env_bool("WRITER_REQUIRE_WORKSPACE_CLAIM_MATCH", False):
        return

    token_workspace = (
        str(token_payload.get("workspace_id") or token_payload.get("workspaceId") or "").strip()
    )
    if token_workspace and token_workspace != workspace_id:
        raise HTTPException(status_code=403, detail="Token/header workspace mismatch")
