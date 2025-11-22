"""
Tests for Lyra Agent Brain (Reasoning Engine)

Phase 3: Tests for structured reasoning pipeline.
"""

import pytest
from fastapi.testclient import TestClient

from app.server import app
from app.services.lyra_brain import LyraBrain
from app.tools.divergence import DivergenceTool
from app.tools.convergence import ConvergenceTool
from app.tools.analogies import AnalogyTool
from app.tools.narratives import NarrativeTool
from app.tools.counterfactuals import CounterfactualTool
from app.tools.tone_map import ToneMapper


@pytest.fixture
def tools():
    """Create tool instances for testing."""
    return {
        "divergence": DivergenceTool(),
        "convergence": ConvergenceTool(),
        "analogies": AnalogyTool(),
        "narratives": NarrativeTool(),
        "counterfactuals": CounterfactualTool(),
        "tonemap": ToneMapper(),
    }


@pytest.fixture
def brain(tools):
    """Create a LyraBrain instance."""
    return LyraBrain(tools)


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestLyraBrainUnit:
    """Unit tests for LyraBrain class."""

    def test_brain_initialization(self, brain):
        """Test that brain initializes correctly."""
        assert brain.tools is not None
        assert len(brain.tools) == 6

    def test_get_supported_tasks(self, brain):
        """Test that supported tasks are returned."""
        tasks = brain.get_supported_tasks()
        assert "idea_generation" in tasks
        assert "narrative_design" in tasks
        assert "counterfactual_analysis" in tasks
        assert "analogy_exploration" in tasks
        assert "tone_mapping" in tasks
        assert "mixed_creative" in tasks

    def test_get_task_tools(self, brain):
        """Test that task tools are correctly mapped."""
        assert brain.get_task_tools("idea_generation") == ["divergence", "convergence"]
        assert brain.get_task_tools("narrative_design") == ["narratives"]
        assert brain.get_task_tools("analogy_exploration") == ["analogies"]


class TestIdeaGeneration:
    """Tests for idea_generation task type."""

    def test_idea_generation_produces_divergence_and_convergence(self, brain):
        """Test idea_generation uses divergence + convergence."""
        result = brain.process("idea_generation", "sustainable cities")

        assert result["task_type"] == "idea_generation"
        assert "result" in result
        assert "steps" in result

        # Should have options from divergence
        assert "options" in result["result"] or "divergence" in str(result)

        # Should have distilled output from convergence
        assert "distilled" in result["result"] or "convergence" in str(result)

    def test_idea_generation_steps_count(self, brain):
        """Test that idea_generation has at least 4 steps."""
        result = brain.process("idea_generation", "innovation strategy")
        assert len(result["steps"]) >= 4


class TestNarrativeDesign:
    """Tests for narrative_design task type."""

    def test_narrative_design_produces_outline(self, brain):
        """Test narrative_design produces narrative_outline."""
        result = brain.process("narrative_design", "digital transformation")

        assert result["task_type"] == "narrative_design"
        assert "narrative_outline" in result["result"]

    def test_narrative_outline_structure(self, brain):
        """Test narrative outline has expected structure."""
        result = brain.process("narrative_design", "hero's journey")
        outline = result["result"].get("narrative_outline", {})

        # Should have narrative structure elements
        assert "premise" in outline or len(outline) > 0


class TestCounterfactualAnalysis:
    """Tests for counterfactual_analysis task type."""

    def test_counterfactual_analysis_produces_counterfactuals(self, brain):
        """Test counterfactual_analysis produces counterfactuals."""
        result = brain.process(
            "counterfactual_analysis",
            "Company launches AI product"
        )

        assert result["task_type"] == "counterfactual_analysis"
        assert "counterfactuals" in result["result"]

    def test_counterfactual_has_baseline_and_alternatives(self, brain):
        """Test counterfactual output has baseline and what-ifs."""
        result = brain.process(
            "counterfactual_analysis",
            "Team adopts agile methodology"
        )
        counterfactuals = result["result"].get("counterfactuals", {})

        assert "baseline" in counterfactuals
        assert "what_if_A" in counterfactuals
        assert "what_if_B" in counterfactuals


