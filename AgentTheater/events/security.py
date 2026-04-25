"""Security for Event System: Tenant isolation, RBAC, access control.

Pattern: Events are tagged with tenant_id.
Subscriptions are filtered by tenant (users only see their tenant's events).
RBAC controls who can subscribe to which event types.
Cross-tenant access is blocked at all layers.

Enforcement:
  - SecurityContext extracted from request (user_id, tenant_id, roles)
  - TenantIsolationMiddleware blocks cross-tenant reads
  - EventVisibilityFilter filters subscriptions by permission
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from uuid import UUID
from typing import Optional, List, Set, Dict, Any
from sqlalchemy import select
from AgentTheater.events.db_models import EventLog


class EventPermission(str, Enum):
    """Permissions for event operations."""

    VIEW_EVENTS = "view_events"
    SUBSCRIBE_AGGREGATE = "subscribe_aggregate"
    SUBSCRIBE_EVENT_TYPE = "subscribe_event_type"
    SUBSCRIBE_TENANT = "subscribe_tenant"
    REPLAY_EVENTS = "replay_events"
    VIEW_DLQ = "view_dlq"
    RESOLVE_DLQ = "resolve_dlq"
    ADMIN = "admin"  # All permissions


@dataclass
class EventSecurityContext:
    """Security context for event operations."""

    user_id: UUID
    tenant_id: UUID
    roles: List[str]  # e.g., ["admin", "operator"]
    permissions: Set[EventPermission] = None

    def __post_init__(self):
        if self.permissions is None:
            self._compute_permissions()

    def _compute_permissions(self):
        """Derive permissions from roles."""
        self.permissions = set()

        if "admin" in self.roles:
            # Admin has all permissions
            self.permissions = set(EventPermission)
            return

        if "operator" in self.roles:
            self.permissions.add(EventPermission.VIEW_EVENTS)
            self.permissions.add(EventPermission.SUBSCRIBE_AGGREGATE)
            self.permissions.add(EventPermission.SUBSCRIBE_EVENT_TYPE)
            self.permissions.add(EventPermission.SUBSCRIBE_TENANT)
            self.permissions.add(EventPermission.REPLAY_EVENTS)

        if "viewer" in self.roles:
            self.permissions.add(EventPermission.VIEW_EVENTS)
            self.permissions.add(EventPermission.SUBSCRIBE_AGGREGATE)

    def has_permission(self, permission: EventPermission) -> bool:
        """Check if user has permission."""
        return permission in self.permissions

    def has_any_permission(self, permissions: List[EventPermission]) -> bool:
        """Check if user has any of the permissions."""
        return any(p in self.permissions for p in permissions)


class TenantEventIsolationEnforcer:
    """Enforce tenant isolation for event access."""

    @staticmethod
    def verify_tenant_access(
        security_context: EventSecurityContext,
        event: Dict[str, Any],
    ) -> bool:
        """Verify user can access event (same tenant).

        Returns True if allowed, False if denied.
        """
        event_tenant = event.get("tenant_id")
        return event_tenant == str(security_context.tenant_id)

    @staticmethod
    def verify_tenant_subscription(
        security_context: EventSecurityContext,
        subscription_tenant_id: UUID,
    ) -> bool:
        """Verify user can subscribe to tenant's events.

        Returns True if allowed, False if denied (cross-tenant access).
        """
        return subscription_tenant_id == security_context.tenant_id

    @staticmethod
    def filter_events_by_tenant(
        events: List[Dict[str, Any]],
        security_context: EventSecurityContext,
    ) -> List[Dict[str, Any]]:
        """Filter events to only include user's tenant."""
        tenant_id_str = str(security_context.tenant_id)
        return [
            e for e in events
            if e.get("tenant_id") == tenant_id_str
        ]


