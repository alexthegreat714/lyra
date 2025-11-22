"""
Tests for Lyra History Logging

Phase 7: Creative history logging and export tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.server import app
from app.history.logger import CreativeHistoryLogger, LogEntryType
from app.history.exporter import HistoryExporter


client = TestClient(app)


class TestCreativeHistoryLogger:
    """Tests for the CreativeHistoryLogger class."""

    def test_logger_initialization(self):
        """Test logger initialization."""
        logger = CreativeHistoryLogger()

        assert logger._session_id is not None
        assert logger._session_start is not None
        assert len(logger._entries) == 0

    def test_log_entry(self):
        """Test logging a basic entry."""
        logger = CreativeHistoryLogger()

        entry = logger.log(
            entry_type=LogEntryType.SYSTEM_EVENT,
            operation="test_operation",
            data={"key": "value"},
        )

        assert entry["type"] == "system_event"
        assert entry["operation"] == "test_operation"
        assert entry["data"]["key"] == "value"
        assert "entry_id" in entry
        assert "timestamp" in entry

    def test_log_creative_task(self):
        """Test logging a creative task."""
        logger = CreativeHistoryLogger()

        entry = logger.log_creative_task(
            task_type="idea_generation",
            prompt="test prompt",
            result={"output": "test"},
            duration_ms=100,
        )

        assert entry["type"] == "creative_task"
        assert entry["operation"] == "idea_generation"
        assert entry["metadata"]["duration_ms"] == 100

    def test_log_tool_usage(self):
        """Test logging tool usage."""
        logger = CreativeHistoryLogger()

        entry = logger.log_tool_usage(
            tool_name="divergence",
            input_summary="test input",
            output_summary="test output",
            success=True,
        )

        assert entry["type"] == "tool_usage"
        assert entry["data"]["tool"] == "divergence"
        assert entry["data"]["success"] is True

    def test_log_brain_execution(self):
        """Test logging brain execution."""
        logger = CreativeHistoryLogger()

        entry = logger.log_brain_execution(
            task_type="idea_generation",
            stages_completed=["interpretation", "classification"],
            tools_used=["divergence", "convergence"],
            memory_items_retrieved=3,
        )

        assert entry["type"] == "brain_execution"
        assert entry["data"]["stages"] == ["interpretation", "classification"]
        assert entry["data"]["memory_items"] == 3

    def test_log_congress_vote(self):
        """Test logging a Congress vote."""
        logger = CreativeHistoryLogger()

        entry = logger.log_congress_vote(
            proposal_id="prop-123",
            vote="approve",
            domain="creative",
            auto_abstain=False,
        )

        assert entry["type"] == "congress_vote"
        assert entry["data"]["vote"] == "approve"
        assert entry["data"]["auto_abstain"] is False

    def test_log_protocol_message(self):
        """Test logging a protocol message."""
        logger = CreativeHistoryLogger()

        entry = logger.log_protocol_message(
            message_type="task_request",
            direction="incoming",
            source="sky",
            destination="lyra",
        )

        assert entry["type"] == "protocol_message"
        assert entry["data"]["direction"] == "incoming"

    def test_get_entries_filter(self):
        """Test getting entries with filter."""
        logger = CreativeHistoryLogger()

        # Log different types
        logger.log_tool_usage("tool1", "in", "out", True)
        logger.log_system_event("event1")
        logger.log_tool_usage("tool2", "in", "out", True)

        # Get only tool usage
        entries = logger.get_entries(entry_type=LogEntryType.TOOL_USAGE)
        assert len(entries) == 2
        assert all(e["type"] == "tool_usage" for e in entries)

    def test_get_session_summary(self):
        """Test getting session summary."""
        logger = CreativeHistoryLogger()

        # Log some entries
        logger.log_tool_usage("tool1", "in", "out", True)
        logger.log_creative_task("idea_generation", "prompt", {})

        summary = logger.get_session_summary()

        assert summary["total_entries"] == 2
        assert "entries_by_type" in summary
        assert "tool_usage" in summary["entries_by_type"]

    def test_max_entries_limit(self):
        """Test max entries limit."""
        logger = CreativeHistoryLogger(max_memory_entries=5)

        # Log more than max
        for i in range(10):
            logger.log_system_event(f"event_{i}")

        assert len(logger._entries) == 5


class TestHistoryExporter:
    """Tests for the HistoryExporter class."""

    def test_exporter_initialization(self):
        """Test exporter initialization."""
        exporter = HistoryExporter()
        assert exporter.log_dir is not None

    def test_export_to_json(self):
        """Test JSON export."""
        exporter = HistoryExporter()

        entries = [
            {"entry_id": "1", "type": "test", "operation": "op1"},
            {"entry_id": "2", "type": "test", "operation": "op2"},
        ]

        json_str = exporter.export_to_json(entries)

        import json
        data = json.loads(json_str)

        assert data["entry_count"] == 2
        assert len(data["entries"]) == 2

    def test_export_to_csv(self):
        """Test CSV export."""
        exporter = HistoryExporter()

        entries = [
            {"entry_id": "1", "type": "test", "operation": "op1", "timestamp": "2024-01-01"},
            {"entry_id": "2", "type": "test", "operation": "op2", "timestamp": "2024-01-02"},
        ]

        csv_str = exporter.export_to_csv(entries)

        assert "entry_id" in csv_str
        assert "operation" in csv_str

    def test_generate_summary_report(self):
        """Test summary report generation."""
        exporter = HistoryExporter()

        entries = [
            {"type": "tool_usage", "operation": "divergence", "timestamp": "2024-01-01"},
            {"type": "tool_usage", "operation": "convergence", "timestamp": "2024-01-02"},
            {"type": "creative_task", "operation": "idea_generation", "timestamp": "2024-01-03"},
        ]

        report = exporter.generate_summary_report(entries)

        assert report["total_entries"] == 3
        assert "entries_by_type" in report
        assert report["entries_by_type"]["tool_usage"] == 2

    def test_generate_tool_report(self):
        """Test tool usage report generation."""
        exporter = HistoryExporter()

        entries = [
            {"type": "tool_usage", "data": {"tool": "divergence", "success": True}},
            {"type": "tool_usage", "data": {"tool": "divergence", "success": True}},
            {"type": "tool_usage", "data": {"tool": "convergence", "success": False}},
        ]

        report = exporter.generate_tool_usage_report(entries)

        assert report["total_tool_uses"] == 3
        assert report["tool_counts"]["divergence"] == 2
        assert report["success_rates"]["divergence"] == 1.0

    def test_generate_congress_report(self):
        """Test Congress participation report."""
        exporter = HistoryExporter()

        entries = [
            {"type": "congress_vote", "data": {"vote": "approve", "domain": "creative"}},
            {"type": "congress_vote", "data": {"vote": "abstain", "auto_abstain": True}},
            {"type": "congress_contribution", "data": {"contribution_type": "perspective"}},
        ]

        report = exporter.generate_congress_report(entries)

        assert report["total_votes"] == 2
        assert report["vote_breakdown"]["approve"] == 1
        assert report["auto_abstains"] == 1
        assert report["total_contributions"] == 1

    def test_sanitize_entry(self):
        """Test entry sanitization."""
        exporter = HistoryExporter()

        entry = {
            "entry_id": "1",
            "data": {"user_data": "sensitive", "result": "ok"},
        }

        sanitized = exporter._sanitize_entry(entry)

        assert "user_data" not in sanitized.get("data", {})
        assert sanitized["data"]["result"] == "ok"


class TestHistoryEndpoints:
    """Tests for History API endpoints."""

    def test_history_stats(self):
        """Test /history/stats endpoint."""
        response = client.get("/history/stats")
        assert response.status_code == 200

        data = response.json()
        assert "session" in data
        assert "export" in data
        assert "entry_types" in data

    def test_history_types(self):
        """Test /history/types endpoint."""
        response = client.get("/history/types")
        assert response.status_code == 200

        data = response.json()
        assert "entry_types" in data
        assert "descriptions" in data
        assert "creative_task" in data["entry_types"]

    def test_log_entry_endpoint(self):
        """Test /history/log endpoint."""
        response = client.post(
            "/history/log",
            json={
                "entry_type": "system_event",
                "operation": "test_event",
                "data": {"key": "value"},
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["type"] == "system_event"
        assert data["operation"] == "test_event"

    def test_log_entry_invalid_type(self):
        """Test /history/log with invalid type."""
        response = client.post(
            "/history/log",
            json={
                "entry_type": "invalid_type",
                "operation": "test",
                "data": {},
            }
        )
        assert response.status_code == 400

    def test_get_entries_endpoint(self):
        """Test /history/entries endpoint."""
        response = client.get("/history/entries")
        assert response.status_code == 200

        data = response.json()
        assert "entries" in data
        assert "count" in data

    def test_get_entries_with_filter(self):
        """Test /history/entries with filter."""
        response = client.get("/history/entries?entry_type=tool_usage")
        assert response.status_code == 200

        data = response.json()
        assert data["entry_type_filter"] == "tool_usage"

    def test_session_summary(self):
        """Test /history/session endpoint."""
        response = client.get("/history/session")
        assert response.status_code == 200

        data = response.json()
        assert "session_id" in data
        assert "total_entries" in data

    def test_summary_report(self):
        """Test /history/report/summary endpoint."""
        response = client.get("/history/report/summary")
        assert response.status_code == 200

        data = response.json()
        assert "total_entries" in data
        assert "report_time" in data

    def test_tool_report(self):
        """Test /history/report/tools endpoint."""
        response = client.get("/history/report/tools")
        assert response.status_code == 200

        data = response.json()
        assert "total_tool_uses" in data

    def test_congress_report(self):
        """Test /history/report/congress endpoint."""
        response = client.get("/history/report/congress")
        assert response.status_code == 200

        data = response.json()
        assert "total_votes" in data
        assert "total_contributions" in data

    def test_export_json(self):
        """Test /history/export/json endpoint."""
        response = client.post(
            "/history/export/json",
            json={"limit": 10, "sanitize": True}
        )
        assert response.status_code == 200

        data = response.json()
        assert "entries" in data
        assert "export_time" in data

    def test_export_csv(self):
        """Test /history/export/csv endpoint."""
        response = client.post(
            "/history/export/csv",
            json={"limit": 10, "sanitize": True}
        )
        assert response.status_code == 200

        # Response is plain text CSV
        assert response.headers["content-type"].startswith("text/plain")


class TestLogEntryTypes:
    """Tests for log entry types."""

    def test_all_entry_types_defined(self):
        """Test all entry types are defined."""
        expected_types = [
            "creative_task",
            "tool_usage",
            "brain_execution",
            "congress_contribution",
            "congress_vote",
            "protocol_message",
            "memory_operation",
            "system_event",
        ]

        actual = [t.value for t in LogEntryType]
        for t in expected_types:
            assert t in actual
