"""
Lyra Agent Protocol Module

Phase 6: Sky Protocol for inter-agent communication.

GUARDRAILS:
    Lyra's protocol participation follows these boundaries:
    - Lyra only responds to creative/strategic requests
    - Lyra defers non-creative tasks to appropriate agents
    - All messages are structured and inspectable
    - No emotional content in protocol messages
"""

from app.protocol.sky_protocol import (
    SkyProtocol,
    MessageType,
    MessagePriority,
    AgentCapability,
)

__all__ = [
    "SkyProtocol",
    "MessageType",
    "MessagePriority",
    "AgentCapability",
]
