"""
Lyra Agent - Analogy Tool

Generates analogies and metaphors from different domains.
Phase 2: Pure logic, no RAG or memory.
"""

import hashlib
from typing import List, Dict, Any, Optional


class AnalogyTool:
    """
    Analogy and metaphor generator for cross-domain conceptual mapping.
    """

    # Domain templates for analogy generation
    DOMAINS = {
        "biology": {
            "patterns": ["ecosystem", "evolution", "symbiosis", "metabolism", "adaptation"],
            "template": "Like {pattern} in biology, {concept} involves {connection}.",
        },
        "architecture": {
            "patterns": ["foundation", "scaffolding", "load-bearing", "facade", "blueprint"],
            "template": "In architecture, {pattern} serves a similar role to how {concept} {connection}.",
        },
        "music": {
            "patterns": ["rhythm", "harmony", "counterpoint", "crescendo", "improvisation"],
            "template": "Musical {pattern} mirrors {concept} through {connection}.",
        },
        "physics": {
            "patterns": ["momentum", "equilibrium", "resonance", "entropy", "gravity"],
            "template": "The physical principle of {pattern} parallels {concept} in how {connection}.",
        },
        "economics": {
            "patterns": ["market", "supply-demand", "investment", "compound growth", "scarcity"],
            "template": "Economic {pattern} offers insight into {concept} where {connection}.",
        },
        "ecology": {
            "patterns": ["niche", "food web", "succession", "carrying capacity", "biodiversity"],
            "template": "Ecological {pattern} illuminates {concept} through {connection}.",
        },
        "cooking": {
            "patterns": ["fermentation", "reduction", "seasoning", "mise en place", "layering"],
            "template": "Culinary {pattern} resembles {concept} in how {connection}.",
        },
        "navigation": {
            "patterns": ["compass", "waypoint", "current", "dead reckoning", "landmark"],
            "template": "Navigational {pattern} maps to {concept} where {connection}.",
        },
        "gardening": {
            "patterns": ["pruning", "grafting", "composting", "seasonal cycles", "root systems"],
            "template": "Garden {pattern} reflects {concept} through {connection}.",
        },
        "games": {
            "patterns": ["strategy", "turn-taking", "resource management", "risk-reward", "leveling"],
            "template": "Game {pattern} parallels {concept} in how {connection}.",
        },
    }

    def __init__(self):
        """Initialize the analogy tool."""
        pass

    def generate(self, concept: str) -> List[Dict[str, str]]:
        """
        Produce 3-5 analogies from different domains.

        Args:
            concept: The concept to find analogies for

        Returns:
            List of analogies, each with:
                - analogy: The analogy statement
                - domain: The source domain
                - explanation: How the analogy illuminates the concept
        """
        if not concept or not concept.strip():
            return []

        # Select diverse domains based on concept
        selected_domains = self._select_domains(concept, count=4)

        analogies = []
        for domain in selected_domains:
            analogy = self._create_analogy(concept, domain)
            analogies.append(analogy)

        return analogies

    def _select_domains(self, concept: str, count: int = 4) -> List[str]:
        """
        Select domains that offer useful analogical distance.
        """
        # Use concept hash for deterministic but varied selection
        concept_hash = int(hashlib.md5(concept.encode()).hexdigest(), 16)

        all_domains = list(self.DOMAINS.keys())
        selected = []

        # Ensure variety by stepping through domains
        step = max(1, len(all_domains) // count)
        start = concept_hash % len(all_domains)

        for i in range(count):
            idx = (start + i * step) % len(all_domains)
            selected.append(all_domains[idx])

        return selected

    def _create_analogy(self, concept: str, domain: str) -> Dict[str, str]:
        """
        Create an analogy mapping concept to a domain.
        """
        domain_info = self.DOMAINS[domain]

        # Select pattern based on concept characteristics
        concept_hash = int(hashlib.md5(f"{concept}{domain}".encode()).hexdigest(), 16)
        pattern_idx = concept_hash % len(domain_info["patterns"])
        pattern = domain_info["patterns"][pattern_idx]

        # Generate connection explanation
        connection = self._generate_connection(concept, domain, pattern)

        # Build the analogy statement
        analogy_statement = domain_info["template"].format(
            pattern=pattern,
            concept=concept,
            connection=connection,
        )

        # Build explanation
        explanation = self._build_explanation(concept, domain, pattern)

        return {
            "analogy": analogy_statement,
            "domain": domain,
            "explanation": explanation,
        }

    def _generate_connection(self, concept: str, domain: str, pattern: str) -> str:
        """
        Generate the connecting insight between concept and pattern.
        """
        connections = {
            "ecosystem": "multiple interdependent elements interact to create emergent behavior",
            "evolution": "iterative refinement through selection pressure shapes outcomes",
            "symbiosis": "mutual benefit arises from complementary capabilities",
            "metabolism": "transformation of inputs into useful outputs sustains the system",
            "adaptation": "responsive change to environmental conditions ensures survival",
            "foundation": "establishes stable ground for building higher-order structures",
            "scaffolding": "provides temporary support during construction phases",
            "load-bearing": "distributes weight and stress across the structure",
            "facade": "presents an interface that differs from internal structure",
            "blueprint": "abstract specification guides concrete implementation",
            "rhythm": "recurring patterns create structure and expectation",
            "harmony": "multiple elements combine to produce coherent wholes",
            "counterpoint": "independent lines interweave to create rich texture",
            "crescendo": "gradual intensification builds toward a peak",
            "improvisation": "structured spontaneity within established constraints",
            "momentum": "accumulated force continues in the same direction",
            "equilibrium": "balanced forces create stable states",
            "resonance": "matching frequencies amplify effects",
            "entropy": "natural tendency toward disorder requires energy to counter",
            "gravity": "fundamental attraction draws elements together",
            "market": "distributed decision-making aggregates information",
            "supply-demand": "scarcity and desire interact to determine value",
            "investment": "present sacrifice enables future returns",
            "compound growth": "returns on returns accelerate over time",
            "scarcity": "limited availability increases perceived value",
            "niche": "specialized roles enable coexistence",
            "food web": "energy flows through interconnected relationships",
            "succession": "stages of development follow predictable patterns",
            "carrying capacity": "environmental limits constrain growth",
            "biodiversity": "variety provides resilience and adaptability",
            "fermentation": "controlled transformation over time yields new properties",
            "reduction": "concentration through removal intensifies essence",
            "seasoning": "small additions create disproportionate impact",
            "mise en place": "preparation enables fluid execution",
            "layering": "sequential additions create complex results",
            "compass": "consistent reference enables navigation through uncertainty",
            "waypoint": "intermediate goals mark progress toward destination",
            "current": "underlying forces influence direction and speed",
            "dead reckoning": "extrapolation from known position estimates location",
            "landmark": "distinctive features enable orientation",
            "pruning": "selective removal stimulates healthy growth",
            "grafting": "combining different sources creates hybrid vigor",
            "composting": "decomposition of old material feeds new growth",
            "seasonal cycles": "rhythmic phases govern appropriate actions",
            "root systems": "hidden foundations support visible growth",
            "strategy": "long-term planning shapes tactical decisions",
            "turn-taking": "sequential action with response opportunities",
            "resource management": "allocation decisions determine outcomes",
            "risk-reward": "potential gains correlate with potential losses",
            "leveling": "progressive development unlocks new capabilities",
        }

        return connections.get(
            pattern,
            f"both involve {pattern} dynamics in their operation"
        )

    def _build_explanation(self, concept: str, domain: str, pattern: str) -> str:
        """
        Build an explanation of how the analogy illuminates the concept.
        """
        return (
            f"This analogy draws from {domain} to illuminate '{concept}'. "
            f"The {pattern} pattern in {domain} shares structural similarities "
            f"that can reveal non-obvious aspects of the original concept. "
            f"By mapping familiar {domain} dynamics onto '{concept}', "
            f"we can leverage existing intuitions to generate new insights."
        )

    def generate_for_domains(
        self, concept: str, domains: List[str]
    ) -> List[Dict[str, str]]:
        """
        Generate analogies for specific domains.

        Args:
            concept: The concept to find analogies for
            domains: List of domain names to use

        Returns:
            List of analogies for the specified domains
        """
        analogies = []

        for domain in domains:
            if domain in self.DOMAINS:
                analogy = self._create_analogy(concept, domain)
                analogies.append(analogy)

        return analogies

    def get_available_domains(self) -> List[str]:
        """
        Return list of available domains for analogy generation.
        """
        return list(self.DOMAINS.keys())
