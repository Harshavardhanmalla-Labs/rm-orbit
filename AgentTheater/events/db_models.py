"""Database models for production-grade event system.

Tables:
- EventLog: Immutable event ledger
- EventOutbox: Transactional outbox (ensures no lost events)
- ConsumerCheckpoint: Track consumer progress
- DeadLetterQueue: Failed events for manual review
- EventSchema: Schema registry with versioning
"""
from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Index,
    UniqueConstraint,
    Text,
    Boolean,
    Float,
    LargeBinary,
)
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TypeDecorator, CHAR
from uuid import UUID as PythonUUID, uuid4
import uuid


class GUID(TypeDecorator):
    """Platform-independent GUID type for SQLite/MySQL/PostgreSQL."""
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            from sqlalchemy.dialects.postgresql import UUID as PG_UUID
            return dialect.type_descriptor(PG_UUID(as_uuid=False))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, PythonUUID):
            return str(value)
        if isinstance(value, str):
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return PythonUUID(value)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""

    pass


class EventLog(Base):
    """Immutable event ledger (source of truth)."""

    __tablename__ = "event_log"

    # Identification
    event_id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    event_type = Column(String(100), nullable=False, index=True)

    # Aggregation
    aggregate_id = Column(GUID, nullable=False, index=True)
    aggregate_type = Column(String(100), nullable=False)
    sequence_number = Column(Integer, nullable=False)  # Per aggregate

    # Tenancy
    tenant_id = Column(GUID, nullable=False, index=True)
    operator_id = Column(GUID)

    # Data
    data = Column(JSON, nullable=False)
    meta = Column(JSON)

    # Versioning
    version = Column(Integer, default=1, nullable=False)
    schema_version = Column(String(10), default="v1", nullable=False)

    # Tracing
    correlation_id = Column(String(100), nullable=False)
    request_id = Column(String(100))

    # Timestamps
    timestamp = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Indexes
    __table_args__ = (
        Index("ix_event_log_aggregate_sequence", "aggregate_id", "sequence_number", unique=True),
        Index("ix_event_log_tenant_timestamp", "tenant_id", "timestamp"),
        Index("ix_event_log_correlation_id", "correlation_id"),
    )


class EventOutbox(Base):
    """Transactional outbox (guarantees no lost events)."""

    __tablename__ = "event_outbox"

    # Identification
    outbox_id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    event_id = Column(GUID, nullable=False, unique=True, index=True)

    # Publishing state
    published = Column(Boolean, default=False, nullable=False)
    published_at = Column(DateTime(timezone=True))
    attempts = Column(Integer, default=0)
    last_error = Column(Text)

    # Event data
    event_type = Column(String(100), nullable=False)
    aggregate_id = Column(GUID, nullable=False, index=True)
    tenant_id = Column(GUID, nullable=False)
    event_payload = Column(JSON, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Indexes
    __table_args__ = (
        Index("ix_event_outbox_published", "published", "created_at"),
        Index("ix_event_outbox_tenant", "tenant_id"),
    )


class ConsumerCheckpoint(Base):
    """Track consumer progress (safe resume after crash)."""

    __tablename__ = "consumer_checkpoint"

    # Identification
    checkpoint_id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    consumer_name = Column(String(100), nullable=False)
    consumer_group = Column(String(100), nullable=False)

    # Progress tracking
    last_processed_event_id = Column(GUID)
    last_processed_sequence = Column(Integer, default=0, nullable=False)
    last_processed_at = Column(DateTime(timezone=True))

    # State
    is_active = Column(Boolean, default=True, nullable=False)
    last_heartbeat = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Stats
    total_processed = Column(Integer, default=0, nullable=False)
    total_errors = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Uniqueness
    __table_args__ = (
        UniqueConstraint("consumer_name", "consumer_group", name="uq_consumer_group"),
        Index("ix_consumer_checkpoint_active", "is_active", "last_heartbeat"),
    )


class DeadLetterQueue(Base):
    """Failed events for manual review and replay."""

    __tablename__ = "dead_letter_queue"

    # Identification
    dlq_id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    event_id = Column(GUID, nullable=False, unique=True, index=True)
    original_consumer = Column(String(100), nullable=False)

    # Event data
    event_type = Column(String(100), nullable=False)
    aggregate_id = Column(GUID, nullable=False, index=True)
    tenant_id = Column(GUID, nullable=False, index=True)
    event_payload = Column(JSON, nullable=False)

    # Failure details
    error_message = Column(Text, nullable=False)
    error_type = Column(String(100))
    failure_reason = Column(Text)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)

    # Retry info
    next_retry_at = Column(DateTime(timezone=True))
    last_retry_at = Column(DateTime(timezone=True))

    # Resolution
    resolved = Column(Boolean, default=False, nullable=False, index=True)
    resolved_at = Column(DateTime(timezone=True))
    resolution_action = Column(String(100))  # "manual_fix", "replayed", "discarded"

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Indexes
    __table_args__ = (
        Index("ix_dlq_tenant_resolved", "tenant_id", "resolved"),
        Index("ix_dlq_next_retry", "next_retry_at"),
    )


