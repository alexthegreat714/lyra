"""
Lyra Agent Congress - Bill Interface

Interface for analyzing and providing creative input on bills/proposals.
Phase 5: Congress integration.

GUARDRAILS:
    Lyra analyzes bills from creative perspective only:
    - No legal interpretation (Sophia's domain)
    - No security impact assessment (Aegis's domain)
    - No resource impact calculation (Argus's domain)
    - No health/social impact assessment (Mercury's domain)

    Lyra's bill analysis focuses on:
    - Creative potential of proposals
    - Narrative structure and clarity
    - Strategic coherence
    - Conceptual framing effectiveness
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from loguru import logger


class BillInterface:
    """
    Interface for Lyra to analyze and comment on Congress bills/proposals.

    Provides creative perspective on proposals without overstepping
    into other agents' domains.

    GUARDRAILS:
        - Only creative/narrative/strategic analysis
        - No legal, security, resource, or health assessments
        - Structured output format
    """

    # Domains that require deferral to other agents
    DEFERRED_DOMAINS = {
        "legal": "Sophia",
        "security": "Aegis",
        "compute": "Argus",
        "resource": "Argus",
        "health": "Mercury",
        "social": "Mercury",
        "factual": "Veritas",
    }

    def __init__(self):
        """Initialize the bill interface."""
        self._analyses: Dict[str, Dict[str, Any]] = {}
        self._comments: Dict[str, List[Dict[str, Any]]] = {}
        logger.info("BillInterface initialized")

    def analyze_bill(
        self,
        bill_id: str,
        title: str,
        content: str,
        domain: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a bill from Lyra's creative perspective.

        Args:
            bill_id: ID of the bill
            title: Bill title
            content: Bill content/description
            domain: Optional domain classification
            context: Optional additional context

        Returns:
            Analysis result with creative assessment
        """
        analysis_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Check for domain restrictions
        if domain and self._is_deferred_domain(domain):
            expert = self.DEFERRED_DOMAINS.get(domain.lower())
            return {
                "analysis_id": analysis_id,
                "bill_id": bill_id,
                "title": title,
                "analyzable": False,
                "reason": f"Domain '{domain}' requires expertise from {expert}",
                "defer_to": expert,
                "timestamp": timestamp,
            }

        # Perform creative analysis
        creative_analysis = self._analyze_creative_aspects(title, content)
        narrative_analysis = self._analyze_narrative_structure(title, content)
        strategic_analysis = self._analyze_strategic_coherence(title, content)

        analysis = {
            "analysis_id": analysis_id,
            "bill_id": bill_id,
            "title": title,
            "analyzable": True,
            "domain": domain or "general",
            "creative_assessment": creative_analysis,
            "narrative_assessment": narrative_analysis,
            "strategic_assessment": strategic_analysis,
            "overall_score": self._calculate_overall_score(
                creative_analysis,
                narrative_analysis,
                strategic_analysis,
            ),
            "suggestions": self._generate_suggestions(
                creative_analysis,
                narrative_analysis,
                strategic_analysis,
            ),
            "timestamp": timestamp,
            "agent": "Lyra",
        }

        self._analyses[analysis_id] = analysis
        logger.info(f"Analyzed bill {bill_id} (analysis_id: {analysis_id})")

        return analysis

    def add_comment(
        self,
        bill_id: str,
        comment_type: str,
        content: str,
        section: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Add a creative comment to a bill.

        Args:
            bill_id: ID of the bill
            comment_type: Type of comment (perspective, suggestion, concern)
            content: Comment content
            section: Optional specific section reference
            metadata: Optional additional metadata

        Returns:
            Created comment record
        """
        comment_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        comment = {
            "comment_id": comment_id,
            "bill_id": bill_id,
            "type": comment_type,
            "content": content,
            "section": section,
            "metadata": metadata or {},
            "timestamp": timestamp,
            "agent": "Lyra",
        }

        if bill_id not in self._comments:
            self._comments[bill_id] = []
        self._comments[bill_id].append(comment)

        logger.info(f"Added comment {comment_id} to bill {bill_id}")

        return comment

    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific analysis.

        Args:
            analysis_id: ID of the analysis

        Returns:
            Analysis record or None
        """
        return self._analyses.get(analysis_id)

    def get_bill_comments(self, bill_id: str) -> List[Dict[str, Any]]:
        """
        Get all comments for a bill.

        Args:
            bill_id: ID of the bill

        Returns:
            List of comments
        """
        return self._comments.get(bill_id, [])

    def suggest_reframe(
        self,
        bill_id: str,
        original_text: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Suggest a conceptual reframe for bill text.

        Args:
            bill_id: ID of the bill
            original_text: Text to reframe
            context: Optional context for reframing

        Returns:
            Reframe suggestions
        """
        suggestions = []

        # Generate reframe angles (simplified - in production would use tools)
        angles = [
            ("stakeholder", "Consider from different stakeholder viewpoints"),
            ("temporal", "Consider short-term vs long-term implications"),
            ("scale", "Consider individual vs systemic scale"),
            ("narrative", "Consider the story this tells"),
        ]

        for angle_name, description in angles:
            suggestions.append({
                "angle": angle_name,
                "description": description,
                "reframed_perspective": f"[{angle_name.title()} perspective on: {original_text[:50]}...]",
            })

        return {
            "bill_id": bill_id,
            "original_text": original_text,
            "context": context,
            "reframe_suggestions": suggestions,
            "suggestion_count": len(suggestions),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    def _is_deferred_domain(self, domain: str) -> bool:
        """Check if domain should be deferred to another agent."""
        return domain.lower() in self.DEFERRED_DOMAINS

    def _analyze_creative_aspects(
        self,
        title: str,
        content: str
    ) -> Dict[str, Any]:
        """Analyze creative aspects of the bill."""
        combined = f"{title} {content}".lower()
        words = combined.split()
        word_count = len(words)

        # Creative indicators
        innovation_words = {
            "innovative", "creative", "novel", "unique", "original",
            "transform", "reimagine", "pioneer", "breakthrough",
        }

        innovation_count = sum(1 for w in words if w in innovation_words)
        innovation_density = innovation_count / word_count if word_count > 0 else 0

        score = min(1.0, 0.5 + innovation_density * 5)

        return {
            "score": round(score, 2),
            "innovation_indicators": innovation_count,
            "assessment": self._score_to_assessment(score),
            "notes": "Assessed creative potential and innovation indicators",
        }

    def _analyze_narrative_structure(
        self,
        title: str,
        content: str
    ) -> Dict[str, Any]:
        """Analyze narrative structure of the bill."""
        combined = f"{title} {content}".lower()
        words = combined.split()
        word_count = len(words)

        # Narrative indicators
        narrative_words = {
            "story", "journey", "mission", "vision", "goal",
            "purpose", "outcome", "result", "impact", "change",
        }

        # Structure indicators
        structure_words = {
            "first", "second", "then", "next", "finally",
            "phase", "stage", "step", "process", "framework",
        }

        narrative_count = sum(1 for w in words if w in narrative_words)
        structure_count = sum(1 for w in words if w in structure_words)

        combined_density = (narrative_count + structure_count) / word_count if word_count > 0 else 0
        score = min(1.0, 0.5 + combined_density * 3)

        return {
            "score": round(score, 2),
            "narrative_indicators": narrative_count,
            "structure_indicators": structure_count,
            "assessment": self._score_to_assessment(score),
            "notes": "Assessed narrative clarity and structural coherence",
        }

    def _analyze_strategic_coherence(
        self,
        title: str,
        content: str
    ) -> Dict[str, Any]:
        """Analyze strategic coherence of the bill."""
        combined = f"{title} {content}".lower()
        words = combined.split()
        word_count = len(words)

        # Strategic indicators
        strategic_words = {
            "strategy", "strategic", "objective", "target", "measure",
            "align", "coordinate", "integrate", "optimize", "leverage",
        }

        strategic_count = sum(1 for w in words if w in strategic_words)
        strategic_density = strategic_count / word_count if word_count > 0 else 0

        score = min(1.0, 0.5 + strategic_density * 5)

        return {
            "score": round(score, 2),
            "strategic_indicators": strategic_count,
            "assessment": self._score_to_assessment(score),
            "notes": "Assessed strategic alignment and coherence",
        }

    def _calculate_overall_score(
        self,
        creative: Dict[str, Any],
        narrative: Dict[str, Any],
        strategic: Dict[str, Any],
    ) -> float:
        """Calculate overall assessment score."""
        scores = [
            creative.get("score", 0.5),
            narrative.get("score", 0.5),
            strategic.get("score", 0.5),
        ]
        return round(sum(scores) / len(scores), 2)

    def _generate_suggestions(
        self,
        creative: Dict[str, Any],
        narrative: Dict[str, Any],
        strategic: Dict[str, Any],
    ) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []

        if creative.get("score", 0.5) < 0.5:
            suggestions.append(
                "Consider adding more innovative or transformative language"
            )

        if narrative.get("score", 0.5) < 0.5:
            suggestions.append(
                "Consider strengthening the narrative structure and flow"
            )

        if strategic.get("score", 0.5) < 0.5:
            suggestions.append(
                "Consider clarifying strategic objectives and alignment"
            )

        if not suggestions:
            suggestions.append(
                "The bill demonstrates solid creative, narrative, and strategic elements"
            )

        return suggestions

    def _score_to_assessment(self, score: float) -> str:
        """Convert score to qualitative assessment."""
        if score >= 0.8:
            return "excellent"
        if score >= 0.6:
            return "good"
        if score >= 0.4:
            return "moderate"
        if score >= 0.2:
            return "limited"
        return "minimal"

    def get_interface_stats(self) -> Dict[str, Any]:
        """Get bill interface statistics."""
        total_analyses = len(self._analyses)
        total_comments = sum(len(c) for c in self._comments.values())
        bills_commented = len(self._comments)

        return {
            "total_analyses": total_analyses,
            "total_comments": total_comments,
            "bills_commented": bills_commented,
            "average_score": self._calculate_average_score(),
        }

    def _calculate_average_score(self) -> float:
        """Calculate average overall score across analyses."""
        if not self._analyses:
            return 0.0

        scores = [
            a.get("overall_score", 0)
            for a in self._analyses.values()
            if a.get("analyzable", False)
        ]

        return round(sum(scores) / len(scores), 2) if scores else 0.0
