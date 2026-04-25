"""Delivery Guarantees: Idempotent processing and duplicate handling.

Pattern: Events must be delivered at-least-once (may retry on failure).
Consumers must be idempotent (processing same event twice = same result).

Idempotency strategies:
  1. Idempotency key: Track by event_id + consumer_name (prevent re-processing)
  2. State-based: Check if operation already done (already updated DB)
  3. Hash-based: Store hash of event, skip if duplicate received

This module provides tools for any of these approaches.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4
from typing import Optional, Dict, Any
from enum import Enum
from sqlalchemy import select, Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import DeclarativeBase


class IdempotencyStrategy(str, Enum):
    """Strategies for ensuring idempotent delivery."""

    IDEMPOTENCY_KEY = "idempotency_key"  # Track by event_id + consumer
    STATE_BASED = "state_based"  # Check if state already matches
    HASH_BASED = "hash_based"  # Track hash of event payload


# Optional: SQLAlchemy model for idempotency tracking
class IdempotencyRecord:
    """Tracks processed events to prevent duplicates (optional persistence).

    Usage:
        record = await idempotency_tracker.get_or_create(
            event_id=event.id,
            consumer_name="decision-processor",
            consumer_group="default"
        )

        if record.was_processed:
            return record.result  # Skip re-processing

        # Process event
        result = await process(event)
        await idempotency_tracker.mark_processed(record, result)
    """

    __tablename__ = "idempotency_record"

    idempotency_id = Column(PG_UUID, primary_key=True, default=uuid4)
    event_id = Column(PG_UUID, nullable=False, index=True)
    consumer_name = Column(String(100), nullable=False, index=True)
    consumer_group = Column(String(100), nullable=False)

    # Processing result (to return if called again)
    was_processed = Column(String(10), default="pending", nullable=False)  # pending|success|failed
    result = Column(JSONB)  # Result of processing (if successful)
    error_message = Column(Text)  # Error if processing failed

    # Timestamps
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)
    expires_at = Column(DateTime(timezone=True))  # TTL for cleanup


class IdempotencyTracker:
    """Track processed events to prevent duplicate processing."""

    def __init__(self, db_session, ttl_days: int = 7):
        self.db = db_session
        self.ttl_days = ttl_days

    async def get_or_create(
        self,
        event_id: UUID,
        consumer_name: str,
        consumer_group: str = "default",
    ) -> Dict[str, Any]:
        """Get or create idempotency record for this event+consumer.

        Returns:
            {
                "idempotency_id": UUID,
                "event_id": UUID,
                "consumer_name": str,
                "was_processed": "pending" | "success" | "failed",
                "result": dict or None,
                "error_message": str or None
            }
        """
        # Query idempotency record
        result = await self.db.execute(
            select(IdempotencyRecord).where(
                (IdempotencyRecord.event_id == event_id)
                & (IdempotencyRecord.consumer_name == consumer_name)
                & (IdempotencyRecord.consumer_group == consumer_group)
            )
        )
        record = result.scalar_one_or_none()

        if record:
            # Already exists, return it
            return {
                "idempotency_id": record.idempotency_id,
                "event_id": record.event_id,
                "consumer_name": record.consumer_name,
                "was_processed": record.was_processed,
                "result": record.result,
                "error_message": record.error_message,
                "is_duplicate": True,
            }

        # Create new record (mark as pending)
        expires_at = datetime.now(timezone.utc) + timedelta(days=self.ttl_days)

        record = IdempotencyRecord(
            idempotency_id=uuid4(),
            event_id=event_id,
            consumer_name=consumer_name,
            consumer_group=consumer_group,
            was_processed="pending",
            expires_at=expires_at,
        )
        self.db.add(record)
        await self.db.commit()

        return {
            "idempotency_id": record.idempotency_id,
            "event_id": record.event_id,
            "consumer_name": record.consumer_name,
            "was_processed": "pending",
            "result": None,
            "error_message": None,
            "is_duplicate": False,
        }

    async def mark_processed(
        self,
        event_id: UUID,
        consumer_name: str,
        consumer_group: str,
        result: Dict[str, Any] = None,
    ) -> None:
        """Mark event as successfully processed."""
        record_result = await self.db.execute(
            select(IdempotencyRecord).where(
                (IdempotencyRecord.event_id == event_id)
                & (IdempotencyRecord.consumer_name == consumer_name)
                & (IdempotencyRecord.consumer_group == consumer_group)
            )
        )
        record = record_result.scalar_one_or_none()

        if record:
            record.was_processed = "success"
            record.result = result
            record.processed_at = datetime.now(timezone.utc)
            await self.db.commit()

    async def mark_failed(
        self,
        event_id: UUID,
        consumer_name: str,
        consumer_group: str,
        error_message: str,
    ) -> None:
        """Mark event processing as failed."""
        record_result = await self.db.execute(
            select(IdempotencyRecord).where(
                (IdempotencyRecord.event_id == event_id)
                & (IdempotencyRecord.consumer_name == consumer_name)
                & (IdempotencyRecord.consumer_group == consumer_group)
            )
        )
        record = record_result.scalar_one_or_none()

        if record:
            record.was_processed = "failed"
            record.error_message = error_message
            record.processed_at = datetime.now(timezone.utc)
            await self.db.commit()

    async def cleanup_expired(self) -> int:
        """Delete expired idempotency records (TTL cleanup).

        Returns count of deleted records.
        """
        now = datetime.now(timezone.utc)

        # Find expired records
        result = await self.db.execute(
            select(IdempotencyRecord).where(IdempotencyRecord.expires_at <= now)
        )
        expired = result.scalars().all()

        # Delete them
        for record in expired:
            await self.db.delete(record)

        await self.db.commit()
        return len(expired)


class DuplicateDetector:
    """Detect duplicate events (same payload sent twice)."""

    @staticmethod
    def compute_event_hash(event_id: str, event_type: str, payload: Dict[str, Any]) -> str:
        """Compute hash for duplicate detection.

        Hash includes event_id (so same business operation with different event_id != duplicate)
        and payload (so if payload changes, it's not a duplicate).
        """
        import hashlib
        import json

        content = json.dumps(
            {
                "event_id": event_id,
                "event_type": event_type,
                "payload": payload,
            },
            sort_keys=True,
        )
        return hashlib.sha256(content.encode()).hexdigest()

    @staticmethod
    async def check_duplicate(
        db_session,
        event_id: str,
        event_type: str,
        payload: Dict[str, Any],
    ) -> bool:
        """Check if event with this content was already processed.

        Returns True if duplicate (already seen), False if new.
        """
        event_hash = DuplicateDetector.compute_event_hash(event_id, event_type, payload)

        # In real implementation, query a deduplication table
        # For now, this is a placeholder for the pattern
        # Actual implementation would look like:
        #   result = await db_session.execute(
        #       select(DeduplicationRecord).where(
        #           DeduplicationRecord.event_hash == event_hash
        #       )
        #   )
        #   return result.scalar_one_or_none() is not None

        return False


class IdempotentConsumerPattern:
    """Template for building idempotent event consumers.

    Usage:
        class DecisionOutcomeConsumer(IdempotentConsumerPattern):
            async def process_unique(self, event):
                # This only runs if event is new (not duplicate)
                await decision_service.record_outcome(event["data"])

        consumer = DecisionOutcomeConsumer(db, idempotency_tracker)
        await consumer.handle_event(event)
    """

    def __init__(self, db_session, idempotency_tracker: IdempotencyTracker = None):
        self.db = db_session
        self.idempotency_tracker = (
            idempotency_tracker or IdempotencyTracker(db_session)
        )

    async def handle_event(
        self,
        event: Dict[str, Any],
        consumer_name: str,
        consumer_group: str = "default",
    ) -> Dict[str, Any]:
        """Handle event with idempotency guarantee.

        If event was already processed, returns cached result.
        Otherwise, calls process_unique() and caches result.
        """
        event_id = event["event_id"]

        # Check idempotency
        idempotency = await self.idempotency_tracker.get_or_create(
            event_id=UUID(event_id),
            consumer_name=consumer_name,
            consumer_group=consumer_group,
        )

        if idempotency["is_duplicate"]:
            # Already processed, return cached result
            if idempotency["was_processed"] == "success":
                return {
                    "processed": True,
                    "duplicate": True,
                    "result": idempotency["result"],
                }
            elif idempotency["was_processed"] == "failed":
                return {
                    "processed": False,
                    "duplicate": True,
                    "error": idempotency["error_message"],
                }
            else:
                # Still pending? Shouldn't happen, but handle gracefully
                return {
                    "processed": False,
                    "duplicate": False,
                    "error": "Event processing still pending",
                }

        # New event, process it
        try:
            result = await self.process_unique(event)

            await self.idempotency_tracker.mark_processed(
                event_id=UUID(event_id),
                consumer_name=consumer_name,
                consumer_group=consumer_group,
                result=result,
            )

            return {
                "processed": True,
                "duplicate": False,
                "result": result,
            }

        except Exception as e:
            await self.idempotency_tracker.mark_failed(
                event_id=UUID(event_id),
                consumer_name=consumer_name,
                consumer_group=consumer_group,
                error_message=str(e),
            )

            raise

    async def process_unique(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Override this to handle unique (non-duplicate) events.

        Guaranteed to run only once per unique event.
        """
        raise NotImplementedError(
            "Subclasses must implement process_unique(event)"
        )
