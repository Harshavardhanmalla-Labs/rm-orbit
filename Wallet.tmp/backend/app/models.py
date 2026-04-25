import uuid
from sqlalchemy import Column, String, DateTime, Integer, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


JSON_TYPE = JSON().with_variant(JSONB(), "postgresql")


class Vault(Base):
    __tablename__ = "vaults"
    __table_args__ = (
        Index("ix_wallet_vaults_org_created", "org_id", "created_at"),
    )

    id = Column(String, primary_key=True, default=lambda: f"rwv-{uuid.uuid4().hex[:10]}")
    org_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    owner_team = Column(String, nullable=True)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    secrets = relationship("Secret", back_populates="vault")

class Secret(Base):
    __tablename__ = "secrets"
    __table_args__ = (
        Index("ix_wallet_secrets_org_project", "org_id", "project"),
        Index("ix_wallet_secrets_org_vault", "org_id", "vault_id"),
    )

    id = Column(String, primary_key=True, default=lambda: f"rw-{uuid.uuid4().hex[:12]}")
    org_id = Column(String, nullable=False, index=True)
    vault_id = Column(String, ForeignKey("vaults.id"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    secret_type = Column(String, default="api_key")
    project = Column(String, nullable=True)
    tags = Column(JSON_TYPE, default=list)
    owner_user_id = Column(String, nullable=False)
    encrypted_value = Column(String, nullable=False)
    iv_material = Column(String, default="static_fernet")
    shares = Column(JSON_TYPE, default=list) # List of SecretShareRecord dicts
    rotation_interval_days = Column(Integer, default=90)
    last_rotated_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    last_revealed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    vault = relationship("Vault", back_populates="secrets")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_wallet_audit_org_timestamp", "org_id", "timestamp"),
    )

    id = Column(String, primary_key=True, default=lambda: f"rwa-{uuid.uuid4().hex[:10]}")
    org_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False)
    role = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ip_address = Column(String, nullable=True)
    metadata_json = Column(JSON_TYPE, default=dict)

class SharedInfo(Base):
    __tablename__ = "shared_info"
    __table_args__ = (
        Index("ix_wallet_shared_info_org_category", "org_id", "category"),
    )

    id = Column(String, primary_key=True, default=lambda: f"rwsi-{uuid.uuid4().hex[:10]}")
    org_id = Column(String, default="*", index=True)
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)
    value = Column(String, nullable=False)
    environment = Column(String, nullable=True)
    owner_team = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    tags = Column(JSON_TYPE, default=list)
    source = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
