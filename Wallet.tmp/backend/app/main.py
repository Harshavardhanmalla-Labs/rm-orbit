from __future__ import annotations

import base64
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from cryptography.fernet import Fernet
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.gate_auth import Actor, get_actor


def _build_wallet_fernet() -> Fernet:
    raw_key = os.getenv("WALLET_MASTER_KEY", "dev-key")
    derived = base64.urlsafe_b64encode(hashlib.sha256(raw_key.encode()).digest())
    return Fernet(derived)


FERNET = _build_wallet_fernet()
app = FastAPI(title="RM Wallet API", version="2.0.0")


class SecretCreate(BaseModel):
    name: str
    value: str
    description: Optional[str] = ""
    vault_id: Optional[str] = None
    secret_type: str = "api_key"
    project: Optional[str] = None
    tags: List[str] = []


class SecretView(BaseModel):
    id: str
    org_id: str
    name: str
    description: str
    secret_type: str
    project: Optional[str]
    tags: List[str]
    owner_user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "wallet"}


@app.get("/api/wallet/secrets", response_model=List[SecretView])
def list_secrets(
    actor: Actor = Depends(get_actor),
    db: Session = Depends(get_db),
) -> List[models.Secret]:
    return (
        db.query(models.Secret)
        .filter(models.Secret.org_id == actor.org_id)
        .order_by(models.Secret.updated_at.desc())
        .all()
    )


@app.post("/api/wallet/secrets", response_model=SecretView, status_code=201)
def create_secret(
    payload: SecretCreate,
    actor: Actor = Depends(get_actor),
    db: Session = Depends(get_db),
) -> models.Secret:
    encrypted = FERNET.encrypt(payload.value.encode()).decode()
    secret = models.Secret(
        org_id=actor.org_id,
        vault_id=payload.vault_id,
        name=payload.name,
        description=payload.description,
        secret_type=payload.secret_type,
        project=payload.project,
        tags=payload.tags,
        owner_user_id=actor.user_id,
        encrypted_value=encrypted,
    )
    db.add(secret)
    db.commit()
    db.refresh(secret)

    audit = models.AuditLog(
        org_id=actor.org_id,
        user_id=actor.user_id,
        role=actor.role,
        action="secret.create",
        resource_type="secret",
        resource_id=secret.id,
        metadata_json={"secret_type": secret.secret_type, "vault_id": secret.vault_id},
    )
    db.add(audit)
    db.commit()
    return secret


@app.get("/api/wallet/secrets/{secret_id}/reveal")
def reveal_secret(
    secret_id: str,
    actor: Actor = Depends(get_actor),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    secret = (
        db.query(models.Secret)
        .filter(models.Secret.id == secret_id, models.Secret.org_id == actor.org_id)
        .first()
    )
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    value = FERNET.decrypt(secret.encrypted_value.encode()).decode()
    secret.last_revealed_at = datetime.utcnow()
    db.add(secret)

    audit = models.AuditLog(
        org_id=actor.org_id,
        user_id=actor.user_id,
        role=actor.role,
        action="secret.reveal",
        resource_type="secret",
        resource_id=secret.id,
        metadata_json={"secret_name": secret.name},
    )
    db.add(audit)
    db.commit()

    return {"id": secret.id, "value": value}


@app.get("/api/wallet/shared-info")
def list_shared_info(
    category: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    actor: Actor = Depends(get_actor),
    db: Session = Depends(get_db),
) -> list[dict[str, object]]:
    query = db.query(models.SharedInfo).filter(
        or_(models.SharedInfo.org_id == actor.org_id, models.SharedInfo.org_id == "*")
    )
    if category:
        query = query.filter(models.SharedInfo.category == category)
    if search:
        like = f"%{search.strip()}%"
        query = query.filter(
            or_(
                models.SharedInfo.title.ilike(like),
                models.SharedInfo.value.ilike(like),
                models.SharedInfo.notes.ilike(like),
            )
        )

    rows = query.order_by(models.SharedInfo.updated_at.desc()).all()
    return [
        {
            "id": row.id,
            "org_id": row.org_id,
            "category": row.category,
            "title": row.title,
            "value": row.value,
            "environment": row.environment,
            "owner_team": row.owner_team,
            "notes": row.notes,
            "tags": row.tags or [],
            "source": row.source,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }
        for row in rows
    ]


DIST_PATH = Path(__file__).resolve().parents[1] / "frontend" / "dist"
if not DIST_PATH.exists():
    DIST_PATH = Path(__file__).resolve().parents[2] / "frontend" / "dist"

if DIST_PATH.exists():
    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        if full_path.startswith("api/") or full_path.startswith("docs"):
            return None

        target = DIST_PATH / full_path
        if target.is_file():
            return FileResponse(target)
        return FileResponse(DIST_PATH / "index.html")
