"""System 4: Execution & Outcome Tracking endpoints."""
from __future__ import annotations

from uuid import UUID
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
from AgentTheater.api.integration.execution_emitters import ExecutionEmitters
from AgentTheater.api.integration.request_hooks import transactional_event_scope
from AgentTheater.schemas import (
    ExecutionCreateRequest,
    ExecutionResponse,
    ExecutionArtifactRequest,
    ExecutionArtifactResponse,
    ExecutionAssignRequest,
    ExecutionStateTransitionRequest,
    OutcomeRecordRequest,
    OutcomeRecordResponse,
    ExecutionReadModelResponse,
)
from AgentTheater.events import EventStore
from AgentTheater.events.db_models import (
    Decision,
    Execution,
    ExecutionArtifact,
    ExecutionStateHistory,
    OutcomeRecord,
    ExecutionReadModel,
)
from AgentTheater.api.services.execution_state_machine import ExecutionStateMachine
from AgentTheater.api.services.event_driven_projections import ExecutionProjector

router = APIRouter(prefix="/executions", tags=["execution"])


def get_db():
    """Dependency for database session."""
    raise RuntimeError("get_db not initialized")


def get_event_store():
    """Dependency for event store."""
    raise RuntimeError("get_event_store not initialized")


@router.post("", response_model=ExecutionResponse)
async def create_execution(
    request: Request,
    response: Response,
    req: ExecutionCreateRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> ExecutionResponse:
    """Create execution for a decision."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    async with transactional_event_scope(db, event_store) as (session, store):
        # Verify decision exists
        result = await session.execute(select(Decision).where(Decision.id == req.decision_id))
        decision = result.scalar_one_or_none()

        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")

        if decision.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        # Create execution
        execution = Execution(
            decision_id=req.decision_id,
            state="approved",
            predicted_outcome=req.predicted_outcome,
            tenant_id=security_context.tenant_id,
            created_by=security_context.user_id,
        )
        session.add(execution)
        await session.flush()

        # Create read model
        read_model = ExecutionReadModel(
            execution_id=execution.id,
            decision_id=req.decision_id,
            decision_question=decision.question,
            state="approved",
            predicted_outcome=req.predicted_outcome,
            tenant_id=security_context.tenant_id,
        )
        session.add(read_model)

        # Emit event
        emitters = ExecutionEmitters(store)
        await emitters.emit_execution_created(
            execution_id=execution.id,
            decision_id=req.decision_id,
            security_context=security_context,
            correlation_id=correlation_id,
            predicted_outcome=req.predicted_outcome,
        )

        await session.flush()

    # Add headers
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    return ExecutionResponse(
        id=execution.id,
        decision_id=execution.decision_id,
        state=execution.state,
        assigned_to=execution.assigned_to,
        predicted_outcome=execution.predicted_outcome,
        actual_outcome=execution.actual_outcome,
        created_at=execution.created_at,
    )


@router.post("/{execution_id}/artifact", response_model=ExecutionArtifactResponse)
async def link_artifact(
    execution_id: UUID,
    request: Request,
    response: Response,
    req: ExecutionArtifactRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> ExecutionArtifactResponse:
    """Link artifact (GitHub issue, PR, task, etc.) to execution."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    async with transactional_event_scope(db, event_store) as (session, store):
        # Verify execution exists
        result = await session.execute(select(Execution).where(Execution.id == execution_id))
        execution = result.scalar_one_or_none()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        if execution.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        # Create artifact link
        artifact = ExecutionArtifact(
            execution_id=execution_id,
            artifact_type=req.artifact_type,
            artifact_id=req.artifact_id,
            artifact_url=req.artifact_url,
            artifact_title=req.artifact_title,
            tenant_id=security_context.tenant_id,
            created_by=security_context.user_id,
        )
        session.add(artifact)

        # Update artifact count in read model
        rm = await session.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )
        if rm:
            if req.artifact_type == "github_issue":
                rm.github_issues_count += 1
            elif req.artifact_type == "github_pr":
                rm.github_prs_count += 1
            elif req.artifact_type == "task":
                rm.tasks_count += 1
            elif req.artifact_type == "doc":
                rm.docs_count += 1
            elif req.artifact_type == "deployment":
                rm.deployments_count += 1

        # Emit event
        emitters = ExecutionEmitters(store)
        await emitters.emit_artifact_linked(
            execution_id=execution_id,
            artifact_type=req.artifact_type,
            artifact_id=req.artifact_id,
            security_context=security_context,
            correlation_id=correlation_id,
            artifact_url=req.artifact_url,
        )

        await session.flush()

    # Add headers
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    return ExecutionArtifactResponse(
        id=artifact.id,
        execution_id=artifact.execution_id,
        artifact_type=artifact.artifact_type,
        artifact_id=artifact.artifact_id,
        artifact_url=artifact.artifact_url,
        artifact_title=artifact.artifact_title,
        created_at=artifact.created_at,
    )


