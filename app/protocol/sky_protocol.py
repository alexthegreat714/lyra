"""
Lyra Agent - Sky Protocol

Message passing framework for Sky<->Lyra communication.
Phase 6: Inter-agent communication protocol.

GUARDRAILS:
    Lyra's protocol participation:
    - Responds only to creative/strategic requests
    - Defers non-creative tasks to appropriate agents
    - All messages are structured and inspectable
    - No emotional content in protocol messages

    Sky orchestrates, Lyra contributes creative strategy.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

from loguru import logger


class MessageType(str, Enum):
    """Types of protocol messages."""
    # Requests from Sky
    TASK_REQUEST = "task_request"
    STATUS_REQUEST = "status_request"
    CAPABILITY_QUERY = "capability_query"
    COORDINATION_REQUEST = "coordination_request"
    SHUTDOWN_REQUEST = "shutdown_request"

    # Responses to Sky
    TASK_RESPONSE = "task_response"
    STATUS_RESPONSE = "status_response"
    CAPABILITY_RESPONSE = "capability_response"
    COORDINATION_RESPONSE = "coordination_response"
    ERROR_RESPONSE = "error_response"

    # Events/Notifications
    EVENT_NOTIFICATION = "event_notification"
    HEARTBEAT = "heartbeat"
    REGISTRATION = "registration"


class MessagePriority(str, Enum):
    """Priority levels for messages."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class AgentCapability(str, Enum):
    """Capabilities Lyra can advertise."""
    CREATIVE_STRATEGY = "creative_strategy"
    IDEA_GENERATION = "idea_generation"
    NARRATIVE_DESIGN = "narrative_design"
    CONCEPTUAL_REFRAMING = "conceptual_reframing"
    ANALOGY_CREATION = "analogy_creation"
    COUNTERFACTUAL_ANALYSIS = "counterfactual_analysis"
    TONE_MAPPING = "tone_mapping"
    CONGRESS_PARTICIPATION = "congress_participation"


