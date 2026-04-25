from __future__ import annotations

from pathlib import Path

import jwt
import pytest
from fastapi.testclient import TestClient

from app.main import create_app, redact_database_url


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    database_url = f"sqlite:///{tmp_path / 'writer-test.db'}"
    app = create_app(database_url=database_url)
    with TestClient(app) as test_client:
        yield test_client


def _build_auth_header(
    *,
    secret: str = "writer-test-secret",
    subject: str = "user-1",
    org_id: str = "org-1",
    workspace_id: str = "ws-ops",
) -> str:
    payload = {
        "sub": subject,
        "org_id": org_id,
        "workspace_id": workspace_id,
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return f"Bearer {token}"


def test_workspace_header_is_required(client: TestClient) -> None:
    response = client.post("/api/documents", json={"title": "Missing workspace"})
    assert response.status_code == 400
    assert "X-Workspace-Id" in response.json()["detail"]


def test_writer_sets_request_id_header(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers.get("x-request-id")


def test_redact_database_url_masks_password() -> None:
    raw = "postgresql+psycopg://orbit_writer:super-secret@db:5432/orbit_writer"
    redacted = redact_database_url(raw)
    assert "super-secret" not in redacted
    assert "***" in redacted


def test_feedback_submission(client: TestClient) -> None:
    response = client.post(
        "/api/feedback",
        headers={"X-Workspace-Id": "ws-feedback"},
        json={
            "rating": 5,
            "area": "editor",
            "message": "Fast and clear editing flow.",
            "page": "/document",
        },
    )
    assert response.status_code == 202
    payload = response.json()
    assert payload["status"] == "accepted"
    assert payload["received_at"]

    summary = client.get(
        "/api/feedback/summary?days=30",
        headers={"X-Workspace-Id": "ws-feedback"},
    )
    assert summary.status_code == 200
    summary_payload = summary.json()
    assert summary_payload["total"] == 1
    assert summary_payload["average_rating"] == 5
    assert summary_payload["areas"][0]["area"] == "editor"
    assert summary_payload["recent"][0]["page"] == "/document"


def test_feedback_summary_is_workspace_scoped(client: TestClient) -> None:
    response_a = client.post(
        "/api/feedback",
        headers={"X-Workspace-Id": "ws-a"},
        json={"rating": 4, "area": "dashboard", "message": "Good"},
    )
    response_b = client.post(
        "/api/feedback",
        headers={"X-Workspace-Id": "ws-b"},
        json={"rating": 2, "area": "editor", "message": "Laggy"},
    )
    assert response_a.status_code == 202
    assert response_b.status_code == 202

    summary_a = client.get("/api/feedback/summary", headers={"X-Workspace-Id": "ws-a"})
    summary_b = client.get("/api/feedback/summary", headers={"X-Workspace-Id": "ws-b"})
    assert summary_a.status_code == 200
    assert summary_b.status_code == 200
    assert summary_a.json()["total"] == 1
    assert summary_b.json()["total"] == 1
    assert summary_a.json()["recent"][0]["area"] == "dashboard"
    assert summary_b.json()["recent"][0]["area"] == "editor"


def test_document_block_graph_and_versions_flow(client: TestClient) -> None:
    headers = {"X-Workspace-Id": "ws-ops"}

    created_doc = client.post(
        "/api/documents",
        headers=headers,
        json={
            "title": "Q2 Planning",
            "initial_block_type": "text",
            "initial_content": {"text": "Root note"},
        },
    )
    assert created_doc.status_code == 201
    doc_payload = created_doc.json()
    doc_id = doc_payload["id"]

    list_docs = client.get("/api/documents", headers=headers)
    assert list_docs.status_code == 200
    assert len(list_docs.json()) == 1
    assert list_docs.json()[0]["block_count"] == 1

    blocks = client.get(f"/api/documents/{doc_id}/blocks", headers=headers)
    assert blocks.status_code == 200
    root_block_id = blocks.json()[0]["id"]

    child = client.post(
        f"/api/documents/{doc_id}/blocks",
        headers=headers,
        json={
            "parent_block_id": root_block_id,
            "type": "table",
            "content": {"columns": ["kpi", "value"], "rows": [["ARR", "1.2M"]]},
            "position_index": 10,
        },
    )
    assert child.status_code == 201
    child_id = child.json()["id"]
    assert child.json()["version"] == 1

    updated = client.patch(
        f"/api/blocks/{child_id}",
        headers=headers,
        json={
            "content": {"columns": ["kpi", "value"], "rows": [["ARR", "1.4M"]]},
            "metadata": {"updated_by": "ai-assist"},
        },
    )
    assert updated.status_code == 200
    assert updated.json()["version"] == 2
    assert updated.json()["content"]["rows"][0][1] == "1.4M"

    versions = client.get(f"/api/blocks/{child_id}/versions", headers=headers)
    assert versions.status_code == 200
    assert len(versions.json()) == 1
    assert versions.json()[0]["snapshot"]["version"] == 1

    relation = client.post(
        f"/api/blocks/{child_id}/relations",
        headers=headers,
        json={"target_block_id": root_block_id, "relation_type": "supports"},
    )
    assert relation.status_code == 201
    assert relation.json()["relation_type"] == "supports"

    graph = client.get(f"/api/documents/{doc_id}/graph", headers=headers)
    assert graph.status_code == 200
    assert len(graph.json()["nodes"]) == 2
    assert len(graph.json()["edges"]) == 1


def test_workspace_isolation(client: TestClient) -> None:
    created_doc = client.post(
        "/api/documents",
        headers={"X-Workspace-Id": "ws-a"},
        json={"title": "Confidential"},
    )
    assert created_doc.status_code == 201
    doc_id = created_doc.json()["id"]

    forbidden = client.get(f"/api/documents/{doc_id}", headers={"X-Workspace-Id": "ws-b"})
    assert forbidden.status_code == 404


def test_create_document_publishes_writer_event(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: list[tuple[str, dict]] = []

    def fake_publish(event_type: str, event: dict | None = None) -> dict:
        captured.append((event_type, dict(event or {})))
        return {}

    monkeypatch.setattr("app.main.publish_writer_event", fake_publish)

    response = client.post(
        "/api/documents",
        headers={
            "X-Workspace-Id": "ws-events",
            "X-Org-Id": "org-events",
        },
        json={"title": "Evented Doc"},
    )
    assert response.status_code == 201
    assert len(captured) == 1
    event_type, event_payload = captured[0]
    assert event_type == "writer.document.created"
    assert event_payload["org_id"] == "org-events"
    assert event_payload["workspace_id"] == "ws-events"
    assert event_payload["data"]["document_id"] == response.json()["id"]


def test_auth_required_rejects_missing_bearer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WRITER_AUTH_REQUIRED", "1")
    monkeypatch.setenv("JWT_SECRET", "writer-test-secret")

    database_url = f"sqlite:///{tmp_path / 'writer-auth-required.db'}"
    app = create_app(database_url=database_url)
    with TestClient(app) as auth_client:
        response = auth_client.get("/api/render-modes")

    assert response.status_code == 401
    assert "credentials" in response.json()["detail"].lower()


def test_auth_required_accepts_valid_hs256_token(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("WRITER_AUTH_REQUIRED", "1")
    monkeypatch.setenv("ALLOW_LOCAL_HS256_FALLBACK", "1")
    monkeypatch.setenv("JWT_SECRET", "writer-test-secret")

    database_url = f"sqlite:///{tmp_path / 'writer-auth-valid.db'}"
    app = create_app(database_url=database_url)
    with TestClient(app) as auth_client:
        response = auth_client.post(
            "/api/documents",
            headers={
                "Authorization": _build_auth_header(),
                "X-Workspace-Id": "ws-ops",
            },
            json={"title": "JWT Protected Doc"},
        )

    assert response.status_code == 201
    assert response.json()["workspace_id"] == "ws-ops"


def test_auth_rejects_org_header_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("WRITER_AUTH_REQUIRED", "1")
    monkeypatch.setenv("ALLOW_LOCAL_HS256_FALLBACK", "1")
    monkeypatch.setenv("JWT_SECRET", "writer-test-secret")

    database_url = f"sqlite:///{tmp_path / 'writer-auth-org-mismatch.db'}"
    app = create_app(database_url=database_url)
    with TestClient(app) as auth_client:
        response = auth_client.post(
            "/api/documents",
            headers={
                "Authorization": _build_auth_header(org_id="org-a"),
                "X-Workspace-Id": "ws-ops",
                "X-Org-Id": "org-b",
            },
            json={"title": "Org mismatch"},
        )

    assert response.status_code == 403
    assert "org mismatch" in response.json()["detail"].lower()
