"""
Lyra Agent - Convergence Tool

Distills multiple options into core insights.
Phase 2: Pure logic, no RAG or memory.
"""

from typing import List, Dict, Any


class ConvergenceTool:
    """
    Convergence tool for distilling divergent options into unified insights.
    """

    def __init__(self):
        """Initialize the convergence tool."""
        pass

    def distill(self, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Distill a list of divergent options into a core insight.

        Args:
            options: List of divergent options/angles to synthesize

        Returns:
            Dict containing:
                - core_idea: The central synthesized insight
                - supporting_points: Key points that support the core idea
                - rationale: Explanation of how the synthesis was derived
        """
        if not options:
            return {
                "core_idea": "",
                "supporting_points": [],
                "rationale": "No options provided for synthesis.",
            }

        # Extract themes and patterns from options
        themes = self._extract_themes(options)
        common_threads = self._find_common_threads(options)

        # Synthesize core idea
        core_idea = self._synthesize_core(themes, common_threads)

        # Generate supporting points
        supporting_points = self._generate_supporting_points(options, themes)

        # Build rationale
        rationale = self._build_rationale(options, themes, common_threads)

        return {
            "core_idea": core_idea,
            "supporting_points": supporting_points,
            "rationale": rationale,
        }

    def _extract_themes(self, options: List[Dict[str, Any]]) -> List[str]:
        """
        Extract thematic elements from options.
        """
        themes = []

        for option in options:
            # Handle different option formats
            if isinstance(option, dict):
                if "angle" in option:
                    themes.append(option["angle"])
                if "description" in option:
                    # Extract key concepts from description
                    desc = option["description"]
                    if "pattern" in desc.lower():
                        themes.append("pattern recognition")
                    if "scale" in desc.lower():
                        themes.append("scale dynamics")
                    if "time" in desc.lower() or "temporal" in desc.lower():
                        themes.append("temporal perspective")
                    if "constraint" in desc.lower():
                        themes.append("constraint analysis")
            elif isinstance(option, str):
                themes.append(option)

        return list(set(themes))  # Remove duplicates

    def _find_common_threads(self, options: List[Dict[str, Any]]) -> List[str]:
        """
        Identify common threads across options.
        """
        threads = []

        # Look for structural commonalities
        if len(options) > 1:
            threads.append("multiple perspectives considered")

        # Check for complementary relationships
        has_abstract = any(
            "abstract" in str(opt).lower() or "pattern" in str(opt).lower()
            for opt in options
        )
        has_concrete = any(
            "concrete" in str(opt).lower() or "tangible" in str(opt).lower()
            for opt in options
        )

        if has_abstract and has_concrete:
            threads.append("spans abstract and concrete")

        if len(options) >= 3:
            threads.append("rich conceptual coverage")

        return threads

    def _synthesize_core(self, themes: List[str], threads: List[str]) -> str:
        """
        Synthesize a core idea from themes and threads.
        """
        if not themes and not threads:
            return "The concept requires further exploration to identify a unifying insight."

        theme_str = ", ".join(themes[:3]) if themes else "the explored dimensions"

        if "multiple perspectives considered" in threads:
            return f"A multi-faceted understanding emerges from {theme_str}, revealing interconnected aspects that inform a holistic view."
        elif "spans abstract and concrete" in threads:
            return f"The synthesis bridges theoretical and practical dimensions through {theme_str}, enabling both conceptual clarity and actionable application."
        else:
            return f"The central insight draws from {theme_str}, suggesting an integrated approach that honors the complexity of the subject."

    def _generate_supporting_points(
        self, options: List[Dict[str, Any]], themes: List[str]
    ) -> List[str]:
        """
        Generate supporting points from the analysis.
        """
        points = []

        # Generate points based on option count and content
        if len(options) >= 2:
            points.append(
                f"Analysis considered {len(options)} distinct conceptual angles"
            )

        for theme in themes[:3]:
            points.append(f"The '{theme}' dimension contributes unique insight")

        if len(options) >= 4:
            points.append("Breadth of exploration enables robust synthesis")

        return points

    def _build_rationale(
        self,
        options: List[Dict[str, Any]],
        themes: List[str],
        threads: List[str],
    ) -> str:
        """
        Build an explanation of the synthesis process.
        """
        parts = []

        parts.append(f"This synthesis examined {len(options)} input option(s).")

        if themes:
            parts.append(f"Key themes identified: {', '.join(themes[:4])}.")

        if threads:
            parts.append(f"Common threads: {', '.join(threads)}.")

        parts.append(
            "The core idea represents the intersection of these elements, "
            "prioritizing coherence while preserving nuance."
        )

        return " ".join(parts)

    def rank_options(
        self, options: List[Dict[str, Any]], criteria: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Rank options by relevance to given criteria.

        Args:
            options: List of options to rank
            criteria: Optional criteria for ranking

        Returns:
            Ranked list of options with scores
        """
        if not options:
            return []

        criteria = criteria or ["novelty", "coherence", "applicability"]

        ranked = []
        for i, option in enumerate(options):
            # Simple scoring based on content richness
            score = 0

            if isinstance(option, dict):
                if option.get("description"):
                    score += len(option["description"]) // 50  # Content depth
                if option.get("angle"):
                    score += 1  # Has structure

            ranked.append({
                "option": option,
                "rank": i + 1,
                "score": min(score, 10),  # Cap at 10
            })

        # Sort by score descending
        ranked.sort(key=lambda x: x["score"], reverse=True)

        # Update ranks after sorting
        for i, item in enumerate(ranked):
            item["rank"] = i + 1

        return ranked
