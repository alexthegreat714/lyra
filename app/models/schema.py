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
