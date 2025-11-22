"""
Tests for Lyra Congress Integration

Phase 5: Congress voting, contributions, and bill analysis.
"""

import pytest
from fastapi.testclient import TestClient

from app.server import app
from app.congress.voting import VotingModule, VoteType, RESTRICTED_DOMAINS
from app.congress.contributions import ContributionTracker, ContributionType
from app.congress.bill_interface import BillInterface


client = TestClient(app)


class TestVotingModule:
    """Tests for the VotingModule."""

    def test_cast_vote_approve(self):
        """Test casting an approve vote."""
        voting = VotingModule()

        result = voting.cast_vote(
            proposal_id="prop-123",
            vote=VoteType.APPROVE,
            domain="creative",
            rationale={"reason": "Strong creative merit"},
        )

        assert result["vote"] == "approve"
        assert result["proposal_id"] == "prop-123"
        assert result["valid"] is True
        assert result["agent"] == "Lyra"

    def test_cast_vote_restricted_domain(self):
        """Test auto-abstain on restricted domain."""
        voting = VotingModule()

        result = voting.cast_vote(
            proposal_id="prop-456",
            vote=VoteType.APPROVE,
            domain="legal",
            rationale={"reason": "Test"},
        )

        # Should auto-abstain
        assert result["vote"] == "abstain"
        assert result["auto_abstain"] is True
        assert "outside Lyra's expertise" in result["rationale"]["reason"]

    def test_evaluate_proposal_creative_domain(self):
        """Test evaluating a proposal in creative domain."""
        voting = VotingModule()

        result = voting.evaluate_proposal(
            proposal_id="prop-789",
            proposal_content="An innovative creative strategy for transformation",
            domain="creative",
        )

        assert result["evaluable"] is True
        assert "assessment" in result
        assert "suggested_vote" in result

    def test_evaluate_proposal_restricted_domain(self):
        """Test evaluating a proposal in restricted domain."""
        voting = VotingModule()

        result = voting.evaluate_proposal(
            proposal_id="prop-999",
            proposal_content="Security protocol update",
            domain="security",
        )

        assert result["evaluable"] is False
        assert result["defer_to"] == "Aegis"

    def test_restricted_domains(self):
        """Test all restricted domains are defined."""
        expected_restricted = [
            "legal", "security", "compute", "resource", "health", "social", "factual"
        ]
        for domain in expected_restricted:
            assert domain in RESTRICTED_DOMAINS


class TestContributionTracker:
    """Tests for the ContributionTracker."""

    def test_create_contribution(self):
        """Test creating a contribution."""
        tracker = ContributionTracker()

        result = tracker.create_contribution(
            contribution_type=ContributionType.CREATIVE_PERSPECTIVE,
            content={"perspectives": [{"angle": "test", "insight": "insight"}]},
            proposal_id="prop-123",
        )

        assert result["type"] == "creative_perspective"
        assert result["status"] == "draft"
        assert result["agent"] == "Lyra"
        assert result["id"] is not None

    def test_submit_contribution(self):
        """Test submitting a contribution."""
        tracker = ContributionTracker()

        # Create first
        contribution = tracker.create_contribution(
            contribution_type=ContributionType.NARRATIVE_ANALYSIS,
            content={"subject": "test"},
        )

        # Submit
        result = tracker.submit_contribution(contribution["id"])

        assert result["status"] == "submitted"
        assert "submitted_at" in result

    def test_create_creative_perspective(self):
        """Test creating a creative perspective contribution."""
        tracker = ContributionTracker()

        result = tracker.create_creative_perspective(
            topic="Innovation Strategy",
            perspectives=[
                {"angle": "stakeholder", "insight": "Test insight"},
            ],
            proposal_id="prop-123",
        )

        assert result["type"] == "creative_perspective"
        assert result["content"]["topic"] == "Innovation Strategy"

    def test_create_narrative_analysis(self):
        """Test creating a narrative analysis contribution."""
        tracker = ContributionTracker()

        result = tracker.create_narrative_analysis(
            subject="Digital Transformation",
            narrative_elements={"arc": "three_act", "theme": "change"},
        )

        assert result["type"] == "narrative_analysis"
        assert result["content"]["subject"] == "Digital Transformation"

    def test_contribution_types(self):
        """Test all contribution types are defined."""
        expected_types = [
            "creative_perspective",
            "narrative_analysis",
            "conceptual_reframe",
            "strategic_suggestion",
            "analogy_insight",
            "counterfactual_scenario",
        ]
        actual_types = [t.value for t in ContributionType]
        for t in expected_types:
            assert t in actual_types


