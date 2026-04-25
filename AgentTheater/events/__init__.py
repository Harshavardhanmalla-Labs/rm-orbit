"""Event-driven architecture: Ledger, streaming, state machines.

System 2 powers:
- Immutable audit trails (EventLog table)
- Real-time synchronization (EventBus pub/sub)
- Event replay for debugging (EventReplayer)
- State machine enforcement (DecisionStateMachine)
- Production hardening:
  * Transactional outbox (no lost events)
  * Consumer checkpointing (safe resume after crash)
  * Dead letter queue (failed event handling)
  * Schema registry (versioned event validation)
  * Idempotent processing (duplicate handling)
  * Observability (metrics, logging)
  * Security (tenant isolation, RBAC)
"""
from AgentTheater.events.consumer_checkpoint import (
    ConsumerCheckpointManager,
    ConsumerGroupCoordinator,
    EventConsumer,
)
from AgentTheater.events.dlq_handler import (
    DLQHandler,
    DLQRetryProcessor,
    ResolutionAction,
)
from AgentTheater.events.schema_registry import (
    SchemaRegistry,
    BackwardCompatibilityChecker,
    SchemaEvolutionValidator,
    CompatibilityMode,
)
from AgentTheater.events.delivery_guarantees import (
    IdempotencyTracker,
    IdempotentConsumerPattern,
    DuplicateDetector,
    IdempotencyStrategy,
)
from AgentTheater.events.replay import (
    EventReplayer,
    ProjectionBuilder,
    ConsistencyChecker,
    ReplayScope,
    ReplayStatus,
)
from AgentTheater.events.observability import (
    EventMetricsCollector,
    EventLogger,
    MetricType,
    measure_latency,
)
from AgentTheater.events.security import (
    EventSecurityContext,
    TenantEventIsolationEnforcer,
    EventVisibilityFilter,
    RBACEventRouter,
    EventAccessLog,
    EventPermission,
)

__all__ = [
    # Consumer checkpointing (safe resume)
    "ConsumerCheckpointManager",
    "ConsumerGroupCoordinator",
    "EventConsumer",
    # Dead letter queue (failed event handling)
    "DLQHandler",
    "DLQRetryProcessor",
    "ResolutionAction",
    # Schema registry (versioned validation)
    "SchemaRegistry",
    "BackwardCompatibilityChecker",
    "SchemaEvolutionValidator",
    "CompatibilityMode",
    # Idempotent processing (duplicate handling)
    "IdempotencyTracker",
    "IdempotentConsumerPattern",
    "DuplicateDetector",
    "IdempotencyStrategy",
    # Replay system (rebuild state)
    "EventReplayer",
    "ProjectionBuilder",
    "ConsistencyChecker",
    "ReplayScope",
    "ReplayStatus",
    # Observability (metrics, logging)
    "EventMetricsCollector",
    "EventLogger",
    "MetricType",
    "measure_latency",
    # Security (tenant isolation, RBAC)
    "EventSecurityContext",
    "TenantEventIsolationEnforcer",
    "EventVisibilityFilter",
    "RBACEventRouter",
    "EventAccessLog",
    "EventPermission",
]
