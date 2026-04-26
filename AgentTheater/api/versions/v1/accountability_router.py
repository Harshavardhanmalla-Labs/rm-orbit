"""System 3: Decision Accountability endpoints with versioning, rationale, scoring."""
from __future__ import annotations

from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.api.integration.context_flow import (
    extract_security_context,
    extract_correlation_id,
    propagate_context_to_response_headers,
)
from AgentTheater.api.integration.accountability_emitters import DecisionAccountabilityEmitters
from AgentTheater.api.integration.request_hooks import transactional_event_scope
from typing import Optional
from sqlalchemy import select
from AgentTheater.schemas import (
    DecisionRationaleRequest,
    DecisionRationaleResponse,
    DecisionConfidenceRequest,
    DecisionConfidenceResponse,
    RiskAssessmentRequest,
    RiskAssessmentResponse,
    DecisionStateTransitionRequest,
    DecisionReadModelResponse,
)
from AgentTheater.events import EventStore
from AgentTheater.events.db_models import (
    Decision,
    DecisionVersion,
    DecisionRationale,
    DecisionConfidence,
    RiskAssessment,
    DecisionStateHistory,
    DecisionReadModel,
)
from AgentTheater.api.services.guardrail_enforcement_engine import GuardrailEnforcementEngine
from AgentTheater.api.services.event_driven_projections import DecisionReadModelProjector
from AgentTheater.observability.metrics import get_metrics

router = APIRouter(prefix="/decisions", tags=["accountability"])


def get_db():
    """Dependency for database session."""
    raise RuntimeError("get_db not initialized")


def get_event_store():
    """Dependency for event store."""
    raise RuntimeError("get_event_store not initialized")


