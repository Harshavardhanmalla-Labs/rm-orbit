"""System 6: Confidence calibration — expected vs actual success rate per confidence band."""
from __future__ import annotations

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from AgentTheater.events.db_models import ConfidenceCalibration, DecisionAccuracy


BANDS = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.01)]


class ConfidenceCalibrationEngine:
    """Calibrates confidence predictions against actual outcomes across bands."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def calibrate_for_role(
        self, tenant_id: UUID, role_id: UUID
    ) -> list[ConfidenceCalibration]:
        rows = (await self.db.execute(
            select(DecisionAccuracy).where(
                DecisionAccuracy.tenant_id == tenant_id,
                DecisionAccuracy.role_id == role_id,
                DecisionAccuracy.is_correct.isnot(None),
            )
        )).scalars().all()

        results = []
        for low, high in BANDS:
            in_band = [a for a in rows if low <= a.predicted_confidence < high]
            if not in_band:
                continue

            cal = await self.db.scalar(
                select(ConfidenceCalibration).where(
                    ConfidenceCalibration.tenant_id == tenant_id,
                    ConfidenceCalibration.role_id == role_id,
                    ConfidenceCalibration.confidence_band_low == low,
                    ConfidenceCalibration.confidence_band_high == high,
                )
            )
            if not cal:
                cal = ConfidenceCalibration(
                    tenant_id=tenant_id,
                    role_id=role_id,
                    confidence_band_low=low,
                    confidence_band_high=min(high, 1.0),
                )
                self.db.add(cal)

            cal.predictions_in_band = len(in_band)
            cal.successes_in_band = sum(1 for a in in_band if a.is_correct)
            cal.expected_success_rate = (low + min(high, 1.0)) / 2.0
            cal.actual_success_rate = cal.successes_in_band / cal.predictions_in_band
            cal.calibration_error = abs(cal.expected_success_rate - cal.actual_success_rate)
            if cal.expected_success_rate > 0:
                cal.adjustment_factor = cal.actual_success_rate / cal.expected_success_rate
            else:
                cal.adjustment_factor = 1.0

            if cal.calibration_error > 0.15:
                direction = "underconfident" if cal.actual_success_rate > cal.expected_success_rate else "overconfident"
                cal.recommendation = (
                    f"Role is {direction} in band {low:.1f}-{min(high, 1.0):.1f}. "
                    f"Multiply confidence by {cal.adjustment_factor:.2f}."
                )
            else:
                cal.recommendation = "Well-calibrated in this band."

            await self.db.flush()
            results.append(cal)

        return results
