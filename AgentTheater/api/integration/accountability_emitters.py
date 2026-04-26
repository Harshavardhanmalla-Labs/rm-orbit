"""System 3: Decision Accountability Engine event emitters."""
from __future__ import annotations

from uuid import UUID
from typing import Optional, List
from AgentTheater.events.ledger import EventStore
from AgentTheater.events.security import EventSecurityContext


class DecisionAccountabilityEmitters:
    """Emit System 3 accountability events."""

    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    async def emit_version_created(
        self,
        decision_id: UUID,
        version: int,
        security_context: EventSecurityContext,
        question: str,
        state: str,
        correlation_id: str,
    ) -> None:
        """Emit decision version created event."""
        await self.event_store.record_decision_version_created(
            decision_id=decision_id,
            version=version,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            question=question,
            state=state,
            correlation_id=correlation_id,
        )

    async def emit_rationale_added(
        self,
        decision_id: UUID,
        role: str,
        reasoning: str,
        security_context: EventSecurityContext,
        correlation_id: str,
    ) -> None:
        """Emit decision rationale added event."""
        await self.event_store.record_decision_rationale_added(
            decision_id=decision_id,
            role=role,
            reasoning=reasoning,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            correlation_id=correlation_id,
        )

    async def emit_confidence_scored(
        self,
        decision_id: UUID,
        technical: float,
        market: float,
        team: float,
        overall: float,
        security_context: EventSecurityContext,
        correlation_id: str,
    ) -> None:
        """Emit decision confidence scored event."""
        await self.event_store.record_decision_confidence_scored(
            decision_id=decision_id,
            technical=technical,
            market=market,
            team=team,
            overall=overall,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            correlation_id=correlation_id,
        )

    async def emit_risk_assessed(
        self,
        decision_id: UUID,
        technical_risk: float,
        market_risk: float,
        financial_risk: float,
        team_risk: float,
        overall_risk: float,
        security_context: EventSecurityContext,
        correlation_id: str,
    ) -> None:
        """Emit decision risk assessed event."""
        await self.event_store.record_decision_risk_assessed(
            decision_id=decision_id,
            technical_risk=technical_risk,
            market_risk=market_risk,
            financial_risk=financial_risk,
            team_risk=team_risk,
            overall_risk=overall_risk,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            correlation_id=correlation_id,
        )

    async def emit_state_transitioned(
        self,
        decision_id: UUID,
        from_state: str,
        to_state: str,
        security_context: EventSecurityContext,
        reason: Optional[str],
        correlation_id: str,
    ) -> None:
        """Emit decision state transitioned event."""
        await self.event_store.record_decision_state_transitioned(
            decision_id=decision_id,
            from_state=from_state,
            to_state=to_state,
            reason=reason,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            correlation_id=correlation_id,
        )
