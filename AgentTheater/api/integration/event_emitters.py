"""Map API operations to System 2 events."""
from __future__ import annotations

from uuid import UUID
from typing import Optional
from AgentTheater.events.ledger import EventStore, DomainEvent, EventType
from AgentTheater.events.security import EventSecurityContext


class DecisionEventEmitters:
    """Emit events from decision API endpoints.

    All methods:
      - Must be called within transactional_event_scope
      - Event write happens in same DB transaction as domain change
      - If either fails, both rollback
    """

    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    async def emit_decision_created(
        self,
        decision_id: UUID,
        security_context: EventSecurityContext,
        project_id: UUID,
        question: str,
        roles: list[str],
        correlation_id: str,
    ) -> None:
        """Emit decision.created event."""
        await self.event_store.record_decision_created(
            decision_id=decision_id,
            project_id=project_id,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            question=question,
            roles=roles,
            correlation_id=correlation_id,
        )

    async def emit_decision_outcome_recorded(
        self,
        decision_id: UUID,
        security_context: EventSecurityContext,
        outcome: str,
        note: Optional[str],
        correlation_id: str,
    ) -> None:
        """Emit decision.outcome_recorded event."""
        await self.event_store.record_decision_outcome(
            decision_id=decision_id,
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            outcome=outcome,
            note=note,
            correlation_id=correlation_id,
        )

    async def emit_github_issue_added(
        self,
        decision_id: UUID,
        security_context: EventSecurityContext,
        repo: str,
        issue_id: int,
        url: str,
        correlation_id: str,
    ) -> None:
        """Emit github_issue.added event."""
        event = DomainEvent(
            event_id=None,  # Will be generated
            event_type=EventType.GITHUB_ISSUE_ADDED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            data={
                "repo": repo,
                "issue_id": issue_id,
                "url": url,
            },
            correlation_id=correlation_id,
        )
        await self.event_store.append(event)

    async def emit_github_issues_created(
        self,
        decision_id: UUID,
        security_context: EventSecurityContext,
        count: int,
        urls: list[str],
        correlation_id: str,
    ) -> None:
        """Emit github_issues.created event."""
        event = DomainEvent(
            event_id=None,  # Will be generated
            event_type=EventType.GITHUB_ISSUES_CREATED,
            aggregate_id=decision_id,
            aggregate_type="Decision",
            tenant_id=security_context.tenant_id,
            operator_id=security_context.user_id,
            data={
                "count": count,
                "urls": urls,
            },
            correlation_id=correlation_id,
        )
        await self.event_store.append(event)