@router.post("/{execution_id}/assign", response_model=ExecutionResponse)
async def assign_execution(
    execution_id: UUID,
    request: Request,
    response: Response,
    req: ExecutionAssignRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> ExecutionResponse:
    """Assign execution to team member."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    if_match = request.headers.get("If-Match")

    async with transactional_event_scope(db, event_store) as (session, store):
        # Verify execution exists
        result = await session.execute(select(Execution).where(Execution.id == execution_id))
        execution = result.scalar_one_or_none()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        if execution.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        if if_match is not None:
            expected = if_match.strip('"')
            if str(execution.version) != expected:
                raise HTTPException(
                    status_code=409,
                    detail=f"Conflict: current version is {execution.version}, If-Match was {expected}",
                )

        from_state = execution.state
        try:
            ExecutionStateMachine.validate_transition(from_state, "assigned")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        execution.assigned_to = req.assigned_to
        execution.state = "assigned"
        execution.assigned_at = datetime.now(timezone.utc)
        execution.version += 1

        # Record state history
        history = ExecutionStateHistory(
            execution_id=execution_id,
            from_state=from_state,
            to_state="assigned",
            reason="Assigned to team member",
            tenant_id=security_context.tenant_id,
            transitioned_by=security_context.user_id,
        )
        session.add(history)

        # Update read model
        rm = await session.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )
        if rm:
            rm.state = "assigned"
            rm.assigned_to = req.assigned_to
            rm.updated_at = datetime.now(timezone.utc)

        # Emit event
        emitters = ExecutionEmitters(store)
        await emitters.emit_execution_state_transition(
            execution_id=execution_id,
            from_state=from_state,
            to_state="assigned",
            security_context=security_context,
            correlation_id=correlation_id,
            reason="Assigned to team member",
        )

        await session.flush()

    # Add headers
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )
    response.headers["ETag"] = f'"{execution.version}"'

    return ExecutionResponse(
        id=execution.id,
        decision_id=execution.decision_id,
        state=execution.state,
        assigned_to=execution.assigned_to,
        predicted_outcome=execution.predicted_outcome,
        actual_outcome=execution.actual_outcome,
        created_at=execution.created_at,
    )


@router.post("/{execution_id}/start", response_model=ExecutionResponse)
async def start_execution(
    execution_id: UUID,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> ExecutionResponse:
    """Start execution (transition to in_progress)."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    if_match = request.headers.get("If-Match")

    async with transactional_event_scope(db, event_store) as (session, store):
        result = await session.execute(select(Execution).where(Execution.id == execution_id))
        execution = result.scalar_one_or_none()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        if execution.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        if if_match is not None:
            expected = if_match.strip('"')
            if str(execution.version) != expected:
                raise HTTPException(
                    status_code=409,
                    detail=f"Conflict: current version is {execution.version}, If-Match was {expected}",
                )

        # Validate state transition BEFORE making changes
        from_state = execution.state
        try:
            ExecutionStateMachine.validate_transition(from_state, "in_progress")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        execution.state = "in_progress"
        execution.started_at = datetime.now(timezone.utc)
        execution.version += 1

        # Record state history
        history = ExecutionStateHistory(
            execution_id=execution_id,
            from_state=from_state,
            to_state="in_progress",
            reason="Execution started",
            tenant_id=security_context.tenant_id,
            transitioned_by=security_context.user_id,
        )
        session.add(history)

        # Emit event (read model will be updated via event-driven projection)
        emitters = ExecutionEmitters(store)
        await emitters.emit_execution_state_transition(
            execution_id=execution_id,
            from_state=from_state,
            to_state="in_progress",
            security_context=security_context,
            correlation_id=correlation_id,
        )

        # Project state change to read model
        projector = ExecutionProjector(session)
        await projector.project_state_transitioned(
            execution_id=execution_id,
            to_state="in_progress",
            started_at=execution.started_at,
        )

        await session.flush()

    propagate_context_to_response_headers(response, correlation_id=correlation_id, api_version="v1")
    response.headers["ETag"] = f'"{execution.version}"'

    return ExecutionResponse(
        id=execution.id,
        decision_id=execution.decision_id,
        state=execution.state,
        assigned_to=execution.assigned_to,
        predicted_outcome=execution.predicted_outcome,
        actual_outcome=execution.actual_outcome,
        created_at=execution.created_at,
    )


@router.post("/{execution_id}/block", response_model=ExecutionResponse)
async def block_execution(
    execution_id: UUID,
    request: Request,
    response: Response,
    req: ExecutionStateTransitionRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> ExecutionResponse:
    """Block execution with reason."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    if_match = request.headers.get("If-Match")

    async with transactional_event_scope(db, event_store) as (session, store):
        result = await session.execute(select(Execution).where(Execution.id == execution_id))
        execution = result.scalar_one_or_none()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        if execution.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        if if_match is not None:
            expected = if_match.strip('"')
            if str(execution.version) != expected:
                raise HTTPException(
                    status_code=409,
                    detail=f"Conflict: current version is {execution.version}, If-Match was {expected}",
                )

        from_state = execution.state
        try:
            ExecutionStateMachine.validate_transition(from_state, "blocked")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        execution.state = "blocked"
        execution.blocked_at = datetime.now(timezone.utc)
        execution.blocked_reason = req.blocked_reason
        execution.version += 1

        # Record state history
        history = ExecutionStateHistory(
            execution_id=execution_id,
            from_state=from_state,
            to_state="blocked",
            blocked_reason=req.blocked_reason,
            tenant_id=security_context.tenant_id,
            transitioned_by=security_context.user_id,
        )
        session.add(history)

        # Update read model
        rm = await session.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )
        if rm:
            rm.state = "blocked"
            rm.updated_at = datetime.now(timezone.utc)

        # Emit event
        emitters = ExecutionEmitters(store)
        await emitters.emit_execution_state_transition(
            execution_id=execution_id,
            from_state=from_state,
            to_state="blocked",
            security_context=security_context,
            correlation_id=correlation_id,
            blocked_reason=req.blocked_reason,
        )

        await session.flush()

    propagate_context_to_response_headers(response, correlation_id=correlation_id, api_version="v1")
    response.headers["ETag"] = f'"{execution.version}"'

    return ExecutionResponse(
        id=execution.id,
        decision_id=execution.decision_id,
        state=execution.state,
        assigned_to=execution.assigned_to,
        predicted_outcome=execution.predicted_outcome,
        actual_outcome=execution.actual_outcome,
        created_at=execution.created_at,
    )


@router.post("/{execution_id}/complete", response_model=ExecutionResponse)
async def complete_execution(
    execution_id: UUID,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> ExecutionResponse:
    """Mark execution as completed."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    if_match = request.headers.get("If-Match")

    async with transactional_event_scope(db, event_store) as (session, store):
        result = await session.execute(select(Execution).where(Execution.id == execution_id))
        execution = result.scalar_one_or_none()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        if execution.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        if if_match is not None:
            expected = if_match.strip('"')
            if str(execution.version) != expected:
                raise HTTPException(
                    status_code=409,
                    detail=f"Conflict: current version is {execution.version}, If-Match was {expected}",
                )

        from_state = execution.state
        try:
            ExecutionStateMachine.validate_transition(from_state, "completed")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        execution.state = "completed"
        execution.completed_at = datetime.now(timezone.utc)
        execution.version += 1

        # Record state history
        history = ExecutionStateHistory(
            execution_id=execution_id,
            from_state=from_state,
            to_state="completed",
            tenant_id=security_context.tenant_id,
            transitioned_by=security_context.user_id,
        )
        session.add(history)

        # Update read model
        rm = await session.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )
        if rm:
            rm.state = "completed"
            rm.completed_at = execution.completed_at
            rm.updated_at = datetime.now(timezone.utc)

        # Emit event
        emitters = ExecutionEmitters(store)
        await emitters.emit_execution_state_transition(
            execution_id=execution_id,
            from_state=from_state,
            to_state="completed",
            security_context=security_context,
            correlation_id=correlation_id,
        )

        await session.flush()

    propagate_context_to_response_headers(response, correlation_id=correlation_id, api_version="v1")
    response.headers["ETag"] = f'"{execution.version}"'

    return ExecutionResponse(
        id=execution.id,
        decision_id=execution.decision_id,
        state=execution.state,
        assigned_to=execution.assigned_to,
        predicted_outcome=execution.predicted_outcome,
        actual_outcome=execution.actual_outcome,
        created_at=execution.created_at,
    )


@router.post("/{execution_id}/outcome", response_model=OutcomeRecordResponse)
async def record_outcome(
    execution_id: UUID,
    request: Request,
    response: Response,
    req: OutcomeRecordRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> OutcomeRecordResponse:
    """Record actual outcome for execution."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    async with transactional_event_scope(db, event_store) as (session, store):
        result = await session.execute(select(Execution).where(Execution.id == execution_id))
        execution = result.scalar_one_or_none()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        if execution.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        # Create outcome record
        outcome = OutcomeRecord(
            execution_id=execution_id,
            predicted_outcome=execution.predicted_outcome or "unknown",
            predicted_confidence=None,
            predicted_at=execution.created_at,
            actual_outcome=req.actual_outcome,
            actual_at=datetime.now(timezone.utc),
            success_metrics=req.success_metrics,
            failure_reason=req.failure_reason,
            lessons_learned=req.lessons_learned,
            tenant_id=security_context.tenant_id,
            recorded_by=security_context.user_id,
        )
        session.add(outcome)

        # Update execution
        execution.actual_outcome = req.actual_outcome

        # Update read model
        rm = await session.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )
        if rm:
            rm.actual_outcome = req.actual_outcome
            rm.updated_at = datetime.now(timezone.utc)

        # Emit event
        emitters = ExecutionEmitters(store)
        await emitters.emit_outcome_recorded(
            execution_id=execution_id,
            actual_outcome=req.actual_outcome,
            security_context=security_context,
            correlation_id=correlation_id,
            success_metrics=req.success_metrics,
            failure_reason=req.failure_reason,
            lessons_learned=req.lessons_learned,
        )

        await session.flush()

    propagate_context_to_response_headers(response, correlation_id=correlation_id, api_version="v1")

    return OutcomeRecordResponse(
        id=outcome.id,
        execution_id=outcome.execution_id,
        predicted_outcome=outcome.predicted_outcome,
        actual_outcome=outcome.actual_outcome,
        validated=outcome.validated,
        created_at=outcome.created_at,
    )


@router.post("/{execution_id}/validate-outcome", response_model=OutcomeRecordResponse)
async def validate_outcome(
    execution_id: UUID,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> OutcomeRecordResponse:
    """Validate recorded outcome (decision verdict)."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    async with transactional_event_scope(db, event_store) as (session, store):
        # Get outcome record
        result = await session.execute(
            select(OutcomeRecord).where(OutcomeRecord.execution_id == execution_id)
        )
        outcome = result.scalar_one_or_none()

        if not outcome:
            raise HTTPException(status_code=404, detail="Outcome not found")

        if outcome.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        # Mark validated
        outcome.validated = True
        outcome.validated_at = datetime.now(timezone.utc)
        outcome.validated_by = security_context.user_id

        # Update read model
        rm = await session.scalar(
            select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
        )
        if rm:
            rm.outcome_validated = True
            rm.updated_at = datetime.now(timezone.utc)

        # Emit event
        emitters = ExecutionEmitters(store)
        await emitters.emit_outcome_validated(
            execution_id=execution_id,
            security_context=security_context,
            correlation_id=correlation_id,
        )

        await session.flush()

    propagate_context_to_response_headers(response, correlation_id=correlation_id, api_version="v1")

    return OutcomeRecordResponse(
        id=outcome.id,
        execution_id=outcome.execution_id,
        predicted_outcome=outcome.predicted_outcome,
        actual_outcome=outcome.actual_outcome,
        validated=outcome.validated,
        created_at=outcome.created_at,
    )


@router.get("/{execution_id}/dashboard", response_model=ExecutionReadModelResponse)
async def get_execution_dashboard(
    execution_id: UUID,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> ExecutionReadModelResponse:
    """Get execution dashboard read model."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    # Get read model
    read_model = await db.scalar(
        select(ExecutionReadModel).where(ExecutionReadModel.execution_id == execution_id)
    )

    if not read_model:
        raise HTTPException(status_code=404, detail="Execution read model not found")

    if read_model.tenant_id != security_context.tenant_id:
        raise HTTPException(status_code=403, detail="Tenant mismatch")

    propagate_context_to_response_headers(response, correlation_id=correlation_id, api_version="v1")

    return ExecutionReadModelResponse(
        id=read_model.id,
        execution_id=read_model.execution_id,
        decision_id=read_model.decision_id,
        decision_question=read_model.decision_question,
        state=read_model.state,
        assigned_to=read_model.assigned_to,
        started_at=read_model.started_at,
        completed_at=read_model.completed_at,
        age_days=read_model.age_days,
        github_issues_count=read_model.github_issues_count,
        github_prs_count=read_model.github_prs_count,
        tasks_count=read_model.tasks_count,
        docs_count=read_model.docs_count,
        deployments_count=read_model.deployments_count,
        predicted_outcome=read_model.predicted_outcome,
        actual_outcome=read_model.actual_outcome,
        outcome_validated=read_model.outcome_validated,
        created_at=read_model.created_at,
    )
