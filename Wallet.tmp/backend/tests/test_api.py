from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import get_db
from app.main import app


TEST_DATABASE_URL = "sqlite:///./wallet_test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def auth_headers(org: str, user: str, role: str = "admin") -> dict[str, str]:
    return {
        "X-Org-Id": org,
        "X-User-Id": user,
        "X-User-Role": role,
    }


def setup_function() -> None:
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "wallet"}


def test_secret_create_list_reveal_flow() -> None:
    created = client.post(
        "/api/wallet/secrets",
        headers=auth_headers("org-1", "alice"),
        json={
            "name": "Stripe Key",
            "value": "sk-live-123",
            "description": "Billing secret",
            "secret_type": "api_key",
            "tags": ["billing", "prod"],
        },
    )
    assert created.status_code == 201
    secret_id = created.json()["id"]

    listed = client.get("/api/wallet/secrets", headers=auth_headers("org-1", "alice"))
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["name"] == "Stripe Key"

    revealed = client.get(f"/api/wallet/secrets/{secret_id}/reveal", headers=auth_headers("org-1", "alice"))
    assert revealed.status_code == 200
    assert revealed.json()["value"] == "sk-live-123"


def test_shared_info_is_org_scoped_with_global_visibility() -> None:
    db = TestingSessionLocal()
    try:
        db.add(
            models.SharedInfo(
                org_id="*",
                category="misc",
                title="Global DNS",
                value="ns1.example.net",
                tags=["dns"],
            )
        )
        db.add(
            models.SharedInfo(
                org_id="org-2",
                category="cloudflare",
                title="Org2 Zone",
                value="org2.zone",
                tags=["zone"],
            )
        )
        db.add(
            models.SharedInfo(
                org_id="org-3",
                category="cloudflare",
                title="Org3 Zone",
                value="org3.zone",
                tags=["zone"],
            )
        )
        db.commit()
    finally:
        db.close()

    response = client.get("/api/wallet/shared-info", headers=auth_headers("org-2", "bob"))
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 2
    titles = {row["title"] for row in rows}
    assert "Global DNS" in titles
    assert "Org2 Zone" in titles
    assert "Org3 Zone" not in titles
