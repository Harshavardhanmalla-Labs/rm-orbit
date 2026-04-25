"""add_budget_and_procurement_policies

Revision ID: 37fec8f797a3
Revises: f5f164f1d072
Create Date: 2026-03-12 21:35:44.299016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "37fec8f797a3"
down_revision: Union[str, None] = "f5f164f1d072"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dock_budget_policies",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("org_id", sa.String(), nullable=False),
        sa.Column("department_id", sa.String(), nullable=True),
        sa.Column("monthly_limit", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False, server_default="USD"),
        sa.Column("alert_threshold_pct", sa.Float(), nullable=False, server_default="80"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dock_budget_policies_department_id"), "dock_budget_policies", ["department_id"], unique=False)
    op.create_index(op.f("ix_dock_budget_policies_org_id"), "dock_budget_policies", ["org_id"], unique=False)

    op.create_table(
        "dock_procurement_configs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("org_id", sa.String(), nullable=False),
        sa.Column("require_manager_approval", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("auto_approve_threshold", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dock_procurement_configs_org_id"), "dock_procurement_configs", ["org_id"], unique=True)

    op.add_column(
        "dock_licenses",
        sa.Column("status", sa.String(), nullable=False, server_default=sa.text("'active'")),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_dock_licenses_org_id ON dock_licenses(org_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_dock_licenses_org_id")
    op.drop_column("dock_licenses", "status")

    op.drop_index(op.f("ix_dock_procurement_configs_org_id"), table_name="dock_procurement_configs")
    op.drop_table("dock_procurement_configs")

    op.drop_index(op.f("ix_dock_budget_policies_org_id"), table_name="dock_budget_policies")
    op.drop_index(op.f("ix_dock_budget_policies_department_id"), table_name="dock_budget_policies")
    op.drop_table("dock_budget_policies")