class EventSchema(Base):
    """Schema registry for event versioning."""

    __tablename__ = "event_schema"

    # Identification
    schema_id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    event_type = Column(String(100), nullable=False)
    schema_version = Column(String(10), nullable=False)

    # Schema definition
    json_schema = Column(JSON, nullable=False)  # JSON Schema format
    schema_hash = Column(String(64), nullable=False, unique=True)

    # Compatibility (stored as JSON for SQLite compatibility)
    compatible_versions = Column(JSON)  # Which v1 versions this is compatible with
    breaking_changes = Column(JSON)  # List of breaking changes from previous

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    deprecated = Column(Boolean, default=False, nullable=False)
    deprecated_at = Column(DateTime(timezone=True))

    # Documentation
    description = Column(Text)
    example_payload = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Uniqueness
    __table_args__ = (
        UniqueConstraint("event_type", "schema_version", name="uq_event_schema_version"),
        Index("ix_event_schema_active", "event_type", "is_active"),
    )


class EventMetric(Base):
    """Metrics for observability (event processing latency, lag, etc)."""

    __tablename__ = "event_metric"

    # Identification
    metric_id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    metric_name = Column(String(100), nullable=False, index=True)

    # Labels
    tenant_id = Column(GUID, index=True)
    event_type = Column(String(100), index=True)
    consumer_name = Column(String(100), index=True)

    # Values
    value = Column(Float, nullable=False)
    count = Column(Integer, default=1)

    # Timestamp (for time-series)
    measured_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Indexes
    __table_args__ = (
        Index("ix_event_metric_name_time", "metric_name", "measured_at"),
    )


# Domain models for decision API
class Decision(Base):
    """Decision record."""

    __tablename__ = "decisions"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    project_id = Column(GUID, nullable=False, index=True)
    question = Column(String(500), nullable=False)
    roles = Column(JSON, nullable=False)  # List of required roles
    outcome = Column(String(50))  # succeeded | failed | pivoted | abandoned
    note = Column(Text)

    tenant_id = Column(GUID, nullable=False, index=True)
    created_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_decisions_tenant_created", "tenant_id", "created_at"),
    )


class GithubIssue(Base):
    """GitHub issue linked to decision."""

    __tablename__ = "github_issues"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    decision_id = Column(GUID, nullable=False, index=True)
    repo = Column(String(100), nullable=False)
    issue_id = Column(String(50), nullable=False)
    url = Column(String(500), nullable=False)

    tenant_id = Column(GUID, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_github_issues_decision", "decision_id"),
    )


# System 3: Decision Accountability Engine
class DecisionVersion(Base):
    """Immutable decision snapshot with version history."""

    __tablename__ = "decision_versions"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    decision_id = Column(GUID, nullable=False, index=True)
    version = Column(Integer, nullable=False)  # 1, 2, 3, ...

    # Snapshot data (immutable once created)
    question = Column(String(500), nullable=False)
    rationale = Column(Text)  # Consolidated rationale
    state = Column(String(50), nullable=False)  # ideation|planning|execution|review|completed|abandoned

    # Metadata
    tenant_id = Column(GUID, nullable=False, index=True)
    created_by = Column(GUID, nullable=False)  # Who created this version
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_versions_decision", "decision_id", "version"),
        Index("ix_decision_versions_tenant", "tenant_id"),
    )


