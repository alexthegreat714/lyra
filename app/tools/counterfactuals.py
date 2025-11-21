"""
Lyra Agent - Counterfactual Tool

Constructs structured what-if scenario analyses.
Phase 2: Pure logic, no RAG or memory.
"""

import hashlib
from typing import Dict, Any, List, Optional


class CounterfactualTool:
    """
    Counterfactual constructor for exploring alternative scenarios.
    """

    # Counterfactual dimensions
    DIMENSIONS = [
        "temporal",      # What if timing was different?
        "magnitude",     # What if scale was different?
        "actor",         # What if different agents were involved?
        "method",        # What if approach was different?
        "context",       # What if environment was different?
        "constraint",    # What if limitations were different?
        "information",   # What if knowledge was different?
        "motivation",    # What if goals were different?
    ]

    # Impact categories
    IMPACT_CATEGORIES = [
        "immediate_effects",
        "ripple_effects",
        "stakeholder_impacts",
        "reversibility",
        "probability_shift",
    ]

    def __init__(self):
        """Initialize the counterfactual tool."""
        pass

    def build(self, scenario: str) -> Dict[str, Any]:
        """
        Provide a structured what-if scenario analysis.

        Args:
            scenario: The baseline scenario to analyze

        Returns:
            Dict containing:
                - baseline: The original scenario
                - what_if_A: First alternative scenario
                - what_if_B: Second alternative scenario
                - impact_analysis: List of impact considerations
        """
        if not scenario or not scenario.strip():
            return {
                "baseline": "",
                "what_if_A": "",
                "what_if_B": "",
                "impact_analysis": [],
            }

        # Select dimensions for alternatives
        dim_a, dim_b = self._select_dimensions(scenario)

        # Build alternative scenarios
        what_if_a = self._build_alternative(scenario, dim_a)
        what_if_b = self._build_alternative(scenario, dim_b)

        # Analyze impacts
        impact_analysis = self._analyze_impacts(scenario, what_if_a, what_if_b)

        return {
            "baseline": scenario,
            "what_if_A": what_if_a,
            "what_if_B": what_if_b,
            "impact_analysis": impact_analysis,
        }

    def _select_dimensions(self, scenario: str) -> tuple:
        """
        Select two different dimensions for counterfactual exploration.
        """
        scenario_hash = int(hashlib.md5(scenario.encode()).hexdigest(), 16)

        idx_a = scenario_hash % len(self.DIMENSIONS)
        idx_b = (scenario_hash // 7 + 3) % len(self.DIMENSIONS)

        # Ensure different dimensions
        if idx_a == idx_b:
            idx_b = (idx_b + 1) % len(self.DIMENSIONS)

        return self.DIMENSIONS[idx_a], self.DIMENSIONS[idx_b]

    def _build_alternative(self, scenario: str, dimension: str) -> Dict[str, str]:
        """
        Build an alternative scenario along a given dimension.
        """
        alternatives = {
            "temporal": {
                "modification": "What if the timing was significantly different?",
                "scenario": f"Consider '{scenario}' occurring at a different point in time - either much earlier when conditions were different, or much later when new factors have emerged. How would the sequence of events and available options change?",
                "dimension": "temporal",
            },
            "magnitude": {
                "modification": "What if the scale was dramatically different?",
                "scenario": f"Imagine '{scenario}' at 10x or 0.1x its current scale. At larger scale, what systemic effects emerge? At smaller scale, what becomes more manageable but also less impactful?",
                "dimension": "magnitude",
            },
            "actor": {
                "modification": "What if different agents were involved?",
                "scenario": f"Replace the key actors in '{scenario}' with different individuals or groups with distinct capabilities, motivations, and constraints. How do outcomes shift?",
                "dimension": "actor",
            },
            "method": {
                "modification": "What if a completely different approach was used?",
                "scenario": f"Instead of the current approach in '{scenario}', consider an orthogonal method - perhaps more gradual vs. sudden, distributed vs. centralized, or technical vs. social.",
                "dimension": "method",
            },
            "context": {
                "modification": "What if the environment was fundamentally different?",
                "scenario": f"Place '{scenario}' in a different context - different industry, culture, era, or physical environment. What assumptions break down and what new possibilities emerge?",
                "dimension": "context",
            },
            "constraint": {
                "modification": "What if key constraints were removed or added?",
                "scenario": f"Modify the constraints in '{scenario}' - remove a major limitation, or introduce a new one. How does this reshape the solution space and strategic options?",
                "dimension": "constraint",
            },
            "information": {
                "modification": "What if knowledge/information was different?",
                "scenario": f"Alter the information landscape of '{scenario}' - what if key facts were known earlier, or remained hidden? What if there was more uncertainty, or more clarity?",
                "dimension": "information",
            },
            "motivation": {
                "modification": "What if goals and incentives were different?",
                "scenario": f"Change the underlying motivations in '{scenario}' - what if success was defined differently, or incentives pointed in another direction entirely?",
                "dimension": "motivation",
            },
        }

        return alternatives.get(dimension, {
            "modification": f"What if {dimension} was different?",
            "scenario": f"Explore '{scenario}' with modified {dimension}.",
            "dimension": dimension,
        })

    def _analyze_impacts(
        self, baseline: str, alt_a: Dict[str, str], alt_b: Dict[str, str]
    ) -> List[Dict[str, str]]:
        """
        Analyze the impacts of counterfactual scenarios.
        """
        impacts = []

        # Immediate effects
        impacts.append({
            "category": "immediate_effects",
            "analysis": (
                f"The {alt_a['dimension']} modification would immediately affect "
                f"the core dynamics of the scenario. The {alt_b['dimension']} change "
                f"would alter initial conditions and available responses."
            ),
        })

        # Ripple effects
        impacts.append({
            "category": "ripple_effects",
            "analysis": (
                "Both alternatives create cascading consequences: changes propagate "
                "through connected systems, potentially amplifying or dampening "
                "effects in unexpected ways. Second and third-order effects "
                "often diverge significantly from initial projections."
            ),
        })

        # Stakeholder impacts
        impacts.append({
            "category": "stakeholder_impacts",
            "analysis": (
                "Different stakeholders experience these alternatives differently. "
                "Some may benefit from changes that harm others. Power dynamics, "
                "resource access, and voice in decision-making shift across scenarios."
            ),
        })

        # Reversibility
        impacts.append({
            "category": "reversibility",
            "analysis": (
                "Consider whether each alternative creates reversible or irreversible "
                "changes. Some paths close off future options while others maintain "
                "flexibility. The baseline and alternatives differ in their "
                "commitment levels and exit costs."
            ),
        })

        # Probability considerations
        impacts.append({
            "category": "probability_assessment",
            "analysis": (
                "Each scenario carries different likelihood profiles. The baseline "
                "represents observed or expected reality. Alternatives require "
                "assessing what conditions would need to change for them to occur, "
                "and how plausible those changes are."
            ),
        })

        return impacts

    def build_extended(
        self, scenario: str, dimensions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Build extended counterfactual analysis with specific dimensions.

        Args:
            scenario: The baseline scenario
            dimensions: Specific dimensions to explore (defaults to all)

        Returns:
            Extended analysis with multiple alternatives
        """
        if not scenario or not scenario.strip():
            return {"baseline": "", "alternatives": [], "impact_analysis": []}

        dimensions = dimensions or self.DIMENSIONS

        alternatives = []
        for dim in dimensions:
            if dim in self.DIMENSIONS:
                alt = self._build_alternative(scenario, dim)
                alternatives.append(alt)

        # Build comparative analysis
        impact_analysis = []
        for category in self.IMPACT_CATEGORIES:
            impact_analysis.append({
                "category": category,
                "analysis": self._generate_category_analysis(scenario, alternatives, category),
            })

        return {
            "baseline": scenario,
            "alternatives": alternatives,
            "impact_analysis": impact_analysis,
        }

    def _generate_category_analysis(
        self, scenario: str, alternatives: List[Dict], category: str
    ) -> str:
        """
        Generate analysis for a specific impact category.
        """
        analyses = {
            "immediate_effects": (
                f"Across {len(alternatives)} alternative scenarios, immediate effects "
                "vary based on which dimension is modified. Each change creates "
                "distinct initial conditions and response requirements."
            ),
            "ripple_effects": (
                "Cascading effects differ by dimension: some changes propagate slowly "
                "but deeply, others create rapid but shallow ripples. Interaction "
                "effects between dimensions may amplify or cancel out."
            ),
            "stakeholder_impacts": (
                "Each dimensional shift redistributes benefits and costs among "
                "stakeholders differently. No single alternative uniformly improves "
                "or worsens outcomes for all parties."
            ),
            "reversibility": (
                "Alternatives range from easily reversible to highly path-dependent. "
                "Understanding reversibility helps prioritize which counterfactuals "
                "merit serious consideration."
            ),
            "probability_shift": (
                "Modifying different dimensions changes scenario probability in "
                "distinct ways. Some dimensions are more malleable than others "
                "given current conditions and resources."
            ),
        }

        return analyses.get(category, f"Analysis of {category} across alternatives.")

    def get_available_dimensions(self) -> List[str]:
        """
        Return available counterfactual dimensions.
        """
        return self.DIMENSIONS.copy()
