"""Decision endpoints with System 2 event emission."""
from __future__ import annotations

from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.api.integration.context_flow import (
    extract_security_context,
    extract_correlation_id,
    propagate_context_to_response_headers,
)
from AgentTheater.api.integration.event_emitters import DecisionEventEmitters
from AgentTheater.api.integration.request_hooks import transactional_event_scope
from AgentTheater.schemas import (
    DecisionCreateRequest,
    DecisionCreateResponse,
    OutcomeRequest,
    DecisionRecordResponse,
    ListDecisionsResponse,
    GithubIssueRequest,
    GithubIssuesRequest,
)
from AgentTheater.events import EventStore
from AgentTheater.events.db_models import Decision, GithubIssue, DecisionReadModel
from AgentTheater.api.services.event_driven_projections import DecisionReadModelProjector
from AgentTheater.schemas import DecisionReadModelResponse, DecisionReadModelListResponse

router = APIRouter(prefix="/decisions", tags=["decisions"])


def get_db():
    """Stub for dependency injection."""
    raise NotImplementedError("Override in main.py")


def get_event_store():
    """Stub for dependency injection."""
    raise NotImplementedError("Override in main.py")


@router.post("", status_code=201, response_model=DecisionCreateResponse)
async def create_decision(
    request: Request,
    response: Response,
    req: DecisionCreateRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> DecisionCreateResponse:
    """Create decision and emit event.

    Atomically:
      1. Write decision to DB
      2. Emit decision.created event to outbox
      3. If either fails, both rollback
      4. Return response

    Event emission is background (via OutboxPublisher).
    """

    # Extract context
    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    # Verify tenant isolation
    if req.tenant_id != security_context.tenant_id:
        raise HTTPException(status_code=403, detail="Tenant mismatch")

    # Generate decision ID
    decision_id = uuid4()

    # Atomic transaction: write domain + event
    async with transactional_event_scope(db, event_store) as (session, store):
        # 1. Create decision record
        decision = Decision(
            id=decision_id,
            project_id=req.project_id,
            question=req.question,
            roles=req.roles,
            tenant_id=security_context.tenant_id,
            created_by=security_context.user_id,
            created_at=datetime.now(timezone.utc),
        )
        session.add(decision)

        # 2. Emit event (same transaction)
        emitters = DecisionEventEmitters(store)
        await emitters.emit_decision_created(
            decision_id=decision_id,
            security_context=security_context,
            project_id=req.project_id,
            question=req.question,
            roles=req.roles,
            correlation_id=correlation_id,
        )

        # 3. Project to read model (same transaction)
        projector = DecisionReadModelProjector(session)
        await projector.project_decision_created(
            decision_id=decision_id,
            question=req.question,
            project_id=req.project_id,
            owner_id=security_context.user_id,
            tenant_id=security_context.tenant_id,
        )

        # Flush to validate constraints
        await session.flush()

    # After context: both committed, events in outbox

    # Add context headers to response
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    # Build response body
    return DecisionCreateResponse(
        id=decision_id,
        question=req.question,
        roles=req.roles,
        created_at=decision.created_at,
    )


@router.get("/read-models", response_model=DecisionReadModelListResponse)
async def list_decision_read_models(
    request: Request,
    response: Response,
    limit: int = 50,
    offset: int = 0,
    state: Optional[str] = None,
    project_id: Optional[UUID] = None,
    min_confidence: Optional[float] = None,
    max_risk: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
) -> DecisionReadModelListResponse:
    """List decision read models with optional filters (paginated, tenant-scoped)."""

    if limit > 200:
        raise HTTPException(status_code=400, detail="limit cannot exceed 200")

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    base_filter = [DecisionReadModel.tenant_id == security_context.tenant_id]
    if state:
        base_filter.append(DecisionReadModel.current_state == state)
    if project_id:
        base_filter.append(DecisionReadModel.project_id == project_id)
    if min_confidence is not None:
        base_filter.append(DecisionReadModel.overall_confidence >= min_confidence)
    if max_risk is not None:
        base_filter.append(DecisionReadModel.overall_risk <= max_risk)

    count_result = await db.execute(
        select(func.count(DecisionReadModel.id)).where(*base_filter)
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(DecisionReadModel)
        .where(*base_filter)
        .order_by(DecisionReadModel.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    items = result.scalars().all()

    propagate_context_to_response_headers(response, correlation_id=correlation_id, api_version="v1")

    return DecisionReadModelListResponse(
        items=[DecisionReadModelResponse.model_validate(rm) for rm in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{id}", response_model=DecisionRecordResponse)
async def get_decision(
    id: UUID,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> DecisionRecordResponse:
    """Get decision (read-only, no event)."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    # Get decision
    result = await db.execute(select(Decision).where(Decision.id == id))
    decision = result.scalar_one_or_none()

    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")

    # Verify tenant isolation
    if decision.tenant_id != security_context.tenant_id:
        raise HTTPException(status_code=403, detail="Tenant mismatch")

    # Add headers to response
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    # Build response body
    return DecisionRecordResponse(
        id=decision.id,
        question=decision.question,
        roles=decision.roles,
        created_at=decision.created_at,
        outcome=decision.outcome,
        note=decision.note,
        completed_at=decision.completed_at,
    )


@router.get("", response_model=ListDecisionsResponse)
async def list_decisions(
    request: Request,
    response: Response,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> ListDecisionsResponse:
    """List decisions for user's tenant (paginated)."""

    if limit > 200:
        raise HTTPException(status_code=400, detail="limit cannot exceed 200")

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    # Accurate total count (separate query, not len of current page)
    count_result = await db.execute(
        select(func.count(Decision.id)).where(Decision.tenant_id == security_context.tenant_id)
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(Decision)
        .where(Decision.tenant_id == security_context.tenant_id)
        .order_by(Decision.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    decisions = result.scalars().all()

    # Add headers to response
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    # Build response body
    return ListDecisionsResponse(
        items=[
            DecisionRecordResponse(
                id=d.id,
                question=d.question,
                roles=d.roles,
                created_at=d.created_at,
                outcome=d.outcome,
                note=d.note,
                completed_at=d.completed_at,
            )
            for d in decisions
        ],
        total=total,
    )


@router.post("/{id}/outcome", response_model=DecisionRecordResponse)
async def record_outcome(
    id: UUID,
    request: Request,
    response: Response,
    req: OutcomeRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> DecisionRecordResponse:
    """Record decision outcome and emit event.

    Atomically:
      1. Update decision.outcome
      2. Emit decision.outcome_recorded event
      3. If either fails, both rollback
    """

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    # Atomic transaction
    async with transactional_event_scope(db, event_store) as (session, store):
        # 1. Get and validate decision
        result = await session.execute(select(Decision).where(Decision.id == id))
        decision = result.scalar_one_or_none()

        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")

        # Verify tenant isolation
        if decision.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        # 2. Update decision
        decision.outcome = req.outcome
        decision.note = req.note
        decision.completed_at = datetime.now(timezone.utc)

        # 3. Emit event (same transaction)
        emitters = DecisionEventEmitters(store)
        await emitters.emit_decision_outcome_recorded(
            decision_id=decision.id,
            security_context=security_context,
            outcome=req.outcome,
            note=req.note,
            correlation_id=correlation_id,
        )

        await session.flush()

    # Add headers to response
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    # Build response body
    return DecisionRecordResponse(
        id=decision.id,
        question=decision.question,
        roles=decision.roles,
        outcome=decision.outcome,
        note=decision.note,
        created_at=decision.created_at,
        completed_at=decision.completed_at,
    )



@router.post("/{id}/github-issue")
async def add_github_issue(
    id: UUID,
    request: Request,
    req: GithubIssueRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
):
    """Add GitHub issue to decision and emit event."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    async with transactional_event_scope(db, event_store) as (session, store):
        # Verify decision exists
        result = await session.execute(select(Decision).where(Decision.id == id))
        decision = result.scalar_one_or_none()

        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")

        if decision.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        # Create GitHub issue record
        github_issue = GithubIssue(
            decision_id=decision.id,
            repo=req.repo,
            issue_id=str(req.issue_id),
            url=req.url,
            tenant_id=security_context.tenant_id,
        )
        session.add(github_issue)

        # Emit event
        emitters = DecisionEventEmitters(store)
        await emitters.emit_github_issue_added(
            decision_id=decision.id,
            security_context=security_context,
            repo=req.repo,
            issue_id=req.issue_id,
            url=req.url,
            correlation_id=correlation_id,
        )

        await session.flush()

    return {"message": "GitHub issue added", "correlation_id": correlation_id}


@router.post("/{id}/github-issues")
async def create_github_issues(
    id: UUID,
    request: Request,
    req: GithubIssuesRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
):
    """Create multiple GitHub issues and emit event."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    urls = req.urls

    async with transactional_event_scope(db, event_store) as (session, store):
        # Verify decision exists
        result = await session.execute(select(Decision).where(Decision.id == id))
        decision = result.scalar_one_or_none()

        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")

        if decision.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        # Emit event
        emitters = DecisionEventEmitters(store)
        await emitters.emit_github_issues_created(
            decision_id=decision.id,
            security_context=security_context,
            count=len(urls),
            urls=urls,
            correlation_id=correlation_id,
        )

        await session.flush()

    return {
        "message": "GitHub issues created",
        "count": len(urls),
        "correlation_id": correlation_id,
    }
