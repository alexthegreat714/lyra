"""
Lyra Agent Congress - Contribution Tracker

Tracks Lyra's creative contributions to Congress proceedings.
Phase 5: Congress integration.

GUARDRAILS:
    Lyra's contributions are creative/strategic only:
    - No legal opinions (Sophia's domain)
    - No security assessments (Aegis's domain)
    - No resource calculations (Argus's domain)
    - No health/social evaluations (Mercury's domain)

    Valid contribution types:
    - Creative perspectives
    - Narrative analyses
    - Conceptual reframings
    - Strategic suggestions
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from loguru import logger


class ContributionType(str, Enum):
    """Types of contributions Lyra can make."""
    CREATIVE_PERSPECTIVE = "creative_perspective"
    NARRATIVE_ANALYSIS = "narrative_analysis"
    CONCEPTUAL_REFRAME = "conceptual_reframe"
    STRATEGIC_SUGGESTION = "strategic_suggestion"
    ANALOGY_INSIGHT = "analogy_insight"
    COUNTERFACTUAL_SCENARIO = "counterfactual_scenario"


class ContributionStatus(str, Enum):
    """Status of a contribution."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    INCORPORATED = "incorporated"
    ARCHIVED = "archived"


class ContributionTracker:
    """
    Tracks Lyra's contributions to Congress proceedings.

    Manages contribution lifecycle from draft to incorporation.
    Links contributions to proposals and sessions.

    GUARDRAILS:
        - All contributions must have structured format
        - No emotional content in contributions
        - Contributions stay within creative domain
    """

    def __init__(self):
        """Initialize the contribution tracker."""
        self._contributions: Dict[str, Dict[str, Any]] = {}
        self._session_contributions: Dict[str, List[str]] = {}
        logger.info("ContributionTracker initialized")

    def create_contribution(
        self,
        contribution_type: ContributionType,
        content: Dict[str, Any],
        proposal_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new contribution.

        Args:
            contribution_type: Type of contribution
            content: Structured content of the contribution
            proposal_id: Optional linked proposal
            session_id: Optional Congress session ID
            metadata: Optional additional metadata

        Returns:
            Created contribution record
        """
        contribution_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        contribution = {
            "id": contribution_id,
            "type": contribution_type.value,
            "content": content,
            "proposal_id": proposal_id,
            "session_id": session_id,
            "status": ContributionStatus.DRAFT.value,
            "metadata": metadata or {},
            "created_at": timestamp,
            "updated_at": timestamp,
            "agent": "Lyra",
        }

        self._contributions[contribution_id] = contribution

        # Track session contributions
        if session_id:
            if session_id not in self._session_contributions:
                self._session_contributions[session_id] = []
            self._session_contributions[session_id].append(contribution_id)

        logger.info(
            f"Created contribution {contribution_id} "
            f"(type: {contribution_type.value})"
        )

        return contribution

    def submit_contribution(
        self,
        contribution_id: str
    ) -> Dict[str, Any]:
        """
        Submit a draft contribution to Congress.

        Args:
            contribution_id: ID of the contribution to submit

        Returns:
            Updated contribution record
        """
        contribution = self._contributions.get(contribution_id)

        if not contribution:
            raise ValueError(f"Contribution {contribution_id} not found")

        if contribution["status"] != ContributionStatus.DRAFT.value:
            raise ValueError(
                f"Cannot submit contribution with status {contribution['status']}"
            )

        contribution["status"] = ContributionStatus.SUBMITTED.value
        contribution["updated_at"] = datetime.utcnow().isoformat() + "Z"
        contribution["submitted_at"] = contribution["updated_at"]

        logger.info(f"Submitted contribution {contribution_id}")

        return contribution

    def update_status(
        self,
        contribution_id: str,
        status: ContributionStatus,
        feedback: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update the status of a contribution.

        Args:
            contribution_id: ID of the contribution
            status: New status
            feedback: Optional feedback from Congress

        Returns:
            Updated contribution record
        """
        contribution = self._contributions.get(contribution_id)

        if not contribution:
            raise ValueError(f"Contribution {contribution_id} not found")

        contribution["status"] = status.value
        contribution["updated_at"] = datetime.utcnow().isoformat() + "Z"

        if feedback:
            if "feedback_history" not in contribution:
                contribution["feedback_history"] = []
            contribution["feedback_history"].append({
                "status": status.value,
                "feedback": feedback,
                "timestamp": contribution["updated_at"],
            })

        logger.info(
            f"Updated contribution {contribution_id} status to {status.value}"
        )

        return contribution

    def create_creative_perspective(
        self,
        topic: str,
        perspectives: List[Dict[str, str]],
        proposal_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a creative perspective contribution.

        Args:
            topic: Topic being addressed
            perspectives: List of perspectives with angle and insight
            proposal_id: Optional linked proposal
            session_id: Optional session ID

        Returns:
            Created contribution
        """
        content = {
            "topic": topic,
            "perspectives": perspectives,
            "perspective_count": len(perspectives),
        }

        return self.create_contribution(
            contribution_type=ContributionType.CREATIVE_PERSPECTIVE,
            content=content,
            proposal_id=proposal_id,
            session_id=session_id,
        )

    def create_narrative_analysis(
        self,
        subject: str,
        narrative_elements: Dict[str, Any],
        proposal_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a narrative analysis contribution.

        Args:
            subject: Subject of analysis
            narrative_elements: Identified narrative elements
            proposal_id: Optional linked proposal
            session_id: Optional session ID

        Returns:
            Created contribution
        """
        content = {
            "subject": subject,
            "narrative_elements": narrative_elements,
            "analysis_type": "narrative",
        }

        return self.create_contribution(
            contribution_type=ContributionType.NARRATIVE_ANALYSIS,
            content=content,
            proposal_id=proposal_id,
            session_id=session_id,
        )

    def create_conceptual_reframe(
        self,
        original_framing: str,
        reframed_perspectives: List[Dict[str, str]],
        proposal_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a conceptual reframe contribution.

        Args:
            original_framing: The original framing to reframe
            reframed_perspectives: Alternative perspectives
            proposal_id: Optional linked proposal
            session_id: Optional session ID

        Returns:
            Created contribution
        """
        content = {
            "original_framing": original_framing,
            "reframed_perspectives": reframed_perspectives,
            "reframe_count": len(reframed_perspectives),
        }

        return self.create_contribution(
            contribution_type=ContributionType.CONCEPTUAL_REFRAME,
            content=content,
            proposal_id=proposal_id,
            session_id=session_id,
        )

    def get_contribution(self, contribution_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific contribution.

        Args:
            contribution_id: ID of the contribution

        Returns:
            Contribution record or None
        """
        return self._contributions.get(contribution_id)

    def get_contributions_by_session(
        self,
        session_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all contributions for a session.

        Args:
            session_id: Congress session ID

        Returns:
            List of contributions
        """
        contribution_ids = self._session_contributions.get(session_id, [])
        return [
            self._contributions[cid]
            for cid in contribution_ids
            if cid in self._contributions
        ]

    def get_contributions_by_proposal(
        self,
        proposal_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all contributions for a proposal.

        Args:
            proposal_id: Proposal ID

        Returns:
            List of contributions
        """
        return [
            c for c in self._contributions.values()
            if c.get("proposal_id") == proposal_id
        ]

    def get_contributions_by_status(
        self,
        status: ContributionStatus
    ) -> List[Dict[str, Any]]:
        """
        Get contributions by status.

        Args:
            status: Status to filter by

        Returns:
            List of contributions
        """
        return [
            c for c in self._contributions.values()
            if c.get("status") == status.value
        ]

    def get_contribution_stats(self) -> Dict[str, Any]:
        """
        Get contribution statistics.

        Returns:
            Dict with contribution statistics
        """
        total = len(self._contributions)

        by_type = {}
        by_status = {}

        for c in self._contributions.values():
            # Count by type
            ctype = c.get("type", "unknown")
            by_type[ctype] = by_type.get(ctype, 0) + 1

            # Count by status
            status = c.get("status", "unknown")
            by_status[status] = by_status.get(status, 0) + 1

        incorporated = by_status.get(ContributionStatus.INCORPORATED.value, 0)

        return {
            "total_contributions": total,
            "by_type": by_type,
            "by_status": by_status,
            "incorporation_rate": round(incorporated / total, 2) if total > 0 else 0,
            "sessions_participated": len(self._session_contributions),
        }
