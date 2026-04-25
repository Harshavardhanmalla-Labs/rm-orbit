"""Pydantic schemas for API requests/responses."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, Field


class DecisionCreateRequest(BaseModel):
    """Request to create a decision."""

    project_id: UUID
    question: str = Field(..., min_length=10, max_length=500)
    roles: List[str] = Field(..., min_items=1)
    tenant_id: UUID


class DecisionCreateResponse(BaseModel):
    """Response when decision created."""

    id: UUID
    question: str
    roles: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DecisionRecordResponse(BaseModel):
    """Response for decision details."""

    id: UUID
    question: str
    roles: List[str]
    outcome: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OutcomeRequest(BaseModel):
    """Request to record decision outcome."""

    outcome: str = Field(..., pattern="^(succeeded|failed|pivoted|abandoned)$")
    note: Optional[str] = None


class GithubIssueRequest(BaseModel):
    """Request to add GitHub issue."""

    repo: str = Field(..., min_length=1)
    issue_id: int
    url: str


class ListDecisionsResponse(BaseModel):
    """Response for list decisions."""

    items: List[DecisionRecordResponse]
    total: int
