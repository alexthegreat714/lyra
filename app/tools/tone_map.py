"""
Lyra Agent - Tone Mapper Tool

Maps conceptual tones and themes (NOT emotional inference).
Phase 2: Pure logic, no RAG or memory.
"""

import re
from typing import Dict, Any, List, Optional


class ToneMapper:
    """
    Tone and theme mapper for conceptual categorization.

    Note: This is NOT emotional state detection or psychology.
    This maps conceptual tone categories only.
    """

    # Allowed conceptual tones
    ALLOWED_TONES = [
        "abstract",
        "grounded",
        "technical",
        "whimsical",
        "strategic",
        "narrative",
    ]

    # Tone indicators (keywords and patterns)
    TONE_INDICATORS = {
        "abstract": {
            "keywords": [
                "concept", "theory", "principle", "idea", "notion", "essence",
                "framework", "paradigm", "abstraction", "meta", "philosophical",
                "fundamental", "underlying", "transcendent", "universal",
            ],
            "patterns": [
                r"\b(what is|nature of|essence of)\b",
                r"\b(in principle|theoretically|conceptually)\b",
            ],
        },
        "grounded": {
            "keywords": [
                "practical", "concrete", "specific", "example", "case",
                "implementation", "actual", "real", "applied", "tangible",
                "hands-on", "pragmatic", "actionable", "measurable",
            ],
            "patterns": [
                r"\b(how to|step by step|in practice)\b",
                r"\b(for example|such as|specifically)\b",
            ],
        },
        "technical": {
            "keywords": [
                "system", "process", "algorithm", "architecture", "interface",
                "protocol", "specification", "component", "module", "function",
                "data", "structure", "optimize", "implement", "configure",
            ],
            "patterns": [
                r"\b(API|SDK|CLI|GUI|SQL|HTTP)\b",
                r"\b(input|output|parameter|variable)\b",
            ],
        },
        "whimsical": {
            "keywords": [
                "imagine", "wonder", "play", "explore", "curious", "surprise",
                "unexpected", "creative", "experiment", "possibility", "dream",
                "magical", "delightful", "adventure", "discovery",
            ],
            "patterns": [
                r"\b(what if|wouldn't it be|imagine if)\b",
                r"\b(playfully|curiously|surprisingly)\b",
            ],
        },
        "strategic": {
            "keywords": [
                "goal", "objective", "strategy", "plan", "resource", "priority",
                "tradeoff", "decision", "risk", "opportunity", "competitive",
                "leverage", "position", "advantage", "outcome", "impact",
            ],
            "patterns": [
                r"\b(in order to|so that|with the goal of)\b",
                r"\b(trade-off|cost-benefit|risk-reward)\b",
            ],
        },
        "narrative": {
            "keywords": [
                "story", "journey", "character", "arc", "beginning", "end",
                "conflict", "resolution", "scene", "chapter", "plot", "theme",
                "protagonist", "tension", "climax", "transformation",
            ],
            "patterns": [
                r"\b(once upon|in the beginning|the story of)\b",
                r"\b(led to|resulted in|culminated in)\b",
            ],
        },
    }

    # Tone compatibility matrix (which tones combine well)
    TONE_COMPATIBILITY = {
        "abstract": ["narrative", "strategic", "whimsical"],
        "grounded": ["technical", "strategic", "narrative"],
        "technical": ["grounded", "strategic", "abstract"],
        "whimsical": ["narrative", "abstract", "grounded"],
        "strategic": ["grounded", "technical", "abstract"],
        "narrative": ["whimsical", "abstract", "grounded"],
    }

    def __init__(self):
        """Initialize the tone mapper."""
        pass

    def map(self, prompt: str) -> Dict[str, Any]:
        """
        Provide conceptual tone categories for a prompt.

        Args:
            prompt: The text to analyze for conceptual tone

        Returns:
            Dict containing:
                - detected: List of detected tones
                - recommended: List of recommended complementary tones
        """
        if not prompt or not prompt.strip():
            return {
                "detected": [],
                "recommended": [],
            }

        # Detect tones
        detected = self._detect_tones(prompt)

        # Generate recommendations
        recommended = self._recommend_tones(detected)

        return {
            "detected": detected,
            "recommended": recommended,
        }

    def _detect_tones(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Detect conceptual tones present in the prompt.
        """
        prompt_lower = prompt.lower()
        detected = []

        for tone in self.ALLOWED_TONES:
            score = self._calculate_tone_score(prompt_lower, tone)
            if score > 0:
                detected.append({
                    "tone": tone,
                    "confidence": min(score / 5, 1.0),  # Normalize to 0-1
                    "indicators": self._get_matched_indicators(prompt_lower, tone),
                })

        # Sort by confidence
        detected.sort(key=lambda x: x["confidence"], reverse=True)

        return detected

    def _calculate_tone_score(self, text: str, tone: str) -> int:
        """
        Calculate a score for how strongly a tone is present.
        """
        score = 0
        indicators = self.TONE_INDICATORS.get(tone, {})

        # Check keywords
        for keyword in indicators.get("keywords", []):
            if keyword in text:
                score += 1

        # Check patterns
        for pattern in indicators.get("patterns", []):
            if re.search(pattern, text, re.IGNORECASE):
                score += 2  # Patterns are stronger indicators

        return score

    def _get_matched_indicators(self, text: str, tone: str) -> List[str]:
        """
        Get the specific indicators that matched for a tone.
        """
        matched = []
        indicators = self.TONE_INDICATORS.get(tone, {})

        for keyword in indicators.get("keywords", []):
            if keyword in text:
                matched.append(keyword)

        # Limit to top 3 for brevity
        return matched[:3]

    def _recommend_tones(
        self, detected: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Recommend complementary tones based on detected ones.
        """
        if not detected:
            # If no tones detected, suggest balanced starting point
            return [
                {"tone": "grounded", "reason": "Provides concrete foundation"},
                {"tone": "strategic", "reason": "Adds goal-oriented framing"},
            ]

        recommendations = []
        detected_tones = {d["tone"] for d in detected}

        # Find compatible tones not already detected
        for detected_tone in detected_tones:
            compatible = self.TONE_COMPATIBILITY.get(detected_tone, [])
            for comp_tone in compatible:
                if comp_tone not in detected_tones:
                    recommendations.append({
                        "tone": comp_tone,
                        "reason": f"Complements {detected_tone} for balanced exploration",
                    })

        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec["tone"] not in seen:
                seen.add(rec["tone"])
                unique_recommendations.append(rec)

        return unique_recommendations[:3]  # Return top 3 recommendations

    def analyze_extended(self, prompt: str) -> Dict[str, Any]:
        """
        Provide extended tone analysis with additional context.

        Args:
            prompt: The text to analyze

        Returns:
            Extended analysis including tone balance and suggestions
        """
        base_analysis = self.map(prompt)

        # Calculate tone balance
        balance = self._assess_tone_balance(base_analysis["detected"])

        # Generate suggestions for tone adjustment
        suggestions = self._generate_tone_suggestions(
            base_analysis["detected"],
            balance,
        )

        return {
            **base_analysis,
            "balance": balance,
            "suggestions": suggestions,
        }

    def _assess_tone_balance(
        self, detected: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Assess the balance of detected tones.
        """
        if not detected:
            return {
                "status": "neutral",
                "description": "No strong tones detected; content is tonally neutral.",
            }

        if len(detected) == 1:
            return {
                "status": "focused",
                "description": f"Strongly focused on {detected[0]['tone']} tone.",
            }

        # Check if tones are compatible
        detected_tones = [d["tone"] for d in detected]
        all_compatible = all(
            any(t2 in self.TONE_COMPATIBILITY.get(t1, []) for t2 in detected_tones if t2 != t1)
            for t1 in detected_tones
        )

        if all_compatible:
            return {
                "status": "harmonious",
                "description": "Detected tones complement each other well.",
            }
        else:
            return {
                "status": "tension",
                "description": "Detected tones create productive tension.",
            }

    def _generate_tone_suggestions(
        self,
        detected: List[Dict[str, Any]],
        balance: Dict[str, str],
    ) -> List[str]:
        """
        Generate suggestions for working with the detected tones.
        """
        suggestions = []

        if balance["status"] == "neutral":
            suggestions.append(
                "Consider adding specificity to establish a clearer conceptual frame."
            )
            suggestions.append(
                "Technical, grounded, or narrative elements could add direction."
            )

        elif balance["status"] == "focused":
            tone = detected[0]["tone"]
            suggestions.append(
                f"Strong {tone} focus is clear. Consider whether complementary "
                f"tones could enrich the exploration."
            )
            compatible = self.TONE_COMPATIBILITY.get(tone, [])[:2]
            if compatible:
                suggestions.append(
                    f"Compatible tones to consider: {', '.join(compatible)}."
                )

        elif balance["status"] == "harmonious":
            suggestions.append(
                "Tones are well-balanced. Maintain this coherence as ideas develop."
            )

        elif balance["status"] == "tension":
            suggestions.append(
                "Tonal tension can be generative. Consider whether to resolve "
                "or leverage this contrast."
            )

        return suggestions

    def get_allowed_tones(self) -> List[str]:
        """
        Return the list of allowed conceptual tones.
        """
        return self.ALLOWED_TONES.copy()

    def get_tone_description(self, tone: str) -> Optional[str]:
        """
        Get a description of a specific tone.
        """
        descriptions = {
            "abstract": "Conceptual, theoretical, dealing with ideas and principles",
            "grounded": "Practical, concrete, focused on specific applications",
            "technical": "System-oriented, precise, dealing with mechanisms and processes",
            "whimsical": "Playful, imaginative, open to unexpected possibilities",
            "strategic": "Goal-oriented, considering tradeoffs and outcomes",
            "narrative": "Story-focused, dealing with arcs, characters, and transformation",
        }
        return descriptions.get(tone)
