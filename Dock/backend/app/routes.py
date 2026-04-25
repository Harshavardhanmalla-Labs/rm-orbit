from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Assignment,
    BudgetPolicy,
    DockApp,
    DockAuditEvent,
    DockRequest,
    License,
    ProcurementConfig,
)

router = APIRouter()

UserRole = Literal["admin", "manager", "member"]
RequestStatus = Literal["pending", "under_review", "approved", "rejected", "provisioned"]
AssignmentStatus = Literal["active", "revoked"]
LicenseStatus = Literal["active", "pending_finance_approval"]


class Actor(BaseModel):
    org_id: str
    user_id: str
    role: UserRole


class DockAppCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    vendor: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=2000)
    url: Optional[str] = Field(default=None, max_length=4000)
    advertised: bool = True
    license_model: str = Field(default="per_user", max_length=64)
    integrations: list[str] = Field(default_factory=list)


class DockAppUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=200)
    vendor: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    url: Optional[str] = Field(default=None, max_length=4000)
    advertised: Optional[bool] = None
    license_model: Optional[str] = Field(default=None, max_length=64)
    integrations: Optional[list[str]] = None


class LicenseCreate(BaseModel):
    app_id: str = Field(min_length=1, max_length=64)
    seats_purchased: int = Field(ge=1, le=100000)
    currency: str = Field(default="USD", min_length=3, max_length=8)
    total_cost: float = Field(default=0, ge=0)
    renewal_date: Optional[str] = None


class AssignmentCreate(BaseModel):
    app_id: str = Field(min_length=1, max_length=64)
    user_id: str = Field(min_length=1, max_length=128)
    access_level: str = Field(default="user", max_length=64)


class AssignmentUpdate(BaseModel):
    access_level: Optional[str] = Field(default=None, max_length=64)
    status: Optional[AssignmentStatus] = None


class DockRequestCreate(BaseModel):
    app_name: str = Field(min_length=2, max_length=200)
    reason: str = Field(min_length=3, max_length=2000)
    requested_seats: int = Field(default=1, ge=1, le=100000)
    business_justification: str = Field(default="", max_length=2000)


class DockRequestUpdate(BaseModel):
    status: Optional[RequestStatus] = None
    review_notes: Optional[str] = Field(default=None, max_length=2000)
    linked_app_id: Optional[str] = Field(default=None, max_length=64)


class BudgetPolicyCreate(BaseModel):
    department_id: Optional[str] = Field(default=None, max_length=64)
    monthly_limit: float = Field(ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=8)
    alert_threshold_pct: float = Field(default=80.0, ge=0, le=100)


class ProcurementConfigUpsert(BaseModel):
    require_manager_approval: bool = True
    auto_approve_threshold: float = Field(default=0.0, ge=0)


DOCK_AUTOMATION_ENABLED = os.getenv("DOCK_AUTOMATION_ENABLED", "true").strip().lower() not in {"0", "false", "no"}
DOCK_TURBOTICK_BASE_URL = os.getenv("DOCK_TURBOTICK_BASE_URL", "http://localhost:6100").rstrip("/")
DOCK_AUTOMATION_TIMEOUT_SECONDS = float(os.getenv("DOCK_AUTOMATION_TIMEOUT_SECONDS", "3.0"))
DOCK_AUTH_MODE = os.getenv("DOCK_AUTH_MODE", "hybrid").strip().lower() or "hybrid"
DOCK_GATE_USERINFO_URL = os.getenv("DOCK_GATE_USERINFO_URL", "http://localhost:45001/api/v1/oidc/userinfo").strip()
DOCK_GATE_TIMEOUT_SECONDS = float(os.getenv("DOCK_GATE_TIMEOUT_SECONDS", "3.0"))
DOCK_AUDIT_ENABLED = os.getenv("DOCK_AUDIT_ENABLED", "true").strip().lower() not in {"0", "false", "no"}
DOCK_EVENT_SINK_URL = os.getenv("DOCK_EVENT_SINK_URL", "").strip()
DOCK_AUDIT_TIMEOUT_SECONDS = float(os.getenv("DOCK_AUDIT_TIMEOUT_SECONDS", "3.0"))
POST_COMMIT_SYNC_ENABLED = os.getenv("POST_COMMIT_SYNC_ENABLED", "true").strip().lower() not in {"0", "false", "no"}
DOCK_SECURE_BRIDGE_URL = os.getenv(
    "DOCK_SECURE_BRIDGE_URL",
    "http://localhost:6004/api/v1/internal/bridge/dock/assignments",
).strip()
DOCK_SECURE_INTERNAL_TOKEN = os.getenv("DOCK_SECURE_INTERNAL_TOKEN", "").strip()
DOCK_SECURE_TIMEOUT_SECONDS = float(os.getenv("DOCK_SECURE_TIMEOUT_SECONDS", "3.0"))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def string_or_empty(value: object) -> str:
    return str(value or "").strip()


