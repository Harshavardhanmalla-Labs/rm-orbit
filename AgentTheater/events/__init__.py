"""Event-driven architecture with event sourcing and immutable ledgers.

Production-hardened System 2 with:
- Transactional outbox (no lost events)
- Consumer checkpointing (safe resume)
- Dead letter queue (failed event handling)
- Schema registry (versioned events)
- Idempotent processing (no duplicates)
- Event replay (rebuild state)
- Observability (metrics, logging)
- Security (tenant isolation, RBAC)
"""

# Core event system
from AgentTheater.events.ledger import EventStore, EventLedger, DomainEvent, EventType
from AgentTheater.events.outbox import (
    TransactionalOutbox,
    OutboxPublisher,
    OutboxScheduler,
)

__all__ = [
    "EventStore",
    "EventLedger",
    "DomainEvent",
    "EventType",
    "TransactionalOutbox",
    "OutboxPublisher",
    "OutboxScheduler",
]
