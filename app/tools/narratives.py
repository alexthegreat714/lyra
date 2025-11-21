"""
Lyra Agent - Narrative Tool

Generates narrative scaffolds and story structures.
Phase 2: Pure logic, no RAG or memory.
"""

import hashlib
from typing import Dict, Any, List, Optional


class NarrativeTool:
    """
    Narrative architect for generating story structures and thematic scaffolds.
    """

    # Conflict archetypes
    CONFLICT_TYPES = [
        {"type": "person_vs_self", "description": "Internal struggle with identity, values, or desires"},
        {"type": "person_vs_person", "description": "Direct opposition between individuals or groups"},
        {"type": "person_vs_nature", "description": "Struggle against environmental or natural forces"},
        {"type": "person_vs_society", "description": "Individual against institutional or cultural norms"},
        {"type": "person_vs_technology", "description": "Tension with tools, systems, or artificial forces"},
        {"type": "person_vs_fate", "description": "Confrontation with destiny, time, or inevitability"},
    ]

    # Tension patterns
    TENSION_PATTERNS = [
        {"pattern": "escalating", "description": "Stakes progressively increase"},
        {"pattern": "oscillating", "description": "Alternating rises and falls in intensity"},
        {"pattern": "sustained", "description": "Constant pressure maintained throughout"},
        {"pattern": "delayed", "description": "Tension builds invisibly then erupts"},
        {"pattern": "layered", "description": "Multiple tension sources interact"},
    ]

    # Structural beat templates
    BEAT_TEMPLATES = {
        "three_act": [
            {"beat": "setup", "purpose": "Establish world, characters, and stakes"},
            {"beat": "inciting_incident", "purpose": "Disrupt equilibrium and launch journey"},
            {"beat": "rising_action", "purpose": "Escalate challenges and develop characters"},
            {"beat": "midpoint", "purpose": "Major revelation or shift in understanding"},
            {"beat": "crisis", "purpose": "Protagonist faces greatest challenge"},
            {"beat": "climax", "purpose": "Decisive confrontation or transformation"},
            {"beat": "resolution", "purpose": "New equilibrium established"},
        ],
        "hero_journey": [
            {"beat": "ordinary_world", "purpose": "Establish baseline reality"},
            {"beat": "call_to_adventure", "purpose": "Invitation to change"},
            {"beat": "refusal", "purpose": "Initial resistance or doubt"},
            {"beat": "meeting_mentor", "purpose": "Receive guidance or tools"},
            {"beat": "crossing_threshold", "purpose": "Commit to the journey"},
            {"beat": "tests_allies_enemies", "purpose": "Navigate new world challenges"},
            {"beat": "approach_cave", "purpose": "Prepare for central ordeal"},
            {"beat": "ordeal", "purpose": "Face death/rebirth moment"},
            {"beat": "reward", "purpose": "Claim the prize or insight"},
            {"beat": "road_back", "purpose": "Begin return with knowledge"},
            {"beat": "resurrection", "purpose": "Final test applying lessons"},
            {"beat": "return_elixir", "purpose": "Share transformation with world"},
        ],
        "five_act": [
            {"beat": "exposition", "purpose": "Introduce world and conflict seeds"},
            {"beat": "rising_action", "purpose": "Complications multiply"},
            {"beat": "climax", "purpose": "Point of no return"},
            {"beat": "falling_action", "purpose": "Consequences unfold"},
            {"beat": "denouement", "purpose": "Final resolution and meaning"},
        ],
        "circular": [
            {"beat": "departure", "purpose": "Leave familiar ground"},
            {"beat": "initiation", "purpose": "Face trials and gain wisdom"},
            {"beat": "return", "purpose": "Come back transformed"},
            {"beat": "integration", "purpose": "Apply lessons to original context"},
        ],
    }

    # Resolution styles
    RESOLUTION_STYLES = [
        {"style": "triumphant", "description": "Clear victory and positive transformation"},
        {"style": "pyrrhic", "description": "Victory at significant cost"},
        {"style": "ambiguous", "description": "Uncertain outcome inviting interpretation"},
        {"style": "tragic", "description": "Downfall despite noble effort"},
        {"style": "transcendent", "description": "Resolution beyond original conflict frame"},
        {"style": "cyclical", "description": "Return to beginning with new understanding"},
        {"style": "open", "description": "Story continues beyond narrative bounds"},
    ]

    def __init__(self):
        """Initialize the narrative tool."""
        pass

    def outline(self, theme: str, constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a narrative scaffold for a given theme.

        Args:
            theme: The central theme or concept for the narrative
            constraints: Optional constraints like:
                - structure: "three_act", "hero_journey", "five_act", "circular"
                - tone: Preferred tone
                - length: "short", "medium", "long"

        Returns:
            Dict containing:
                - premise: Core narrative premise
                - conflicts: List of relevant conflict types
                - beats: Structural beats with purposes
                - resolution_patterns: Possible resolution styles
        """
        if not theme or not theme.strip():
            return {
                "premise": "",
                "conflicts": [],
                "beats": [],
                "resolution_patterns": [],
            }

        constraints = constraints or {}

        # Generate premise
        premise = self._generate_premise(theme, constraints)

        # Select conflicts
        conflicts = self._select_conflicts(theme, constraints)

        # Determine beats
        beats = self._determine_beats(theme, constraints)

        # Select resolution patterns
        resolution_patterns = self._select_resolutions(theme, constraints)

        return {
            "premise": premise,
            "conflicts": conflicts,
            "beats": beats,
            "resolution_patterns": resolution_patterns,
        }

    def _generate_premise(self, theme: str, constraints: Dict[str, Any]) -> str:
        """
        Generate a narrative premise from the theme.
        """
        # Create a premise that frames the theme as a story question
        return (
            f"A narrative exploration of '{theme}' that examines how "
            f"individuals and systems navigate the tensions inherent in this concept. "
            f"The story asks: What is at stake when '{theme}' is challenged, "
            f"and what transformation becomes possible?"
        )

    def _select_conflicts(
        self, theme: str, constraints: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Select relevant conflict types for the theme.
        """
        # Use hash for deterministic selection
        theme_hash = int(hashlib.md5(theme.encode()).hexdigest(), 16)

        # Select 2-3 conflicts
        num_conflicts = 2 + (theme_hash % 2)
        start_idx = theme_hash % len(self.CONFLICT_TYPES)

        conflicts = []
        for i in range(num_conflicts):
            idx = (start_idx + i * 2) % len(self.CONFLICT_TYPES)
            conflict = self.CONFLICT_TYPES[idx].copy()
            conflict["relevance"] = f"Relevant to '{theme}' through its exploration of {conflict['type'].replace('_', ' ')}"
            conflicts.append(conflict)

        return conflicts

    def _determine_beats(
        self, theme: str, constraints: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Determine structural beats based on constraints.
        """
        # Select structure type
        structure = constraints.get("structure", "three_act")

        if structure not in self.BEAT_TEMPLATES:
            structure = "three_act"

        beats = []
        for beat in self.BEAT_TEMPLATES[structure]:
            themed_beat = beat.copy()
            themed_beat["theme_application"] = self._apply_theme_to_beat(
                theme, beat["beat"], beat["purpose"]
            )
            beats.append(themed_beat)

        return beats

    def _apply_theme_to_beat(self, theme: str, beat: str, purpose: str) -> str:
        """
        Apply the theme to a specific beat.
        """
        applications = {
            "setup": f"Establish the current state of '{theme}' in the world",
            "inciting_incident": f"Something disrupts the accepted understanding of '{theme}'",
            "rising_action": f"Challenges related to '{theme}' multiply and intensify",
            "midpoint": f"A key truth about '{theme}' is revealed",
            "crisis": f"The protagonist must choose how to relate to '{theme}'",
            "climax": f"The central tension around '{theme}' reaches its peak",
            "resolution": f"A new relationship with '{theme}' is established",
            "ordinary_world": f"Show '{theme}' as part of everyday reality",
            "call_to_adventure": f"'{theme}' presents an opportunity or threat",
            "refusal": f"Resist engaging deeply with '{theme}'",
            "meeting_mentor": f"Receive wisdom about '{theme}'",
            "crossing_threshold": f"Commit to exploring '{theme}' fully",
            "ordeal": f"Face the deepest challenge related to '{theme}'",
            "reward": f"Gain insight or mastery regarding '{theme}'",
            "return_elixir": f"Share new understanding of '{theme}' with others",
        }

        return applications.get(beat, f"Engage with '{theme}' through {purpose.lower()}")

    def _select_resolutions(
        self, theme: str, constraints: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Select appropriate resolution styles.
        """
        # Use hash for selection
        theme_hash = int(hashlib.md5(theme.encode()).hexdigest(), 16)

        # Select 2-3 resolution options
        num_resolutions = 2 + (theme_hash % 2)
        start_idx = (theme_hash // 7) % len(self.RESOLUTION_STYLES)

        resolutions = []
        for i in range(num_resolutions):
            idx = (start_idx + i * 2) % len(self.RESOLUTION_STYLES)
            resolution = self.RESOLUTION_STYLES[idx].copy()
            resolution["theme_fit"] = f"How '{theme}' might conclude: {resolution['description'].lower()}"
            resolutions.append(resolution)

        return resolutions

    def get_available_structures(self) -> List[str]:
        """
        Return available narrative structures.
        """
        return list(self.BEAT_TEMPLATES.keys())

    def get_conflict_types(self) -> List[Dict[str, str]]:
        """
        Return all conflict type definitions.
        """
        return self.CONFLICT_TYPES.copy()

    def get_resolution_styles(self) -> List[Dict[str, str]]:
        """
        Return all resolution style definitions.
        """
        return self.RESOLUTION_STYLES.copy()
