"""
Lyra Agent Congress - Voting Module

Voting mechanisms for multi-agent collaboration.
Phase 5: Congress integration.

GUARDRAILS:
    Lyra participates in Congress for creative strategy only:
    - No voting on legal matters (Sophia's domain)
    - No voting on security protocols (Aegis's domain)
    - No voting on resource allocation (Argus's domain)
    - No voting on health/social matters (Mercury's domain)

    Lyra's voting is based on:
    - Creative merit of proposals
    - Strategic narrative coherence
    - Conceptual alignment with creative goals
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from loguru import logger


class VoteType(str, Enum):
    """Valid vote types for Lyra."""
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"
    DEFER = "defer"  # Defer to another agent's expertise


class VotingDomain(str, Enum):
    """Domains where Lyra can vote."""
    CREATIVE = "creative"
    NARRATIVE = "narrative"
    CONCEPTUAL = "conceptual"
    STRATEGIC = "strategic"


# Domains Lyra must abstain from (other agents' expertise)
RESTRICTED_DOMAINS = [
    "legal",       # Sophia
    "security",    # Aegis
    "compute",     # Argus
    "resource",    # Argus
    "health",      # Mercury
    "social",      # Mercury
    "factual",     # Veritas
]


class VotingModule:
    """
    Lyra's voting module for Congress participation.

    Handles vote casting, vote records, and domain validation.
    Ensures Lyra only votes on matters within creative domain.

    GUARDRAILS:
        - Auto-abstain on restricted domains
        - No emotional reasoning in votes
        - All votes include structured rationale
    """

    def __init__(self):
        """Initialize the voting module."""
        self._vote_history: List[Dict[str, Any]] = []
        self._pending_votes: Dict[str, Dict[str, Any]] = {}
        logger.info("VotingModule initialized")

    def cast_vote(
        self,
        proposal_id: str,
        vote: VoteType,
        domain: str,
        rationale: Dict[str, Any],
        proposal_summary: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Cast a vote on a proposal.

        Args:
            proposal_id: ID of the proposal to vote on
            vote: The vote type (approve, reject, abstain, defer)
            domain: Domain of the proposal
            rationale: Structured rationale for the vote
            proposal_summary: Optional summary of the proposal

        Returns:
            Vote record with validation status
        """
        # Check if domain is restricted
        if self._is_restricted_domain(domain):
            logger.info(
                f"Auto-abstaining from proposal {proposal_id} "
                f"(restricted domain: {domain})"
            )
            return self._create_abstention(
                proposal_id=proposal_id,
                domain=domain,
                reason=f"Domain '{domain}' outside Lyra's expertise",
            )

        # Create vote record
        vote_record = {
            "vote_id": str(uuid4()),
            "proposal_id": proposal_id,
            "vote": vote.value,
            "domain": domain,
            "rationale": rationale,
            "proposal_summary": proposal_summary,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "Lyra",
            "valid": True,
        }

        self._vote_history.append(vote_record)
        logger.info(f"Vote cast: {vote.value} on proposal {proposal_id}")

        return vote_record

    def evaluate_proposal(
        self,
        proposal_id: str,
        proposal_content: str,
        domain: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate a proposal from a creative perspective.

        Args:
            proposal_id: ID of the proposal
            proposal_content: Content/description of the proposal
            domain: Domain of the proposal
            context: Optional additional context

        Returns:
            Evaluation with creative assessment and suggested vote
        """
        # Check domain restriction
        if self._is_restricted_domain(domain):
            return {
                "proposal_id": proposal_id,
                "evaluable": False,
                "reason": f"Domain '{domain}' outside Lyra's expertise",
                "suggested_vote": VoteType.ABSTAIN.value,
                "defer_to": self._get_domain_expert(domain),
            }

        # Creative evaluation criteria
        evaluation = {
            "proposal_id": proposal_id,
            "evaluable": True,
            "domain": domain,
            "assessment": self._assess_creative_merit(proposal_content),
            "suggested_vote": None,
            "rationale": {},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        # Determine suggested vote based on assessment
        assessment = evaluation["assessment"]
        score = assessment.get("overall_score", 0.5)

        if score >= 0.7:
            evaluation["suggested_vote"] = VoteType.APPROVE.value
        elif score <= 0.3:
            evaluation["suggested_vote"] = VoteType.REJECT.value
        else:
            evaluation["suggested_vote"] = VoteType.ABSTAIN.value

        evaluation["rationale"] = {
            "creative_merit": assessment.get("creative_merit", "neutral"),
            "narrative_coherence": assessment.get("narrative_coherence", "neutral"),
            "strategic_alignment": assessment.get("strategic_alignment", "neutral"),
        }

        return evaluation

    def _is_restricted_domain(self, domain: str) -> bool:
        """Check if domain is restricted for Lyra."""
        domain_lower = domain.lower()
        return any(
            restricted in domain_lower
            for restricted in RESTRICTED_DOMAINS
        )

    def _get_domain_expert(self, domain: str) -> Optional[str]:
        """Get the expert agent for a domain."""
        domain_lower = domain.lower()

        if "legal" in domain_lower:
            return "Sophia"
        if "security" in domain_lower:
            return "Aegis"
        if "compute" in domain_lower or "resource" in domain_lower:
            return "Argus"
        if "health" in domain_lower or "social" in domain_lower:
            return "Mercury"
        if "factual" in domain_lower:
            return "Veritas"

        return None

    def _assess_creative_merit(self, content: str) -> Dict[str, Any]:
        """
        Assess the creative merit of proposal content.

        This is a structured assessment, not emotional inference.

        Args:
            content: Proposal content to assess

        Returns:
            Assessment metrics
        """
        # Simple heuristic-based assessment
        # In production, this could use LyraBrain tools

        words = content.lower().split() if content else []
        word_count = len(words)

        # Creative indicators (not exhaustive)
        creative_words = {
            "innovative", "creative", "novel", "unique", "original",
            "transform", "reimagine", "explore", "discover", "design",
        }

        # Strategic indicators
        strategic_words = {
            "strategy", "approach", "framework", "methodology", "process",
            "plan", "vision", "goal", "objective", "outcome",
        }

        # Narrative indicators
        narrative_words = {
            "story", "narrative", "journey", "experience", "arc",
            "theme", "motif", "structure", "flow", "progression",
        }

        creative_count = sum(1 for w in words if w in creative_words)
        strategic_count = sum(1 for w in words if w in strategic_words)
        narrative_count = sum(1 for w in words if w in narrative_words)

        # Calculate scores (0.0 to 1.0)
        base_score = 0.5

        if word_count > 0:
            creative_score = min(1.0, base_score + (creative_count / word_count) * 2)
            strategic_score = min(1.0, base_score + (strategic_count / word_count) * 2)
            narrative_score = min(1.0, base_score + (narrative_count / word_count) * 2)
        else:
            creative_score = strategic_score = narrative_score = 0.5

        overall = (creative_score + strategic_score + narrative_score) / 3

        return {
            "creative_merit": self._score_to_label(creative_score),
            "creative_score": round(creative_score, 2),
            "narrative_coherence": self._score_to_label(narrative_score),
            "narrative_score": round(narrative_score, 2),
            "strategic_alignment": self._score_to_label(strategic_score),
            "strategic_score": round(strategic_score, 2),
            "overall_score": round(overall, 2),
            "word_count": word_count,
        }

    def _score_to_label(self, score: float) -> str:
        """Convert a score to a qualitative label."""
        if score >= 0.7:
            return "strong"
        if score >= 0.5:
            return "moderate"
        if score >= 0.3:
            return "weak"
        return "minimal"

    def _create_abstention(
        self,
        proposal_id: str,
        domain: str,
        reason: str
    ) -> Dict[str, Any]:
        """Create an abstention vote record."""
        vote_record = {
            "vote_id": str(uuid4()),
            "proposal_id": proposal_id,
            "vote": VoteType.ABSTAIN.value,
            "domain": domain,
            "rationale": {"reason": reason},
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "Lyra",
            "valid": True,
            "auto_abstain": True,
        }

        self._vote_history.append(vote_record)
        return vote_record

    def get_vote_history(
        self,
        limit: int = 50,
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get vote history.

        Args:
            limit: Maximum records to return
            domain: Optional domain filter

        Returns:
            List of vote records
        """
        history = self._vote_history

        if domain:
            history = [v for v in history if v.get("domain") == domain]

        return history[-limit:]

    def get_voting_stats(self) -> Dict[str, Any]:
        """
        Get voting statistics.

        Returns:
            Dict with voting statistics
        """
        total = len(self._vote_history)
        approvals = sum(1 for v in self._vote_history if v["vote"] == "approve")
        rejections = sum(1 for v in self._vote_history if v["vote"] == "reject")
        abstentions = sum(1 for v in self._vote_history if v["vote"] == "abstain")
        deferrals = sum(1 for v in self._vote_history if v["vote"] == "defer")

        return {
            "total_votes": total,
            "approvals": approvals,
            "rejections": rejections,
            "abstentions": abstentions,
            "deferrals": deferrals,
            "approval_rate": round(approvals / total, 2) if total > 0 else 0,
        }
