from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


BlockType = Literal[
    "text",
    "table",
    "chart",
    "slide",
    "code",
    "sticky",
    "ai",
    "heading1",
    "heading2",
    "heading3",
    "quote",
    "bullet",
    "numbered",
    "divider",
]


class HealthResponse(BaseModel):
    status: str
    service: str
    database_url: str


class FeedbackCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    area: str = Field(min_length=1, max_length=64)
    message: str | None = Field(default=None, max_length=2000)
    page: str | None = Field(default=None, max_length=255)


class FeedbackAck(BaseModel):
    status: str
    received_at: datetime


class FeedbackAreaSummary(BaseModel):
    area: str
    count: int
    average_rating: float


class FeedbackRecentItem(BaseModel):
    id: int
    rating: int
    area: str
    page: str | None
    message: str | None
    created_at: datetime


class FeedbackSummary(BaseModel):
    days: int
    total: int
    average_rating: float
    areas: list[FeedbackAreaSummary]
    recent: list[FeedbackRecentItem]


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    initial_block_type: BlockType = "text"
    initial_content: dict[str, Any] = Field(default_factory=dict)
    initial_metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentSummary(BaseModel):
    id: str
    workspace_id: str
    title: str
    root_block_id: str | None
    block_count: int
    created_at: datetime
    updated_at: datetime


class DocumentDetail(BaseModel):
    id: str
    workspace_id: str
    title: str
    root_block_id: str | None
    created_at: datetime
    updated_at: datetime


class DocumentUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class BlockCreate(BaseModel):
    parent_block_id: str | None = None
    type: BlockType = "text"
    content: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    position_index: int = 0


class BlockUpdate(BaseModel):
    parent_block_id: str | None = None
    type: BlockType | None = None
    content: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    position_index: int | None = None


class BlockOut(BaseModel):
    id: str
    document_id: str
    parent_block_id: str | None
    type: str
    content: dict[str, Any]
    metadata: dict[str, Any]
    position_index: int
    version: int
    created_at: datetime
    updated_at: datetime


class BlockRelationCreate(BaseModel):
    target_block_id: str
    relation_type: str = Field(default="references", min_length=1, max_length=64)


class BlockRelationOut(BaseModel):
    id: int
    document_id: str
    source_block_id: str
    target_block_id: str
    relation_type: str
    created_at: datetime


class BlockVersionOut(BaseModel):
    id: int
    block_id: str
    snapshot: dict[str, Any]
    created_at: datetime


class DocumentGraph(BaseModel):
    document_id: str
    nodes: list[BlockOut]
    edges: list[BlockRelationOut]