class DecisionRationale(Base):
    """Role-level rationale capture for decisions."""

    __tablename__ = "decision_rationales"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    decision_id = Column(GUID, nullable=False, index=True)

    role = Column(String(50), nullable=False)  # ceo, cto, designer, etc.
    reasoning = Column(Text, nullable=False)
    context = Column(JSON)  # Additional context/data for this role's view

    # Attribution
    tenant_id = Column(GUID, nullable=False, index=True)
    provided_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_rationale_decision", "decision_id"),
        Index("ix_decision_rationale_role", "decision_id", "role"),
    )


class DecisionConfidence(Base):
    """Confidence scoring for decisions."""

    __tablename__ = "decision_confidences"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    decision_id = Column(GUID, nullable=False, index=True)

    # Scoring (0-100)
    technical_confidence = Column(Float, nullable=False)  # 0-100
    market_confidence = Column(Float, nullable=False)  # 0-100
    team_confidence = Column(Float, nullable=False)  # 0-100
    overall_confidence = Column(Float, nullable=False)  # Average or weighted

    # Rationale
    reasoning = Column(Text)

    # Attribution
    tenant_id = Column(GUID, nullable=False, index=True)
    scored_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_confidence_decision", "decision_id"),
    )


class RiskAssessment(Base):
    """Risk assessment for decisions."""

    __tablename__ = "risk_assessments"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    decision_id = Column(GUID, nullable=False, index=True)

    # Risk dimensions (0-10 scale)
    technical_risk = Column(Float, nullable=False)  # 0-10
    market_risk = Column(Float, nullable=False)  # 0-10
    financial_risk = Column(Float, nullable=False)  # 0-10
    team_risk = Column(Float, nullable=False)  # 0-10
    overall_risk = Column(Float, nullable=False)  # Overall risk score

    # Mitigation
    mitigations = Column(JSON)  # List of mitigation strategies
    contingency = Column(Text)

    # Attribution
    tenant_id = Column(GUID, nullable=False, index=True)
    assessed_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_risk_assessment_decision", "decision_id"),
    )


class DecisionStateHistory(Base):
    """State machine history for decisions."""

    __tablename__ = "decision_state_history"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    decision_id = Column(GUID, nullable=False, index=True)

    # State transition
    from_state = Column(String(50), nullable=False)
    to_state = Column(String(50), nullable=False)

    # Context
    reason = Column(Text)
    context_data = Column(JSON)

    # Attribution
    tenant_id = Column(GUID, nullable=False, index=True)
    transitioned_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_state_history_decision", "decision_id", "created_at"),
    )


class DecisionReadModel(Base):
    """Denormalized read model optimized for UI queries."""

    __tablename__ = "decision_read_models"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    decision_id = Column(GUID, nullable=False, unique=True, index=True)

    # Current state (denormalized for fast reads)
    question = Column(String(500), nullable=False)
    current_state = Column(String(50), nullable=False)
    current_version = Column(Integer, nullable=False, default=1)

    # Aggregated scores
    overall_confidence = Column(Float)
    overall_risk = Column(Float)

    # Count of contributions
    rationale_count = Column(Integer, default=0)
    confidence_count = Column(Integer, default=0)
    risk_count = Column(Integer, default=0)

    # Last activity
    last_activity_at = Column(DateTime(timezone=True))
    last_activity_by = Column(GUID)

    # Extended fields (added for full read-model support)
    project_id = Column(GUID, index=True)        # Filter by project
    owner_id = Column(GUID)                       # Decision creator
    is_blocked = Column(Boolean, default=False, nullable=False)
    block_reason = Column(Text)
    execution_count = Column(Integer, default=0)

    # Metadata
    tenant_id = Column(GUID, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_read_model_tenant", "tenant_id"),
        Index("ix_decision_read_model_project", "tenant_id", "project_id"),
        Index("ix_decision_read_model_state", "tenant_id", "current_state"),
        Index("ix_decision_read_model_blocked", "tenant_id", "is_blocked"),
    )


