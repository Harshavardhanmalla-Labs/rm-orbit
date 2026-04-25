"""Domain models for AgentTheatre."""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import Column, String, DateTime, Text, JSON, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""
    pass


class Decision(Base):
    """Decision record."""

    __tablename__ = "decisions"

    id = Column(PG_UUID, primary_key=True, default=uuid4)
    project_id = Column(PG_UUID, nullable=False, index=True)
    question = Column(String(500), nullable=False)
    roles = Column(JSON, nullable=False)  # List of required roles
    outcome = Column(String(50))  # succeeded | failed | pivoted | abandoned
    note = Column(Text)

    tenant_id = Column(PG_UUID, nullable=False, index=True)
    created_by = Column(PG_UUID, nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_decisions_tenant_created", "tenant_id", "created_at"),
    )


class GithubIssue(Base):
    """GitHub issue linked to decision."""

    __tablename__ = "github_issues"

    id = Column(PG_UUID, primary_key=True, default=uuid4)
    decision_id = Column(PG_UUID, nullable=False, index=True)
    repo = Column(String(100), nullable=False)
    issue_id = Column(String(50), nullable=False)
    url = Column(String(500), nullable=False)

    tenant_id = Column(PG_UUID, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_github_issues_decision", "decision_id"),
    )
