"""init_wallet

Revision ID: 1c7e78015c1e
Revises: 
Create Date: 2026-03-12 02:51:21.119675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c7e78015c1e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id UUID PRIMARY KEY,
            org_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            encrypted_value TEXT NOT NULL,
            iv_material TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_secrets_org ON secrets(org_id);
    """)

def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS secrets;")
