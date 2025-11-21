"""
Tests for Lyra Agent Creative Tools
"""

import pytest

from app.tools.divergence import DivergenceTool
from app.tools.convergence import ConvergenceTool
from app.tools.analogies import AnalogyTool
from app.tools.narratives import NarrativeTool
from app.tools.counterfactuals import CounterfactualTool
from app.tools.tone_map import ToneMapper


class TestDivergenceTool:
    """Tests for the Divergence Tool."""

    @pytest.fixture
    def tool(self):
        return DivergenceTool()

    def test_generate_returns_multiple_angles(self, tool):
        """Test that divergence generates multiple angles."""
        result = tool.generate("sustainable energy solutions")
        assert isinstance(result, list)
        assert len(result) >= 5
        assert len(result) <= 7

    def test_generate_angle_structure(self, tool):
        """Test that each angle has correct structure."""
        result = tool.generate("artificial intelligence ethics")
        for angle in result:
            assert "angle" in angle
            assert "description" in angle
            assert isinstance(angle["angle"], str)
            assert isinstance(angle["description"], str)

    def test_generate_empty_prompt_returns_empty(self, tool):
        """Test that empty prompt returns empty list."""
        result = tool.generate("")
        assert result == []

    def test_generate_deterministic_for_same_prompt(self, tool):
        """Test that same prompt produces same results."""
        result1 = tool.generate("test concept")
        result2 = tool.generate("test concept")
        assert result1 == result2

    def test_generate_different_for_different_prompts(self, tool):
        """Test that different prompts produce different results."""
        result1 = tool.generate("concept A")
        result2 = tool.generate("concept B completely different")
        # At least some angles should differ
        assert result1 != result2


class TestConvergenceTool:
    """Tests for the Convergence Tool."""

    @pytest.fixture
    def tool(self):
        return ConvergenceTool()

    def test_distill_returns_core_structure(self, tool):
        """Test that distill returns correct structure."""
        options = [
            {"angle": "A", "description": "First option"},
            {"angle": "B", "description": "Second option"},
        ]
        result = tool.distill(options)
        assert "core_idea" in result
        assert "supporting_points" in result
        assert "rationale" in result

    def test_distill_empty_options(self, tool):
        """Test distill with empty options."""
        result = tool.distill([])
        assert result["core_idea"] == ""
        assert result["supporting_points"] == []

    def test_distill_returns_supporting_points_list(self, tool):
        """Test that supporting_points is a list."""
        options = [{"angle": "Test", "description": "Description"}]
        result = tool.distill(options)
        assert isinstance(result["supporting_points"], list)

    def test_distill_returns_rationale_string(self, tool):
        """Test that rationale is a string."""
        options = [{"angle": "Test", "description": "Description"}]
        result = tool.distill(options)
        assert isinstance(result["rationale"], str)


class TestAnalogyTool:
    """Tests for the Analogy Tool."""

    @pytest.fixture
    def tool(self):
        return AnalogyTool()

    def test_generate_returns_list(self, tool):
        """Test that generate returns a list."""
        result = tool.generate("organizational change")
        assert isinstance(result, list)

    def test_generate_returns_3_to_5_analogies(self, tool):
        """Test that generate returns 3-5 analogies."""
        result = tool.generate("learning process")
        assert len(result) >= 3
        assert len(result) <= 5

    def test_analogy_structure(self, tool):
        """Test that each analogy has correct structure."""
        result = tool.generate("problem solving")
        for analogy in result:
            assert "analogy" in analogy
            assert "domain" in analogy
            assert "explanation" in analogy

    def test_analogies_from_different_domains(self, tool):
        """Test that analogies come from different domains."""
        result = tool.generate("innovation")
        domains = [a["domain"] for a in result]
        # All domains should be unique
        assert len(domains) == len(set(domains))

    def test_generate_empty_concept_returns_empty(self, tool):
        """Test that empty concept returns empty list."""
        result = tool.generate("")
        assert result == []


class TestNarrativeTool:
    """Tests for the Narrative Tool."""

    @pytest.fixture
    def tool(self):
        return NarrativeTool()

    def test_outline_returns_structured_output(self, tool):
        """Test that outline returns correct structure."""
        result = tool.outline("transformation")
        assert "premise" in result
        assert "conflicts" in result
        assert "beats" in result
        assert "resolution_patterns" in result

    def test_outline_conflicts_is_list(self, tool):
        """Test that conflicts is a list."""
        result = tool.outline("journey")
        assert isinstance(result["conflicts"], list)

    def test_outline_beats_is_list(self, tool):
        """Test that beats is a list."""
        result = tool.outline("discovery")
        assert isinstance(result["beats"], list)

    def test_outline_with_constraints(self, tool):
        """Test outline with structure constraint."""
        result = tool.outline("growth", {"structure": "hero_journey"})
        assert len(result["beats"]) > 0

    def test_outline_empty_theme_returns_empty(self, tool):
        """Test that empty theme returns empty structure."""
        result = tool.outline("")
        assert result["premise"] == ""
        assert result["conflicts"] == []


