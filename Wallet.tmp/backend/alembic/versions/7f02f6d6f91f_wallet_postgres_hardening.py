"""wallet_postgres_hardening

Revision ID: 7f02f6d6f91f
Revises: 1c7e78015c1e
Create Date: 2026-03-12 22:05:00.000000
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "7f02f6d6f91f"
down_revision: Union[str, None] = "1c7e78015c1e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS vaults (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            owner_team TEXT,
            created_by TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            action TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            resource_id TEXT NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            ip_address TEXT,
            metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb
        );

        CREATE TABLE IF NOT EXISTS shared_info (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL DEFAULT '*',
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            value TEXT NOT NULL,
            environment TEXT,
            owner_team TEXT,
            notes TEXT,
            tags JSONB NOT NULL DEFAULT '[]'::jsonb,
            source TEXT,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS secrets (
            id TEXT PRIMARY KEY,
            org_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            encrypted_value TEXT NOT NULL,
            iv_material TEXT NOT NULL DEFAULT 'static_fernet',
            vault_id TEXT,
            secret_type TEXT NOT NULL DEFAULT 'api_key',
            project TEXT,
            tags JSONB NOT NULL DEFAULT '[]'::jsonb,
            owner_user_id TEXT NOT NULL DEFAULT 'system',
            shares JSONB NOT NULL DEFAULT '[]'::jsonb,
            rotation_interval_days INTEGER NOT NULL DEFAULT 90,
            last_rotated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            expires_at TIMESTAMPTZ,
            last_revealed_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )

    op.execute(
        """
        ALTER TABLE secrets ALTER COLUMN id TYPE TEXT USING id::text;
        ALTER TABLE secrets ALTER COLUMN org_id TYPE TEXT;
        ALTER TABLE secrets ALTER COLUMN name TYPE TEXT;
        ALTER TABLE secrets ALTER COLUMN description TYPE TEXT;
        ALTER TABLE secrets ALTER COLUMN encrypted_value TYPE TEXT;
        ALTER TABLE secrets ALTER COLUMN iv_material TYPE TEXT;

        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS vault_id TEXT;
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS secret_type TEXT NOT NULL DEFAULT 'api_key';
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS project TEXT;
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS tags JSONB NOT NULL DEFAULT '[]'::jsonb;
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS owner_user_id TEXT NOT NULL DEFAULT 'system';
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS shares JSONB NOT NULL DEFAULT '[]'::jsonb;
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS rotation_interval_days INTEGER NOT NULL DEFAULT 90;
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS last_rotated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS expires_at TIMESTAMPTZ;
        ALTER TABLE secrets ADD COLUMN IF NOT EXISTS last_revealed_at TIMESTAMPTZ;

        ALTER TABLE secrets ALTER COLUMN tags TYPE JSONB USING
            CASE WHEN tags IS NULL THEN '[]'::jsonb ELSE tags::jsonb END;
        ALTER TABLE secrets ALTER COLUMN shares TYPE JSONB USING
            CASE WHEN shares IS NULL THEN '[]'::jsonb ELSE shares::jsonb END;
        """
    )

    op.execute(
        """
        ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb;
        ALTER TABLE audit_logs ALTER COLUMN metadata_json TYPE JSONB USING
            CASE WHEN metadata_json IS NULL THEN '{}'::jsonb ELSE metadata_json::jsonb END;

        ALTER TABLE shared_info ADD COLUMN IF NOT EXISTS tags JSONB NOT NULL DEFAULT '[]'::jsonb;
        ALTER TABLE shared_info ALTER COLUMN tags TYPE JSONB USING
            CASE WHEN tags IS NULL THEN '[]'::jsonb ELSE tags::jsonb END;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'fk_wallet_secrets_vault_id'
            ) THEN
                ALTER TABLE secrets
                ADD CONSTRAINT fk_wallet_secrets_vault_id
                FOREIGN KEY (vault_id) REFERENCES vaults(id) ON DELETE SET NULL;
            END IF;
        END $$;
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_wallet_vaults_org_created ON vaults(org_id, created_at);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_wallet_secrets_org ON secrets(org_id);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_wallet_secrets_org_project ON secrets(org_id, project);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_wallet_secrets_org_vault ON secrets(org_id, vault_id);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_wallet_audit_org_timestamp ON audit_logs(org_id, timestamp);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_wallet_shared_info_org_category ON shared_info(org_id, category);")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_wallet_shared_info_org_category;")
    op.execute("DROP INDEX IF EXISTS ix_wallet_audit_org_timestamp;")
    op.execute("DROP INDEX IF EXISTS ix_wallet_secrets_org_vault;")
    op.execute("DROP INDEX IF EXISTS ix_wallet_secrets_org_project;")
    op.execute("DROP INDEX IF EXISTS ix_wallet_secrets_org;")
    op.execute("DROP INDEX IF EXISTS ix_wallet_vaults_org_created;")
    op.execute("ALTER TABLE secrets DROP CONSTRAINT IF EXISTS fk_wallet_secrets_vault_id;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS vault_id;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS secret_type;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS project;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS tags;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS owner_user_id;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS shares;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS rotation_interval_days;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS last_rotated_at;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS expires_at;")
    op.execute("ALTER TABLE secrets DROP COLUMN IF EXISTS last_revealed_at;")
    op.execute("DROP TABLE IF EXISTS shared_info;")
    op.execute("DROP TABLE IF EXISTS audit_logs;")
    op.execute("DROP TABLE IF EXISTS vaults;")