# System 4: Decision Execution & Outcome Tracker
class Execution(Base):
    """Execution instance connecting decision to real-world work."""

    __tablename__ = "executions"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    decision_id = Column(GUID, nullable=False, index=True)

    # State machine: approved|assigned|in_progress|blocked|completed|succeeded|failed|pivoted
    state = Column(String(50), nullable=False, default="approved")
    version = Column(Integer, nullable=False, default=1)  # Optimistic locking

    # Assignment
    assigned_to = Column(GUID)  # Team member ID
    assigned_at = Column(DateTime(timezone=True))

    # Timeline
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Blocking
    blocked_at = Column(DateTime(timezone=True))
    blocked_reason = Column(Text)
    unblocked_at = Column(DateTime(timezone=True))

    # Outcome (initially None, set when completed)
    predicted_outcome = Column(String(50))  # succeeded | failed | pivoted
    actual_outcome = Column(String(50))  # succeeded | failed | pivoted | abandoned
    success_metrics = Column(JSON)  # Custom metrics object
    failure_reason = Column(Text)
    lessons_learned = Column(Text)

    # Attribution
    tenant_id = Column(GUID, nullable=False, index=True)
    created_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_execution_decision", "decision_id"),
        Index("ix_execution_tenant_state", "tenant_id", "state"),
        Index("ix_execution_assigned", "assigned_to"),
        Index("ix_execution_blocked", "state", "blocked_reason"),
    )


class ExecutionArtifact(Base):
    """Link execution to GitHub issues, PRs, tasks, docs, deployments."""

    __tablename__ = "execution_artifacts"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    execution_id = Column(GUID, nullable=False, index=True)
    version = Column(Integer, nullable=False, default=1)  # Optimistic locking

    # Artifact type discriminator
    artifact_type = Column(String(50), nullable=False)  # github_issue|github_pr|task|doc|deployment

    # Artifact identifier (varies by type)
    artifact_id = Column(String(100), nullable=False)  # Issue #123, PR #456, task-789, etc.
    artifact_url = Column(String(500))
    artifact_title = Column(String(500))

    # Artifact metadata (flexible JSON for different types)
    artifact_data = Column(JSON)

    # Status (synchronized with artifact state if possible)
    status = Column(String(50))  # open|in_progress|completed|closed|merged|deployed

    # External sync tracking
    artifact_sync_status = Column(String(50), default="pending")  # pending|synced|failed
    last_sync_attempt = Column(DateTime(timezone=True))
    sync_retry_count = Column(Integer, default=0)
    last_synced_at = Column(DateTime(timezone=True))

    # Attribution
    tenant_id = Column(GUID, nullable=False, index=True)
    created_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_execution_artifact_execution", "execution_id", "artifact_type"),
        Index("ix_execution_artifact_tenant", "tenant_id"),
    )


class ExecutionStateHistory(Base):
    """Audit trail of execution state transitions."""

    __tablename__ = "execution_state_history"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    execution_id = Column(GUID, nullable=False, index=True)

    # State transition
    from_state = Column(String(50), nullable=False)
    to_state = Column(String(50), nullable=False)

    # Context
    reason = Column(Text)
    blocked_reason = Column(Text)  # If transitioning to blocked
    context_data = Column(JSON)

    # Attribution
    tenant_id = Column(GUID, nullable=False, index=True)
    transitioned_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_execution_state_history_execution", "execution_id", "created_at"),
        Index("ix_execution_state_history_tenant", "tenant_id"),
    )


