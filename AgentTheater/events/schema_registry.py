"""Event Schema Registry: Versioned schemas with backward-compatible evolution.

Pattern: Events are versioned with JSON Schema.
New schema versions must be backward-compatible with old events.
Consumers validate incoming events against schema.
Producers register schema before creating events.

Evolution rules:
  ALLOWED: Add optional field, widen type, loosen constraints
  FORBIDDEN: Remove field, narrow type, make field required, change meaning
"""
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any
from enum import Enum
from sqlalchemy import select
from jsonschema import Draft7Validator, ValidationError
from AgentTheater.events.db_models import EventSchema


class CompatibilityMode(str, Enum):
    """Schema compatibility rules."""

    BACKWARD = "backward"  # New schema can read old events
    FORWARD = "forward"  # Old schema can read new events
    FULL = "full"  # Both directions
    NONE = "none"  # No compatibility required


class SchemaRegistry:
    """Manage event schema versions and validation."""

    def __init__(self, db_session):
        self.db = db_session

    def _compute_schema_hash(self, json_schema: Dict[str, Any]) -> str:
        """Compute hash of schema for deduplication."""
        schema_str = json.dumps(json_schema, sort_keys=True)
        return hashlib.sha256(schema_str.encode()).hexdigest()

    async def register_schema(
        self,
        event_type: str,
        schema_version: str,
        json_schema: Dict[str, Any],
        compatible_versions: List[str] = None,
        breaking_changes: List[str] = None,
        description: str = None,
        example_payload: Dict[str, Any] = None,
    ) -> EventSchema:
        """Register a new event schema version.

        Args:
            event_type: Event type (e.g., "decision.outcome_recorded")
            schema_version: Version (e.g., "v1", "v2")
            json_schema: JSON Schema definition (Draft 7)
            compatible_versions: Which older versions this is compatible with
            breaking_changes: List of breaking changes from previous (optional)
            description: Human description
            example_payload: Example valid event

        Returns:
            Registered EventSchema
        """
        schema_hash = self._compute_schema_hash(json_schema)

        # Check if hash already exists (duplicate schema)
        result = await self.db.execute(
            select(EventSchema).where(EventSchema.schema_hash == schema_hash)
        )
        existing = result.scalar_one_or_none()

        if existing and existing.event_type == event_type:
            # Same schema already registered for this event type
            return existing

        # Create new schema version
        schema = EventSchema(
            schema_id=uuid4(),
            event_type=event_type,
            schema_version=schema_version,
            json_schema=json_schema,
            schema_hash=schema_hash,
            compatible_versions=compatible_versions or [],
            breaking_changes=breaking_changes or [],
            is_active=True,
            description=description,
            example_payload=example_payload,
        )

        self.db.add(schema)
        await self.db.commit()

        return schema

    async def get_schema(
        self, event_type: str, schema_version: str = None
    ) -> Optional[EventSchema]:
        """Get schema for event type.

        If schema_version not specified, returns active version.
        """
        if schema_version:
            result = await self.db.execute(
                select(EventSchema).where(
                    (EventSchema.event_type == event_type)
                    & (EventSchema.schema_version == schema_version)
                )
            )
        else:
            # Get active schema
            result = await self.db.execute(
                select(EventSchema).where(
                    (EventSchema.event_type == event_type)
                    & (EventSchema.is_active == True)
                    & (EventSchema.deprecated == False)
                )
            )

        return result.scalar_one_or_none()

    async def validate_event(
        self,
        event_type: str,
        event_payload: Dict[str, Any],
        schema_version: str = None,
    ) -> Dict[str, Any]:
        """Validate event against schema.

        Args:
            event_type: Event type
            event_payload: Event data to validate
            schema_version: Specific version to validate against (optional)

        Returns:
            Validation result with success/errors

        Raises:
            ValidationError if event doesn't match schema
        """
        schema = await self.get_schema(event_type, schema_version)

        if not schema:
            raise ValueError(
                f"No schema found for {event_type} "
                f"(version: {schema_version or 'latest'})"
            )

        # Validate against JSON Schema
        validator = Draft7Validator(schema.json_schema)
        errors = list(validator.iter_errors(event_payload))

        if errors:
            error_details = [
                f"{e.path}: {e.message}" for e in errors
            ]
            raise ValidationError(
                f"Event validation failed for {event_type}: {', '.join(error_details)}"
            )

        return {
            "valid": True,
            "event_type": event_type,
            "schema_version": schema.schema_version,
        }

    async def get_schema_versions(self, event_type: str) -> List[Dict[str, Any]]:
        """Get all versions of a schema."""
        result = await self.db.execute(
            select(EventSchema)
            .where(EventSchema.event_type == event_type)
            .order_by(EventSchema.created_at.desc())
        )
        schemas = result.scalars().all()

        return [
            {
                "schema_version": s.schema_version,
                "is_active": s.is_active,
                "deprecated": s.deprecated,
                "breaking_changes": s.breaking_changes,
                "created_at": s.created_at.isoformat(),
            }
            for s in schemas
        ]

    async def deprecate_schema(self, event_type: str, schema_version: str) -> EventSchema:
        """Mark schema as deprecated (stop creating new events with it)."""
        result = await self.db.execute(
            select(EventSchema).where(
                (EventSchema.event_type == event_type)
                & (EventSchema.schema_version == schema_version)
            )
        )
        schema = result.scalar_one_or_none()

        if not schema:
            raise ValueError(f"Schema {event_type}:{schema_version} not found")

        schema.deprecated = True
        schema.deprecated_at = datetime.now(timezone.utc)
        schema.is_active = False
        await self.db.commit()

        return schema


