from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.main import build_app


def test_sources_endpoint_lists_writer_and_learn() -> None:
    app = build_app()
    client = TestClient(app)
    response = client.get("/api/search/sources")
    assert response.status_code == 200
    payload = response.json()
    keys = [entry["key"] for entry in payload["sources"]]
    assert "writer" in keys
    assert "learn" in keys
    assert response.headers.get("x-request-id")


def test_search_merges_and_sorts_results(
    monkeypatch,
) -> None:
    from app import main as search_main

    def fake_writer(query, workspace_id, org_id, limit):
        return [
            search_main.SearchResult(
                id="writer:1",
                source="writer",
                entity_type="document",
                title="Q4 Planning",
                score=7.0,
                metadata={},
            )
        ]

    def fake_learn(query, limit):
        return [
            search_main.SearchResult(
                id="learn:a",
                source="learn",
                entity_type="doc_page",
                title="Search Guide",
                score=6.0,
                metadata={},
            ),
            search_main.SearchResult(
                id="learn:b",
                source="learn",
                entity_type="doc_page",
                title="Advanced Querying",
                score=9.0,
                metadata={},
            ),
        ]

    monkeypatch.setattr(search_main, "search_writer_documents", fake_writer)
    monkeypatch.setattr(search_main, "search_learn_docs", fake_learn)

    app = build_app()
    client = TestClient(app)
    response = client.get(
        "/api/search",
        params={"q": "search", "limit": 2},
        headers={"X-Workspace-Id": "ws-test", "X-Org-Id": "org-test"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    assert payload["org_id"] == "org-test"
    assert payload["workspace_id"] == "ws-test"
    assert payload["results"][0]["id"] == "learn:b"
    assert payload["results"][1]["id"] == "writer:1"


def test_learn_adapter_reads_local_html(tmp_path: Path, monkeypatch) -> None:
    from app import main as search_main

    learn_dir = tmp_path / "learn"
    learn_dir.mkdir(parents=True, exist_ok=True)
    (learn_dir / "guide.html").write_text(
        "<html><head><title>Getting Started</title></head><body><h1>Quick setup</h1></body></html>",
        encoding="utf-8",
    )
    monkeypatch.setattr(search_main, "LEARN_SITE_DIR", learn_dir)

    results = search_main.search_learn_docs("getting", limit=10)
    assert len(results) == 1
    assert results[0].source == "learn"
    assert "Getting Started" in results[0].title