class OutcomeRecord(Base):
    """Record of predicted vs actual outcome."""

    __tablename__ = "outcome_records"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    execution_id = Column(GUID, nullable=False, index=True)
    version = Column(Integer, nullable=False, default=1)  # Optimistic locking

    # Prediction (from decision accountability)
    predicted_outcome = Column(String(50), nullable=False)  # succeeded | failed | pivoted
    predicted_confidence = Column(Float)  # 0-100, from confidence scoring
    predicted_at = Column(DateTime(timezone=True), nullable=False)

    # Reality
    actual_outcome = Column(String(50), nullable=False)  # succeeded | failed | pivoted | abandoned
    actual_at = Column(DateTime(timezone=True), nullable=False)

    # Metrics
    success_metrics = Column(JSON)  # Custom metrics object: {metric_name: value, ...}
    failure_reason = Column(Text)
    lessons_learned = Column(Text)

    # Validation
    validated = Column(Boolean, default=False, nullable=False)
    validated_at = Column(DateTime(timezone=True))
    validated_by = Column(GUID)

    # Attribution
    tenant_id = Column(GUID, nullable=False, index=True)
    recorded_by = Column(GUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_outcome_record_execution", "execution_id"),
        Index("ix_outcome_record_tenant_validated", "tenant_id", "validated"),
    )


class ExecutionReadModel(Base):
    """Denormalized read model for execution dashboard."""

    __tablename__ = "execution_read_models"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    execution_id = Column(GUID, nullable=False, unique=True, index=True)
    decision_id = Column(GUID, nullable=False, index=True)

    # Decision context
    decision_question = Column(String(500), nullable=False)

    # Current state
    state = Column(String(50), nullable=False)
    assigned_to = Column(GUID)

    # Timeline
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    age_days = Column(Integer)  # Days since creation

    # Artifacts
    github_issues_count = Column(Integer, default=0)
    github_prs_count = Column(Integer, default=0)
    tasks_count = Column(Integer, default=0)
    docs_count = Column(Integer, default=0)
    deployments_count = Column(Integer, default=0)

    # Outcome
    predicted_outcome = Column(String(50))
    actual_outcome = Column(String(50))
    outcome_validated = Column(Boolean, default=False)

    # Metadata
    tenant_id = Column(GUID, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_execution_read_model_tenant", "tenant_id"),
        Index("ix_execution_read_model_state", "state"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Infrastructure: Atomic sequence counter (replaces SELECT MAX+1 race)
# ─────────────────────────────────────────────────────────────────────────────

class AggregateSequence(Base):
    """Row-locked sequence counter per aggregate stream.

    Guarantees no duplicate sequence_numbers even under concurrent writes.
    PostgreSQL: SELECT FOR UPDATE locks the row.
    SQLite: WAL serializes writes, so no gap even without the lock.
    """
    __tablename__ = "aggregate_sequences"

    aggregate_id = Column(GUID, primary_key=True)
    next_sequence = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), nullable=False,
                        default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# System 6: Learning & Intelligence Layer
# ─────────────────────────────────────────────────────────────────────────────

class DecisionAccuracy(Base):
    """Per-decision accuracy: predicted outcome vs actual validated outcome."""
    __tablename__ = "decision_accuracy"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)
    decision_id = Column(GUID, nullable=False, index=True)
    role_id = Column(GUID, nullable=False, index=True)

    predicted_outcome = Column(String(100), nullable=False)
    predicted_confidence = Column(Float, nullable=False)
    predicted_at = Column(DateTime(timezone=True), nullable=False)

    actual_outcome = Column(String(100))
    actual_at = Column(DateTime(timezone=True))
    validation_source = Column(String(100))

    is_correct = Column(Boolean)
    accuracy_score = Column(Float)
    confidence_error = Column(Float)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_accuracy_tenant_decision", "tenant_id", "decision_id"),
        Index("ix_decision_accuracy_role", "tenant_id", "role_id"),
        Index("ix_decision_accuracy_is_correct", "tenant_id", "is_correct"),
    )


