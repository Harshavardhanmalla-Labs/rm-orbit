"""Observability for Event System: Metrics, logging, health checks.

Metrics:
  - event_publish_latency: Time from event creation to successful publish
  - event_consumer_lag: How far behind consumers are vs latest event
  - dlq_count: Number of failed events in dead letter queue
  - replay_duration: Time to rebuild state from events
  - schema_validation_errors: Events rejected by schema validation

Logging:
  - All operations include correlation_id for tracing
  - Tenant_id included for multi-tenant debugging
  - Event_id included for event tracing
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import UUID
from typing import Optional, Dict, Any, List
from enum import Enum
import time
from contextlib import asynccontextmanager
from sqlalchemy import select, func
from AgentTheater.events.db_models import (
    EventLog,
    EventOutbox,
    ConsumerCheckpoint,
    DeadLetterQueue,
    EventMetric,
)


class MetricType(str, Enum):
    """Event system metrics."""

    PUBLISH_LATENCY = "event_publish_latency"
    CONSUMER_LAG = "event_consumer_lag"
    DLQ_COUNT = "dlq_count"
    SCHEMA_VALIDATION_ERROR = "schema_validation_error"
    REPLAY_DURATION = "replay_duration"
    CONSUMER_ERROR_RATE = "consumer_error_rate"


class EventMetricsCollector:
    """Collect and track event system metrics."""

    def __init__(self, db_session):
        self.db = db_session

    async def record_metric(
        self,
        metric_name: str,
        value: float,
        tenant_id: UUID = None,
        event_type: str = None,
        consumer_name: str = None,
        tags: Dict[str, str] = None,
    ) -> EventMetric:
        """Record a metric value.

        Args:
            metric_name: Metric type (from MetricType enum)
            value: Numeric value
            tenant_id: Optional tenant context
            event_type: Optional event type context
            consumer_name: Optional consumer context
            tags: Additional metadata

        Returns:
            Recorded EventMetric
        """
        metric = EventMetric(
            metric_name=metric_name,
            tenant_id=tenant_id,
            event_type=event_type,
            consumer_name=consumer_name,
            value=value,
            measured_at=datetime.now(timezone.utc),
        )
        self.db.add(metric)
        await self.db.commit()

        return metric

    async def get_publish_latency_stats(
        self,
        tenant_id: UUID = None,
        time_window_minutes: int = 60,
    ) -> Dict[str, Any]:
        """Get event publish latency statistics.

        Returns:
            {
                "p50_ms": 45,
                "p95_ms": 280,
                "p99_ms": 890,
                "avg_ms": 120,
                "samples": 1234,
                "time_window_minutes": 60
            }
        """
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=time_window_minutes)

        query = select(EventMetric).where(
            (EventMetric.metric_name == MetricType.PUBLISH_LATENCY.value)
            & (EventMetric.measured_at >= cutoff)
        )

        if tenant_id:
            query = query.where(EventMetric.tenant_id == tenant_id)

        result = await self.db.execute(query)
        metrics = result.scalars().all()

        if not metrics:
            return {
                "p50_ms": None,
                "p95_ms": None,
                "p99_ms": None,
                "avg_ms": None,
                "samples": 0,
            }

        values = sorted([m.value for m in metrics])
        n = len(values)

        return {
            "p50_ms": values[int(n * 0.50)],
            "p95_ms": values[int(n * 0.95)],
            "p99_ms": values[int(n * 0.99)],
            "avg_ms": sum(values) / n,
            "samples": n,
            "time_window_minutes": time_window_minutes,
        }

    async def get_consumer_lag(
        self,
        consumer_group: str,
    ) -> Dict[str, Any]:
        """Get consumer lag (how far behind consumers are).

        Returns:
            {
                "latest_event_sequence": 12345,
                "consumers": {
                    "consumer-1": {
                        "last_processed_sequence": 12340,
                        "lag_count": 5,
                        "is_active": true
                    }
                }
            }
        """
        # Get latest event sequence
        result = await self.db.execute(
            select(func.max(EventLog.sequence_number))
        )
        latest_sequence = result.scalar() or 0

        # Get consumer checkpoints
        result = await self.db.execute(
            select(ConsumerCheckpoint).where(
                ConsumerCheckpoint.consumer_group == consumer_group
            )
        )
        consumers = result.scalars().all()

        consumer_lag = {}
        for consumer in consumers:
            lag = latest_sequence - consumer.last_processed_sequence
            consumer_lag[consumer.consumer_name] = {
                "last_processed_sequence": consumer.last_processed_sequence,
                "lag_count": lag,
                "is_active": consumer.is_active,
                "last_heartbeat_seconds_ago": int(
                    (datetime.now(timezone.utc) - consumer.last_heartbeat).total_seconds()
                ) if consumer.last_heartbeat else None,
            }

        return {
            "latest_event_sequence": latest_sequence,
            "consumers": consumer_lag,
        }

    async def get_dlq_metrics(
        self,
        tenant_id: UUID = None,
    ) -> Dict[str, Any]:
        """Get dead letter queue metrics.

        Returns:
            {
                "total_dlq_count": 5,
                "unresolved_count": 3,
                "resolved_count": 2,
                "by_consumer": {...},
                "by_event_type": {...},
                "oldest_unresolved_age_seconds": 3600
            }
        """
        query = select(DeadLetterQueue)
        if tenant_id:
            query = query.where(DeadLetterQueue.tenant_id == tenant_id)

        result = await self.db.execute(query)
        dlq_entries = result.scalars().all()

        unresolved = [e for e in dlq_entries if not e.resolved]
        resolved = [e for e in dlq_entries if e.resolved]

        # By consumer
        by_consumer = {}
        for entry in unresolved:
            key = entry.original_consumer
            by_consumer[key] = by_consumer.get(key, 0) + 1

        # By event type
        by_event_type = {}
        for entry in unresolved:
            key = entry.event_type
            by_event_type[key] = by_event_type.get(key, 0) + 1

        # Oldest unresolved
        oldest_age = None
        if unresolved:
            oldest = min(unresolved, key=lambda e: e.created_at)
            oldest_age = int(
                (datetime.now(timezone.utc) - oldest.created_at).total_seconds()
            )

        return {
            "total_dlq_count": len(dlq_entries),
            "unresolved_count": len(unresolved),
            "resolved_count": len(resolved),
            "by_consumer": by_consumer,
            "by_event_type": by_event_type,
            "oldest_unresolved_age_seconds": oldest_age,
        }

    async def get_health_report(
        self,
        tenant_id: UUID = None,
    ) -> Dict[str, Any]:
        """Get health report for dashboard/monitoring.

        Returns:
            {
                "status": "healthy" | "degraded" | "unhealthy",
                "checks": {
                    "event_publish_latency": {...},
                    "consumer_lag": {...},
                    "dlq_count": {...},
                },
                "overall_metrics": {...}
            }
        """
        checks = {}

        # Publish latency check
        latency_stats = await self.get_publish_latency_stats(tenant_id, 60)
        p95_ms = latency_stats.get("p95_ms")
        latency_status = "healthy"
        if p95_ms and p95_ms > 5000:
            latency_status = "unhealthy"
        elif p95_ms and p95_ms > 2000:
            latency_status = "degraded"

        checks["event_publish_latency"] = {
            "status": latency_status,
            "p95_ms": p95_ms,
            "threshold_warning_ms": 2000,
            "threshold_critical_ms": 5000,
        }

        # DLQ check
        dlq_metrics = await self.get_dlq_metrics(tenant_id)
        dlq_status = "healthy"
        if dlq_metrics["unresolved_count"] > 10:
            dlq_status = "unhealthy"
        elif dlq_metrics["unresolved_count"] > 5:
            dlq_status = "degraded"

        checks["dlq_count"] = {
            "status": dlq_status,
            "unresolved_count": dlq_metrics["unresolved_count"],
            "threshold_warning": 5,
            "threshold_critical": 10,
        }

        # Consumer lag check
        # Note: would need to know consumer group to check this fully
        checks["consumer_lag"] = {
            "status": "unknown",
            "message": "Check specific consumer groups for lag metrics",
        }

        # Overall status
        statuses = [c.get("status") for c in checks.values()]
        if "unhealthy" in statuses:
            overall = "unhealthy"
        elif "degraded" in statuses:
            overall = "degraded"
        else:
            overall = "healthy"

        return {
            "status": overall,
            "checks": checks,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }


@asynccontextmanager
async def measure_latency(
    metrics_collector: EventMetricsCollector,
    metric_name: str,
    tenant_id: UUID = None,
    event_type: str = None,
):
    """Context manager to measure operation latency.

    Usage:
        async with measure_latency(collector, "event_publish_latency", tenant_id):
            await event_bus.publish(event)
    """
    start = time.time()

    try:
        yield
    finally:
        elapsed_ms = (time.time() - start) * 1000
        await metrics_collector.record_metric(
            metric_name,
            elapsed_ms,
            tenant_id=tenant_id,
            event_type=event_type,
        )


class EventLogger:
    """Structured logging for event system with correlation tracking."""

    def __init__(self, logger=None):
        self.logger = logger

    def log_event_created(
        self,
        event_id: str,
        event_type: str,
        aggregate_id: str,
        tenant_id: str,
        correlation_id: str,
        **context,
    ):
        """Log event creation."""
        msg = (
            f"Event created: {event_type} "
            f"(id={event_id}, aggregate={aggregate_id}, "
            f"tenant={tenant_id}, correlation={correlation_id})"
        )
        if self.logger:
            self.logger.info(msg, extra=context)

    def log_event_published(
        self,
        event_id: str,
        event_type: str,
        correlation_id: str,
        latency_ms: float,
        **context,
    ):
        """Log successful event publication."""
        msg = (
            f"Event published: {event_type} "
            f"(id={event_id}, latency={latency_ms:.2f}ms, "
            f"correlation={correlation_id})"
        )
        if self.logger:
            self.logger.info(msg, extra=context)

    def log_consumer_processed(
        self,
        event_id: str,
        consumer_name: str,
        sequence_number: int,
        correlation_id: str,
        **context,
    ):
        """Log consumer successfully processed event."""
        msg = (
            f"Event processed: consumer={consumer_name} "
            f"(id={event_id}, seq={sequence_number}, "
            f"correlation={correlation_id})"
        )
        if self.logger:
            self.logger.info(msg, extra=context)

    def log_consumer_error(
        self,
        event_id: str,
        consumer_name: str,
        error: str,
        correlation_id: str,
        **context,
    ):
        """Log consumer processing error."""
        msg = (
            f"Event processing failed: consumer={consumer_name} "
            f"(id={event_id}, error={error}, "
            f"correlation={correlation_id})"
        )
        if self.logger:
            self.logger.error(msg, extra=context)

    def log_dlq_move(
        self,
        event_id: str,
        event_type: str,
        consumer_name: str,
        error_reason: str,
        correlation_id: str,
        **context,
    ):
        """Log event moved to DLQ."""
        msg = (
            f"Event moved to DLQ: {event_type} "
            f"(id={event_id}, consumer={consumer_name}, "
            f"reason={error_reason}, correlation={correlation_id})"
        )
        if self.logger:
            self.logger.warning(msg, extra=context)
