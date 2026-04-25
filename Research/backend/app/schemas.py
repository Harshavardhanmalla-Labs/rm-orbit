from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class PaperType(str, Enum):
    original_research = "original_research"
    survey = "survey"
    case_study = "case_study"
    technical_report = "technical_report"
    position_paper = "position_paper"


class TargetVenue(str, Enum):
    ieee = "ieee"
    acm = "acm"
    arxiv = "arxiv"
    nature = "nature"
    springer = "springer"
    custom = "custom"


class PaperCreate(BaseModel):
    topic: str
    niche: str = ""
    paper_type: PaperType = PaperType.original_research
    target_venue: TargetVenue = TargetVenue.arxiv
    author_name: str
    author_affiliation: str = ""
    word_count_target: int = Field(default=8000, ge=2000, le=30000)


class PaperListItem(BaseModel):
    id: str
    title: Optional[str]
    topic: str
    target_venue: str
    paper_type: str
    status: str
    current_stage: str
    stage_progress: float
    created_at: str


class PipelineStatus(BaseModel):
    paper_id: str
    status: str
    current_stage: str
    stage_progress: float
    message: str = ""
    error_message: Optional[str] = None