class RolePerformance(Base):
    """Aggregated decision accuracy metrics per role."""
    __tablename__ = "role_performance"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)
    role_id = Column(GUID, nullable=False)
    role_name = Column(String(100), nullable=False)

    total_decisions = Column(Integer, default=0)
    decisions_correct = Column(Integer, default=0)
    decisions_incorrect = Column(Integer, default=0)
    decisions_pending = Column(Integer, default=0)

    accuracy_score = Column(Float, default=0.0)
    avg_predicted_confidence = Column(Float, default=0.0)
    avg_confidence_error = Column(Float, default=0.0)
    is_overconfident = Column(Boolean)
    calibration_gap = Column(Float, default=0.0)

    decisions_last_30_days = Column(Integer, default=0)
    accuracy_last_30_days = Column(Float)
    trend = Column(String(20))

    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_role_performance_tenant_role", "tenant_id", "role_id", unique=True),
    )


class ConfidenceCalibration(Base):
    """Per-band calibration: expected vs actual success rate for a confidence range."""
    __tablename__ = "confidence_calibration"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)
    role_id = Column(GUID, nullable=False)

    confidence_band_low = Column(Float, nullable=False)
    confidence_band_high = Column(Float, nullable=False)

    predictions_in_band = Column(Integer, default=0)
    successes_in_band = Column(Integer, default=0)
    expected_success_rate = Column(Float)
    actual_success_rate = Column(Float)
    calibration_error = Column(Float)
    adjustment_factor = Column(Float)
    recommendation = Column(String(300))

    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_confidence_calibration_role_band", "tenant_id", "role_id", "confidence_band_low"),
    )


class FailurePattern(Base):
    """Detected patterns correlating with decision failures."""
    __tablename__ = "failure_pattern"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)
    role_id = Column(GUID, nullable=False, index=True)

    pattern_name = Column(String(200), nullable=False)
    pattern_description = Column(Text)
    conditions = Column(Text, nullable=False)  # JSON
    failure_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)
    failure_rate = Column(Float)
    severity = Column(String(20))
    recommendation = Column(Text)

    detected_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    last_updated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_failure_pattern_tenant_role", "tenant_id", "role_id"),
        Index("ix_failure_pattern_name", "tenant_id", "pattern_name"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# System 6.5: Decision Influence Engine
# ─────────────────────────────────────────────────────────────────────────────

class RoleReliabilityScore(Base):
    """Composite reliability score for a role, used to weight decision influence."""
    __tablename__ = "role_reliability_score"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)
    role_id = Column(GUID, nullable=False)
    role_name = Column(String(100), nullable=False)

    accuracy_score = Column(Float, default=0.5)
    confidence_calibration = Column(Float, default=1.0)
    decision_volume = Column(Integer, default=0)
    recency_factor = Column(Float, default=0.5)
    reliability_score = Column(Float, default=0.5)
    reliability_tier = Column(String(20))  # expert|trusted|developing|unproven

    last_calculated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_role_reliability_tenant_role", "tenant_id", "role_id", unique=True),
    )


class DecisionInfluenceRecord(Base):
    """Log of all influences applied to a decision before finalization."""
    __tablename__ = "decision_influence_record"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)
    decision_id = Column(GUID, nullable=False, unique=True, index=True)

    original_confidence = Column(Float, nullable=False)
    adjusted_confidence = Column(Float, nullable=False)
    confidence_adjustment_factor = Column(Float)
    confidence_adjustment_reason = Column(String(300))

    risk_level = Column(String(20))
    risk_score = Column(Float)
    risk_factors = Column(Text)  # JSON list

    role_reliability_applied = Column(Boolean, default=False)
    role_reliability_score = Column(Float)
    role_weight_adjustment = Column(Float)

    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(Text)
    is_blocked = Column(Boolean, default=False)
    block_reason = Column(Text)
    requires_additional_review = Column(Boolean, default=False)
    requires_multi_role_consensus = Column(Boolean, default=False)

    recommendation = Column(Text)
    similar_failed_decisions = Column(Integer, default=0)

    influence_applied = Column(Boolean, default=False)
    applied_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_influence_tenant", "tenant_id"),
        Index("ix_decision_influence_risk", "tenant_id", "risk_level"),
        Index("ix_decision_influence_blocked", "tenant_id", "is_blocked"),
    )


