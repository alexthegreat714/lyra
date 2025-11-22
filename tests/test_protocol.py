"""
Tests for Lyra Sky Protocol

Phase 6: Inter-agent communication tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.server import app
from app.protocol.sky_protocol import (
    SkyProtocol,
    MessageType,
    MessagePriority,
    AgentCapability,
)


client = TestClient(app)


class TestSkyProtocol:
    """Tests for the SkyProtocol class."""

    def test_protocol_initialization(self):
        """Test protocol initialization."""
        protocol = SkyProtocol(agent_id="test-lyra")

        assert protocol.agent_id == "test-lyra"
        assert not protocol.registered
        assert len(protocol.CAPABILITIES) > 0
        assert len(protocol.SUPPORTED_TASKS) > 0

    def test_create_message(self):
        """Test creating a protocol message."""
        protocol = SkyProtocol()

        message = protocol.create_message(
            message_type=MessageType.STATUS_RESPONSE,
            payload={"status": "online"},
        )

        assert message["type"] == "status_response"
        assert message["source"] == "lyra"
        assert message["destination"] == "sky"
        assert message["payload"]["status"] == "online"
        assert "message_id" in message
        assert "timestamp" in message

    def test_create_message_with_priority(self):
        """Test creating a message with priority."""
        protocol = SkyProtocol()

        message = protocol.create_message(
            message_type=MessageType.ERROR_RESPONSE,
            payload={"error": "test"},
            priority=MessagePriority.HIGH,
        )

        assert message["priority"] == "high"

    def test_process_task_request_supported(self):
        """Test processing a supported task request."""
        protocol = SkyProtocol()

        message = {
            "message_id": "test-123",
            "type": "task_request",
            "source": "sky",
            "payload": {"task_type": "idea_generation"},
        }

        response = protocol.process_message(message)

        assert response["type"] == "task_response"
        assert response["payload"]["status"] == "accepted"
        assert response["correlation_id"] == "test-123"

    def test_process_task_request_deferred(self):
        """Test processing a deferred task request."""
        protocol = SkyProtocol()

        message = {
            "message_id": "test-456",
            "type": "task_request",
            "source": "sky",
            "payload": {"task_type": "legal_analysis"},
        }

        response = protocol.process_message(message)

        assert response["type"] == "task_response"
        assert response["payload"]["status"] == "deferred"
        assert response["payload"]["suggested_agent"] == "Sophia"

    def test_process_task_request_unsupported(self):
        """Test processing an unsupported task request."""
        protocol = SkyProtocol()

        message = {
            "type": "task_request",
            "source": "sky",
            "payload": {"task_type": "unknown_task"},
        }

        response = protocol.process_message(message)

        assert response["type"] == "task_response"
        assert response["payload"]["status"] == "unsupported"

    def test_process_status_request(self):
        """Test processing a status request."""
        protocol = SkyProtocol()

        message = {
            "type": "status_request",
            "source": "sky",
            "payload": {},
        }

        response = protocol.process_message(message)

        assert response["type"] == "status_response"
        assert response["payload"]["agent"] == "lyra"
        assert response["payload"]["status"] == "online"

    def test_process_capability_query(self):
        """Test processing a capability query."""
        protocol = SkyProtocol()

        message = {
            "type": "capability_query",
            "source": "sky",
            "payload": {},
        }

        response = protocol.process_message(message)

        assert response["type"] == "capability_response"
        assert "capabilities" in response["payload"]
        assert "supported_tasks" in response["payload"]
        assert "deferred_tasks" in response["payload"]

    def test_process_unknown_message_type(self):
        """Test processing an unknown message type."""
        protocol = SkyProtocol()

        message = {
            "type": "unknown_type",
            "source": "sky",
            "payload": {},
        }

        response = protocol.process_message(message)

        assert response["type"] == "error_response"
        assert "error" in response["payload"]

    def test_create_registration_message(self):
        """Test creating a registration message."""
        protocol = SkyProtocol()

        message = protocol.create_registration_message()

        assert message["type"] == "registration"
        assert message["payload"]["agent"] == "lyra"
        assert message["payload"]["agent_type"] == "creative_strategist"
        assert "capabilities" in message["payload"]

    def test_create_heartbeat_message(self):
        """Test creating a heartbeat message."""
        protocol = SkyProtocol()

        message = protocol.create_heartbeat_message()

        assert message["type"] == "heartbeat"
        assert message["payload"]["status"] == "alive"
        assert message["priority"] == "low"

    def test_create_event_notification(self):
        """Test creating an event notification."""
        protocol = SkyProtocol()

        message = protocol.create_event_notification(
            event_type="task_completed",
            event_data={"task_id": "test-task"},
        )

        assert message["type"] == "event_notification"
        assert message["payload"]["event_type"] == "task_completed"

    def test_message_history(self):
        """Test message history tracking."""
        protocol = SkyProtocol()

        # Process a message
        protocol.process_message({
            "type": "status_request",
            "source": "sky",
            "payload": {},
        })

        history = protocol.get_message_history()
        assert len(history) >= 2  # Incoming + outgoing

    def test_protocol_stats(self):
        """Test protocol statistics."""
        protocol = SkyProtocol()

        # Process some messages
        protocol.process_message({
            "type": "status_request",
            "source": "sky",
            "payload": {},
        })

        stats = protocol.get_protocol_stats()
        assert stats["agent_id"] == "lyra"
        assert "total_messages" in stats
        assert "incoming_messages" in stats
        assert "outgoing_messages" in stats


class TestAgentCapabilities:
    """Tests for agent capabilities."""

    def test_capabilities_defined(self):
        """Test all capabilities are defined."""
        expected_capabilities = [
            "creative_strategy",
            "idea_generation",
            "narrative_design",
            "conceptual_reframing",
            "analogy_creation",
            "counterfactual_analysis",
            "tone_mapping",
            "congress_participation",
        ]

        actual = [c.value for c in AgentCapability]
        for cap in expected_capabilities:
            assert cap in actual

    def test_supported_tasks(self):
        """Test supported tasks are defined."""
        protocol = SkyProtocol()
        expected_tasks = [
            "idea_generation",
            "reframe",
            "narrative_design",
            "counterfactual_analysis",
            "analogy_exploration",
            "tone_mapping",
            "mixed_creative",
        ]

        for task in expected_tasks:
            assert task in protocol.SUPPORTED_TASKS

    def test_deferred_tasks(self):
        """Test deferred tasks are mapped correctly."""
        protocol = SkyProtocol()

        assert protocol.DEFERRED_TASKS["legal_analysis"] == "Sophia"
        assert protocol.DEFERRED_TASKS["security_assessment"] == "Aegis"
        assert protocol.DEFERRED_TASKS["resource_allocation"] == "Argus"
        assert protocol.DEFERRED_TASKS["health_evaluation"] == "Mercury"


class TestProtocolEndpoints:
    """Tests for Protocol API endpoints."""

    def test_protocol_status(self):
        """Test /protocol/status endpoint."""
        response = client.get("/protocol/status")
        assert response.status_code == 200

        data = response.json()
        assert data["type"] == "status_response"
        assert data["payload"]["agent"] == "lyra"

    def test_protocol_capabilities(self):
        """Test /protocol/capabilities endpoint."""
        response = client.get("/protocol/capabilities")
        assert response.status_code == 200

        data = response.json()
        assert data["type"] == "capability_response"
        assert "capabilities" in data["payload"]

    def test_protocol_message(self):
        """Test /protocol/message endpoint."""
        response = client.post(
            "/protocol/message",
            json={
                "type": "status_request",
                "source": "sky",
                "payload": {},
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["type"] == "status_response"

    def test_protocol_task(self):
        """Test /protocol/task endpoint."""
        response = client.post(
            "/protocol/task",
            json={
                "task_type": "idea_generation",
                "prompt": "test prompt",
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["type"] == "task_response"
        assert data["payload"]["status"] == "accepted"

    def test_protocol_task_deferred(self):
        """Test /protocol/task with deferred task."""
        response = client.post(
            "/protocol/task",
            json={
                "task_type": "legal_analysis",
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["payload"]["status"] == "deferred"
        assert data["payload"]["suggested_agent"] == "Sophia"

    def test_protocol_heartbeat(self):
        """Test /protocol/heartbeat endpoint."""
        response = client.get("/protocol/heartbeat")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "sent"
        assert data["message"]["type"] == "heartbeat"

    def test_protocol_register(self):
        """Test /protocol/register endpoint."""
        response = client.get("/protocol/register")
        assert response.status_code == 200

        data = response.json()
        assert data["type"] == "registration"
        assert data["payload"]["agent"] == "lyra"

    def test_protocol_event(self):
        """Test /protocol/event endpoint."""
        response = client.post(
            "/protocol/event",
            json={
                "event_type": "task_completed",
                "event_data": {"task_id": "test"},
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "sent"

    def test_protocol_history(self):
        """Test /protocol/history endpoint."""
        response = client.get("/protocol/history")
        assert response.status_code == 200

        data = response.json()
        assert "messages" in data
        assert "count" in data

    def test_protocol_stats(self):
        """Test /protocol/stats endpoint."""
        response = client.get("/protocol/stats")
        assert response.status_code == 200

        data = response.json()
        assert data["agent_id"] == "lyra"
        assert "total_messages" in data
