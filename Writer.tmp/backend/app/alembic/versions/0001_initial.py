"""initial writer schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-03-02
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("root_block_id", sa.String(length=36), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_workspace_id", "documents", ["workspace_id"], unique=False)
    op.create_index(
        "ix_documents_workspace_updated_at",
        "documents",
        ["workspace_id", "updated_at"],
        unique=False,
    )

    op.create_table(
        "blocks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("parent_block_id", sa.String(length=36), nullable=True),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("content", sa.JSON(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("position_index", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_block_id"], ["blocks.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_blocks_document_id", "blocks", ["document_id"], unique=False)
    op.create_index(
        "ix_blocks_document_parent_position",
        "blocks",
        ["document_id", "parent_block_id", "position_index"],
        unique=False,
    )

    op.create_table(
        "block_relations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("document_id", sa.String(length=36), nullable=False),
        sa.Column("source_block_id", sa.String(length=36), nullable=False),
        sa.Column("target_block_id", sa.String(length=36), nullable=False),
        sa.Column("relation_type", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_block_id"], ["blocks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_block_id"], ["blocks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_block_relations_document_id", "block_relations", ["document_id"], unique=False)
    op.create_index(
        "ix_block_relations_document_relation_type",
        "block_relations",
        ["document_id", "relation_type"],
        unique=False,
    )
    op.create_index("ix_block_relations_source_block_id", "block_relations", ["source_block_id"], unique=False)
    op.create_index("ix_block_relations_target_block_id", "block_relations", ["target_block_id"], unique=False)
    op.create_index(
        "ix_block_relations_unique",
        "block_relations",
        ["source_block_id", "target_block_id", "relation_type"],
        unique=True,
    )

    op.create_table(
        "block_versions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("block_id", sa.String(length=36), nullable=False),
        sa.Column("snapshot", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["block_id"], ["blocks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_block_versions_block_id", "block_versions", ["block_id"], unique=False)
    op.create_index(
        "ix_block_versions_block_created_at",
        "block_versions",
        ["block_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_block_versions_block_created_at", table_name="block_versions")
    op.drop_index("ix_block_versions_block_id", table_name="block_versions")
    op.drop_table("block_versions")

    op.drop_index("ix_block_relations_unique", table_name="block_relations")
    op.drop_index("ix_block_relations_target_block_id", table_name="block_relations")
    op.drop_index("ix_block_relations_source_block_id", table_name="block_relations")
    op.drop_index("ix_block_relations_document_relation_type", table_name="block_relations")
    op.drop_index("ix_block_relations_document_id", table_name="block_relations")
    op.drop_table("block_relations")

    op.drop_index("ix_blocks_document_parent_position", table_name="blocks")
    op.drop_index("ix_blocks_document_id", table_name="blocks")
    op.drop_table("blocks")

    op.drop_index("ix_documents_workspace_updated_at", table_name="documents")
    op.drop_index("ix_documents_workspace_id", table_name="documents")
    op.drop_table("documents")
