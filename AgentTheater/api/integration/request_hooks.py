"""Hooks for transactional event emission (atomic writes)."""
from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from AgentTheater.events import EventStore


@asynccontextmanager
async def transactional_event_scope(
    db_session: AsyncSession,
    event_store: EventStore,
):
    """Ensure atomic transaction for domain change + event.

    Usage:
        async with transactional_event_scope(db, event_store) as (db, store):
            # Write domain change
            decision = Decision(...)
            db.add(decision)

            # Emit event (same transaction)
            await store.record_decision_created(...)

            # On exit: both committed or both rolled back
            # After context: events published to subscribers

    Guarantees:
      - Decision written IFF event written
      - No partial state
      - No lost events
    """

    async with db_session.begin():
        # Transaction open
        yield db_session, event_store

        # Auto-commit on exit (or rollback on exception)

    # After transaction commits, publish pending events
    await event_store.commit()


class RequestContext:
    """Store per-request context (correlation_id, user, tenant, etc)."""

    def __init__(
        self,
        correlation_id: str,
        user_id: UUID,
        tenant_id: UUID,
        roles: list[str],
        api_version: str = "v1",
    ):
        self.correlation_id = correlation_id
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.roles = roles
        self.api_version = api_version

    def to_dict(self) -> dict:
        """Convert to dict for response headers."""
        return {
            "correlation_id": self.correlation_id,
            "api_version": self.api_version,
        }