class BackwardCompatibilityChecker:
    """Verify schema evolution is backward-compatible."""

    @staticmethod
    def check_compatibility(
        old_schema: Dict[str, Any],
        new_schema: Dict[str, Any],
        mode: CompatibilityMode = CompatibilityMode.BACKWARD,
    ) -> Dict[str, Any]:
        """Check if new schema is compatible with old.

        Mode BACKWARD: All valid old events must be valid for new schema
        Mode FORWARD: All valid new events must be valid for old schema
        Mode FULL: Both directions

        Returns:
            {
                "compatible": bool,
                "violations": [list of breaking changes],
                "safe_to_deploy": bool
            }
        """
        violations = []

        # Check required fields
        old_required = set(old_schema.get("required", []))
        new_required = set(new_schema.get("required", []))

        # BACKWARD: Can't make fields required (old events won't have them)
        if mode in (CompatibilityMode.BACKWARD, CompatibilityMode.FULL):
            new_required_fields = new_required - old_required
            if new_required_fields:
                violations.append(
                    f"BREAKING: New required fields {new_required_fields} "
                    "(old events won't have these)"
                )

        # Check field removals
        old_props = set(old_schema.get("properties", {}).keys())
        new_props = set(new_schema.get("properties", {}).keys())

        # BACKWARD: Can't remove fields (old events have them)
        if mode in (CompatibilityMode.BACKWARD, CompatibilityMode.FULL):
            removed = old_props - new_props
            if removed:
                violations.append(
                    f"BREAKING: Removed fields {removed} (old events have these)"
                )

        # FORWARD: Can't remove optional fields that new code expects
        if mode in (CompatibilityMode.FORWARD, CompatibilityMode.FULL):
            # Only check if new schema lists them as properties
            if removed:
                violations.append(
                    f"BREAKING: Removed fields {removed} (new schema expects them)"
                )

        # Check type changes (simplified: just check if types changed)
        old_field_types = {
            k: v.get("type") for k, v in old_schema.get("properties", {}).items()
        }
        new_field_types = {
            k: v.get("type") for k, v in new_schema.get("properties", {}).items()
        }

        # BACKWARD: Can't change field types (old events have old type)
        if mode in (CompatibilityMode.BACKWARD, CompatibilityMode.FULL):
            for field, old_type in old_field_types.items():
                new_type = new_field_types.get(field)
                if new_type and old_type != new_type:
                    violations.append(
                        f"BREAKING: Field '{field}' type changed "
                        f"{old_type} → {new_type}"
                    )

        safe = len(violations) == 0

        return {
            "compatible": safe,
            "violations": violations,
            "safe_to_deploy": safe,
            "mode": mode.value,
        }


class SchemaEvolutionValidator:
    """Validate that event schema evolution follows rules."""

    ALLOWED_ADDITIONS = [
        "Add optional field",
        "Widen type constraint",
        "Loosen regex pattern",
        "Increase number limit",
    ]

    FORBIDDEN_CHANGES = [
        "Remove field",
        "Make field required",
        "Narrow type constraint",
        "Tighten regex pattern",
        "Change field meaning",
        "Remove enum value",
    ]

    @staticmethod
    def document_breaking_changes(
        old_schema_version: str,
        new_schema_version: str,
        changes: List[str],
    ) -> Dict[str, Any]:
        """Document breaking changes for schema evolution.

        Changes should be from ALLOWED_ADDITIONS list (safe) or
        FORBIDDEN_CHANGES list (require explicit approval).
        """
        breaking = [c for c in changes if c in SchemaEvolutionValidator.FORBIDDEN_CHANGES]
        allowed = [c for c in changes if c in SchemaEvolutionValidator.ALLOWED_ADDITIONS]

        return {
            "old_version": old_schema_version,
            "new_version": new_schema_version,
            "breaking_changes": breaking,
            "safe_changes": allowed,
            "requires_approval": len(breaking) > 0,
            "changes": changes,
        }
