from __future__ import annotations

from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
from time import perf_counter
import sys
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.orbit_audit import build_audit_record, emit_audit, get_audit_logger

from .auth import (
    validate_org_header,
    validate_workspace_claim,
    verify_gate_token,
)
from .database import get_db, init_db, setup_database
from .eventbus import publish_writer_event
from . import models  # noqa: F401 (ensures model metadata registration)
from .models import Block, BlockRelation, BlockVersion, Document, FeedbackEntry
from .schemas import (
    BlockCreate,
    BlockOut,
    BlockRelationCreate,
    BlockRelationOut,
    BlockUpdate,
    BlockVersionOut,
    DocumentCreate,
    DocumentDetail,
    DocumentUpdate,
    DocumentGraph,
    DocumentSummary,
    FeedbackAck,
    FeedbackAreaSummary,
    FeedbackCreate,
    FeedbackRecentItem,
    FeedbackSummary,
    HealthResponse,
)


SUPPORTED_RENDER_MODES = {"document", "data", "slide", "notes"}
DATABASE_URL = ""
AUDIT_LOGGER = get_audit_logger("orbit.audit.writer")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def redact_database_url(raw_url: str) -> str:
    try:
        parsed = make_url(raw_url)
        if parsed.password:
            parsed = parsed.set(password="***")
        return str(parsed)
    except Exception:
        return raw_url


def block_to_schema(block: Block) -> BlockOut:
    return BlockOut(
        id=block.id,
        document_id=block.document_id,
        parent_block_id=block.parent_block_id,
        type=block.type,
        content=block.content or {},
        metadata=block.block_metadata or {},
        position_index=block.position_index,
        version=block.version,
        created_at=block.created_at,
        updated_at=block.updated_at,
    )


def relation_to_schema(relation: BlockRelation) -> BlockRelationOut:
    return BlockRelationOut(
        id=relation.id,
        document_id=relation.document_id,
        source_block_id=relation.source_block_id,
        target_block_id=relation.target_block_id,
        relation_type=relation.relation_type,
        created_at=relation.created_at,
    )


def get_workspace_id(
    request: Request,
    x_workspace_id: Annotated[str | None, Header(alias="X-Workspace-Id")] = None,
    x_org_id: Annotated[str | None, Header(alias="X-Org-Id")] = None,
    token_payload: dict | None = Depends(verify_gate_token),
) -> str:
    if not x_workspace_id:
        raise HTTPException(
            status_code=400,
            detail="Missing required header: X-Workspace-Id",
    )
    validate_org_header(token_payload, x_org_id)
    validate_workspace_claim(token_payload, x_workspace_id)
    token_org = (
        str(token_payload.get("org_id") or token_payload.get("orgId") or "").strip()
        if token_payload
        else ""
    )
    token_user = (
        str(token_payload.get("sub") or token_payload.get("id") or "").strip()
        if token_payload
        else ""
    )
    request.state.writer_org_id = (x_org_id or "").strip() or token_org or None
    request.state.writer_user_id = token_user or None
    return x_workspace_id


def get_request_actor(request: Request) -> tuple[str | None, str | None]:
    org_id = getattr(request.state, "writer_org_id", None)
    user_id = getattr(request.state, "writer_user_id", None)
    return org_id, user_id


def get_document_or_404(db: Session, document_id: str, workspace_id: str) -> Document:
    stmt = select(Document).where(
        Document.id == document_id,
        Document.workspace_id == workspace_id,
    )
    document = db.scalar(stmt)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


def get_block_or_404(db: Session, block_id: str, workspace_id: str) -> tuple[Block, Document]:
    stmt = (
        select(Block, Document)
        .join(Document, Document.id == Block.document_id)
        .where(Block.id == block_id, Document.workspace_id == workspace_id)
    )
    row = db.execute(stmt).first()
    if not row:
        raise HTTPException(status_code=404, detail="Block not found")
    return row[0], row[1]


