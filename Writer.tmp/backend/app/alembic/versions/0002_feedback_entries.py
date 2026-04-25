"""add writer feedback entries table

Revision ID: 0002_feedback_entries
Revises: 0001_initial
Create Date: 2026-04-22
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_feedback_entries"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "feedback_entries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("org_id", sa.String(length=128), nullable=True),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("area", sa.String(length=64), nullable=False),
        sa.Column("page", sa.String(length=255), nullable=True),
        sa.Column("message", sa.String(length=2000), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_feedback_entries_workspace_id", "feedback_entries", ["workspace_id"], unique=False)
    op.create_index(
        "ix_feedback_entries_workspace_created_at",
        "feedback_entries",
        ["workspace_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_feedback_entries_workspace_area",
        "feedback_entries",
        ["workspace_id", "area"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_feedback_entries_workspace_area", table_name="feedback_entries")
    op.drop_index("ix_feedback_entries_workspace_created_at", table_name="feedback_entries")
    op.drop_index("ix_feedback_entries_workspace_id", table_name="feedback_entries")
    op.drop_table("feedback_entries")
