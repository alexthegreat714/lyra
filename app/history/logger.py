"""
Lyra Agent - Creative History Logger

Logs creative task executions, tool usage, and contributions.
Phase 7: History logging for audit and analysis.

GUARDRAILS:
    Logged items are creative outputs only:
    - No user personal information
    - No cross-agent confidential data
    - No security incident details (Aegis)
    - No health records (Mercury)

    Logs support:
    - Creative task tracking
    - Tool usage analytics
    - Contribution audit trail
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from loguru import logger


class LogEntryType(str, Enum):
    """Types of log entries."""
    CREATIVE_TASK = "creative_task"
    TOOL_USAGE = "tool_usage"
    BRAIN_EXECUTION = "brain_execution"
    CONGRESS_CONTRIBUTION = "congress_contribution"
    CONGRESS_VOTE = "congress_vote"
    PROTOCOL_MESSAGE = "protocol_message"
    MEMORY_OPERATION = "memory_operation"
    SYSTEM_EVENT = "system_event"


class CreativeHistoryLogger:
    """
    Logger for Lyra's creative history.

    Maintains an audit trail of creative operations for:
    - Performance analysis
    - Usage patterns
    - Contribution tracking
    - Debugging

    GUARDRAILS:
        - Only logs creative/strategic content
        - No personal user data
        - No cross-agent confidential info
    """

    # Log file location
    LOG_DIR = Path(__file__).parent.parent / "logs" / "history"

    def __init__(self, max_memory_entries: int = 1000):
        """
        Initialize the history logger.

        Args:
            max_memory_entries: Maximum entries to keep in memory
        """
        self._entries: List[Dict[str, Any]] = []
        self._max_entries = max_memory_entries
        self._session_id = str(uuid4())
        self._session_start = datetime.utcnow().isoformat() + "Z"

        # Ensure log directory exists
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

        logger.info(f"CreativeHistoryLogger initialized (session: {self._session_id})")

    def log(
        self,
        entry_type: LogEntryType,
        operation: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Log an entry to the history.

        Args:
            entry_type: Type of log entry
            operation: Name of the operation
            data: Data to log
            metadata: Optional additional metadata

        Returns:
            The created log entry
        """
        entry = {
            "entry_id": str(uuid4()),
            "session_id": self._session_id,
            "type": entry_type.value,
            "operation": operation,
            "data": data,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        # Add to memory buffer
        self._entries.append(entry)

        # Trim if over limit
        if len(self._entries) > self._max_entries:
            self._entries = self._entries[-self._max_entries:]

        logger.debug(f"Logged {entry_type.value}: {operation}")

        return entry

    def log_creative_task(
        self,
        task_type: str,
        prompt: str,
        result: Dict[str, Any],
        duration_ms: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Log a creative task execution.

        Args:
            task_type: Type of creative task
            prompt: Input prompt
            result: Task result
            duration_ms: Optional execution duration

        Returns:
            Log entry
        """
        return self.log(
            entry_type=LogEntryType.CREATIVE_TASK,
            operation=task_type,
            data={
                "task_type": task_type,
                "prompt_length": len(prompt),
                "result_summary": self._summarize_result(result),
            },
            metadata={"duration_ms": duration_ms} if duration_ms else {},
        )

    def log_tool_usage(
        self,
        tool_name: str,
        input_summary: str,
        output_summary: str,
        success: bool = True,
    ) -> Dict[str, Any]:
        """
        Log a tool usage event.

        Args:
            tool_name: Name of the tool used
            input_summary: Summary of input
            output_summary: Summary of output
            success: Whether tool succeeded

        Returns:
            Log entry
        """
        return self.log(
            entry_type=LogEntryType.TOOL_USAGE,
            operation=tool_name,
            data={
                "tool": tool_name,
                "input_summary": input_summary,
                "output_summary": output_summary,
                "success": success,
            },
        )

    def log_brain_execution(
        self,
        task_type: str,
        stages_completed: List[str],
        tools_used: List[str],
        memory_items_retrieved: int = 0,
    ) -> Dict[str, Any]:
        """
        Log a brain execution pipeline.

        Args:
            task_type: Type of task executed
            stages_completed: Pipeline stages completed
            tools_used: Tools used in execution
            memory_items_retrieved: Number of memory items retrieved

        Returns:
            Log entry
        """
        return self.log(
            entry_type=LogEntryType.BRAIN_EXECUTION,
            operation="brain_pipeline",
            data={
                "task_type": task_type,
                "stages": stages_completed,
                "tools": tools_used,
                "memory_items": memory_items_retrieved,
            },
        )

    def log_congress_contribution(
        self,
        contribution_type: str,
        contribution_id: str,
        proposal_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Log a Congress contribution.

        Args:
            contribution_type: Type of contribution
            contribution_id: ID of the contribution
            proposal_id: Related proposal ID
            session_id: Congress session ID

        Returns:
            Log entry
        """
        return self.log(
            entry_type=LogEntryType.CONGRESS_CONTRIBUTION,
            operation=contribution_type,
            data={
                "contribution_id": contribution_id,
                "contribution_type": contribution_type,
                "proposal_id": proposal_id,
                "congress_session_id": session_id,
            },
        )

    def log_congress_vote(
        self,
        proposal_id: str,
        vote: str,
        domain: str,
        auto_abstain: bool = False,
    ) -> Dict[str, Any]:
        """
        Log a Congress vote.

        Args:
            proposal_id: ID of the proposal
            vote: Vote cast
            domain: Domain of the proposal
            auto_abstain: Whether this was an auto-abstain

        Returns:
            Log entry
        """
        return self.log(
            entry_type=LogEntryType.CONGRESS_VOTE,
            operation="vote",
            data={
                "proposal_id": proposal_id,
                "vote": vote,
                "domain": domain,
                "auto_abstain": auto_abstain,
            },
        )

    def log_protocol_message(
        self,
        message_type: str,
        direction: str,  # "incoming" or "outgoing"
        source: str,
        destination: str,
    ) -> Dict[str, Any]:
        """
        Log a protocol message.

        Args:
            message_type: Type of message
            direction: Message direction
            source: Message source
            destination: Message destination

        Returns:
            Log entry
        """
        return self.log(
            entry_type=LogEntryType.PROTOCOL_MESSAGE,
            operation=message_type,
            data={
                "message_type": message_type,
                "direction": direction,
                "source": source,
                "destination": destination,
            },
        )

    def log_memory_operation(
        self,
        operation: str,  # "ingest" or "retrieve"
        category: Optional[str] = None,
        item_count: int = 0,
    ) -> Dict[str, Any]:
        """
        Log a memory operation.

        Args:
            operation: Type of operation
            category: Memory category
            item_count: Number of items involved

        Returns:
            Log entry
        """
        return self.log(
            entry_type=LogEntryType.MEMORY_OPERATION,
            operation=operation,
            data={
                "operation": operation,
                "category": category,
                "item_count": item_count,
            },
        )

    def log_system_event(
        self,
        event: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Log a system event.

        Args:
            event: Event name
            details: Event details

        Returns:
            Log entry
        """
        return self.log(
            entry_type=LogEntryType.SYSTEM_EVENT,
            operation=event,
            data=details or {},
        )

    def _summarize_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize a result for logging (remove large data)."""
        summary = {}

        for key, value in result.items():
            if isinstance(value, list):
                summary[key] = f"[{len(value)} items]"
            elif isinstance(value, dict):
                summary[key] = f"{{...}} ({len(value)} keys)"
            elif isinstance(value, str) and len(value) > 100:
                summary[key] = value[:100] + "..."
            else:
                summary[key] = value

        return summary

    def get_entries(
        self,
        entry_type: Optional[LogEntryType] = None,
        limit: int = 100,
        since: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get log entries.

        Args:
            entry_type: Optional filter by entry type
            limit: Maximum entries to return
            since: Optional ISO timestamp filter

        Returns:
            List of log entries
        """
        entries = self._entries

        if entry_type:
            entries = [e for e in entries if e["type"] == entry_type.value]

        if since:
            entries = [e for e in entries if e["timestamp"] >= since]

        return entries[-limit:]

    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current session.

        Returns:
            Session summary statistics
        """
        by_type = {}
        for entry in self._entries:
            etype = entry["type"]
            by_type[etype] = by_type.get(etype, 0) + 1

        return {
            "session_id": self._session_id,
            "session_start": self._session_start,
            "total_entries": len(self._entries),
            "entries_by_type": by_type,
        }

    def flush_to_file(self) -> str:
        """
        Flush current entries to a log file.

        Returns:
            Path to the created log file
        """
        if not self._entries:
            return ""

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"history_{self._session_id}_{timestamp}.json"
        filepath = self.LOG_DIR / filename

        log_data = {
            "session_id": self._session_id,
            "session_start": self._session_start,
            "export_time": datetime.utcnow().isoformat() + "Z",
            "entry_count": len(self._entries),
            "entries": self._entries,
        }

        with open(filepath, "w") as f:
            json.dump(log_data, f, indent=2)

        logger.info(f"Flushed {len(self._entries)} entries to {filepath}")

        return str(filepath)

    def clear(self):
        """Clear the in-memory log entries."""
        self._entries = []
        logger.info("History log cleared")
