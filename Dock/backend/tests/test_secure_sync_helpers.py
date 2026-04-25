from __future__ import annotations

from dataclasses import dataclass

import app.routes as routes_module


@dataclass
class _AssignmentStub:
    id: str = "rd-asg-unit-1"
    org_id: str = "org-unit"
    user_id: str = "user-unit"
    app_id: str = "rm-connect"
    status: str = "active"


class _ResponseStub:
    def __init__(self, status_code: int, text: str = ""):
        self.status_code = status_code
        self.text = text


def test_sync_assignment_to_secure_posts_expected_payload(monkeypatch):
    captured: dict[str, object] = {}

    class _ClientStub:
        def __init__(self, timeout: float):
            captured["timeout"] = timeout

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def post(self, url, headers, json):
            captured["url"] = url
            captured["headers"] = headers
            captured["json"] = json
            return _ResponseStub(200)

    monkeypatch.setattr(routes_module, "POST_COMMIT_SYNC_ENABLED", True)
    monkeypatch.setattr(routes_module, "DOCK_SECURE_BRIDGE_URL", "http://secure.local/bridge")
    monkeypatch.setattr(routes_module, "DOCK_SECURE_INTERNAL_TOKEN", "secret")
    monkeypatch.setattr(routes_module.httpx, "Client", _ClientStub)

    error = routes_module.sync_assignment_to_secure(_AssignmentStub())
    assert error is None
    assert captured["url"] == "http://secure.local/bridge"
    assert captured["headers"] == {
        "Content-Type": "application/json",
        "X-Tenant-ID": "org-unit",
        "X-Internal-Token": "secret",
    }
    assert captured["json"] == {
        "tenant_id": "org-unit",
        "user_id": "user-unit",
        "app_id": "rm-connect",
        "status": "active",
    }


def test_sync_assignment_to_secure_returns_error_for_non_2xx(monkeypatch):
    class _ClientStub:
        def __init__(self, timeout: float):
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def post(self, url, headers, json):
            return _ResponseStub(500, "secure bridge unavailable")

    monkeypatch.setattr(routes_module, "POST_COMMIT_SYNC_ENABLED", True)
    monkeypatch.setattr(routes_module, "DOCK_SECURE_BRIDGE_URL", "http://secure.local/bridge")
    monkeypatch.setattr(routes_module, "DOCK_SECURE_INTERNAL_TOKEN", "")
    monkeypatch.setattr(routes_module.httpx, "Client", _ClientStub)

    error = routes_module.sync_assignment_to_secure(_AssignmentStub())
    assert error == "secure bridge unavailable"


def test_sync_assignment_to_secure_noop_when_disabled(monkeypatch):
    monkeypatch.setattr(routes_module, "POST_COMMIT_SYNC_ENABLED", False)
    error = routes_module.sync_assignment_to_secure(_AssignmentStub())
    assert error is None
