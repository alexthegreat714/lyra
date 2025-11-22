"""
Lyra Agent Schema Models

Pydantic models for API request and response validation.
"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# Phase 3: Supported creative task types
LyraTaskType = Literal[
    "idea_generation",
    "reframe",
    "narrative_design",
    "counterfactual_analysis",
    "analogy_exploration",
    "tone_mapping",
    "mixed_creative",
]


class TaskRequest(BaseModel):
    """Request model for task execution."""

    task: str = Field(..., description="The type of task to execute")
    payload: Dict[str, Any] = Field(
        default_factory=dict, description="Task-specific payload data"
    )


class TaskResponse(BaseModel):
    """Response model for task execution."""

    status: str = Field(..., description="Task execution status")
    task_id: str = Field(..., description="Unique identifier for the task")
    result: Dict[str, Any] = Field(
        default_factory=dict, description="Task execution result"
    )


class EventRequest(BaseModel):
    """Request model for incoming events."""

    event_type: str = Field(..., description="Type of event")
    payload: Dict[str, Any] = Field(
        default_factory=dict, description="Event-specific payload data"
    )


class EventResponse(BaseModel):
    """Response model for event handling."""

    acknowledged: bool = Field(..., description="Whether the event was acknowledged")


class StatusResponse(BaseModel):
    """Response model for agent status."""

    agent: str = Field(..., description="Agent name")
    version: str = Field(..., description="Agent version")
    state: str = Field(..., description="Current agent state")


class ShutdownResponse(BaseModel):
    """Response model for shutdown request."""

    status: str = Field(..., description="Shutdown status")
    message: str = Field(..., description="Shutdown message")


# Phase 3: Creative Brain Models


class CreativeTaskRequest(BaseModel):
    """Request model for creative brain task execution."""

    task_type: LyraTaskType = Field(
        ..., description="Type of creative task to perform"
    )
    prompt: str = Field(..., description="The input prompt to process")
    context: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional context for the task"
    )


class CreativeTaskResponse(BaseModel):
    """Response model for creative brain task execution."""

    task_type: str = Field(..., description="The executed task type")
    prompt: str = Field(..., description="The original prompt")
    result: Dict[str, Any] = Field(
        ..., description="Synthesized result from the reasoning pipeline"
    )
    steps: List[Dict[str, Any]] = Field(
        ..., description="List of pipeline stages executed"
    )


# Phase 4: Memory Models

# Valid memory categories for Lyra's creative context
MemoryCategory = Literal[
    "themes",
    "narratives",
    "styles",
    "user_preferences",
    "creative_history",
    "motifs",
]


class MemoryItem(BaseModel):
    """A single item for memory ingestion."""

    text: str = Field(..., description="The content to store")
    category: MemoryCategory = Field(
        default="creative_history", description="Category for organization"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Optional metadata"
    )


class IngestRequest(BaseModel):
    """Request model for memory ingestion."""

    items: List[MemoryItem] = Field(..., description="Items to ingest into memory")


class IngestResult(BaseModel):
    """Result for a single ingested item."""

    id: Optional[str] = Field(None, description="ID of the ingested item")
    category: Optional[str] = Field(None, description="Category of the item")
    status: str = Field(..., description="Ingestion status")
    timestamp: Optional[str] = Field(None, description="Ingestion timestamp")
    error: Optional[str] = Field(None, description="Error message if failed")


class IngestResponse(BaseModel):
    """Response model for memory ingestion."""

    ingested_count: int = Field(..., description="Number of items successfully ingested")
    results: List[IngestResult] = Field(..., description="Per-item ingestion results")


class MemoryPreviewItem(BaseModel):
    """A preview item from memory."""

    id: str = Field(..., description="Item ID")
    text: str = Field(..., description="Item text content")
    category: str = Field(..., description="Item category")
    similarity: Optional[float] = Field(None, description="Similarity score if queried")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Item metadata"
    )


class MemoryPreviewRequest(BaseModel):
    """Request model for memory preview/query."""

    query: Optional[str] = Field(
        None, description="Query text for semantic search"
    )
    category: Optional[MemoryCategory] = Field(
        None, description="Filter by category"
    )
    top_k: int = Field(default=5, ge=1, le=50, description="Number of results")


class MemoryPreviewResponse(BaseModel):
    """Response model for memory preview."""

    items: List[MemoryPreviewItem] = Field(..., description="Retrieved memory items")
    count: int = Field(..., description="Number of items returned")
    query: Optional[str] = Field(None, description="The query used")
    category: Optional[str] = Field(None, description="Category filter used")


class MemoryStatsResponse(BaseModel):
    """Response model for memory statistics."""

    categories: Dict[str, int] = Field(
        ..., description="Item counts per category"
    )
    total_items: int = Field(..., description="Total items in memory")
    valid_categories: List[str] = Field(..., description="List of valid categories")