def create_app(database_url: str | None = None) -> FastAPI:
    global DATABASE_URL
    DATABASE_URL = setup_database(database_url)
    init_db()

    app = FastAPI(
        title="RM Writer Backend",
        version="0.1.0",
        description="Structured block graph API for RM Writer MVP",
    )

    allowed_origins = os.getenv(
        "WRITER_CORS_ORIGINS",
        "http://localhost:45010,http://127.0.0.1:45010",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in allowed_origins.split(",") if origin.strip()],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def audit_requests(request: Request, call_next):
        started = perf_counter()
        request_id = request.headers.get("X-Request-Id") or str(uuid4())
        request.state.request_id = request_id
        response = None
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = int((perf_counter() - started) * 1000)
            org_id = getattr(request.state, "writer_org_id", None) or request.headers.get("X-Org-Id")
            workspace_id = request.headers.get("X-Workspace-Id")
            user_id = getattr(request.state, "writer_user_id", None)
            record = build_audit_record(
                service="writer-backend",
                event="http.request",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                duration_ms=duration_ms,
                org_id=org_id,
                workspace_id=workspace_id,
                user_id=user_id,
                extra={"query": request.url.query},
            )
            emit_audit(AUDIT_LOGGER, record)
            if response is not None:
                response.headers["X-Request-Id"] = request_id

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            status="ok",
            service="writer-backend",
            database_url=redact_database_url(DATABASE_URL),
        )

    # Writer frontend is in ../frontend/dist in Docker, or ../../frontend/dist in native
    dist_path = Path(__file__).resolve().parents[1] / "frontend" / "dist"
    if not dist_path.exists():
        dist_path = Path(__file__).resolve().parents[2] / "frontend" / "dist"

    @app.get("/api/render-modes")
    def render_modes(_token_payload: dict | None = Depends(verify_gate_token)) -> dict:
        return {
            "modes": sorted(SUPPORTED_RENDER_MODES),
            "note": "Mode switching is a rendering strategy on the same block tree.",
        }

    @app.post("/api/feedback", response_model=FeedbackAck, status_code=202)
    def submit_feedback(
        request: Request,
        payload: FeedbackCreate,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> FeedbackAck:
        org_id, user_id = get_request_actor(request)
        request_id = getattr(request.state, "request_id", None)
        feedback = FeedbackEntry(
            workspace_id=workspace_id,
            org_id=org_id,
            user_id=user_id,
            rating=payload.rating,
            area=payload.area.strip(),
            page=(payload.page or "").strip() or None,
            message=(payload.message or "").strip() or None,
        )
        db.add(feedback)
        db.commit()

        feedback_record = build_audit_record(
            service="writer-backend",
            event="writer.feedback.submitted",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=202,
            duration_ms=0,
            org_id=org_id,
            workspace_id=workspace_id,
            user_id=user_id,
            extra={
                "rating": payload.rating,
                "area": payload.area,
                "page": payload.page,
                "message_length": len(payload.message or ""),
            },
        )
        emit_audit(AUDIT_LOGGER, feedback_record)

        publish_writer_event(
            "writer.feedback.submitted",
            {
                "org_id": org_id,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "data": {
                    "rating": payload.rating,
                    "area": payload.area,
                    "page": payload.page,
                },
            },
        )

        return FeedbackAck(status="accepted", received_at=now_utc())

    @app.get("/api/feedback/summary", response_model=FeedbackSummary)
    def feedback_summary(
        workspace_id: str = Depends(get_workspace_id),
        days: int = Query(default=14, ge=1, le=90),
        recent_limit: int = Query(default=10, ge=1, le=50),
        db: Session = Depends(get_db),
    ) -> FeedbackSummary:
        since = now_utc() - timedelta(days=days)

        filters = (
            FeedbackEntry.workspace_id == workspace_id,
            FeedbackEntry.created_at >= since,
        )

        totals_stmt = select(func.count(FeedbackEntry.id), func.avg(FeedbackEntry.rating)).where(*filters)
        total_count, avg_rating = db.execute(totals_stmt).one()

        areas_stmt = (
            select(
                FeedbackEntry.area,
                func.count(FeedbackEntry.id),
                func.avg(FeedbackEntry.rating),
            )
            .where(*filters)
            .group_by(FeedbackEntry.area)
            .order_by(func.count(FeedbackEntry.id).desc(), FeedbackEntry.area.asc())
        )
        area_rows = db.execute(areas_stmt).all()

        recent_stmt = (
            select(FeedbackEntry)
            .where(*filters)
            .order_by(FeedbackEntry.created_at.desc(), FeedbackEntry.id.desc())
            .limit(recent_limit)
        )
        recent_rows = list(db.scalars(recent_stmt))

        return FeedbackSummary(
            days=days,
            total=int(total_count or 0),
            average_rating=float(avg_rating or 0.0),
            areas=[
                FeedbackAreaSummary(
                    area=str(area),
                    count=int(count or 0),
                    average_rating=float(area_avg or 0.0),
                )
                for area, count, area_avg in area_rows
            ],
            recent=[
                FeedbackRecentItem(
                    id=entry.id,
                    rating=entry.rating,
                    area=entry.area,
                    page=entry.page,
                    message=entry.message,
                    created_at=entry.created_at,
                )
                for entry in recent_rows
            ],
        )

    @app.post("/api/documents", response_model=DocumentDetail, status_code=201)
    def create_document(
        request: Request,
        payload: DocumentCreate,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> DocumentDetail:
        document = Document(
            workspace_id=workspace_id,
            title=payload.title.strip(),
            root_block_id=None,
        )
        db.add(document)
        db.flush()

        root_block = Block(
            document_id=document.id,
            parent_block_id=None,
            type=payload.initial_block_type,
            content=payload.initial_content,
            block_metadata=payload.initial_metadata,
            position_index=0,
            version=1,
        )
        db.add(root_block)
        db.flush()

        document.root_block_id = root_block.id
        document.updated_at = now_utc()
        db.commit()
        db.refresh(document)

        org_id, user_id = get_request_actor(request)
        publish_writer_event(
            "writer.document.created",
            {
                "org_id": org_id,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "data": {
                    "document_id": document.id,
                    "title": document.title,
                    "root_block_id": document.root_block_id,
                },
            },
        )

        return DocumentDetail(
            id=document.id,
            workspace_id=document.workspace_id,
            title=document.title,
            root_block_id=document.root_block_id,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    @app.get("/api/documents", response_model=list[DocumentSummary])
    def list_documents(
        workspace_id: str = Depends(get_workspace_id),
        limit: int = Query(default=50, ge=1, le=200),
        offset: int = Query(default=0, ge=0),
        db: Session = Depends(get_db),
    ) -> list[DocumentSummary]:
        docs_stmt = (
            select(Document)
            .where(Document.workspace_id == workspace_id)
            .order_by(Document.updated_at.desc(), Document.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        documents = list(db.scalars(docs_stmt))
        if not documents:
            return []

        doc_ids = [doc.id for doc in documents]
        counts_stmt = (
            select(Block.document_id, func.count(Block.id))
            .where(Block.document_id.in_(doc_ids))
            .group_by(Block.document_id)
        )
        counts = {doc_id: count for doc_id, count in db.execute(counts_stmt)}

        return [
            DocumentSummary(
                id=doc.id,
                workspace_id=doc.workspace_id,
                title=doc.title,
                root_block_id=doc.root_block_id,
                block_count=int(counts.get(doc.id, 0)),
                created_at=doc.created_at,
                updated_at=doc.updated_at,
            )
            for doc in documents
        ]

    @app.get("/api/documents/{document_id}", response_model=DocumentDetail)
    def get_document(
        document_id: str,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> DocumentDetail:
        document = get_document_or_404(db, document_id, workspace_id)
        return DocumentDetail(
            id=document.id,
            workspace_id=document.workspace_id,
            title=document.title,
            root_block_id=document.root_block_id,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    @app.patch("/api/documents/{document_id}", response_model=DocumentDetail)
    def update_document(
        request: Request,
        document_id: str,
        payload: DocumentUpdate,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> DocumentDetail:
        document = get_document_or_404(db, document_id, workspace_id)
        document.title = payload.title.strip()
        document.updated_at = now_utc()
        db.commit()
        db.refresh(document)

        org_id, user_id = get_request_actor(request)
        publish_writer_event(
            "writer.document.updated",
            {
                "org_id": org_id,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "data": {
                    "document_id": document.id,
                    "title": document.title,
                },
            },
        )

        return DocumentDetail(
            id=document.id,
            workspace_id=document.workspace_id,
            title=document.title,
            root_block_id=document.root_block_id,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    @app.get("/api/documents/{document_id}/blocks", response_model=list[BlockOut])
    def list_document_blocks(
        document_id: str,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> list[BlockOut]:
        get_document_or_404(db, document_id, workspace_id)
        stmt = (
            select(Block)
            .where(Block.document_id == document_id)
            .order_by(Block.position_index.asc(), Block.created_at.asc())
        )
        blocks = list(db.scalars(stmt))
        return [block_to_schema(block) for block in blocks]

    @app.post("/api/documents/{document_id}/blocks", response_model=BlockOut, status_code=201)
    def create_block(
        request: Request,
        document_id: str,
        payload: BlockCreate,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> BlockOut:
        document = get_document_or_404(db, document_id, workspace_id)
        if payload.parent_block_id:
            parent_stmt = select(Block).where(
                Block.id == payload.parent_block_id,
                Block.document_id == document_id,
            )
            if not db.scalar(parent_stmt):
                raise HTTPException(status_code=404, detail="Parent block not found in document")

        block = Block(
            document_id=document_id,
            parent_block_id=payload.parent_block_id,
            type=payload.type,
            content=payload.content,
            block_metadata=payload.metadata,
            position_index=payload.position_index,
            version=1,
        )
        db.add(block)
        document.updated_at = now_utc()
        db.commit()
        db.refresh(block)

        org_id, user_id = get_request_actor(request)
        publish_writer_event(
            "writer.block.created",
            {
                "org_id": org_id,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "data": {
                    "document_id": document_id,
                    "block_id": block.id,
                    "parent_block_id": block.parent_block_id,
                    "type": block.type,
                    "version": block.version,
                },
            },
        )

        return block_to_schema(block)

    @app.patch("/api/blocks/{block_id}", response_model=BlockOut)
    def update_block(
        request: Request,
        block_id: str,
        payload: BlockUpdate,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> BlockOut:
        block, document = get_block_or_404(db, block_id, workspace_id)

        snapshot = {
            "version": block.version,
            "type": block.type,
            "content": block.content or {},
            "metadata": block.block_metadata or {},
            "position_index": block.position_index,
            "parent_block_id": block.parent_block_id,
            "captured_at": now_utc().isoformat(),
        }
        db.add(BlockVersion(block_id=block.id, snapshot=snapshot))

        if "parent_block_id" in payload.model_fields_set and payload.parent_block_id:
            parent_stmt = select(Block).where(
                Block.id == payload.parent_block_id,
                Block.document_id == block.document_id,
            )
            if not db.scalar(parent_stmt):
                raise HTTPException(status_code=404, detail="Parent block not found in document")

        field_map = {"metadata": "block_metadata"}
        for field in payload.model_fields_set:
            target_field = field_map.get(field, field)
            setattr(block, target_field, getattr(payload, field))

        block.version = block.version + 1
        block.updated_at = now_utc()
        document.updated_at = now_utc()

        db.commit()
        db.refresh(block)

        org_id, user_id = get_request_actor(request)
        publish_writer_event(
            "writer.block.updated",
            {
                "org_id": org_id,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "data": {
                    "document_id": block.document_id,
                    "block_id": block.id,
                    "type": block.type,
                    "version": block.version,
                },
            },
        )

        return block_to_schema(block)

    @app.delete("/api/blocks/{block_id}", status_code=204)
    def delete_block(
        request: Request,
        block_id: str,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> Response:
        block, document = get_block_or_404(db, block_id, workspace_id)
        if document.root_block_id == block.id:
            raise HTTPException(status_code=409, detail="Cannot delete root block")

        db.delete(block)
        document.updated_at = now_utc()
        db.commit()

        org_id, user_id = get_request_actor(request)
        publish_writer_event(
            "writer.block.deleted",
            {
                "org_id": org_id,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "data": {
                    "document_id": document.id,
                    "block_id": block.id,
                },
            },
        )

        return Response(status_code=204)

    @app.get("/api/blocks/{block_id}/versions", response_model=list[BlockVersionOut])
    def list_block_versions(
        block_id: str,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> list[BlockVersionOut]:
        block, _document = get_block_or_404(db, block_id, workspace_id)
        stmt = (
            select(BlockVersion)
            .where(BlockVersion.block_id == block.id)
            .order_by(BlockVersion.created_at.desc(), BlockVersion.id.desc())
        )
        versions = list(db.scalars(stmt))
        return [
            BlockVersionOut(
                id=version.id,
                block_id=version.block_id,
                snapshot=version.snapshot,
                created_at=version.created_at,
            )
            for version in versions
        ]

    @app.post("/api/blocks/{block_id}/relations", response_model=BlockRelationOut, status_code=201)
    def create_block_relation(
        request: Request,
        block_id: str,
        payload: BlockRelationCreate,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> BlockRelationOut:
        source_block, source_document = get_block_or_404(db, block_id, workspace_id)
        target_stmt = select(Block).where(
            Block.id == payload.target_block_id,
            Block.document_id == source_document.id,
        )
        target_block = db.scalar(target_stmt)
        if not target_block:
            raise HTTPException(status_code=404, detail="Target block not found in document")

        relation = BlockRelation(
            document_id=source_document.id,
            source_block_id=source_block.id,
            target_block_id=target_block.id,
            relation_type=payload.relation_type,
        )
        db.add(relation)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail="Relation already exists") from None
        db.refresh(relation)

        org_id, user_id = get_request_actor(request)
        publish_writer_event(
            "writer.relation.created",
            {
                "org_id": org_id,
                "user_id": user_id,
                "workspace_id": workspace_id,
                "data": {
                    "document_id": source_document.id,
                    "relation_id": relation.id,
                    "source_block_id": relation.source_block_id,
                    "target_block_id": relation.target_block_id,
                    "relation_type": relation.relation_type,
                },
            },
        )

        return relation_to_schema(relation)

    @app.get("/api/documents/{document_id}/graph", response_model=DocumentGraph)
    def get_document_graph(
        document_id: str,
        workspace_id: str = Depends(get_workspace_id),
        db: Session = Depends(get_db),
    ) -> DocumentGraph:
        get_document_or_404(db, document_id, workspace_id)

        blocks_stmt = select(Block).where(Block.document_id == document_id).order_by(
            Block.position_index.asc(), Block.created_at.asc()
        )
        edges_stmt = select(BlockRelation).where(BlockRelation.document_id == document_id).order_by(
            BlockRelation.created_at.asc(), BlockRelation.id.asc()
        )

        blocks = list(db.scalars(blocks_stmt))
        relations = list(db.scalars(edges_stmt))

        return DocumentGraph(
            document_id=document_id,
            nodes=[block_to_schema(block) for block in blocks],
            edges=[relation_to_schema(edge) for edge in relations],
        )

    if dist_path.exists():
        from fastapi.responses import FileResponse
        from fastapi.staticfiles import StaticFiles

        app.mount("/assets", StaticFiles(directory=dist_path / "assets"), name="assets")

        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            if full_path.startswith("api/") or full_path in {"api", "openapi.json", "docs", "redoc", "health"}:
                raise HTTPException(status_code=404, detail="Not found")

            target = dist_path / full_path
            if full_path and target.is_file():
                return FileResponse(target)

            return FileResponse(dist_path / "index.html")

    return app


app = create_app()
