"""
Lyra Agent History Routes

API endpoints for creative history access and export.
Phase 7: History logging and export.

GUARDRAILS:
    History endpoints provide access to creative outputs only:
    - No user personal information
    - No cross-agent confidential data
    - Sanitized exports available
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
from loguru import logger
from pydantic import BaseModel, Field

from app.history.logger import CreativeHistoryLogger, LogEntryType
from app.history.exporter import HistoryExporter


router = APIRouter(prefix="/history", tags=["history"])

# Initialize logger and exporter
history_logger = CreativeHistoryLogger()
exporter = HistoryExporter()


# Request/Response Models

class LogEntryRequest(BaseModel):
    """Request model for logging an entry."""
    entry_type: str = Field(..., description="Type of log entry")
    operation: str = Field(..., description="Operation name")
    data: Dict[str, Any] = Field(default_factory=dict, description="Entry data")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")


class ExportRequest(BaseModel):
    """Request model for export operations."""
    entry_type: Optional[str] = Field(None, description="Filter by entry type")
    limit: int = Field(default=100, ge=1, le=1000, description="Max entries")
    sanitize: bool = Field(default=True, description="Sanitize sensitive data")


# Logging Endpoints

@router.post("/log")
async def log_entry(request: LogEntryRequest) -> Dict[str, Any]:
    """
    Log a custom history entry.

    Args:
        request: Log entry details

    Returns:
        Created log entry
    """
    logger.info(f"Logging entry: {request.entry_type} - {request.operation}")

    try:
        entry_type = LogEntryType(request.entry_type)
    except ValueError:
        valid_types = [t.value for t in LogEntryType]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid entry type. Valid types: {valid_types}"
        )

    entry = history_logger.log(
        entry_type=entry_type,
        operation=request.operation,
        data=request.data,
        metadata=request.metadata,
    )

    return entry


@router.post("/log/creative_task")
async def log_creative_task(
    task_type: str,
    prompt: str,
    result: Dict[str, Any],
    duration_ms: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Log a creative task execution.

    Args:
        task_type: Type of creative task
        prompt: Task prompt
        result: Task result
        duration_ms: Optional execution duration

    Returns:
        Log entry
    """
    return history_logger.log_creative_task(
        task_type=task_type,
        prompt=prompt,
        result=result,
        duration_ms=duration_ms,
    )


@router.post("/log/tool_usage")
async def log_tool_usage(
    tool_name: str,
    input_summary: str,
    output_summary: str,
    success: bool = True,
) -> Dict[str, Any]:
    """
    Log a tool usage event.

    Args:
        tool_name: Name of the tool
        input_summary: Summary of input
        output_summary: Summary of output
        success: Whether successful

    Returns:
        Log entry
    """
    return history_logger.log_tool_usage(
        tool_name=tool_name,
        input_summary=input_summary,
        output_summary=output_summary,
        success=success,
    )


# Query Endpoints

@router.get("/entries")
async def get_entries(
    entry_type: Optional[str] = None,
    limit: int = Query(default=100, ge=1, le=500),
    since: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get history log entries.

    Args:
        entry_type: Optional filter by entry type
        limit: Maximum entries to return
        since: Optional ISO timestamp filter

    Returns:
        List of log entries
    """
    type_filter = None
    if entry_type:
        try:
            type_filter = LogEntryType(entry_type)
        except ValueError:
            valid_types = [t.value for t in LogEntryType]
            raise HTTPException(
                status_code=400,
                detail=f"Invalid entry type. Valid types: {valid_types}"
            )

    entries = history_logger.get_entries(
        entry_type=type_filter,
        limit=limit,
        since=since,
    )

    return {
        "entries": entries,
        "count": len(entries),
        "entry_type_filter": entry_type,
    }


@router.get("/session")
async def get_session_summary() -> Dict[str, Any]:
    """
    Get summary of the current session.

    Returns:
        Session summary statistics
    """
    return history_logger.get_session_summary()


# Export Endpoints

@router.post("/export/json")
async def export_json(request: ExportRequest) -> Dict[str, Any]:
    """
    Export history entries as JSON.

    Args:
        request: Export parameters

    Returns:
        JSON export data
    """
    type_filter = None
    if request.entry_type:
        try:
            type_filter = LogEntryType(request.entry_type)
        except ValueError:
            pass

    entries = history_logger.get_entries(
        entry_type=type_filter,
        limit=request.limit,
    )

    json_str = exporter.export_to_json(
        entries=entries,
        sanitize=request.sanitize,
    )

    # Return parsed JSON
    import json
    return json.loads(json_str)


@router.post("/export/csv", response_class=PlainTextResponse)
async def export_csv(request: ExportRequest) -> str:
    """
    Export history entries as CSV.

    Args:
        request: Export parameters

    Returns:
        CSV string
    """
    type_filter = None
    if request.entry_type:
        try:
            type_filter = LogEntryType(request.entry_type)
        except ValueError:
            pass

    entries = history_logger.get_entries(
        entry_type=type_filter,
        limit=request.limit,
    )

    return exporter.export_to_csv(
        entries=entries,
        sanitize=request.sanitize,
    )


# Report Endpoints

@router.get("/report/summary")
async def get_summary_report() -> Dict[str, Any]:
    """
    Get a summary report of all history.

    Returns:
        Summary report
    """
    entries = history_logger.get_entries(limit=1000)
    return exporter.generate_summary_report(entries)


@router.get("/report/tools")
async def get_tool_report() -> Dict[str, Any]:
    """
    Get a tool usage report.

    Returns:
        Tool usage report
    """
    entries = history_logger.get_entries(limit=1000)
    return exporter.generate_tool_usage_report(entries)


@router.get("/report/congress")
async def get_congress_report() -> Dict[str, Any]:
    """
    Get a Congress participation report.

    Returns:
        Congress participation report
    """
    entries = history_logger.get_entries(limit=1000)
    return exporter.generate_congress_report(entries)


# Management Endpoints

@router.post("/flush")
async def flush_to_file() -> Dict[str, Any]:
    """
    Flush current entries to a log file.

    Returns:
        Path to created file
    """
    filepath = history_logger.flush_to_file()

    if not filepath:
        return {"status": "empty", "message": "No entries to flush"}

    return {
        "status": "flushed",
        "filepath": filepath,
        "entry_count": len(history_logger._entries),
    }


@router.post("/clear")
async def clear_history() -> Dict[str, Any]:
    """
    Clear in-memory history entries.

    Returns:
        Confirmation
    """
    history_logger.clear()
    return {"status": "cleared"}


@router.get("/stats")
async def get_history_stats() -> Dict[str, Any]:
    """
    Get history statistics.

    Returns:
        Combined session and export statistics
    """
    return {
        "session": history_logger.get_session_summary(),
        "export": exporter.get_export_stats(),
        "entry_types": [t.value for t in LogEntryType],
    }


@router.get("/types")
async def list_entry_types() -> Dict[str, Any]:
    """
    List available entry types.

    Returns:
        Available entry types with descriptions
    """
    return {
        "entry_types": [t.value for t in LogEntryType],
        "descriptions": {
            "creative_task": "Creative task execution records",
            "tool_usage": "Tool usage events",
            "brain_execution": "Brain pipeline executions",
            "congress_contribution": "Congress contributions",
            "congress_vote": "Congress votes",
            "protocol_message": "Sky protocol messages",
            "memory_operation": "Memory operations",
            "system_event": "System events",
        },
    }
