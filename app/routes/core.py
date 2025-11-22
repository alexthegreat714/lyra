"""
Lyra Agent Core Routes

Core API endpoints for task execution, status, events, and shutdown.

Phase 3: Added creative_brain endpoint for structured reasoning.

GUARDRAILS:
    - No legal reasoning (Sophia only)
    - No factual judgment (Veritas only)
    - No compute/resource logic (Argus only)
    - No health/social inference (Mercury)
    - No emotional inference
    - No "advice" style output, only structured creative constructs
"""

import uuid
from typing import Any, Union

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.config import get_settings
from app.models.schema import (
    TaskRequest,
    TaskResponse,
    EventRequest,
    EventResponse,
    StatusResponse,
    ShutdownResponse,
    CreativeTaskRequest,
    CreativeTaskResponse,
)
from app.services.lyra_agent import LyraAgent

router = APIRouter()

# Initialize the agent
settings = get_settings()
agent = LyraAgent(settings)


@router.post("/run_task", response_model=TaskResponse)
async def run_task(request: TaskRequest) -> TaskResponse:
    """
    Execute a task through the Lyra agent.

    Supported task types:
        - "use_tool": Direct tool invocation (Phase 2)
        - "creative_brain": Structured reasoning pipeline (Phase 3)
        - Other: Returns available options

    Args:
        request: Task request containing task type and payload

    Returns:
        TaskResponse with status, task_id, and result
    """
    task_id = str(uuid.uuid4())
    logger.info(f"Received task: {request.task} (id: {task_id})")

    try:
        result = agent.run_task(request.task, request.payload)

        # For creative_brain tasks, the result already has full structure
        if request.task == "creative_brain":
            return TaskResponse(
                status="completed",
                task_id=task_id,
                result=result,
            )

        return TaskResponse(
            status="received",
            task_id=task_id,
            result=result,
        )
    except Exception as e:
        logger.error(f"Task execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/creative_brain", response_model=CreativeTaskResponse)
async def creative_brain(request: CreativeTaskRequest) -> CreativeTaskResponse:
    """
    Execute a creative task through Lyra's reasoning brain.

    This endpoint provides structured, inspectable creative processing
    using the LyraBrain reasoning pipeline.

    Supported task types:
        - idea_generation: divergence + convergence
        - reframe: tonemap + divergence + convergence
        - narrative_design: narratives
        - counterfactual_analysis: counterfactuals + convergence
        - analogy_exploration: analogies
        - tone_mapping: tonemap
        - mixed_creative: full pipeline

    Args:
        request: Creative task request with task_type, prompt, and optional context

    Returns:
        CreativeTaskResponse with structured result and pipeline steps
    """
    logger.info(f"Creative brain task: {request.task_type}")

    try:
        result = agent.run_creative_task(
            task_type=request.task_type,
            prompt=request.prompt,
            context=request.context,
        )
        return CreativeTaskResponse(
            task_type=result["task_type"],
            prompt=result["prompt"],
            result=result["result"],
            steps=result["steps"],
        )
    except Exception as e:
        logger.error(f"Creative brain task failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=StatusResponse)
async def get_status() -> StatusResponse:
    """
    Get the current status of the Lyra agent.

    Returns:
        StatusResponse with agent name, version, and state
    """
    return StatusResponse(
        agent=settings.AGENT_NAME,
        version=settings.VERSION,
        state="online",
    )


@router.post("/event", response_model=EventResponse)
async def handle_event(request: EventRequest) -> EventResponse:
    """
    Handle incoming events from Sky/Congress.

    Args:
        request: Event request containing event type and payload

    Returns:
        EventResponse acknowledging receipt
    """
    logger.info(f"Received event: {request.event_type}")

    try:
        agent.handle_event(request.event_type, request.payload)
        return EventResponse(acknowledged=True)
    except Exception as e:
        logger.error(f"Event handling failed: {e}")
        return EventResponse(acknowledged=False)


@router.post("/shutdown", response_model=ShutdownResponse)
async def shutdown() -> ShutdownResponse:
    """
    Initiate graceful shutdown of the Lyra agent.

    Returns:
        ShutdownResponse indicating shutdown has been initiated
    """
    logger.info("Shutdown requested")
    # Placeholder: In production, this would trigger graceful shutdown
    return ShutdownResponse(
        status="shutdown_initiated",
        message="Lyra agent shutdown initiated",
    )
