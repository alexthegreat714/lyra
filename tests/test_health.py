"""
Tests for Lyra Agent Health/Status Endpoint
"""

import pytest
from fastapi.testclient import TestClient

from app.server import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestStatus:
    """Tests for GET /status endpoint."""

    def test_status_returns_200(self, client):
        """Test that status endpoint returns 200."""
        response = client.get("/status")
        assert response.status_code == 200

    def test_status_returns_correct_agent_name(self, client):
        """Test that status returns correct agent name."""
        response = client.get("/status")
        data = response.json()
        assert data["agent"] == "Lyra"

    def test_status_returns_version(self, client):
        """Test that status returns version."""
        response = client.get("/status")
        data = response.json()
        assert data["version"] == "0.1"

    def test_status_returns_online_state(self, client):
        """Test that status returns online state."""
        response = client.get("/status")
        data = response.json()
        assert data["state"] == "online"

    def test_status_response_structure(self, client):
        """Test that status response has correct structure."""
        response = client.get("/status")
        data = response.json()
        assert "agent" in data
        assert "version" in data
        assert "state" in data