class DecisionGuardrail(Base):
    """Tenant-level guardrail rules enforced before decision finalization."""
    __tablename__ = "decision_guardrail"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)

    guardrail_name = Column(String(200), nullable=False)
    guardrail_type = Column(String(50))  # threshold|pattern_block|consensus_required
    rule_definition = Column(Text, nullable=False)  # JSON
    action_on_violation = Column(String(50))  # warn|block|escalate|require_consensus
    severity = Column(String(20))
    enabled = Column(Boolean, default=True)
    violations_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_guardrail_tenant_enabled", "tenant_id", "enabled"),
    )


class GuardrailViolation(Base):
    """Log of guardrail violations per decision."""
    __tablename__ = "guardrail_violation"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)
    decision_id = Column(GUID, nullable=False, index=True)
    guardrail_id = Column(GUID, nullable=False)

    violation_description = Column(Text)
    action_taken = Column(String(50))
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_guardrail_violation_decision", "tenant_id", "decision_id"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# System 7: Decision Intelligence Graph
# ─────────────────────────────────────────────────────────────────────────────

class DecisionCluster(Base):
    """Cluster of similar decisions for cross-decision learning."""
    __tablename__ = "decision_cluster"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)

    cluster_name = Column(String(200), nullable=False)
    cluster_type = Column(String(50))  # outcome_pattern|feature_similarity|risk_cohort
    description = Column(Text)

    decision_count = Column(Integer, default=0)
    member_decision_ids = Column(Text)  # JSON list of UUIDs

    cluster_accuracy = Column(Float)
    cluster_failure_rate = Column(Float)
    cluster_confidence_avg = Column(Float)
    cluster_risk_level = Column(String(20))
    is_healthy = Column(Boolean, default=True)
    health_trend = Column(String(20))

    common_features = Column(Text)    # JSON
    defining_criteria = Column(Text)  # JSON

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_cluster_tenant", "tenant_id"),
        Index("ix_decision_cluster_healthy", "tenant_id", "is_healthy"),
    )


class DecisionSimilarity(Base):
    """Edge: similarity score between two decisions."""
    __tablename__ = "decision_similarity"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)

    decision_id_a = Column(GUID, nullable=False)
    decision_id_b = Column(GUID, nullable=False)
    similarity_score = Column(Float)
    similarity_type = Column(String(50))
    similar_features = Column(Text)  # JSON
    outcome_a = Column(String(100))
    outcome_b = Column(String(100))
    outcome_agreement = Column(Boolean)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_decision_similarity_tenant", "tenant_id"),
        Index("ix_decision_similarity_a", "tenant_id", "decision_id_a"),
        Index("ix_decision_similarity_b", "tenant_id", "decision_id_b"),
        Index("ix_decision_similarity_score", "similarity_score"),
    )


class GlobalRiskSignal(Base):
    """System-wide risk pattern: e.g., 'APPROVED decisions fail 70% of the time'."""
    __tablename__ = "global_risk_signal"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)

    signal_name = Column(String(200), nullable=False)
    signal_type = Column(String(50))
    criteria = Column(Text)  # JSON

    affected_decisions_count = Column(Integer, default=0)
    failure_rate = Column(Float)
    severity = Column(String(20))
    confidence = Column(Float)
    recommendation = Column(Text)
    mitigation_action = Column(String(100))

    is_active = Column(Boolean, default=True)
    first_detected_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    last_validated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_global_risk_signal_tenant_active", "tenant_id", "is_active"),
        Index("ix_global_risk_signal_name", "tenant_id", "signal_name", unique=True),
    )


class ClusterInfluenceLog(Base):
    """Audit: when cluster insights changed a decision's treatment."""
    __tablename__ = "cluster_influence_log"

    id = Column(GUID, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(GUID, nullable=False, index=True)
    cluster_id = Column(GUID, nullable=False, index=True)
    influenced_decision_id = Column(GUID, nullable=False, index=True)

    influence_type = Column(String(50))
    influence_description = Column(Text)
    influence_beneficial = Column(Boolean)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_cluster_influence_log_tenant", "tenant_id"),
    )
