from __future__ import annotations

import os
import re
from time import perf_counter
from pathlib import Path
import sys
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
from uuid import uuid4

from fastapi import FastAPI, Header, Query, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.orbit_audit import build_audit_record, emit_audit, get_audit_logger

LEARN_SITE_DIR = Path(os.getenv("SEARCH_LEARN_SITE_DIR", ROOT_DIR / "Learn" / "site"))
WRITER_API_BASE = os.getenv("SEARCH_WRITER_API_BASE", "http://localhost:6011")
HTTP_TIMEOUT_SECONDS = float(os.getenv("SEARCH_HTTP_TIMEOUT_SECONDS", "2.0"))
AUDIT_LOGGER = get_audit_logger("orbit.audit.search")


class SearchResult(BaseModel):
    id: str
    source: str
    entity_type: str
    title: str
    snippet: str = ""
    url: str = ""
    score: float
    updated_at: str | None = None
    metadata: dict[str, Any] = {}


class SearchResponse(BaseModel):
    query: str
    org_id: str | None = None
    workspace_id: str | None = None
    total: int
    took_ms: int
    sources: list[str]
    results: list[SearchResult]


def _clean_tokens(value: str) -> list[str]:
    return [token for token in re.split(r"\W+", value.lower()) if token]


def _score_text(query_tokens: list[str], text: str) -> float:
    if not text:
        return 0.0
    lowered = text.lower()
    score = 0.0
    for token in query_tokens:
        if token in lowered:
            score += 1.0
        if lowered.startswith(token):
            score += 0.5
    return score