class TestCounterfactualTool:
    """Tests for the Counterfactual Tool."""

    @pytest.fixture
    def tool(self):
        return CounterfactualTool()

    def test_build_returns_baseline_and_alternatives(self, tool):
        """Test that build returns baseline and what-ifs."""
        result = tool.build("Company launches new product")
        assert "baseline" in result
        assert "what_if_A" in result
        assert "what_if_B" in result
        assert "impact_analysis" in result

    def test_build_baseline_matches_input(self, tool):
        """Test that baseline matches input scenario."""
        scenario = "Team adopts new methodology"
        result = tool.build(scenario)
        assert result["baseline"] == scenario

    def test_build_what_ifs_are_different(self, tool):
        """Test that what_if_A and what_if_B are different."""
        result = tool.build("Market conditions change")
        assert result["what_if_A"] != result["what_if_B"]

    def test_build_impact_analysis_is_list(self, tool):
        """Test that impact_analysis is a list."""
        result = tool.build("Policy is implemented")
        assert isinstance(result["impact_analysis"], list)
        assert len(result["impact_analysis"]) > 0

    def test_build_empty_scenario_returns_empty(self, tool):
        """Test that empty scenario returns empty structure."""
        result = tool.build("")
        assert result["baseline"] == ""
        assert result["what_if_A"] == ""


class TestToneMapper:
    """Tests for the Tone Mapper."""

    @pytest.fixture
    def tool(self):
        return ToneMapper()

    def test_map_returns_detected_and_recommended(self, tool):
        """Test that map returns correct structure."""
        result = tool.map("A strategic approach to system architecture")
        assert "detected" in result
        assert "recommended" in result

    def test_map_detected_is_list(self, tool):
        """Test that detected is a list."""
        result = tool.map("Technical implementation details")
        assert isinstance(result["detected"], list)

    def test_map_recommended_is_list(self, tool):
        """Test that recommended is a list."""
        result = tool.map("Abstract concept exploration")
        assert isinstance(result["recommended"], list)

    def test_map_detects_technical_tone(self, tool):
        """Test detection of technical tone."""
        result = tool.map("The system architecture uses API interfaces")
        detected_tones = [d["tone"] for d in result["detected"]]
        assert "technical" in detected_tones

    def test_map_detects_narrative_tone(self, tool):
        """Test detection of narrative tone."""
        result = tool.map("The story begins with a journey of transformation")
        detected_tones = [d["tone"] for d in result["detected"]]
        assert "narrative" in detected_tones

    def test_map_returns_only_allowed_tones(self, tool):
        """Test that only allowed tones are returned."""
        allowed = tool.get_allowed_tones()
        result = tool.map("Some complex multi-faceted text about concepts")
        for detected in result["detected"]:
            assert detected["tone"] in allowed

    def test_map_empty_prompt_returns_empty_detected(self, tool):
        """Test that empty prompt returns empty detected list."""
        result = tool.map("")
        assert result["detected"] == []


class TestToolIntegration:
    """Integration tests for tool invocation via LyraAgent."""

    @pytest.fixture
    def client(self):
        from fastapi.testclient import TestClient
        from app.server import app
        return TestClient(app)

    def test_run_task_with_divergence_tool(self, client):
        """Test invoking divergence tool via run_task."""
        response = client.post(
            "/run_task",
            json={
                "task": "use_tool",
                "payload": {
                    "tool": "divergence",
                    "args": {"prompt": "sustainable cities"}
                }
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        # Result should contain the tool output
        result = data["result"]
        assert "result" in result
        assert isinstance(result["result"], list)

    def test_run_task_with_convergence_tool(self, client):
        """Test invoking convergence tool via run_task."""
        response = client.post(
            "/run_task",
            json={
                "task": "use_tool",
                "payload": {
                    "tool": "convergence",
                    "args": {
                        "options": [
                            {"angle": "A", "description": "First"},
                            {"angle": "B", "description": "Second"}
                        ]
                    }
                }
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "result" in data

    def test_run_task_with_unknown_tool(self, client):
        """Test invoking unknown tool returns error."""
        response = client.post(
            "/run_task",
            json={
                "task": "use_tool",
                "payload": {
                    "tool": "nonexistent_tool",
                    "args": {}
                }
            },
        )
        assert response.status_code == 200
        data = response.json()
        result = data["result"]
        assert "error" in result
        assert "available_tools" in result
