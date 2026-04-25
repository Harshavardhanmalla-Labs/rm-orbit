from __future__ import annotations

from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

import app.routes as routes_module
from app.database import SessionLocal
from app.main import app


client = TestClient(app)


def headers(org: str, user: str, role: str = "member") -> dict[str, str]:
    return {
        "X-Org-Id": org,
        "X-User-Id": user,
        "X-User-Role": role,
    }


@pytest.fixture(autouse=True)
def disable_secure_sync(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setattr(routes_module, "POST_COMMIT_SYNC_ENABLED", False)
    yield


@pytest.fixture(autouse=True)
def clean_tables() -> Iterator[None]:
    try:
        with SessionLocal() as db:
            db.execute(
                text(
                    """
                    TRUNCATE TABLE
                      dock_assignments,
                      dock_licenses,
                      dock_apps,
                      dock_requests,
                      dock_audit_events,
                      dock_budget_policies,
                      dock_procurement_configs
                    RESTART IDENTITY CASCADE
                    """
                )
            )
            db.commit()
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"Dock database unavailable for API tests: {exc}")

    yield


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"service": "rm-dock", "status": "ok"}


def test_budget_guardrail_marks_license_pending_finance_approval() -> None:
    admin_headers = headers("org-budget", "admin-1", "admin")

    policy = client.post(
        "/api/dock/budget-policies",
        headers=admin_headers,
        json={
            "department_id": "eng",
            "monthly_limit": 500,
            "currency": "USD",
            "alert_threshold_pct": 90,
        },
    )
    assert policy.status_code == 201

    app_created = client.post(
        "/api/dock/apps",
        headers=admin_headers,
        json={
            "name": "Figma Enterprise",
            "vendor": "Figma",
            "description": "Design collaboration",
            "advertised": True,
        },
    )
    assert app_created.status_code == 201
    app_id = app_created.json()["id"]

    license_created = client.post(
        "/api/dock/licenses",
        headers=admin_headers,
        json={
            "app_id": app_id,
            "seats_purchased": 5,
            "currency": "USD",
            "total_cost": 1500,
        },
    )
    assert license_created.status_code == 201
    assert license_created.json()["status"] == "pending_finance_approval"


def test_assignment_enforces_seat_capacity() -> None:
    admin_headers = headers("org-seats", "admin-1", "admin")

    app_created = client.post(
        "/api/dock/apps",
        headers=admin_headers,
        json={"name": "Jira Cloud", "vendor": "Atlassian", "advertised": True},
    )
    assert app_created.status_code == 201
    app_id = app_created.json()["id"]

    license_created = client.post(
        "/api/dock/licenses",
        headers=admin_headers,
        json={"app_id": app_id, "seats_purchased": 1, "currency": "USD", "total_cost": 100},
    )
    assert license_created.status_code == 201

    first_assignment = client.post(
        "/api/dock/assignments",
        headers=admin_headers,
        json={"app_id": app_id, "user_id": "designer-1", "access_level": "editor"},
    )
    assert first_assignment.status_code == 201

    second_assignment = client.post(
        "/api/dock/assignments",
        headers=admin_headers,
        json={"app_id": app_id, "user_id": "designer-2", "access_level": "editor"},
    )
    assert second_assignment.status_code == 409
    assert second_assignment.json()["detail"] == "Seat Capacity Reached"


def test_member_cannot_create_licenses() -> None:
    response = client.post(
        "/api/dock/licenses",
        headers=headers("org-rbac", "member-1", "member"),
        json={"app_id": "rd-app-none", "seats_purchased": 2},
    )
    assert response.status_code == 403


def test_assignment_lifecycle_triggers_secure_post_commit_sync(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(routes_module, "POST_COMMIT_SYNC_ENABLED", True)
    synced: list[tuple[str, str, str, str]] = []

    def _fake_sync(assignment):
        synced.append((assignment.org_id, assignment.user_id, assignment.app_id, assignment.status))
        return None

    monkeypatch.setattr(routes_module, "sync_assignment_to_secure", _fake_sync)

    admin_headers = headers("org-sync", "admin-1", "admin")
    app_created = client.post(
        "/api/dock/apps",
        headers=admin_headers,
        json={"name": "Secure Console", "vendor": "RM", "advertised": True},
    )
    assert app_created.status_code == 201
    app_id = app_created.json()["id"]

    license_created = client.post(
        "/api/dock/licenses",
        headers=admin_headers,
        json={"app_id": app_id, "seats_purchased": 1, "currency": "USD", "total_cost": 100},
    )
    assert license_created.status_code == 201

    assignment_created = client.post(
        "/api/dock/assignments",
        headers=admin_headers,
        json={"app_id": app_id, "user_id": "user-sync-1", "access_level": "user"},
    )
    assert assignment_created.status_code == 201
    assignment_id = assignment_created.json()["id"]

    assignment_revoked = client.patch(
        f"/api/dock/assignments/{assignment_id}",
        headers=admin_headers,
        json={"status": "revoked"},
    )
    assert assignment_revoked.status_code == 200

    assert len(synced) == 2
    assert synced[0] == ("org-sync", "user-sync-1", app_id, "active")
    assert synced[1] == ("org-sync", "user-sync-1", app_id, "revoked")