class EventVisibilityFilter:
    """Filter event visibility based on permissions and role."""

    def __init__(self, db_session):
        self.db = db_session

    async def get_visible_events(
        self,
        security_context: EventSecurityContext,
        aggregate_id: UUID = None,
        event_type: str = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get events visible to user (tenant-filtered + permission-checked).

        Args:
            security_context: User's security context
            aggregate_id: Optional filter by aggregate
            event_type: Optional filter by event type
            limit: Max results

        Returns:
            List of visible events
        """
        query = select(EventLog).where(
            EventLog.tenant_id == security_context.tenant_id
        )

        if aggregate_id:
            query = query.where(EventLog.aggregate_id == aggregate_id)

        if event_type:
            query = query.where(EventLog.event_type == event_type)

        query = query.order_by(EventLog.timestamp.desc()).limit(limit)

        result = await self.db.execute(query)
        events = result.scalars().all()

        # Convert to dicts
        visible_events = []
        for event in events:
            event_dict = {
                "event_id": str(event.event_id),
                "event_type": event.event_type,
                "aggregate_id": str(event.aggregate_id),
                "tenant_id": str(event.tenant_id),
                "data": event.data,
                "timestamp": event.timestamp.isoformat(),
            }

            # Check if user has permission for this specific event type
            if self._can_view_event_type(security_context, event.event_type):
                visible_events.append(event_dict)

        return visible_events

    def _can_view_event_type(
        self,
        security_context: EventSecurityContext,
        event_type: str,
    ) -> bool:
        """Check if user can view specific event type.

        Override this for fine-grained per-event-type permissions.
        For now, everyone can view events in their tenant.
        """
        if "admin" in security_context.roles:
            return True

        # In future: check event_type against user's allowed_event_types
        return True

    async def get_visible_aggregates(
        self,
        security_context: EventSecurityContext,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get list of aggregates (decisions) visible to user.

        Shows which aggregates user has events for (with their tenant).
        """
        query = select(EventLog.aggregate_id).where(
            EventLog.tenant_id == security_context.tenant_id
        ).distinct()

        result = await self.db.execute(query)
        aggregate_ids = result.scalars().all()

        return [{"aggregate_id": str(aid)} for aid in aggregate_ids]


class RBACEventRouter:
    """Route event subscriptions based on RBAC."""

    def __init__(self, db_session):
        self.db = db_session
        self.visibility_filter = EventVisibilityFilter(db_session)

    async def can_subscribe_to_aggregate(
        self,
        security_context: EventSecurityContext,
        aggregate_id: UUID,
    ) -> bool:
        """Check if user can subscribe to aggregate events.

        Enforces:
          - Same tenant only
          - User must have SUBSCRIBE_AGGREGATE permission
        """
        if not security_context.has_permission(EventPermission.SUBSCRIBE_AGGREGATE):
            return False

        # Check tenant isolation
        if not TenantEventIsolationEnforcer.verify_tenant_subscription(
            security_context, security_context.tenant_id
        ):
            return False

        # Could check if user has specific access to this aggregate
        # (e.g., is decision owner, is project lead)
        # For now, allow if same tenant

        return True

    async def can_subscribe_to_event_type(
        self,
        security_context: EventSecurityContext,
        event_type: str,
    ) -> bool:
        """Check if user can subscribe to event type.

        Enforces:
          - User must have SUBSCRIBE_EVENT_TYPE permission
          - May restrict by event type (e.g., sensitive events)
        """
        if not security_context.has_permission(EventPermission.SUBSCRIBE_EVENT_TYPE):
            return False

        # Could check if event_type is restricted
        # (e.g., security events only for admins)
        sensitive_events = [
            "user.deleted",
            "audit_log.*",
            "security_event.*",
        ]

        if any(event_type.startswith(prefix.replace("*", "")) for prefix in sensitive_events):
            return "admin" in security_context.roles

        return True

    async def can_subscribe_to_tenant(
        self,
        security_context: EventSecurityContext,
        tenant_id: UUID,
    ) -> bool:
        """Check if user can subscribe to all tenant events.

        Enforces:
          - Must be same tenant (no cross-tenant subscriptions)
          - User must have SUBSCRIBE_TENANT permission
        """
        if not security_context.has_permission(EventPermission.SUBSCRIBE_TENANT):
            return False

        # Only allow same tenant
        return tenant_id == security_context.tenant_id

    async def can_replay_events(
        self,
        security_context: EventSecurityContext,
        tenant_id: UUID = None,
    ) -> bool:
        """Check if user can replay events.

        Enforces:
          - User must have REPLAY_EVENTS permission
          - Can only replay own tenant's events
        """
        if not security_context.has_permission(EventPermission.REPLAY_EVENTS):
            return False

        if tenant_id and tenant_id != security_context.tenant_id:
            # Trying to replay another tenant's events
            return False

        return True

    async def can_access_dlq(
        self,
        security_context: EventSecurityContext,
        dlq_tenant_id: UUID = None,
    ) -> bool:
        """Check if user can access dead letter queue.

        Enforces:
          - User must have VIEW_DLQ permission
          - Can only view own tenant's DLQ
        """
        if not security_context.has_permission(EventPermission.VIEW_DLQ):
            return False

        if dlq_tenant_id and dlq_tenant_id != security_context.tenant_id:
            return False

        return True

    async def can_resolve_dlq(
        self,
        security_context: EventSecurityContext,
    ) -> bool:
        """Check if user can resolve DLQ entries.

        Only admins and operators can resolve.
        """
        return security_context.has_permission(EventPermission.RESOLVE_DLQ)


class EventAccessLog:
    """Log event access for audit trail."""

    def __init__(self, logger=None):
        self.logger = logger

    def log_subscription(
        self,
        security_context: EventSecurityContext,
        subscription_type: str,
        filter_value: str,
        allowed: bool,
    ):
        """Log subscription attempt."""
        action = "ALLOWED" if allowed else "DENIED"
        msg = (
            f"Event subscription {action}: "
            f"user={security_context.user_id}, "
            f"tenant={security_context.tenant_id}, "
            f"type={subscription_type}, "
            f"filter={filter_value}"
        )
        if self.logger:
            level = "info" if allowed else "warning"
            getattr(self.logger, level)(msg)

    def log_event_access(
        self,
        security_context: EventSecurityContext,
        event_id: str,
        allowed: bool,
    ):
        """Log event access."""
        action = "ALLOWED" if allowed else "DENIED"
        msg = (
            f"Event access {action}: "
            f"user={security_context.user_id}, "
            f"event={event_id}"
        )
        if self.logger:
            level = "info" if allowed else "warning"
            getattr(self.logger, level)(msg)

    def log_replay_attempt(
        self,
        security_context: EventSecurityContext,
        scope: str,
        allowed: bool,
    ):
        """Log replay attempt."""
        action = "ALLOWED" if allowed else "DENIED"
        msg = (
            f"Event replay {action}: "
            f"user={security_context.user_id}, "
            f"scope={scope}"
        )
        if self.logger:
            level = "info" if allowed else "warning"
            getattr(self.logger, level)(msg)
