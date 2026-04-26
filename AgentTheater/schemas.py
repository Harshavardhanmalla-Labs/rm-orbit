"""Pydantic schemas for API requests/responses."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class DecisionCreateRequest(BaseModel):
    """Request to create a decision."""

    project_id: UUID
    question: str = Field(..., min_length=10, max_length=500)
    roles: List[str] = Field(..., min_length=1)
    tenant_id: UUID


class DecisionCreateResponse(BaseModel):
    """Response when decision created."""

    id: UUID
    question: str
    roles: List[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DecisionRecordResponse(BaseModel):
    """Response for decision details."""

    id: UUID
    question: str
    roles: List[str]
    outcome: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OutcomeRequest(BaseModel):
    """Request to record decision outcome."""

    outcome: str = Field(..., pattern="^(succeeded|failed|pivoted|abandoned)$")
    note: Optional[str] = None


class GithubIssueRequest(BaseModel):
    """Request to add GitHub issue."""

    repo: str = Field(..., min_length=1)
    issue_id: int
    url: str


class GithubIssuesRequest(BaseModel):
    """Request to create multiple GitHub issues."""

    urls: List[str] = Field(default_factory=list)


class ListDecisionsResponse(BaseModel):
    """Response for list decisions."""

    items: List[DecisionRecordResponse]
    total: int


# System 3: Decision Accountability Schemas
class DecisionRationaleRequest(BaseModel):
    """Request to add rationale to decision."""

    role: str = Field(..., min_length=1, max_length=50)
    reasoning: str = Field(..., min_length=10, max_length=5000)


class DecisionRationaleResponse(BaseModel):
    """Response for decision rationale."""

    id: UUID
    decision_id: UUID
    role: str
    reasoning: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DecisionConfidenceRequest(BaseModel):
    """Request to score decision confidence."""

    technical_confidence: float = Field(..., ge=0, le=100)
    market_confidence: float = Field(..., ge=0, le=100)
    team_confidence: float = Field(..., ge=0, le=100)
    reasoning: Optional[str] = Field(None, max_length=1000)


class DecisionConfidenceResponse(BaseModel):
    """Response for decision confidence."""

    id: UUID
    decision_id: UUID
    technical_confidence: float
    market_confidence: float
    team_confidence: float
    overall_confidence: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RiskAssessmentRequest(BaseModel):
    """Request to assess decision risk."""

    technical_risk: float = Field(..., ge=0, le=10)
    market_risk: float = Field(..., ge=0, le=10)
    financial_risk: float = Field(..., ge=0, le=10)
    team_risk: float = Field(..., ge=0, le=10)
    contingency: Optional[str] = Field(None, max_length=2000)


class RiskAssessmentResponse(BaseModel):
    """Response for risk assessment."""

    id: UUID
    decision_id: UUID
    technical_risk: float
    market_risk: float
    financial_risk: float
    team_risk: float
    overall_risk: float
    contingency: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DecisionStateTransitionRequest(BaseModel):
    """Request to transition decision state."""

    to_state: str = Field(..., pattern="^(ideation|planning|execution|review|completed|abandoned)$")
    reason: Optional[str] = Field(None, max_length=1000)


class DecisionReadModelResponse(BaseModel):
    """Read model response optimized for UI."""

    id: UUID
    decision_id: UUID
    question: str
    current_state: str
    current_version: int
    overall_confidence: Optional[float]
    overall_risk: Optional[float]
    rationale_count: int
    confidence_count: int
    risk_count: int
    last_activity_at: Optional[datetime]
    created_at: datetime
    # Extended fields
    project_id: Optional[UUID] = None
    owner_id: Optional[UUID] = None
    is_blocked: bool = False
    block_reason: Optional[str] = None
    execution_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class DecisionReadModelListResponse(BaseModel):
    """Paginated list of decision read models."""

    items: List[DecisionReadModelResponse]
    total: int
    limit: int
    offset: int


# System 4: Decision Execution & Outcome Tracker

class ExecutionCreateRequest(BaseModel):
    """Request to create execution."""

    decision_id: UUID
    predicted_outcome: Optional[str] = Field(None, pattern="^(succeeded|failed|pivoted)$")


class ExecutionResponse(BaseModel):
    """Response for execution details."""

    id: UUID
    decision_id: UUID
    state: str
    assigned_to: Optional[UUID] = None
    predicted_outcome: Optional[str]
    actual_outcome: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExecutionArtifactRequest(BaseModel):
    """Request to link artifact to execution."""

    artifact_type: str = Field(..., pattern="^(github_issue|github_pr|task|doc|deployment)$")
    artifact_id: str = Field(..., min_length=1, max_length=100)
    artifact_url: Optional[str] = Field(None, max_length=500)
    artifact_title: Optional[str] = Field(None, max_length=500)


class ExecutionArtifactResponse(BaseModel):
    """Response for artifact linkage."""

    id: UUID
    execution_id: UUID
    artifact_type: str
    artifact_id: str
    artifact_url: Optional[str]
    artifact_title: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExecutionAssignRequest(BaseModel):
    """Request to assign execution."""

    assigned_to: UUID


class ExecutionStateTransitionRequest(BaseModel):
    """Request to transition execution state."""

    to_state: str = Field(..., pattern="^(approved|assigned|in_progress|blocked|completed|succeeded|failed|pivoted)$")
    reason: Optional[str] = Field(None, max_length=1000)
    blocked_reason: Optional[str] = Field(None, max_length=1000)


class OutcomeRecordRequest(BaseModel):
    """Request to record execution outcome."""

    actual_outcome: str = Field(..., pattern="^(succeeded|failed|pivoted|abandoned)$")
    success_metrics: Optional[dict] = None
    failure_reason: Optional[str] = None
    lessons_learned: Optional[str] = None


class OutcomeRecordResponse(BaseModel):
    """Response for recorded outcome."""

    id: UUID
    execution_id: UUID
    predicted_outcome: str
    actual_outcome: str
    validated: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExecutionReadModelResponse(BaseModel):
    """Read model for execution dashboard."""

    id: UUID
    execution_id: UUID
    decision_id: UUID
    decision_question: str
    state: str
    assigned_to: Optional[UUID]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    age_days: Optional[int]
    github_issues_count: int
    github_prs_count: int
    tasks_count: int
    docs_count: int
    deployments_count: int
    predicted_outcome: Optional[str]
    actual_outcome: Optional[str]
    outcome_validated: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