class TestBillInterface:
    """Tests for the BillInterface."""

    def test_analyze_bill_creative_domain(self):
        """Test analyzing a bill in creative domain."""
        interface = BillInterface()

        result = interface.analyze_bill(
            bill_id="bill-123",
            title="Creative Innovation Initiative",
            content="This bill proposes an innovative framework for creative strategy",
            domain="creative",
        )

        assert result["analyzable"] is True
        assert "creative_assessment" in result
        assert "narrative_assessment" in result
        assert "strategic_assessment" in result
        assert "overall_score" in result

    def test_analyze_bill_restricted_domain(self):
        """Test analyzing a bill in restricted domain."""
        interface = BillInterface()

        result = interface.analyze_bill(
            bill_id="bill-456",
            title="Legal Framework Update",
            content="Updates to legal protocols",
            domain="legal",
        )

        assert result["analyzable"] is False
        assert result["defer_to"] == "Sophia"

    def test_add_comment(self):
        """Test adding a comment to a bill."""
        interface = BillInterface()

        result = interface.add_comment(
            bill_id="bill-123",
            comment_type="perspective",
            content="Consider the narrative implications",
            section="Section 2",
        )

        assert result["bill_id"] == "bill-123"
        assert result["type"] == "perspective"
        assert result["agent"] == "Lyra"

    def test_suggest_reframe(self):
        """Test suggesting reframes."""
        interface = BillInterface()

        result = interface.suggest_reframe(
            bill_id="bill-123",
            original_text="The system shall implement controls",
            context="Innovation initiative",
        )

        assert result["bill_id"] == "bill-123"
        assert "reframe_suggestions" in result
        assert len(result["reframe_suggestions"]) > 0


class TestCongressEndpoints:
    """Tests for Congress API endpoints."""

    def test_congress_status(self):
        """Test /congress/status endpoint."""
        response = client.get("/congress/status")
        assert response.status_code == 200

        data = response.json()
        assert data["agent"] == "Lyra"
        assert data["congress_active"] is True
        assert "voting" in data
        assert "contributions" in data
        assert "guardrails" in data

    def test_cast_vote_endpoint(self):
        """Test /congress/vote endpoint."""
        response = client.post(
            "/congress/vote",
            json={
                "proposal_id": "prop-test-1",
                "vote": "approve",
                "domain": "creative",
                "rationale": {"reason": "Creative merit"},
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["vote"] == "approve"
        assert data["proposal_id"] == "prop-test-1"

    def test_cast_vote_invalid_type(self):
        """Test /congress/vote with invalid vote type."""
        response = client.post(
            "/congress/vote",
            json={
                "proposal_id": "prop-test-2",
                "vote": "invalid_vote",
                "domain": "creative",
                "rationale": {},
            }
        )
        assert response.status_code == 400

    def test_evaluate_endpoint(self):
        """Test /congress/evaluate endpoint."""
        response = client.post(
            "/congress/evaluate",
            json={
                "proposal_id": "prop-eval-1",
                "proposal_content": "An innovative creative approach",
                "domain": "creative",
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["evaluable"] is True
        assert "assessment" in data

    def test_contribution_endpoint(self):
        """Test /congress/contribution endpoint."""
        response = client.post(
            "/congress/contribution",
            json={
                "contribution_type": "creative_perspective",
                "content": {"topic": "test", "perspectives": []},
                "session_id": "session-1",
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["type"] == "creative_perspective"
        assert data["status"] == "draft"

    def test_contribution_invalid_type(self):
        """Test /congress/contribution with invalid type."""
        response = client.post(
            "/congress/contribution",
            json={
                "contribution_type": "invalid_type",
                "content": {},
            }
        )
        assert response.status_code == 400

    def test_bill_analyze_endpoint(self):
        """Test /congress/bill/analyze endpoint."""
        response = client.post(
            "/congress/bill/analyze",
            json={
                "bill_id": "bill-test-1",
                "title": "Innovation Act",
                "content": "Proposal for creative innovation strategy",
                "domain": "creative",
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["analyzable"] is True
        assert data["bill_id"] == "bill-test-1"

    def test_bill_comment_endpoint(self):
        """Test /congress/bill/comment endpoint."""
        response = client.post(
            "/congress/bill/comment",
            json={
                "bill_id": "bill-test-1",
                "comment_type": "suggestion",
                "content": "Consider narrative structure",
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["bill_id"] == "bill-test-1"
        assert data["type"] == "suggestion"

    def test_bill_reframe_endpoint(self):
        """Test /congress/bill/reframe endpoint."""
        response = client.post(
            "/congress/bill/reframe",
            json={
                "bill_id": "bill-test-1",
                "original_text": "The process will be implemented",
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert "reframe_suggestions" in data

    def test_voting_stats_endpoint(self):
        """Test /congress/votes/stats endpoint."""
        response = client.get("/congress/votes/stats")
        assert response.status_code == 200

        data = response.json()
        assert "total_votes" in data

    def test_contribution_stats_endpoint(self):
        """Test /congress/contributions/stats endpoint."""
        response = client.get("/congress/contributions/stats")
        assert response.status_code == 200

        data = response.json()
        assert "total_contributions" in data

    def test_bill_stats_endpoint(self):
        """Test /congress/bill/stats endpoint."""
        response = client.get("/congress/bill/stats")
        assert response.status_code == 200

        data = response.json()
        assert "total_analyses" in data