@router.post("/{id}/rationale", response_model=DecisionRationaleResponse)
async def add_rationale(
    id: UUID,
    request: Request,
    response: Response,
    req: DecisionRationaleRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> DecisionRationaleResponse:
    """Add role-level rationale to decision."""

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

        # Create rationale record
        rationale = DecisionRationale(
            decision_id=id,
            role=req.role,
            reasoning=req.reasoning,
            tenant_id=security_context.tenant_id,
            provided_by=security_context.user_id,
        )
        session.add(rationale)

        # Emit event
        emitters = DecisionAccountabilityEmitters(store)
        await emitters.emit_rationale_added(
            decision_id=id,
            role=req.role,
            reasoning=req.reasoning,
            security_context=security_context,
            correlation_id=correlation_id,
        )

        # Project to read model
        projector = DecisionReadModelProjector(session)
        await projector.project_rationale_added(
            decision_id=id, actor_id=security_context.user_id
        )

        await session.flush()

    # Add headers
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    return DecisionRationaleResponse(
        id=rationale.id,
        decision_id=rationale.decision_id,
        role=rationale.role,
        reasoning=rationale.reasoning,
        created_at=rationale.created_at,
    )


@router.post("/{id}/confidence", response_model=DecisionConfidenceResponse)
async def score_confidence(
    id: UUID,
    request: Request,
    response: Response,
    req: DecisionConfidenceRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> DecisionConfidenceResponse:
    """Score decision confidence."""

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

        # Calculate overall confidence
        overall = (
            req.technical_confidence + req.market_confidence + req.team_confidence
        ) / 3.0

        # Create confidence record
        confidence = DecisionConfidence(
            decision_id=id,
            technical_confidence=req.technical_confidence,
            market_confidence=req.market_confidence,
            team_confidence=req.team_confidence,
            overall_confidence=overall,
            reasoning=req.reasoning,
            tenant_id=security_context.tenant_id,
            scored_by=security_context.user_id,
        )
        session.add(confidence)

        # Enforce guardrails — blocks commit if confidence is below threshold
        guardrails = GuardrailEnforcementEngine(session)
        await guardrails.setup_default_guardrails(security_context.tenant_id)
        influence = await guardrails.check_guardrails(
            tenant_id=security_context.tenant_id,
            decision_id=id,
            predicted_confidence=overall / 100.0,  # Convert 0-100 → 0-1
            risk_level="unknown",
            role_id=security_context.user_id,
        )
        if influence.is_blocked:
            get_metrics().guardrail_blocks_total.labels(
                tenant_id=str(security_context.tenant_id),
                guardrail_name="confidence_guardrail",
            ).inc()
            raise HTTPException(
                status_code=422,
                detail=f"Decision blocked by guardrail: {influence.block_reason}",
            )

        # Emit event
        emitters = DecisionAccountabilityEmitters(store)
        await emitters.emit_confidence_scored(
            decision_id=id,
            technical=req.technical_confidence,
            market=req.market_confidence,
            team=req.team_confidence,
            overall=overall,
            security_context=security_context,
            correlation_id=correlation_id,
        )

        # Project to read model
        projector = DecisionReadModelProjector(session)
        await projector.project_confidence_scored(
            decision_id=id,
            overall_confidence=overall,
            actor_id=security_context.user_id,
        )

        await session.flush()

    # Add headers
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    return DecisionConfidenceResponse(
        id=confidence.id,
        decision_id=confidence.decision_id,
        technical_confidence=confidence.technical_confidence,
        market_confidence=confidence.market_confidence,
        team_confidence=confidence.team_confidence,
        overall_confidence=confidence.overall_confidence,
        created_at=confidence.created_at,
    )


@router.post("/{id}/risk", response_model=RiskAssessmentResponse)
async def assess_risk(
    id: UUID,
    request: Request,
    response: Response,
    req: RiskAssessmentRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> RiskAssessmentResponse:
    """Assess decision risk."""

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

        # Calculate overall risk
        overall = (
            req.technical_risk + req.market_risk + req.financial_risk + req.team_risk
        ) / 4.0

        # Create risk assessment
        assessment = RiskAssessment(
            decision_id=id,
            technical_risk=req.technical_risk,
            market_risk=req.market_risk,
            financial_risk=req.financial_risk,
            team_risk=req.team_risk,
            overall_risk=overall,
            contingency=req.contingency,
            tenant_id=security_context.tenant_id,
            assessed_by=security_context.user_id,
        )
        session.add(assessment)

        # Derive risk level from overall risk score (0-10 scale)
        risk_level = (
            "critical" if overall >= 7.5 else
            "high" if overall >= 5.0 else
            "medium" if overall >= 2.5 else "low"
        )

        # Enforce guardrails — blocks commit on critical/high risk violations
        guardrails = GuardrailEnforcementEngine(session)
        await guardrails.setup_default_guardrails(security_context.tenant_id)
        influence = await guardrails.check_guardrails(
            tenant_id=security_context.tenant_id,
            decision_id=id,
            predicted_confidence=1.0,  # Risk-only check; confidence checked separately
            risk_level=risk_level,
            role_id=security_context.user_id,
        )
        if influence.is_blocked:
            get_metrics().guardrail_blocks_total.labels(
                tenant_id=str(security_context.tenant_id),
                guardrail_name="risk_guardrail",
            ).inc()
            raise HTTPException(
                status_code=422,
                detail=f"Decision blocked by guardrail: {influence.block_reason}",
            )

        # Emit event
        emitters = DecisionAccountabilityEmitters(store)
        await emitters.emit_risk_assessed(
            decision_id=id,
            technical_risk=req.technical_risk,
            market_risk=req.market_risk,
            financial_risk=req.financial_risk,
            team_risk=req.team_risk,
            overall_risk=overall,
            security_context=security_context,
            correlation_id=correlation_id,
        )

        # Project to read model
        projector = DecisionReadModelProjector(session)
        await projector.project_risk_assessed(
            decision_id=id,
            overall_risk=overall,
            actor_id=security_context.user_id,
        )

        await session.flush()

    # Add headers
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    return RiskAssessmentResponse(
        id=assessment.id,
        decision_id=assessment.decision_id,
        technical_risk=assessment.technical_risk,
        market_risk=assessment.market_risk,
        financial_risk=assessment.financial_risk,
        team_risk=assessment.team_risk,
        overall_risk=assessment.overall_risk,
        contingency=assessment.contingency,
        created_at=assessment.created_at,
    )


@router.post("/{id}/state", status_code=200)
async def transition_state(
    id: UUID,
    request: Request,
    response: Response,
    req: DecisionStateTransitionRequest,
    db: AsyncSession = Depends(get_db),
    event_store: EventStore = Depends(get_event_store),
) -> dict:
    """Transition decision state."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    async with transactional_event_scope(db, event_store) as (session, store):
        # Get current decision
        result = await session.execute(select(Decision).where(Decision.id == id))
        decision = result.scalar_one_or_none()

        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")

        if decision.tenant_id != security_context.tenant_id:
            raise HTTPException(status_code=403, detail="Tenant mismatch")

        from_state = decision.outcome or "ideation"

        # Create state history
        history = DecisionStateHistory(
            decision_id=id,
            from_state=from_state,
            to_state=req.to_state,
            reason=req.reason,
            tenant_id=security_context.tenant_id,
            transitioned_by=security_context.user_id,
        )
        session.add(history)

        # Emit event
        emitters = DecisionAccountabilityEmitters(store)
        await emitters.emit_state_transitioned(
            decision_id=id,
            from_state=from_state,
            to_state=req.to_state,
            reason=req.reason,
            security_context=security_context,
            correlation_id=correlation_id,
        )

        # Project to read model
        projector = DecisionReadModelProjector(session)
        await projector.project_state_transitioned(
            decision_id=id,
            to_state=req.to_state,
            actor_id=security_context.user_id,
        )

        await session.flush()

    # Add headers
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    return {"status": "transitioned", "from_state": from_state, "to_state": req.to_state}


@router.get("/{id}/read-model", response_model=DecisionReadModelResponse)
async def get_read_model(
    id: UUID,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> DecisionReadModelResponse:
    """Get optimized read model for UI."""

    try:
        security_context = extract_security_context(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    correlation_id = extract_correlation_id(request)

    # Get read model
    result = await db.execute(
        select(DecisionReadModel).where(DecisionReadModel.decision_id == id)
    )
    read_model = result.scalar_one_or_none()

    if not read_model:
        raise HTTPException(status_code=404, detail="Decision read model not found")

    if read_model.tenant_id != security_context.tenant_id:
        raise HTTPException(status_code=403, detail="Tenant mismatch")

    # Add headers
    propagate_context_to_response_headers(
        response,
        correlation_id=correlation_id,
        api_version="v1",
    )

    return DecisionReadModelResponse(
        id=read_model.id,
        decision_id=read_model.decision_id,
        question=read_model.question,
        current_state=read_model.current_state,
        current_version=read_model.current_version,
        overall_confidence=read_model.overall_confidence,
        overall_risk=read_model.overall_risk,
        rationale_count=read_model.rationale_count,
        confidence_count=read_model.confidence_count,
        risk_count=read_model.risk_count,
        last_activity_at=read_model.last_activity_at,
        created_at=read_model.created_at,
    )
