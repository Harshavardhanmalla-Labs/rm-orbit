"""System 6.5: Guardrail enforcement — blocks, escalates, or requires consensus."""
from __future__ import annotations

import json
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import (
    DecisionGuardrail, GuardrailViolation, DecisionInfluenceRecord
)


class GuardrailEnforcementEngine:
    """Evaluates active guardrails and enforces their actions on influence records."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def setup_default_guardrails(self, tenant_id: UUID) -> None:
        """Create default guardrails for a tenant if none exist."""
        existing = await self.db.scalar(
            select(DecisionGuardrail).where(DecisionGuardrail.tenant_id == tenant_id)
        )
        if existing:
            return

        defaults = [
            DecisionGuardrail(
                tenant_id=tenant_id,
                guardrail_name="minimum_confidence_threshold",
                guardrail_type="threshold",
                rule_definition=json.dumps({"field": "confidence", "operator": "<", "value": 0.3}),
                action_on_violation="block",
                severity="critical",
            ),
            DecisionGuardrail(
                tenant_id=tenant_id,
                guardrail_name="critical_risk_block",
                guardrail_type="pattern_block",
                rule_definition=json.dumps({"risk_level": "critical"}),
                action_on_violation="block",
                severity="critical",
            ),
            DecisionGuardrail(
                tenant_id=tenant_id,
                guardrail_name="high_risk_consensus",
                guardrail_type="consensus_required",
                rule_definition=json.dumps({"risk_level": "high"}),
                action_on_violation="require_consensus",
                severity="high",
            ),
        ]
        for g in defaults:
            self.db.add(g)
        await self.db.flush()

    async def check_guardrails(
        self,
        tenant_id: UUID,
        decision_id: UUID,
        predicted_confidence: float,
        risk_level: str,
        role_id: UUID,
    ) -> DecisionInfluenceRecord:
        influence = await self.db.scalar(
            select(DecisionInfluenceRecord).where(
                DecisionInfluenceRecord.decision_id == decision_id,
                DecisionInfluenceRecord.tenant_id == tenant_id,
            )
        )
        if not influence:
            influence = DecisionInfluenceRecord(
                tenant_id=tenant_id,
                decision_id=decision_id,
                original_confidence=predicted_confidence,
                adjusted_confidence=predicted_confidence,
            )
            self.db.add(influence)

        guardrails = (await self.db.execute(
            select(DecisionGuardrail).where(
                DecisionGuardrail.tenant_id == tenant_id,
                DecisionGuardrail.enabled == True,
            )
        )).scalars().all()

        for g in guardrails:
            violated, desc = self._evaluate(g, predicted_confidence, risk_level)
            if not violated:
                continue

            g.violations_count = (g.violations_count or 0) + 1
            violation = GuardrailViolation(
                tenant_id=tenant_id,
                decision_id=decision_id,
                guardrail_id=g.id,
                violation_description=desc,
            )
            self.db.add(violation)

            if g.action_on_violation == "block":
                influence.is_blocked = True
                influence.block_reason = f"{g.guardrail_name}: {desc}"
                violation.action_taken = "blocked"
            elif g.action_on_violation == "escalate":
                influence.requires_additional_review = True
                violation.action_taken = "escalated"
            elif g.action_on_violation == "require_consensus":
                influence.requires_multi_role_consensus = True
                violation.action_taken = "consensus_required"

        influence.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return influence

    def _evaluate(
        self, g: DecisionGuardrail, confidence: float, risk_level: str
    ) -> tuple[bool, str]:
        try:
            rule = json.loads(g.rule_definition)
        except (json.JSONDecodeError, TypeError):
            return False, ""

        if g.guardrail_type == "threshold":
            field = rule.get("field")
            op = rule.get("operator")
            val = rule.get("value")
            if field == "confidence" and op == "<" and confidence < val:
                return True, f"Confidence {confidence:.2f} below threshold {val}"

        elif g.guardrail_type == "pattern_block":
            if risk_level == "critical":
                return True, f"Critical risk level triggers block"

        elif g.guardrail_type == "consensus_required":
            if risk_level in ("high", "critical"):
                return True, f"Risk level '{risk_level}' requires multi-role consensus"

        return False, ""
