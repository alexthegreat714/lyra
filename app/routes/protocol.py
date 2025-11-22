"""
Lyra Agent Protocol Routes

API endpoints for Sky Protocol communication.
Phase 6: Inter-agent communication.

GUARDRAILS:
    Lyra's protocol participation:
    - Responds only to creative/strategic requests
    - Defers non-creative tasks to appropriate agents
    - All messages are structured and inspectable
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel, Field

from app.protocol.sky_protocol import (
    SkyProtocol,
    MessageType,
    MessagePriority,
)


router = APIRouter(prefix="/protocol", tags=["protocol"])

# Initialize Sky Protocol handler
protocol = SkyProtocol(agent_id="lyra")


# Request/Response Models

class ProtocolMessage(BaseModel):
    """Model for incoming protocol messages."""
    message_id: Optional[str] = Field(None, description="Message ID")
    type: str = Field(..., description="Message type")
    source: str = Field(default="sky", description="Source agent")
    destination: str = Field(default="lyra", description="Destination agent")
    priority: str = Field(default="normal", description="Message priority")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Message payload")
    correlation_id: Optional[str] = Field(None, description="Correlation ID")


class TaskRequestPayload(BaseModel):
    """Payload for task requests."""
    task_type: str = Field(..., description="Type of task to execute")
    prompt: Optional[str] = Field(None, description="Task prompt")
    context: Optional[Dict[str, Any]] = Field(None, description="Task context")


class EventNotification(BaseModel):
    """Model for event notifications."""
    event_type: str = Field(..., description="Type of event")
    event_data: Dict[str, Any] = Field(default_factory=dict, description="Event data")


# Protocol Endpoints

@router.post("/message")
async def handle_protocol_message(message: ProtocolMessage) -> Dict[str, Any]:
    """
    Handle an incoming protocol message from Sky.

    Processes the message and returns appropriate response.

    Args:
        message: Protocol message from Sky

    Returns:
        Response message
    """
    logger.info(f"Received protocol message: {message.type}")

    try:
        response = protocol.process_message(message.model_dump())
        return response
    except Exception as e:
        logger.error(f"Protocol message handling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/task")
async def handle_task_request(payload: TaskRequestPayload) -> Dict[str, Any]:
    """
    Handle a task request via protocol.

    Creates a task_request message and processes it.

    Args:
        payload: Task request payload

    Returns:
        Task response
    """
    logger.info(f"Task request via protocol: {payload.task_type}")

    message = {
        "type": MessageType.TASK_REQUEST.value,
        "source": "sky",
        "payload": payload.model_dump(),
    }

    try:
        response = protocol.process_message(message)
        return response
    except Exception as e:
        logger.error(f"Task request handling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_protocol_status() -> Dict[str, Any]:
    """
    Get protocol status via status request message.

    Returns:
        Status response
    """
    message = {
        "type": MessageType.STATUS_REQUEST.value,
        "source": "sky",
        "payload": {},
    }

    return protocol.process_message(message)


@router.get("/capabilities")
async def get_capabilities() -> Dict[str, Any]:
    """
    Get Lyra's capabilities via capability query.

    Returns:
        Capability response
    """
    message = {
        "type": MessageType.CAPABILITY_QUERY.value,
        "source": "sky",
        "payload": {},
    }

    return protocol.process_message(message)


@router.post("/coordinate")
async def handle_coordination(
    coordination_type: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Handle a coordination request from Sky.

    Args:
        coordination_type: Type of coordination
        context: Optional coordination context

    Returns:
        Coordination response
    """
    logger.info(f"Coordination request: {coordination_type}")

    message = {
        "type": MessageType.COORDINATION_REQUEST.value,
        "source": "sky",
        "payload": {
            "coordination_type": coordination_type,
            "context": context or {},
        },
    }

    return protocol.process_message(message)


@router.post("/event")
async def send_event(notification: EventNotification) -> Dict[str, Any]:
    """
    Send an event notification to Sky.

    Args:
        notification: Event notification

    Returns:
        Event notification message
    """
    logger.info(f"Sending event notification: {notification.event_type}")

    message = protocol.create_event_notification(
        event_type=notification.event_type,
        event_data=notification.event_data,
    )

    return {
        "status": "sent",
        "message": message,
    }


@router.get("/heartbeat")
async def send_heartbeat() -> Dict[str, Any]:
    """
    Send a heartbeat to Sky.

    Returns:
        Heartbeat message
    """
    message = protocol.create_heartbeat_message()
    return {
        "status": "sent",
        "message": message,
    }


@router.get("/register")
async def get_registration_message() -> Dict[str, Any]:
    """
    Get the registration message for Sky.

    Returns:
        Registration message
    """
    return protocol.create_registration_message()


@router.get("/history")
async def get_message_history(
    limit: int = 50,
    direction: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get protocol message history.

    Args:
        limit: Maximum messages to return
        direction: Optional filter (incoming/outgoing)

    Returns:
        Message history
    """
    history = protocol.get_message_history(limit=limit, direction=direction)
    return {
        "messages": history,
        "count": len(history),
        "direction_filter": direction,
    }


@router.get("/stats")
async def get_protocol_stats() -> Dict[str, Any]:
    """
    Get protocol statistics.

    Returns:
        Protocol statistics
    """
    return protocol.get_protocol_stats()