class SkyProtocol:
    """
    Sky Protocol handler for Lyra.

    Manages message passing between Sky orchestrator and Lyra agent.
    Handles registration, task routing, and coordination.

    GUARDRAILS:
        - Only responds to creative/strategic tasks
        - Defers non-creative requests with appropriate referrals
        - All messages have structured format
    """

    # Lyra's advertised capabilities
    CAPABILITIES = [
        AgentCapability.CREATIVE_STRATEGY,
        AgentCapability.IDEA_GENERATION,
        AgentCapability.NARRATIVE_DESIGN,
        AgentCapability.CONCEPTUAL_REFRAMING,
        AgentCapability.ANALOGY_CREATION,
        AgentCapability.COUNTERFACTUAL_ANALYSIS,
        AgentCapability.TONE_MAPPING,
        AgentCapability.CONGRESS_PARTICIPATION,
    ]

    # Task types Lyra can handle
    SUPPORTED_TASKS = [
        "idea_generation",
        "reframe",
        "narrative_design",
        "counterfactual_analysis",
        "analogy_exploration",
        "tone_mapping",
        "mixed_creative",
        "creative_contribution",
        "bill_analysis",
    ]

    # Task types Lyra must defer
    DEFERRED_TASKS = {
        "legal_analysis": "Sophia",
        "security_assessment": "Aegis",
        "resource_allocation": "Argus",
        "compute_optimization": "Argus",
        "health_evaluation": "Mercury",
        "social_analysis": "Mercury",
        "fact_verification": "Veritas",
    }

    def __init__(self, agent_id: str = "lyra"):
        """
        Initialize the Sky Protocol handler.

        Args:
            agent_id: Unique identifier for this agent
        """
        self.agent_id = agent_id
        self.registered = False
        self.sky_endpoint: Optional[str] = None
        self._message_handlers: Dict[MessageType, Callable] = {}
        self._message_queue: List[Dict[str, Any]] = []
        self._message_history: List[Dict[str, Any]] = []
        self._last_heartbeat: Optional[str] = None

        # Register default handlers
        self._register_default_handlers()

        logger.info(f"SkyProtocol initialized for agent: {agent_id}")

    def _register_default_handlers(self):
        """Register default message handlers."""
        self._message_handlers = {
            MessageType.TASK_REQUEST: self._handle_task_request,
            MessageType.STATUS_REQUEST: self._handle_status_request,
            MessageType.CAPABILITY_QUERY: self._handle_capability_query,
            MessageType.COORDINATION_REQUEST: self._handle_coordination_request,
            MessageType.SHUTDOWN_REQUEST: self._handle_shutdown_request,
        }

    def create_message(
        self,
        message_type: MessageType,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        correlation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a protocol message.

        Args:
            message_type: Type of message
            payload: Message payload
            priority: Message priority
            correlation_id: Optional ID for request-response correlation

        Returns:
            Formatted protocol message
        """
        message = {
            "message_id": str(uuid4()),
            "type": message_type.value,
            "source": self.agent_id,
            "destination": "sky",
            "priority": priority.value,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": payload,
        }

        if correlation_id:
            message["correlation_id"] = correlation_id

        return message

    def process_message(
        self,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process an incoming message from Sky.

        Args:
            message: Incoming protocol message

        Returns:
            Response message
        """
        message_type_str = message.get("type")
        message_id = message.get("message_id", "unknown")

        logger.info(f"Processing message: {message_type_str} (id: {message_id})")

        # Record in history
        self._message_history.append({
            **message,
            "received_at": datetime.utcnow().isoformat() + "Z",
            "direction": "incoming",
        })

        try:
            message_type = MessageType(message_type_str)
        except ValueError:
            return self._create_error_response(
                message,
                f"Unknown message type: {message_type_str}"
            )

        handler = self._message_handlers.get(message_type)
        if not handler:
            return self._create_error_response(
                message,
                f"No handler for message type: {message_type_str}"
            )

        try:
            response = handler(message)
            self._message_history.append({
                **response,
                "direction": "outgoing",
            })
            return response
        except Exception as e:
            logger.error(f"Message handler failed: {e}")
            return self._create_error_response(message, str(e))

    def _handle_task_request(
        self,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a task request from Sky."""
        payload = message.get("payload", {})
        task_type = payload.get("task_type", "unknown")
        correlation_id = message.get("message_id")

        # Check if task should be deferred
        if task_type in self.DEFERRED_TASKS:
            suggested_agent = self.DEFERRED_TASKS[task_type]
            return self.create_message(
                message_type=MessageType.TASK_RESPONSE,
                payload={
                    "status": "deferred",
                    "task_type": task_type,
                    "reason": f"Task type '{task_type}' outside Lyra's expertise",
                    "suggested_agent": suggested_agent,
                },
                correlation_id=correlation_id,
            )

        # Check if task is supported
        if task_type not in self.SUPPORTED_TASKS:
            return self.create_message(
                message_type=MessageType.TASK_RESPONSE,
                payload={
                    "status": "unsupported",
                    "task_type": task_type,
                    "supported_tasks": self.SUPPORTED_TASKS,
                },
                correlation_id=correlation_id,
            )

        # Accept the task
        return self.create_message(
            message_type=MessageType.TASK_RESPONSE,
            payload={
                "status": "accepted",
                "task_type": task_type,
                "task_id": str(uuid4()),
                "message": f"Task '{task_type}' accepted for processing",
            },
            correlation_id=correlation_id,
        )

    def _handle_status_request(
        self,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a status request from Sky."""
        return self.create_message(
            message_type=MessageType.STATUS_RESPONSE,
            payload={
                "agent": self.agent_id,
                "status": "online",
                "registered": self.registered,
                "capabilities": [c.value for c in self.CAPABILITIES],
                "queue_length": len(self._message_queue),
                "message_history_count": len(self._message_history),
            },
            correlation_id=message.get("message_id"),
        )

    def _handle_capability_query(
        self,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a capability query from Sky."""
        return self.create_message(
            message_type=MessageType.CAPABILITY_RESPONSE,
            payload={
                "agent": self.agent_id,
                "capabilities": [c.value for c in self.CAPABILITIES],
                "supported_tasks": self.SUPPORTED_TASKS,
                "deferred_tasks": self.DEFERRED_TASKS,
                "guardrails": [
                    "No legal reasoning (Sophia only)",
                    "No security assessment (Aegis only)",
                    "No resource allocation (Argus only)",
                    "No health evaluation (Mercury only)",
                    "Creative and strategic tasks only",
                ],
            },
            correlation_id=message.get("message_id"),
        )

    def _handle_coordination_request(
        self,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a coordination request from Sky."""
        payload = message.get("payload", {})
        coordination_type = payload.get("coordination_type", "unknown")

        return self.create_message(
            message_type=MessageType.COORDINATION_RESPONSE,
            payload={
                "status": "acknowledged",
                "coordination_type": coordination_type,
                "agent": self.agent_id,
                "ready": True,
            },
            correlation_id=message.get("message_id"),
        )

    def _handle_shutdown_request(
        self,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a shutdown request from Sky."""
        logger.info("Shutdown request received from Sky")

        return self.create_message(
            message_type=MessageType.STATUS_RESPONSE,
            payload={
                "status": "shutdown_acknowledged",
                "agent": self.agent_id,
                "message": "Lyra preparing for graceful shutdown",
            },
            correlation_id=message.get("message_id"),
        )

    def _create_error_response(
        self,
        original_message: Dict[str, Any],
        error: str
    ) -> Dict[str, Any]:
        """Create an error response message."""
        return self.create_message(
            message_type=MessageType.ERROR_RESPONSE,
            payload={
                "error": error,
                "original_type": original_message.get("type"),
            },
            priority=MessagePriority.HIGH,
            correlation_id=original_message.get("message_id"),
        )

    def create_registration_message(self) -> Dict[str, Any]:
        """
        Create a registration message to send to Sky.

        Returns:
            Registration message
        """
        return self.create_message(
            message_type=MessageType.REGISTRATION,
            payload={
                "agent": self.agent_id,
                "agent_type": "creative_strategist",
                "capabilities": [c.value for c in self.CAPABILITIES],
                "supported_tasks": self.SUPPORTED_TASKS,
                "version": "0.1",
            },
        )

    def create_heartbeat_message(self) -> Dict[str, Any]:
        """
        Create a heartbeat message.

        Returns:
            Heartbeat message
        """
        self._last_heartbeat = datetime.utcnow().isoformat() + "Z"

        return self.create_message(
            message_type=MessageType.HEARTBEAT,
            payload={
                "agent": self.agent_id,
                "status": "alive",
                "timestamp": self._last_heartbeat,
            },
            priority=MessagePriority.LOW,
        )

    def create_event_notification(
        self,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create an event notification message.

        Args:
            event_type: Type of event
            event_data: Event data

        Returns:
            Event notification message
        """
        return self.create_message(
            message_type=MessageType.EVENT_NOTIFICATION,
            payload={
                "event_type": event_type,
                "event_data": event_data,
                "agent": self.agent_id,
            },
        )

    def register_handler(
        self,
        message_type: MessageType,
        handler: Callable[[Dict[str, Any]], Dict[str, Any]]
    ):
        """
        Register a custom message handler.

        Args:
            message_type: Message type to handle
            handler: Handler function
        """
        self._message_handlers[message_type] = handler
        logger.info(f"Registered handler for message type: {message_type.value}")

    def get_message_history(
        self,
        limit: int = 50,
        direction: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get message history.

        Args:
            limit: Maximum messages to return
            direction: Optional filter by direction (incoming/outgoing)

        Returns:
            List of historical messages
        """
        history = self._message_history

        if direction:
            history = [m for m in history if m.get("direction") == direction]

        return history[-limit:]

    def get_protocol_stats(self) -> Dict[str, Any]:
        """
        Get protocol statistics.

        Returns:
            Protocol statistics
        """
        incoming = sum(
            1 for m in self._message_history
            if m.get("direction") == "incoming"
        )
        outgoing = sum(
            1 for m in self._message_history
            if m.get("direction") == "outgoing"
        )

        return {
            "agent_id": self.agent_id,
            "registered": self.registered,
            "total_messages": len(self._message_history),
            "incoming_messages": incoming,
            "outgoing_messages": outgoing,
            "last_heartbeat": self._last_heartbeat,
            "capabilities_count": len(self.CAPABILITIES),
            "supported_tasks_count": len(self.SUPPORTED_TASKS),
        }
