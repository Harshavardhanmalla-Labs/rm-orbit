"""init_dock

Revision ID: f5f164f1d072
Revises: 
Create Date: 2026-03-12 02:51:51.788179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5f164f1d072'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS dock_apps (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            name TEXT NOT NULL,
            vendor TEXT DEFAULT '',
            description TEXT DEFAULT '',
            url TEXT,
            advertised BOOLEAN DEFAULT TRUE,
            license_model TEXT DEFAULT 'per_user',
            integrations JSONB DEFAULT '[]',
            created_by TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS dock_licenses (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            app_id TEXT NOT NULL REFERENCES dock_apps(id) ON DELETE CASCADE,
            seats_purchased INTEGER DEFAULT 1,
            seats_assigned INTEGER DEFAULT 0,
            currency TEXT DEFAULT 'USD',
            total_cost FLOAT DEFAULT 0.0,
            renewal_date TEXT,
            purchased_by TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS dock_assignments (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            app_id TEXT NOT NULL REFERENCES dock_apps(id) ON DELETE CASCADE,
            user_id TEXT NOT NULL,
            access_level TEXT DEFAULT 'user',
            status TEXT DEFAULT 'active',
            assigned_by TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS dock_requests (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            requester_user_id TEXT NOT NULL,
            app_name TEXT NOT NULL,
            reason TEXT NOT NULL,
            requested_seats INTEGER DEFAULT 1,
            business_justification TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            reviewer_user_id TEXT,
            review_notes TEXT,
            linked_app_id TEXT,
            automation_ticket_id TEXT,
            automation_status TEXT DEFAULT 'idle',
            automation_last_error TEXT,
            automation_hint TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS dock_packages (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            version TEXT NOT NULL,
            s3_key TEXT NOT NULL,
            size_bytes BIGINT NOT NULL DEFAULT 0,
            checksum TEXT DEFAULT '',
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS dock_audit_events (
            id TEXT PRIMARY KEY,
            event_type TEXT NOT NULL,
            org_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            resource_id TEXT NOT NULL,
            request_id TEXT NOT NULL,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            metadata_json JSONB DEFAULT '{}'
        );

        CREATE INDEX IF NOT EXISTS idx_dock_packages_org ON dock_packages(org_id);
        CREATE INDEX IF NOT EXISTS idx_dock_apps_org ON dock_apps(org_id);
        CREATE INDEX IF NOT EXISTS idx_dock_assignments_user ON dock_assignments(user_id, org_id);
    """)

def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS dock_audit_events;
        DROP TABLE IF EXISTS dock_packages;
        DROP TABLE IF EXISTS dock_requests;
        DROP TABLE IF EXISTS dock_assignments;
        DROP TABLE IF EXISTS dock_licenses;
        DROP TABLE IF EXISTS dock_apps;
    """)
