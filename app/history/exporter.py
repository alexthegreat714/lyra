"""
Lyra Agent - History Exporter

Export creative history in various formats.
Phase 7: History export for analysis and audit.

GUARDRAILS:
    Exported data contains creative outputs only:
    - No user personal information
    - No cross-agent confidential data
    - Sanitized for external sharing if needed

    Supports:
    - JSON export
    - CSV export
    - Summary reports
"""

import csv
import json
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


class HistoryExporter:
    """
    Exporter for Lyra's creative history.

    Provides export functionality in multiple formats:
    - JSON (full data)
    - CSV (tabular view)
    - Summary reports

    GUARDRAILS:
        - Sanitizes data before export
        - No personal information included
        - Configurable field filtering
    """

    # Fields that may contain sensitive data (to be sanitized)
    SANITIZE_FIELDS = ["user_data", "personal_info", "credentials"]

    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialize the exporter.

        Args:
            log_dir: Directory containing history logs
        """
        self.log_dir = log_dir or Path(__file__).parent.parent / "logs" / "history"
        logger.info("HistoryExporter initialized")

    def export_to_json(
        self,
        entries: List[Dict[str, Any]],
        output_path: Optional[str] = None,
        sanitize: bool = True,
    ) -> str:
        """
        Export entries to JSON format.

        Args:
            entries: Log entries to export
            output_path: Optional file path (returns string if None)
            sanitize: Whether to sanitize sensitive fields

        Returns:
            JSON string or file path
        """
        if sanitize:
            entries = [self._sanitize_entry(e) for e in entries]

        export_data = {
            "export_time": datetime.utcnow().isoformat() + "Z",
            "entry_count": len(entries),
            "agent": "Lyra",
            "entries": entries,
        }

        json_str = json.dumps(export_data, indent=2)

        if output_path:
            with open(output_path, "w") as f:
                f.write(json_str)
            logger.info(f"Exported {len(entries)} entries to {output_path}")
            return output_path

        return json_str

    def export_to_csv(
        self,
        entries: List[Dict[str, Any]],
        output_path: Optional[str] = None,
        sanitize: bool = True,
    ) -> str:
        """
        Export entries to CSV format.

        Args:
            entries: Log entries to export
            output_path: Optional file path (returns string if None)
            sanitize: Whether to sanitize sensitive fields

        Returns:
            CSV string or file path
        """
        if not entries:
            return ""

        if sanitize:
            entries = [self._sanitize_entry(e) for e in entries]

        # Flatten entries for CSV
        flat_entries = [self._flatten_entry(e) for e in entries]

        # Get all unique columns
        columns = set()
        for entry in flat_entries:
            columns.update(entry.keys())
        columns = sorted(columns)

        # Write CSV
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(flat_entries)

        csv_str = output.getvalue()

        if output_path:
            with open(output_path, "w") as f:
                f.write(csv_str)
            logger.info(f"Exported {len(entries)} entries to CSV: {output_path}")
            return output_path

        return csv_str

    def generate_summary_report(
        self,
        entries: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate a summary report from entries.

        Args:
            entries: Log entries to summarize

        Returns:
            Summary report dictionary
        """
        if not entries:
            return {"total_entries": 0, "report_time": datetime.utcnow().isoformat() + "Z"}

        # Count by type
        by_type = {}
        for entry in entries:
            etype = entry.get("type", "unknown")
            by_type[etype] = by_type.get(etype, 0) + 1

        # Count by operation
        by_operation = {}
        for entry in entries:
            op = entry.get("operation", "unknown")
            by_operation[op] = by_operation.get(op, 0) + 1

        # Time range
        timestamps = [e.get("timestamp", "") for e in entries if e.get("timestamp")]
        timestamps.sort()

        # Top operations
        top_operations = sorted(
            by_operation.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return {
            "report_time": datetime.utcnow().isoformat() + "Z",
            "agent": "Lyra",
            "total_entries": len(entries),
            "entries_by_type": by_type,
            "entries_by_operation": by_operation,
            "top_operations": dict(top_operations),
            "time_range": {
                "earliest": timestamps[0] if timestamps else None,
                "latest": timestamps[-1] if timestamps else None,
            },
            "unique_sessions": len(set(e.get("session_id") for e in entries if e.get("session_id"))),
        }

    def generate_tool_usage_report(
        self,
        entries: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate a tool usage report.

        Args:
            entries: Log entries to analyze

        Returns:
            Tool usage report
        """
        tool_entries = [e for e in entries if e.get("type") == "tool_usage"]

        tool_counts = {}
        tool_success = {}

        for entry in tool_entries:
            data = entry.get("data", {})
            tool = data.get("tool", "unknown")

            tool_counts[tool] = tool_counts.get(tool, 0) + 1

            if data.get("success", True):
                tool_success[tool] = tool_success.get(tool, 0) + 1

        # Calculate success rates
        success_rates = {}
        for tool, count in tool_counts.items():
            success = tool_success.get(tool, 0)
            success_rates[tool] = round(success / count, 2) if count > 0 else 0

        return {
            "report_time": datetime.utcnow().isoformat() + "Z",
            "total_tool_uses": len(tool_entries),
            "tool_counts": tool_counts,
            "success_rates": success_rates,
            "most_used": max(tool_counts.items(), key=lambda x: x[1])[0] if tool_counts else None,
        }

    def generate_congress_report(
        self,
        entries: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate a Congress participation report.

        Args:
            entries: Log entries to analyze

        Returns:
            Congress participation report
        """
        vote_entries = [e for e in entries if e.get("type") == "congress_vote"]
        contrib_entries = [e for e in entries if e.get("type") == "congress_contribution"]

        # Vote analysis
        vote_counts = {}
        auto_abstains = 0
        domains = set()

        for entry in vote_entries:
            data = entry.get("data", {})
            vote = data.get("vote", "unknown")
            vote_counts[vote] = vote_counts.get(vote, 0) + 1

            if data.get("auto_abstain"):
                auto_abstains += 1

            if data.get("domain"):
                domains.add(data["domain"])

        # Contribution analysis
        contribution_types = {}
        for entry in contrib_entries:
            data = entry.get("data", {})
            ctype = data.get("contribution_type", "unknown")
            contribution_types[ctype] = contribution_types.get(ctype, 0) + 1

        return {
            "report_time": datetime.utcnow().isoformat() + "Z",
            "total_votes": len(vote_entries),
            "vote_breakdown": vote_counts,
            "auto_abstains": auto_abstains,
            "domains_participated": list(domains),
            "total_contributions": len(contrib_entries),
            "contribution_types": contribution_types,
        }

    def load_log_files(
        self,
        since: Optional[datetime] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Load entries from log files.

        Args:
            since: Only load files created after this time
            limit: Maximum number of files to load

        Returns:
            Combined list of entries
        """
        if not self.log_dir.exists():
            return []

        entries = []
        files = sorted(self.log_dir.glob("history_*.json"), reverse=True)[:limit]

        for filepath in files:
            try:
                # Check file modification time
                if since:
                    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                    if mtime < since:
                        continue

                with open(filepath, "r") as f:
                    data = json.load(f)
                    entries.extend(data.get("entries", []))

            except Exception as e:
                logger.warning(f"Failed to load log file {filepath}: {e}")
                continue

        return entries

    def _sanitize_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize an entry by removing sensitive fields."""
        sanitized = entry.copy()

        # Remove sensitive fields
        for field in self.SANITIZE_FIELDS:
            if field in sanitized:
                del sanitized[field]
            if "data" in sanitized and field in sanitized.get("data", {}):
                del sanitized["data"][field]
            if "metadata" in sanitized and field in sanitized.get("metadata", {}):
                del sanitized["metadata"][field]

        return sanitized

    def _flatten_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten nested entry for CSV export."""
        flat = {
            "entry_id": entry.get("entry_id"),
            "session_id": entry.get("session_id"),
            "type": entry.get("type"),
            "operation": entry.get("operation"),
            "timestamp": entry.get("timestamp"),
        }

        # Flatten data fields
        data = entry.get("data", {})
        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                flat[f"data_{key}"] = value
            elif isinstance(value, list):
                flat[f"data_{key}"] = str(len(value)) + " items"
            elif isinstance(value, dict):
                flat[f"data_{key}"] = str(len(value)) + " fields"

        # Flatten metadata fields
        metadata = entry.get("metadata", {})
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                flat[f"meta_{key}"] = value

        return flat

    def get_export_stats(self) -> Dict[str, Any]:
        """
        Get statistics about available log files.

        Returns:
            Export statistics
        """
        if not self.log_dir.exists():
            return {"log_dir": str(self.log_dir), "files": 0, "total_size_bytes": 0}

        files = list(self.log_dir.glob("history_*.json"))
        total_size = sum(f.stat().st_size for f in files)

        return {
            "log_dir": str(self.log_dir),
            "files": len(files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }
