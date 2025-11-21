"""
Lyra Agent - Divergence Tool

Generates divergent conceptual angles for creative exploration.
Phase 2: Pure logic, no RAG or memory.
"""

import hashlib
from typing import List, Dict, Any


class DivergenceTool:
    """
    Divergence tool for generating multiple conceptual angles.

    Rules:
        - No emotional manipulation
        - No decisions or commands
        - No artwork or final creative output
        - High novelty, low bias
    """

    # Conceptual lenses for generating diverse angles
    LENSES = [
        ("inversion", "What if we flip the core assumption?"),
        ("scale_shift", "What happens at extreme scales (micro/macro)?"),
        ("temporal", "How does this look across different time horizons?"),
        ("cross_domain", "What parallels exist in unrelated fields?"),
        ("constraint_removal", "What if key limitations didn't exist?"),
        ("stakeholder_shift", "How do different perspectives see this?"),
        ("abstraction", "What's the underlying pattern or principle?"),
        ("materialization", "What concrete forms could this take?"),
        ("synthesis", "What emerges from combining opposing ideas?"),
        ("decomposition", "What are the atomic components?"),
    ]

    def __init__(self):
        """Initialize the divergence tool."""
        pass

    def generate(self, prompt: str) -> List[Dict[str, str]]:
        """
        Generate divergent conceptual angles from a prompt.

        Args:
            prompt: The input prompt to explore

        Returns:
            List of 5-7 divergent angles, each with:
                - angle: Name of the conceptual angle
                - description: Exploration of that angle
        """
        if not prompt or not prompt.strip():
            return []

        # Deterministically select lenses based on prompt content
        selected_lenses = self._select_lenses(prompt, count=6)

        angles = []
        for lens_name, lens_question in selected_lenses:
            angle = self._apply_lens(prompt, lens_name, lens_question)
            angles.append(angle)

        return angles

    def _select_lenses(self, prompt: str, count: int = 6) -> List[tuple]:
        """
        Select lenses based on prompt characteristics.
        Uses deterministic selection for reproducibility.
        """
        # Create a hash-based seed from the prompt for consistent results
        prompt_hash = int(hashlib.md5(prompt.encode()).hexdigest(), 16)

        # Rotate through lenses based on hash
        start_idx = prompt_hash % len(self.LENSES)
        selected = []

        for i in range(count):
            idx = (start_idx + i) % len(self.LENSES)
            selected.append(self.LENSES[idx])

        return selected

    def _apply_lens(self, prompt: str, lens_name: str, lens_question: str) -> Dict[str, str]:
        """
        Apply a conceptual lens to generate an angle.
        """
        # Generate description based on lens type
        descriptions = {
            "inversion": f"Consider the opposite of '{prompt}'. What assumptions are we making that could be reversed? What if the goal was actually the obstacle?",
            "scale_shift": f"Examine '{prompt}' at different scales. How does it manifest at the individual level vs. systemic level? What patterns emerge at extremes?",
            "temporal": f"View '{prompt}' through time. How would this look in 1 year, 10 years, 100 years? What historical parallels exist?",
            "cross_domain": f"Map '{prompt}' to other domains. How would biology, architecture, music, or economics approach this same challenge?",
            "constraint_removal": f"Remove constraints from '{prompt}'. If resources, time, or physics weren't limiting factors, what possibilities emerge?",
            "stakeholder_shift": f"Reframe '{prompt}' from different viewpoints. How would a child, expert, skeptic, or outsider perceive this?",
            "abstraction": f"Abstract '{prompt}' to its essence. What is the fundamental pattern or principle at work? What category does this belong to?",
            "materialization": f"Make '{prompt}' tangible. What physical forms, prototypes, or artifacts could represent this concept?",
            "synthesis": f"Combine opposing elements of '{prompt}'. What emerges from holding contradictions together? Where do tensions create new possibilities?",
            "decomposition": f"Break down '{prompt}' into components. What are the essential building blocks? Which elements are truly necessary?",
        }

        return {
            "angle": lens_name.replace("_", " ").title(),
            "description": descriptions.get(
                lens_name,
                f"Explore '{prompt}' through the lens of {lens_name}: {lens_question}"
            ),
        }

    def generate_with_focus(self, prompt: str, focus_lenses: List[str]) -> List[Dict[str, str]]:
        """
        Generate angles using specific lenses.

        Args:
            prompt: The input prompt
            focus_lenses: List of lens names to apply

        Returns:
            List of angles for the specified lenses
        """
        angles = []
        lens_dict = {name: question for name, question in self.LENSES}

        for lens_name in focus_lenses:
            if lens_name in lens_dict:
                angle = self._apply_lens(prompt, lens_name, lens_dict[lens_name])
                angles.append(angle)

        return angles
