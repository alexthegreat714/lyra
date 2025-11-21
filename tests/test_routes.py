"""
Tests for Lyra Agent Core Routes
"""

import pytest
from fastapi.testclient import TestClient

from app.server import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestRunTask:
    """Tests for POST /run_task endpoint."""

    def test_run_task_returns_placeholder(self, client):
        """Test that run_task returns placeholder response."""
        response = client.post(
            "/run_task",
            json={"task": "test_task", "payload": {"key": "value"}},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "received"
        assert "task_id" in data
        assert "result" in data
        assert data["result"]["note"] == "Lyra Phase 1 placeholder"

    def test_run_task_with_empty_payload(self, client):
        """Test run_task with empty payload."""
        response = client.post(
            "/run_task",
            json={"task": "empty_test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "received"

    def test_run_task_missing_task_field(self, client):
        """Test run_task with missing task field returns 422."""
        response = client.post(
            "/run_task",
            json={"payload": {}},
        )
        assert response.status_code == 422


class TestEvent:
    """Tests for POST /event endpoint."""

    def test_event_acknowledged(self, client):
        """Test that events are acknowledged."""
        response = client.post(
            "/event",
            json={"event_type": "test_event", "payload": {"data": "test"}},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["acknowledged"] is True

    def test_event_with_empty_payload(self, client):
        """Test event with empty payload."""
        response = client.post(
            "/event",
            json={"event_type": "simple_event"},
        )
        assert response.status_code == 200
        assert response.json()["acknowledged"] is True


class TestShutdown:
    """Tests for POST /shutdown endpoint."""

    def test_shutdown_returns_initiated(self, client):
        """Test that shutdown returns initiated status."""
        response = client.post("/shutdown")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "shutdown_initiated"
        assert "message" in data
