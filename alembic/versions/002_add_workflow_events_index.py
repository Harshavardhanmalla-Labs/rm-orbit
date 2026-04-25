"""Add index for idempotency check performance

Revision ID: 002
Revises: 001
Create Date: 2026-04-25 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create index for idempotency checks
    # Idempotency check query:
    # SELECT * FROM workflow_events
    # WHERE paper_id=? AND stage=? AND event='completed'
    # ORDER BY created_at DESC LIMIT 1
    op.create_index(
        'idx_workflow_events_lookup',
        'workflow_events',
        ['paper_id', 'stage', 'event', sa.desc('created_at')],
        postgresql_using='btree'
    )


def downgrade() -> None:
    op.drop_index('idx_workflow_events_lookup', table_name='workflow_events')