class TestAnalogyExploration:
    """Tests for analogy_exploration task type."""

    def test_analogy_exploration_produces_analogies(self, brain):
        """Test analogy_exploration produces analogies."""
        result = brain.process("analogy_exploration", "organizational change")

        assert result["task_type"] == "analogy_exploration"
        assert "analogies" in result["result"]

    def test_analogies_is_list(self, brain):
        """Test analogies result is a list."""
        result = brain.process("analogy_exploration", "learning process")
        analogies = result["result"].get("analogies", [])

        assert isinstance(analogies, list)
        assert len(analogies) >= 3


class TestToneMapping:
    """Tests for tone_mapping task type."""

    def test_tone_mapping_produces_tone_profile(self, brain):
        """Test tone_mapping produces tone_profile."""
        result = brain.process("tone_mapping", "strategic technical approach")

        assert result["task_type"] == "tone_mapping"
        assert "tone_profile" in result["result"]

    def test_tone_profile_has_detected_and_recommended(self, brain):
        """Test tone_profile has detected and recommended."""
        result = brain.process("tone_mapping", "abstract conceptual exploration")
        tone = result["result"].get("tone_profile", {})

        assert "detected" in tone
        assert "recommended" in tone


class TestMixedCreative:
    """Tests for mixed_creative task type."""

    def test_mixed_creative_uses_multiple_tools(self, brain):
        """Test mixed_creative runs full pipeline."""
        result = brain.process("mixed_creative", "future of work")

        assert result["task_type"] == "mixed_creative"
        assert len(result["steps"]) >= 4

        # Should have multiple result types
        insights = result["result"].get("primary_insights", [])
        assert len(insights) >= 2


class TestOutputStructure:
    """Tests for general output structure."""

    def test_structured_json_output(self, brain):
        """Test that output is structured JSON."""
        result = brain.process("idea_generation", "test prompt")

        assert isinstance(result, dict)
        assert "task_type" in result
        assert "prompt" in result
        assert "result" in result
        assert "steps" in result

    def test_steps_list_structure(self, brain):
        """Test that steps list has proper structure."""
        result = brain.process("idea_generation", "test prompt")

        for step in result["steps"]:
            assert "stage" in step
            assert "data" in step

    def test_all_pipeline_stages_present(self, brain):
        """Test that all pipeline stages are executed."""
        result = brain.process("idea_generation", "test prompt")

        stages = [step["stage"] for step in result["steps"]]
        assert "interpretation" in stages
        assert "objective_classification" in stages
        assert "tool_plan" in stages
        assert "tool_execution" in stages
        assert "synthesis" in stages


class TestAPIIntegration:
    """Integration tests for creative_brain API endpoint."""

    def test_creative_brain_endpoint_idea_generation(self, client):
        """Test /creative_brain endpoint with idea_generation."""
        response = client.post(
            "/creative_brain",
            json={
                "task_type": "idea_generation",
                "prompt": "sustainable innovation"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["task_type"] == "idea_generation"
        assert "result" in data
        assert "steps" in data

    def test_creative_brain_endpoint_narrative_design(self, client):
        """Test /creative_brain endpoint with narrative_design."""
        response = client.post(
            "/creative_brain",
            json={
                "task_type": "narrative_design",
                "prompt": "transformation journey"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "narrative_outline" in data["result"]

    def test_creative_brain_endpoint_with_context(self, client):
        """Test /creative_brain endpoint with context."""
        response = client.post(
            "/creative_brain",
            json={
                "task_type": "idea_generation",
                "prompt": "product strategy",
                "context": {"domain": "technology", "constraints": ["budget"]}
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["prompt"] == "product strategy"

    def test_run_task_with_creative_brain(self, client):
        """Test /run_task endpoint with creative_brain task."""
        response = client.post(
            "/run_task",
            json={
                "task": "creative_brain",
                "payload": {
                    "task_type": "tone_mapping",
                    "prompt": "technical strategic implementation"
                }
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert "result" in data
        assert "tone_profile" in data["result"]["result"]


class TestInvalidTaskTypes:
    """Tests for handling invalid task types."""

    def test_invalid_task_type_falls_back_to_mixed(self, brain):
        """Test that invalid task type falls back to mixed_creative."""
        result = brain.process("invalid_task_type", "test prompt")
        # Should fall back gracefully
        assert result["task_type"] == "mixed_creative"

    def test_empty_prompt_handling(self, brain):
        """Test handling of empty prompt."""
        result = brain.process("idea_generation", "")
        # Should not crash, should return structured output
        assert "result" in result
        assert "steps" in result
