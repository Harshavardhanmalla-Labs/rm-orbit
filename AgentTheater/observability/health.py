"""Health checks and diagnostics for production observability."""
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class HealthChecker:
    """Deep health checks for all system components."""

    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db = db_session

    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and performance."""
        status = "healthy"
        details = {}

        if not self.db:
            return {"status": "unknown", "details": "Database session not available"}

        try:
            # Test connectivity
            result = await self.db.execute(text("SELECT 1"))
            await result.close()
            details["connectivity"] = "ok"

            # Check connection pool (if available)
            if hasattr(self.db, "connection"):
                details["connection_pool"] = {
                    "size": getattr(self.db.connection, "pool_size", "unknown"),
                    "active": getattr(self.db.connection, "active_count", "unknown"),
                }
        except Exception as e:
            status = "unhealthy"
            details["error"] = str(e)

        return {"status": status, "details": details}

    async def check_event_store(self) -> Dict[str, Any]:
        """Check event store health."""
        status = "healthy"
        details = {}

        if not self.db:
            return {"status": "unknown", "details": "Database session not available"}

        try:
            # Check EventLog table
            result = await self.db.execute(
                text("SELECT COUNT(*) FROM event_log")
            )
            count = result.scalar()
            details["event_log_count"] = count

            # Check for DLQ entries
            result = await self.db.execute(
                text("SELECT COUNT(*) FROM dead_letter_queue WHERE resolved = 0")
            )
            dlq_count = result.scalar()
            details["dlq_unresolved"] = dlq_count

            if dlq_count > 100:
                status = "degraded"
                details["dlq_warning"] = "Unresolved DLQ items > 100"
        except Exception as e:
            status = "unhealthy"
            details["error"] = str(e)

        return {"status": status, "details": details}

    async def check_executions(self) -> Dict[str, Any]:
        """Check execution system health."""
        status = "healthy"
        details = {}

        if not self.db:
            return {"status": "unknown", "details": "Database session not available"}

        try:
            # Check in-progress executions
            result = await self.db.execute(
                text("SELECT COUNT(*) FROM executions WHERE state = 'in_progress'")
            )
            in_progress = result.scalar()
            details["in_progress_count"] = in_progress

            # Check stale executions (> 7 days in progress)
            result = await self.db.execute(
                text("""
                    SELECT COUNT(*) FROM executions
                    WHERE state = 'in_progress'
                    AND started_at < datetime('now', '-7 days')
                """)
            )
            stale = result.scalar()
            details["stale_count"] = stale

            if stale > 0:
                status = "degraded"
                details["stale_warning"] = f"{stale} stale executions detected"

            # Check blocked executions
            result = await self.db.execute(
                text("SELECT COUNT(*) FROM executions WHERE state = 'blocked'")
            )
            blocked = result.scalar()
            details["blocked_count"] = blocked
        except Exception as e:
            status = "unhealthy"
            details["error"] = str(e)

        return {"status": status, "details": details}

    async def check_outbox_backlog(self) -> Dict[str, Any]:
        """Check event outbox backlog and relay heartbeat."""
        status = "healthy"
        details: Dict[str, Any] = {}

        if self.db:
            try:
                result = await self.db.execute(
                    text("SELECT COUNT(*) FROM event_outbox WHERE published = 0")
                )
                unpublished = result.scalar() or 0
                details["unpublished_count"] = unpublished

                if unpublished > 500:
                    status = "unhealthy"
                    details["backlog_warning"] = f"Outbox backlog critical: {unpublished} unpublished events"
                elif unpublished > 100:
                    status = "degraded"
                    details["backlog_warning"] = f"Outbox backlog elevated: {unpublished} unpublished events"

                # Max attempts exceeded (stuck events)
                result = await self.db.execute(
                    text("SELECT COUNT(*) FROM event_outbox WHERE published = 0 AND attempts >= 5")
                )
                stuck = result.scalar() or 0
                details["stuck_count"] = stuck
                if stuck > 0 and status == "healthy":
                    status = "degraded"
                    details["stuck_warning"] = f"{stuck} events exceeded max retry attempts"
            except Exception as e:
                status = "unhealthy"
                details["error"] = str(e)

        from AgentTheater.events.outbox_relay import get_relay_status
        relay = get_relay_status()
        details["relay"] = relay
        if not relay["running"] and status == "healthy":
            status = "degraded"
            details["relay_warning"] = "Outbox relay has not run recently"

        return {"status": status, "details": details}

    async def deep_health(self) -> Dict[str, Any]:
        """Run all health checks and return aggregate status."""
        db_health = await self.check_database()
        event_health = await self.check_event_store()
        execution_health = await self.check_executions()
        outbox_health = await self.check_outbox_backlog()

        statuses = [
            db_health["status"],
            event_health["status"],
            execution_health["status"],
            outbox_health["status"],
        ]
        if "unhealthy" in statuses:
            aggregate_status = "unhealthy"
        elif "degraded" in statuses:
            aggregate_status = "degraded"
        else:
            aggregate_status = "healthy"

        return {
            "status": aggregate_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": {
                "database": db_health,
                "event_store": event_health,
                "executions": execution_health,
                "outbox": outbox_health,
            },
        }

    async def readiness(self) -> Dict[str, Any]:
        """Check if system is ready to accept traffic."""
        db_health = await self.check_database()
        outbox_health = await self.check_outbox_backlog()

        ready = (
            db_health["status"] == "healthy"
            and outbox_health["status"] != "unhealthy"
        )

        return {
            "ready": ready,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": {
                "database": "ok" if db_health["status"] == "healthy" else "not_ok",
                "outbox": outbox_health["status"],
            },
        }