def _extract_title(html_text: str, fallback: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return fallback
    title = re.sub(r"\s+", " ", match.group(1)).strip()
    return title or fallback


def _extract_snippet(html_text: str) -> str:
    for tag in ("h1", "p", "h2"):
        match = re.search(
            rf"<{tag}[^>]*>(.*?)</{tag}>",
            html_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if match:
            text = re.sub(r"<[^>]+>", " ", match.group(1))
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                return text[:240]
    text = re.sub(r"<[^>]+>", " ", html_text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:240]


def search_learn_docs(query: str, limit: int) -> list[SearchResult]:
    query_tokens = _clean_tokens(query)
    if not query_tokens or not LEARN_SITE_DIR.exists():
        return []

    results: list[SearchResult] = []
    for html_file in LEARN_SITE_DIR.glob("*.html"):
        try:
            html_text = html_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        title = _extract_title(html_text, html_file.stem.replace("-", " ").title())
        snippet = _extract_snippet(html_text)
        combined = f"{title} {snippet} {html_file.name}"
        score = _score_text(query_tokens, combined)
        if score <= 0:
            continue

        results.append(
            SearchResult(
                id=f"learn:{html_file.name}",
                source="learn",
                entity_type="doc_page",
                title=title,
                snippet=snippet,
                url=f"/learn/{html_file.name}",
                score=score,
                metadata={"file": html_file.name},
            )
        )

    return sorted(results, key=lambda item: item.score, reverse=True)[:limit]


def _writer_headers(workspace_id: str, org_id: str | None) -> dict[str, str]:
    headers = {"X-Workspace-Id": workspace_id}
    if org_id:
        headers["X-Org-Id"] = org_id
    return headers


def search_writer_documents(
    query: str,
    workspace_id: str | None,
    org_id: str | None,
    limit: int,
) -> list[SearchResult]:
    if not workspace_id:
        return []

    query_tokens = _clean_tokens(query)
    params = urlencode({"limit": max(limit * 3, 30)})
    url = f"{WRITER_API_BASE}/api/documents?{params}"
    request = Request(url, headers=_writer_headers(workspace_id, org_id))

    try:
        with urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError, ValueError):
        return []

    results: list[SearchResult] = []
    for doc in payload if isinstance(payload, list) else []:
        title = str(doc.get("title") or "").strip()
        if not title:
            continue
        combined = f"{title} {doc.get('id', '')}"
        score = _score_text(query_tokens, combined)
        if score <= 0:
            continue

        results.append(
            SearchResult(
                id=f"writer:{doc.get('id')}",
                source="writer",
                entity_type="document",
                title=title,
                snippet=f"{doc.get('block_count', 0)} blocks",
                url=f"/document?id={doc.get('id')}",
                score=score + 0.25,
                updated_at=doc.get("updated_at"),
                metadata={
                    "document_id": doc.get("id"),
                    "workspace_id": workspace_id,
                },
            )
        )

    return sorted(results, key=lambda item: item.score, reverse=True)[:limit]


def build_app() -> FastAPI:
    app = FastAPI(
        title="RM Orbit Search Aggregator",
        version="0.1.0",
        description="Cross-app search contract baseline (Writer + Learn).",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def audit_requests(request: FastAPIRequest, call_next):
        started = perf_counter()
        request_id = request.headers.get("X-Request-Id") or str(uuid4())
        response = None
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = int((perf_counter() - started) * 1000)
            org_id = request.headers.get("X-Org-Id")
            workspace_id = request.headers.get("X-Workspace-Id")
            record = build_audit_record(
                service="orbit-search",
                event="http.request",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                duration_ms=duration_ms,
                org_id=org_id,
                workspace_id=workspace_id,
                extra={"query": request.url.query},
            )
            emit_audit(AUDIT_LOGGER, record)
            if response is not None:
                response.headers["X-Request-Id"] = request_id

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "service": "orbit-search",
            "sources": ["writer", "learn"],
        }

    @app.get("/api/search/sources")
    def list_sources() -> dict[str, Any]:
        return {
            "sources": [
                {"key": "writer", "entity_types": ["document"]},
                {"key": "learn", "entity_types": ["doc_page"]},
            ]
        }

    @app.get("/api/search", response_model=SearchResponse)
    async def search(
        request: FastAPIRequest,
        q: str = Query(..., min_length=2),
        limit: int = Query(default=20, ge=1, le=50),
        org_id: str | None = Query(default=None),
        workspace_id: str | None = Query(default=None),
        x_org_id: str | None = Header(default=None, alias="X-Org-Id"),
        x_workspace_id: str | None = Header(default=None, alias="X-Workspace-Id"),
        authorization: str | None = Header(default=None),
    ) -> dict: # Returning dict to avoid model issues if the model fields mismatch slightly
        import asyncio
        import httpx
        started = perf_counter()
        resolved_org_id = (org_id or x_org_id or "").strip() or None
        resolved_workspace_id = (workspace_id or x_workspace_id or "").strip() or None

        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        if resolved_org_id:
            headers["X-Org-Id"] = resolved_org_id
        if resolved_workspace_id:
            headers["X-Workspace-Id"] = resolved_workspace_id


        # Async fetch helper
        async def fetch(name: str, url: str) -> list[SearchResult]:
            try:
                async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS) as client:
                    resp = await client.get(url, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        reformatted = []
                        if name == "atlas":
                            for proj in data.get("projects", []):
                                reformatted.append(SearchResult(id=f"atlas:proj:{proj['id']}", source="atlas", entity_type="project", title=proj['name'], snippet=f"Project Key: {proj.get('key', '')}", url=f"http://localhost:5173/projects/{proj['id']}", score=2.0))
                            for task in data.get("tasks", []):
                                reformatted.append(SearchResult(id=f"atlas:task:{task['id']}", source="atlas", entity_type="task", title=task['title'], snippet=f"Task {task.get('task_number', '')} in {task.get('project_key', '')}", url=f"http://localhost:5173/projects/{task.get('project_id')}", score=1.5))
                        elif name == "mail":
                            # Mail returns success({"items": [...]}) or similar
                            items = data.get("data", {}).get("items") if isinstance(data.get("data"), dict) else data.get("results")
                            if items is None and isinstance(data, dict):
                                items = data.get("items") or data.get("data")
                            if items:
                                for item in items:
                                    reformatted.append(SearchResult(id=f"mail:{item['id']}", source="mail", entity_type="email", title=item.get('subject', 'No Subject'), snippet=f"From: {item.get('sender', 'Unknown')}", url=f"http://localhost:45004/inbox", score=1.8))
                        elif name == "connect":
                            for channel in data.get("channels", []):
                                reformatted.append(SearchResult(id=f"connect:channel:{channel['id']}", source="connect", entity_type="channel", title=channel['name'], snippet=channel.get('description', ''), url=f"http://localhost:45008/", score=1.9))
                            for msg in data.get("messages", []):
                                reformatted.append(SearchResult(id=f"connect:msg:{msg['id']}", source="connect", entity_type="message", title=f"Message in {msg.get('channel_name', 'Channel')}", snippet=msg.get('content', '')[:100], url=f"http://localhost:45008/", score=1.2))
                        elif name == "planet":
                            for deal in data.get("results", []):
                                reformatted.append(SearchResult(id=f"planet:{deal['id']}", source="planet", entity_type="deal", title=deal['name'], snippet=f"Company: {deal.get('company', '')} | Industry: {deal.get('industry', '')}", url=f"http://localhost:45006/", score=1.7))
                        elif name == "turbotick":
                            for item in data.get("results", []):
                                reformatted.append(SearchResult(id=f"turbotick:{item['entity_type']}:{item['id']}", source="turbotick", entity_type=item['entity_type'], title=item['title'], snippet=item.get('snippet', ''), url=f"http://localhost:45018/", score=item.get('score', 1.0) + 1.0))
                        return reformatted
            except Exception as e:
                print(f"Error fetching from {name}: {e}")
            return []

        # Run external searches in parallel
        # writer blocks
        collected: list[SearchResult] = []
        collected.extend(
            search_writer_documents(
                query=q,
                workspace_id=resolved_workspace_id,
                org_id=resolved_org_id,
                limit=limit,
            )
        )
        collected.extend(search_learn_docs(query=q, limit=limit))

        tasks = [
            fetch("atlas", f"http://localhost:8000/api/dashboard/search?q={q}"),
            fetch("mail", f"http://localhost:45004/api/v1/search?q={q}"),
            fetch("connect", f"http://localhost:5000/api/search?q={q}"),
            fetch("planet", f"http://localhost:46000/api/planet/search?q={q}"),
            fetch("turbotick", f"http://localhost:6100/api/search?q={q}"),
        ]
        
        results = await asyncio.gather(*tasks)
        for r in results:
            collected.extend(r)

        ranked = sorted(collected, key=lambda item: item.score, reverse=True)[:limit]
        took_ms = int((perf_counter() - started) * 1000)

        # Force dict return matching response model
        return {
            "query": q,
            "org_id": resolved_org_id,
            "workspace_id": resolved_workspace_id,
            "total": len(ranked),
            "took_ms": took_ms,
            "sources": ["writer", "learn", "atlas", "mail", "connect", "planet", "turbotick"],
            "results": [r.dict() for r in ranked],
        }

    return app


app = build_app()