def as_iso(value: object) -> Optional[str]:
    if isinstance(value, datetime):
        return value.isoformat()
    return None


def normalize_metadata(metadata: Optional[dict[str, object]]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in (metadata or {}).items():
        key_text = string_or_empty(key)
        if not key_text:
            continue
        normalized[key_text] = string_or_empty(value)
    return normalized


def require_org(x_org_id: Optional[str]) -> str:
    org_id = string_or_empty(x_org_id)
    if not org_id:
        raise HTTPException(status_code=400, detail="X-Org-Id header is required")
    return org_id


def require_user(x_user_id: Optional[str]) -> str:
    user_id = string_or_empty(x_user_id)
    if not user_id:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")
    return user_id


def normalize_role(x_user_role: Optional[str]) -> UserRole:
    raw = string_or_empty(x_user_role).lower() or "member"
    if raw not in {"admin", "manager", "member"}:
        raise HTTPException(status_code=400, detail="X-User-Role must be admin, manager, or member")
    return raw  # type: ignore[return-value]


def normalize_claimed_role(claims: dict) -> UserRole:
    role_candidates: list[str] = []
    claimed_role = string_or_empty(claims.get("org_role"))
    if claimed_role:
        role_candidates.append(claimed_role.lower())
    roles = claims.get("roles")
    if isinstance(roles, list):
        role_candidates.extend(string_or_empty(value).lower() for value in roles if string_or_empty(value))
    for role in role_candidates:
        if role in {"admin", "manager", "member"}:
            return role  # type: ignore[return-value]
    return "member"


def resolve_actor_from_gate(authorization: str) -> Actor:
    if not DOCK_GATE_USERINFO_URL:
        raise HTTPException(status_code=503, detail="Dock Gate userinfo URL is not configured")
    try:
        with httpx.Client(timeout=DOCK_GATE_TIMEOUT_SECONDS) as client:
            response = client.get(
                DOCK_GATE_USERINFO_URL,
                headers={"Authorization": authorization},
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Unable to validate token against Gate: {exc}") from exc

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    if response.status_code >= 400:
        detail = string_or_empty(response.text) or f"Gate userinfo returned {response.status_code}"
        raise HTTPException(status_code=502, detail=detail)

    payload = response.json() if response.content else {}
    if not isinstance(payload, dict):
        raise HTTPException(status_code=502, detail="Invalid Gate userinfo response")

    user_id = string_or_empty(payload.get("sub"))
    org_id = string_or_empty(payload.get("org_id"))
    if not user_id:
        raise HTTPException(status_code=502, detail="Gate userinfo missing subject")
    if not org_id:
        raise HTTPException(status_code=403, detail="Access token missing organization scope")

    return Actor(
        org_id=org_id,
        user_id=user_id,
        role=normalize_claimed_role(payload),
    )


def get_actor(
    x_org_id: Optional[str],
    x_user_id: Optional[str],
    x_user_role: Optional[str],
    authorization: Optional[str] = None,
) -> Actor:
    if DOCK_AUTH_MODE not in {"headers", "gate", "hybrid"}:
        raise HTTPException(status_code=500, detail="Invalid Dock auth mode configuration")

    token = string_or_empty(authorization)
    has_bearer = token.lower().startswith("bearer ")

    if DOCK_AUTH_MODE == "headers":
        return Actor(
            org_id=require_org(x_org_id),
            user_id=require_user(x_user_id),
            role=normalize_role(x_user_role),
        )

    if has_bearer:
        return resolve_actor_from_gate(token)

    if DOCK_AUTH_MODE == "gate":
        raise HTTPException(status_code=401, detail="Bearer token required")

    return Actor(
        org_id=require_org(x_org_id),
        user_id=require_user(x_user_id),
        role=normalize_role(x_user_role),
    )


def get_actor_dependency(
    x_org_id: Optional[str] = Header(default=None, alias="X-Org-Id"),
    x_user_id: Optional[str] = Header(default=None, alias="X-User-Id"),
    x_user_role: Optional[str] = Header(default=None, alias="X-User-Role"),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> Actor:
    return get_actor(x_org_id, x_user_id, x_user_role, authorization)


def is_privileged(actor: Actor) -> bool:
    return actor.role in {"admin", "manager"}


def require_privileged(actor: Actor) -> None:
    if not is_privileged(actor):
        raise HTTPException(status_code=403, detail="Admin or manager role required")


def serialize_app(row: DockApp) -> dict:
    return {
        "id": row.id,
        "org_id": row.org_id,
        "name": row.name,
        "vendor": row.vendor,
        "description": row.description,
        "url": row.url,
        "advertised": row.advertised,
        "license_model": row.license_model,
        "integrations": list(row.integrations or []),
        "created_by": row.created_by,
        "created_at": as_iso(row.created_at),
        "updated_at": as_iso(row.updated_at),
    }


def serialize_license(row: License) -> dict:
    return {
        "id": row.id,
        "org_id": row.org_id,
        "app_id": row.app_id,
        "seats_purchased": row.seats_purchased,
        "seats_assigned": row.seats_assigned,
        "currency": row.currency,
        "total_cost": row.total_cost,
        "renewal_date": row.renewal_date,
        "status": row.status,
        "purchased_by": row.purchased_by,
        "created_at": as_iso(row.created_at),
    }


def serialize_assignment(row: Assignment) -> dict:
    return {
        "id": row.id,
        "org_id": row.org_id,
        "app_id": row.app_id,
        "user_id": row.user_id,
        "access_level": row.access_level,
        "status": row.status,
        "assigned_by": row.assigned_by,
        "created_at": as_iso(row.created_at),
        "updated_at": as_iso(row.updated_at),
    }


def serialize_request(row: DockRequest) -> dict:
    return {
        "id": row.id,
        "org_id": row.org_id,
        "requester_user_id": row.requester_user_id,
        "app_name": row.app_name,
        "reason": row.reason,
        "requested_seats": row.requested_seats,
        "business_justification": row.business_justification,
        "status": row.status,
        "reviewer_user_id": row.reviewer_user_id,
        "review_notes": row.review_notes,
        "linked_app_id": row.linked_app_id,
        "automation_ticket_id": row.automation_ticket_id,
        "automation_status": row.automation_status,
        "automation_last_error": row.automation_last_error,
        "automation_hint": row.automation_hint,
        "created_at": as_iso(row.created_at),
        "updated_at": as_iso(row.updated_at),
    }


def serialize_event(row: DockAuditEvent) -> dict:
    return {
        "id": row.id,
        "event_type": row.event_type,
        "org_id": row.org_id,
        "user_id": row.user_id,
        "role": row.role,
        "resource_type": row.resource_type,
        "resource_id": row.resource_id,
        "request_id": row.request_id,
        "timestamp": as_iso(row.timestamp),
        "metadata": dict(row.metadata_json or {}),
    }


def serialize_budget_policy(row: BudgetPolicy) -> dict:
    return {
        "id": row.id,
        "org_id": row.org_id,
        "department_id": row.department_id,
        "monthly_limit": row.monthly_limit,
        "currency": row.currency,
        "alert_threshold_pct": row.alert_threshold_pct,
        "created_at": as_iso(row.created_at),
    }


def serialize_procurement_config(row: ProcurementConfig) -> dict:
    return {
        "id": row.id,
        "org_id": row.org_id,
        "require_manager_approval": row.require_manager_approval,
        "auto_approve_threshold": row.auto_approve_threshold,
        "created_at": as_iso(row.created_at),
    }


def emit_dock_event(
    db: Session,
    actor: Actor,
    *,
    event_type: str,
    resource_type: str,
    resource_id: str,
    request_id: Optional[str] = None,
    metadata: Optional[dict[str, object]] = None,
) -> DockAuditEvent:
    request_ref = string_or_empty(request_id) or f"rde-{uuid.uuid4().hex[:12]}"
    event = DockAuditEvent(
        id=f"rde-{uuid.uuid4().hex[:10]}",
        event_type=event_type,
        org_id=actor.org_id,
        user_id=actor.user_id,
        role=actor.role,
        resource_type=resource_type,
        resource_id=resource_id,
        request_id=request_ref,
        metadata_json=normalize_metadata(metadata),
    )
    db.add(event)

    if DOCK_AUDIT_ENABLED and DOCK_EVENT_SINK_URL:
        try:
            with httpx.Client(timeout=DOCK_AUDIT_TIMEOUT_SECONDS) as client:
                client.post(
                    DOCK_EVENT_SINK_URL,
                    headers={"Content-Type": "application/json", "X-Org-Id": actor.org_id},
                    json=serialize_event(event),
                )
        except httpx.HTTPError:
            # Event sink forwarding is best-effort.
            pass

    return event


def sync_assignment_to_secure(assignment: Assignment) -> Optional[str]:
    if not POST_COMMIT_SYNC_ENABLED:
        return None

    if not DOCK_SECURE_BRIDGE_URL:
        return "Secure bridge URL is not configured"

    payload = {
        "tenant_id": assignment.org_id,
        "user_id": assignment.user_id,
        "app_id": assignment.app_id,
        "status": assignment.status,
    }
    headers = {
        "Content-Type": "application/json",
        "X-Tenant-ID": assignment.org_id,
    }
    if DOCK_SECURE_INTERNAL_TOKEN:
        headers["X-Internal-Token"] = DOCK_SECURE_INTERNAL_TOKEN

    try:
        with httpx.Client(timeout=DOCK_SECURE_TIMEOUT_SECONDS) as client:
            response = client.post(
                DOCK_SECURE_BRIDGE_URL,
                headers=headers,
                json=payload,
            )
    except httpx.HTTPError as exc:
        return str(exc)

    if response.status_code >= 400:
        return (response.text or f"HTTP {response.status_code}")[:1500]

    return None


def sync_assignment_post_commit(
    db: Session,
    actor: Actor,
    assignment: Assignment,
    request_id: Optional[str],
) -> None:
    if not POST_COMMIT_SYNC_ENABLED:
        return

    error = sync_assignment_to_secure(assignment)
    if not error:
        return

    emit_dock_event(
        db,
        actor,
        event_type="dock.secure.assignment_sync_failed",
        resource_type="assignment",
        resource_id=assignment.id,
        request_id=request_id,
        metadata={
            "assignment_id": assignment.id,
            "app_id": assignment.app_id,
            "user_id": assignment.user_id,
            "status": assignment.status,
            "sync_error": error,
        },
    )
    db.commit()


def get_app_or_404(db: Session, app_id: str, org_id: str) -> DockApp:
    row = db.query(DockApp).filter(DockApp.id == app_id, DockApp.org_id == org_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="App not found")
    return row


def get_license_for_app(db: Session, app_id: str, org_id: str) -> Optional[License]:
    return (
        db.query(License)
        .filter(License.app_id == app_id, License.org_id == org_id)
        .order_by(License.created_at.desc())
        .first()
    )


def get_assignment_or_404(db: Session, assignment_id: str, org_id: str) -> Assignment:
    row = db.query(Assignment).filter(Assignment.id == assignment_id, Assignment.org_id == org_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return row


def get_request_or_404(db: Session, request_id: str, org_id: str) -> DockRequest:
    row = db.query(DockRequest).filter(DockRequest.id == request_id, DockRequest.org_id == org_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return row


def valid_request_transition(current: RequestStatus, target: RequestStatus) -> bool:
    if current == target:
        return True
    transitions: dict[RequestStatus, set[RequestStatus]] = {
        "pending": {"under_review", "approved", "rejected"},
        "under_review": {"approved", "rejected"},
        "approved": {"provisioned", "rejected"},
        "rejected": {"under_review"},
        "provisioned": set(),
    }
    return target in transitions[current]


def build_request_automation_hint(request_row: DockRequest) -> str:
    return (
        f"CARF {request_row.id} | app={request_row.app_name} | "
        f"seats={request_row.requested_seats} | reason={request_row.reason}"
    )[:1000]


def should_run_request_automation(status: RequestStatus) -> bool:
    return status in {"approved", "provisioned"}


def run_carf_automation(request_row: DockRequest, actor: Actor) -> None:
    if request_row.automation_ticket_id:
        request_row.automation_status = "created"
        request_row.automation_last_error = None
        return

    request_row.automation_hint = build_request_automation_hint(request_row)

    if not should_run_request_automation(request_row.status):
        request_row.automation_status = "idle"
        request_row.automation_last_error = None
        return

    if not DOCK_AUTOMATION_ENABLED:
        request_row.automation_status = "skipped"
        request_row.automation_last_error = "Automation disabled by config"
        return

    ticket_payload = {
        "title": f"CARF follow-up: {request_row.app_name}",
        "description": (
            f"Request ID: {request_row.id}\n"
            f"Requested by: {request_row.requester_user_id}\n"
            f"Seats: {request_row.requested_seats}\n"
            f"Reason: {request_row.reason}\n"
            f"Business justification: {request_row.business_justification}\n"
            f"Status: {request_row.status}"
        )[:3900],
        "queue": "support",
        "priority": "medium",
        "category": "software_access",
        "source": "workflow",
        "requester": request_row.requester_user_id,
    }

    request_row.automation_status = "queued"
    request_row.automation_last_error = None

    try:
        with httpx.Client(timeout=DOCK_AUTOMATION_TIMEOUT_SECONDS) as client:
            response = client.post(
                f"{DOCK_TURBOTICK_BASE_URL}/api/tickets",
                headers={
                    "Content-Type": "application/json",
                    "X-Org-Id": actor.org_id,
                },
                json=ticket_payload,
            )
    except httpx.HTTPError as exc:
        request_row.automation_status = "failed"
        request_row.automation_last_error = str(exc)[:1800]
        return

    if response.status_code >= 400:
        request_row.automation_status = "failed"
        request_row.automation_last_error = (response.text or f"HTTP {response.status_code}")[:1800]
        return

    try:
        payload = response.json()
    except ValueError:
        payload = {}

    ticket_id = str((payload or {}).get("id") or "").strip()
    if not ticket_id:
        request_row.automation_status = "failed"
        request_row.automation_last_error = "TurboTick automation response missing ticket id"
        return

    request_row.automation_ticket_id = ticket_id
    request_row.automation_status = "created"
    request_row.automation_last_error = None


def validate_budget(db: Session, org_id: str, new_license_cost: float) -> dict[str, object]:
    policy = (
        db.query(BudgetPolicy)
        .filter(BudgetPolicy.org_id == org_id)
        .order_by(BudgetPolicy.created_at.desc())
        .first()
    )
    if policy is None:
        return {
            "within_limit": True,
            "policy_id": None,
            "monthly_limit": None,
            "currency": None,
        }

    monthly_limit = float(policy.monthly_limit or 0.0)
    within_limit = float(new_license_cost) <= monthly_limit
    return {
        "within_limit": within_limit,
        "policy_id": policy.id,
        "monthly_limit": monthly_limit,
        "currency": policy.currency,
    }


@router.get("/apps", response_model=list[dict])
def list_apps(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> list[dict]:
    query = db.query(DockApp).filter(DockApp.org_id == actor.org_id)
    if not is_privileged(actor):
        query = query.filter(DockApp.advertised.is_(True))
    rows = query.order_by(DockApp.updated_at.desc()).all()
    return [serialize_app(row) for row in rows]


@router.get("/apps/advertised", response_model=list[dict])
def list_advertised_apps(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> list[dict]:
    rows = (
        db.query(DockApp)
        .filter(DockApp.org_id == actor.org_id, DockApp.advertised.is_(True))
        .order_by(DockApp.updated_at.desc())
        .all()
    )
    return [serialize_app(row) for row in rows]


@router.get("/apps/assigned", response_model=list[dict])
def list_assigned_apps(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> list[dict]:
    app_ids = (
        db.query(Assignment.app_id)
        .filter(
            Assignment.org_id == actor.org_id,
            Assignment.user_id == actor.user_id,
            Assignment.status == "active",
        )
        .all()
    )
    assigned_app_ids = [row[0] for row in app_ids]
    if not assigned_app_ids:
        return []

    rows = (
        db.query(DockApp)
        .filter(DockApp.org_id == actor.org_id, DockApp.id.in_(assigned_app_ids))
        .order_by(DockApp.updated_at.desc())
        .all()
    )
    return [serialize_app(row) for row in rows]


@router.post("/apps", response_model=dict, status_code=201)
def create_app(
    payload: DockAppCreate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(default=None, alias="X-Request-Id"),
) -> dict:
    require_privileged(actor)

    duplicate = (
        db.query(DockApp)
        .filter(DockApp.org_id == actor.org_id, func.lower(DockApp.name) == payload.name.lower())
        .first()
    )
    if duplicate is not None:
        raise HTTPException(status_code=409, detail="App already exists in this org")

    row = DockApp(
        id=f"rd-app-{uuid.uuid4().hex[:10]}",
        org_id=actor.org_id,
        name=payload.name,
        vendor=payload.vendor,
        description=payload.description,
        url=payload.url,
        advertised=payload.advertised,
        license_model=payload.license_model,
        integrations=[string_or_empty(item) for item in payload.integrations if string_or_empty(item)],
        created_by=actor.user_id,
    )
    db.add(row)
    emit_dock_event(
        db,
        actor,
        event_type="dock.app.created",
        resource_type="app",
        resource_id=row.id,
        request_id=x_request_id,
        metadata={"name": row.name, "vendor": row.vendor},
    )
    db.commit()
    db.refresh(row)
    return serialize_app(row)


@router.patch("/apps/{app_id}", response_model=dict)
def update_app(
    app_id: str,
    payload: DockAppUpdate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(default=None, alias="X-Request-Id"),
) -> dict:
    require_privileged(actor)
    row = get_app_or_404(db, app_id, actor.org_id)

    updates = payload.model_dump(exclude_unset=True)
    if "name" in updates:
        row.name = updates["name"]
    if "vendor" in updates:
        row.vendor = updates["vendor"]
    if "description" in updates:
        row.description = updates["description"]
    if "url" in updates:
        row.url = updates["url"]
    if "advertised" in updates:
        row.advertised = updates["advertised"]
    if "license_model" in updates:
        row.license_model = updates["license_model"]
    if "integrations" in updates and isinstance(updates["integrations"], list):
        row.integrations = [string_or_empty(item) for item in updates["integrations"] if string_or_empty(item)]

    emit_dock_event(
        db,
        actor,
        event_type="dock.app.updated",
        resource_type="app",
        resource_id=row.id,
        request_id=x_request_id,
        metadata={"name": row.name},
    )
    db.commit()
    db.refresh(row)
    return serialize_app(row)


@router.get("/licenses", response_model=list[dict])
def list_licenses(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> list[dict]:
    require_privileged(actor)
    rows = (
        db.query(License)
        .filter(License.org_id == actor.org_id)
        .order_by(License.created_at.desc())
        .all()
    )
    return [serialize_license(row) for row in rows]


@router.post("/licenses", response_model=dict, status_code=201)
def create_license(
    payload: LicenseCreate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(default=None, alias="X-Request-Id"),
) -> dict:
    require_privileged(actor)
    get_app_or_404(db, payload.app_id, actor.org_id)

    existing = get_license_for_app(db, payload.app_id, actor.org_id)
    if existing is not None:
        raise HTTPException(status_code=409, detail="License already exists for this app")

    budget_result = validate_budget(db, actor.org_id, payload.total_cost)
    license_status: LicenseStatus = "active"
    if not bool(budget_result["within_limit"]):
        license_status = "pending_finance_approval"

    row = License(
        id=f"rd-lic-{uuid.uuid4().hex[:10]}",
        org_id=actor.org_id,
        app_id=payload.app_id,
        seats_purchased=payload.seats_purchased,
        seats_assigned=0,
        currency=payload.currency.upper(),
        total_cost=payload.total_cost,
        renewal_date=payload.renewal_date,
        status=license_status,
        purchased_by=actor.user_id,
    )
    db.add(row)
    emit_dock_event(
        db,
        actor,
        event_type="dock.license.created",
        resource_type="license",
        resource_id=row.id,
        request_id=x_request_id,
        metadata={
            "app_id": row.app_id,
            "seats_purchased": str(row.seats_purchased),
            "status": row.status,
            "budget_policy_id": budget_result["policy_id"],
        },
    )
    db.commit()
    db.refresh(row)
    return serialize_license(row)


@router.get("/assignments", response_model=list[dict])
def list_assignments(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> list[dict]:
    query = db.query(Assignment).filter(Assignment.org_id == actor.org_id)
    if not is_privileged(actor):
        query = query.filter(Assignment.user_id == actor.user_id)
    rows = query.order_by(Assignment.updated_at.desc()).all()
    return [serialize_assignment(row) for row in rows]


@router.post("/assignments", response_model=dict, status_code=201)
def create_assignment(
    payload: AssignmentCreate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(default=None, alias="X-Request-Id"),
) -> dict:
    require_privileged(actor)
    get_app_or_404(db, payload.app_id, actor.org_id)

    duplicate = (
        db.query(Assignment)
        .filter(
            Assignment.org_id == actor.org_id,
            Assignment.app_id == payload.app_id,
            Assignment.user_id == payload.user_id,
            Assignment.status == "active",
        )
        .first()
    )
    if duplicate is not None:
        raise HTTPException(status_code=409, detail="User already has an active assignment for this app")

    license_row = get_license_for_app(db, payload.app_id, actor.org_id)
    if license_row is None or license_row.seats_assigned >= license_row.seats_purchased:
        raise HTTPException(status_code=409, detail="Seat Capacity Reached")

    row = Assignment(
        id=f"rd-asg-{uuid.uuid4().hex[:10]}",
        org_id=actor.org_id,
        app_id=payload.app_id,
        user_id=payload.user_id,
        access_level=payload.access_level,
        status="active",
        assigned_by=actor.user_id,
    )
    db.add(row)
    license_row.seats_assigned += 1

    emit_dock_event(
        db,
        actor,
        event_type="dock.license.assigned",
        resource_type="assignment",
        resource_id=row.id,
        request_id=x_request_id,
        metadata={"app_id": row.app_id, "user_id": row.user_id, "status": row.status},
    )
    db.commit()
    db.refresh(row)
    sync_assignment_post_commit(db, actor, row, x_request_id)
    return serialize_assignment(row)


@router.patch("/assignments/{assignment_id}", response_model=dict)
def update_assignment(
    assignment_id: str,
    payload: AssignmentUpdate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(default=None, alias="X-Request-Id"),
) -> dict:
    require_privileged(actor)
    row = get_assignment_or_404(db, assignment_id, actor.org_id)
    license_row = get_license_for_app(db, row.app_id, actor.org_id)

    updates = payload.model_dump(exclude_unset=True)
    if "access_level" in updates:
        row.access_level = updates["access_level"]

    if "status" in updates:
        requested_status = updates["status"]
        if row.status != requested_status:
            if row.status == "active" and requested_status == "revoked" and license_row is not None:
                license_row.seats_assigned = max(0, license_row.seats_assigned - 1)
            if row.status == "revoked" and requested_status == "active":
                if license_row is None or license_row.seats_assigned >= license_row.seats_purchased:
                    raise HTTPException(status_code=409, detail="Seat Capacity Reached")
                license_row.seats_assigned += 1
            row.status = requested_status

    emit_dock_event(
        db,
        actor,
        event_type="dock.license.assignment_updated",
        resource_type="assignment",
        resource_id=row.id,
        request_id=x_request_id,
        metadata={"app_id": row.app_id, "user_id": row.user_id, "status": row.status},
    )
    db.commit()
    db.refresh(row)
    sync_assignment_post_commit(db, actor, row, x_request_id)
    return serialize_assignment(row)


@router.get("/requests", response_model=list[dict])
def list_requests(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> list[dict]:
    query = db.query(DockRequest).filter(DockRequest.org_id == actor.org_id)
    if not is_privileged(actor):
        query = query.filter(DockRequest.requester_user_id == actor.user_id)
    rows = query.order_by(DockRequest.updated_at.desc()).all()
    return [serialize_request(row) for row in rows]


@router.post("/requests", response_model=dict, status_code=201)
def create_request(
    payload: DockRequestCreate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(default=None, alias="X-Request-Id"),
) -> dict:
    row = DockRequest(
        id=f"rd-req-{uuid.uuid4().hex[:10]}",
        org_id=actor.org_id,
        requester_user_id=actor.user_id,
        app_name=payload.app_name,
        reason=payload.reason,
        requested_seats=payload.requested_seats,
        business_justification=payload.business_justification,
        status="pending",
        reviewer_user_id=None,
        review_notes=None,
        linked_app_id=None,
        automation_ticket_id=None,
        automation_status="idle",
        automation_last_error=None,
        automation_hint=None,
    )
    row.automation_hint = build_request_automation_hint(row)

    db.add(row)
    emit_dock_event(
        db,
        actor,
        event_type="dock.request.created",
        resource_type="request",
        resource_id=row.id,
        request_id=x_request_id,
        metadata={"app_name": row.app_name, "requested_seats": str(row.requested_seats)},
    )
    db.commit()
    db.refresh(row)
    return serialize_request(row)


@router.patch("/requests/{request_id}", response_model=dict)
def update_request(
    request_id: str,
    payload: DockRequestUpdate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(default=None, alias="X-Request-Id"),
) -> dict:
    require_privileged(actor)
    row = get_request_or_404(db, request_id, actor.org_id)
    status_changed = False

    updates = payload.model_dump(exclude_unset=True)
    if "status" in updates:
        target = updates["status"]
        if not valid_request_transition(row.status, target):
            raise HTTPException(status_code=400, detail="Invalid request status transition")
        status_changed = row.status != target
        row.status = target
        row.reviewer_user_id = actor.user_id

    if "review_notes" in updates:
        row.review_notes = updates["review_notes"]

    if "linked_app_id" in updates:
        linked_app_id = updates["linked_app_id"]
        if linked_app_id:
            get_app_or_404(db, linked_app_id, actor.org_id)
        row.linked_app_id = linked_app_id

    if status_changed or "linked_app_id" in updates:
        run_carf_automation(row, actor)

    emit_dock_event(
        db,
        actor,
        event_type="dock.request.updated",
        resource_type="request",
        resource_id=row.id,
        request_id=x_request_id,
        metadata={
            "status": row.status,
            "reviewer_user_id": string_or_empty(row.reviewer_user_id),
            "automation_status": row.automation_status,
        },
    )
    db.commit()
    db.refresh(row)
    return serialize_request(row)


@router.get("/audit/events", response_model=list[dict])
def list_audit_events(
    limit: int = 200,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
) -> list[dict]:
    require_privileged(actor)
    bounded_limit = min(max(int(limit), 1), 1000)
    rows = (
        db.query(DockAuditEvent)
        .filter(DockAuditEvent.org_id == actor.org_id)
        .order_by(DockAuditEvent.timestamp.desc())
        .limit(bounded_limit)
        .all()
    )
    return [serialize_event(row) for row in rows]


@router.get("/carf", response_model=list[dict])
def list_carf(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> list[dict]:
    return list_requests(actor=actor, db=db)


@router.post("/carf", response_model=dict, status_code=201)
def create_carf(
    payload: DockRequestCreate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(default=None, alias="X-Request-Id"),
) -> dict:
    return create_request(payload=payload, actor=actor, db=db, x_request_id=x_request_id)


@router.get("/budget-policies", response_model=list[dict])
def list_budget_policies(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> list[dict]:
    require_privileged(actor)
    rows = (
        db.query(BudgetPolicy)
        .filter(BudgetPolicy.org_id == actor.org_id)
        .order_by(BudgetPolicy.created_at.desc())
        .all()
    )
    return [serialize_budget_policy(row) for row in rows]


@router.post("/budget-policies", response_model=dict, status_code=201)
def create_budget_policy(
    payload: BudgetPolicyCreate,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
) -> dict:
    require_privileged(actor)
    row = BudgetPolicy(
        id=f"rd-bp-{uuid.uuid4().hex[:10]}",
        org_id=actor.org_id,
        department_id=string_or_empty(payload.department_id) or None,
        monthly_limit=payload.monthly_limit,
        currency=payload.currency.upper(),
        alert_threshold_pct=payload.alert_threshold_pct,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize_budget_policy(row)


@router.get("/procurement-config", response_model=dict)
def get_procurement_config(actor: Actor = Depends(get_actor_dependency), db: Session = Depends(get_db)) -> dict:
    require_privileged(actor)
    row = (
        db.query(ProcurementConfig)
        .filter(ProcurementConfig.org_id == actor.org_id)
        .order_by(ProcurementConfig.created_at.desc())
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Procurement config not found")
    return serialize_procurement_config(row)


@router.put("/procurement-config", response_model=dict)
def upsert_procurement_config(
    payload: ProcurementConfigUpsert,
    actor: Actor = Depends(get_actor_dependency),
    db: Session = Depends(get_db),
) -> dict:
    require_privileged(actor)
    row = (
        db.query(ProcurementConfig)
        .filter(ProcurementConfig.org_id == actor.org_id)
        .order_by(ProcurementConfig.created_at.desc())
        .first()
    )
    if row is None:
        row = ProcurementConfig(
            id=f"rd-pc-{uuid.uuid4().hex[:10]}",
            org_id=actor.org_id,
            require_manager_approval=payload.require_manager_approval,
            auto_approve_threshold=payload.auto_approve_threshold,
        )
        db.add(row)
    else:
        row.require_manager_approval = payload.require_manager_approval
        row.auto_approve_threshold = payload.auto_approve_threshold

    db.commit()
    db.refresh(row)
    return serialize_procurement_config(row)
