"""
Lyra Agent Congress Routes

API endpoints for Congress participation.
Phase 5: Congress integration.

GUARDRAILS:
    Lyra participates in Congress for creative strategy only:
    - No voting on legal matters (Sophia's domain)
    - No voting on security protocols (Aegis's domain)
    - No voting on resource allocation (Argus's domain)
    - No voting on health/social matters (Mercury's domain)
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel, Field

from app.congress.voting import VotingModule, VoteType
from app.congress.contributions import ContributionTracker, ContributionType
from app.congress.bill_interface import BillInterface


router = APIRouter(prefix="/congress", tags=["congress"])

# Initialize Congress modules
voting = VotingModule()
contributions = ContributionTracker()
bills = BillInterface()


# Request/Response Models

class VoteRequest(BaseModel):
    """Request model for casting a vote."""
    proposal_id: str = Field(..., description="ID of the proposal")
    vote: str = Field(..., description="Vote type: approve, reject, abstain, defer")
    domain: str = Field(..., description="Domain of the proposal")
    rationale: Dict[str, Any] = Field(
        default_factory=dict, description="Structured rationale"
    )
    proposal_summary: Optional[str] = Field(
        None, description="Optional proposal summary"
    )


class EvaluateRequest(BaseModel):
    """Request model for evaluating a proposal."""
    proposal_id: str = Field(..., description="ID of the proposal")
    proposal_content: str = Field(..., description="Content of the proposal")
    domain: str = Field(..., description="Domain of the proposal")
    context: Optional[Dict[str, Any]] = Field(
        None, description="Optional context"
    )


class ContributionRequest(BaseModel):
    """Request model for creating a contribution."""
    contribution_type: str = Field(..., description="Type of contribution")
    content: Dict[str, Any] = Field(..., description="Contribution content")
    proposal_id: Optional[str] = Field(None, description="Linked proposal ID")
    session_id: Optional[str] = Field(None, description="Congress session ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class BillAnalysisRequest(BaseModel):
    """Request model for bill analysis."""
    bill_id: str = Field(..., description="ID of the bill")
    title: str = Field(..., description="Bill title")
    content: str = Field(..., description="Bill content")
    domain: Optional[str] = Field(None, description="Bill domain")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class BillCommentRequest(BaseModel):
    """Request model for adding a bill comment."""
    bill_id: str = Field(..., description="ID of the bill")
    comment_type: str = Field(..., description="Type of comment")
    content: str = Field(..., description="Comment content")
    section: Optional[str] = Field(None, description="Section reference")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ReframeRequest(BaseModel):
    """Request model for reframe suggestions."""
    bill_id: str = Field(..., description="ID of the bill")
    original_text: str = Field(..., description="Text to reframe")
    context: Optional[str] = Field(None, description="Context for reframing")


# Voting Endpoints

@router.post("/vote")
async def cast_vote(request: VoteRequest) -> Dict[str, Any]:
    """
    Cast a vote on a Congress proposal.

    Lyra will auto-abstain on proposals outside creative domain.

    Args:
        request: Vote request with proposal details and vote

    Returns:
        Vote record
    """
    logger.info(f"Casting vote on proposal {request.proposal_id}")

    try:
        vote_type = VoteType(request.vote)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid vote type: {request.vote}. "
            f"Valid types: approve, reject, abstain, defer"
        )

    try:
        result = voting.cast_vote(
            proposal_id=request.proposal_id,
            vote=vote_type,
            domain=request.domain,
            rationale=request.rationale,
            proposal_summary=request.proposal_summary,
        )
        return result
    except Exception as e:
        logger.error(f"Vote casting failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate")
async def evaluate_proposal(request: EvaluateRequest) -> Dict[str, Any]:
    """
    Evaluate a proposal from Lyra's creative perspective.

    Returns assessment and suggested vote.

    Args:
        request: Evaluation request with proposal details

    Returns:
        Evaluation with creative assessment
    """
    logger.info(f"Evaluating proposal {request.proposal_id}")

    try:
        result = voting.evaluate_proposal(
            proposal_id=request.proposal_id,
            proposal_content=request.proposal_content,
            domain=request.domain,
            context=request.context,
        )
        return result
    except Exception as e:
        logger.error(f"Proposal evaluation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/votes/history")
async def get_vote_history(
    limit: int = 50,
    domain: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Lyra's voting history.

    Args:
        limit: Maximum records to return
        domain: Optional domain filter

    Returns:
        List of vote records
    """
    history = voting.get_vote_history(limit=limit, domain=domain)
    return {
        "votes": history,
        "count": len(history),
        "domain_filter": domain,
    }


@router.get("/votes/stats")
async def get_voting_stats() -> Dict[str, Any]:
    """
    Get Lyra's voting statistics.

    Returns:
        Voting statistics
    """
    return voting.get_voting_stats()


# Contribution Endpoints

@router.post("/contribution")
async def create_contribution(request: ContributionRequest) -> Dict[str, Any]:
    """
    Create a creative contribution to Congress.

    Args:
        request: Contribution details

    Returns:
        Created contribution record
    """
    logger.info(f"Creating contribution: {request.contribution_type}")

    try:
        contribution_type = ContributionType(request.contribution_type)
    except ValueError:
        valid_types = [t.value for t in ContributionType]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid contribution type: {request.contribution_type}. "
            f"Valid types: {valid_types}"
        )

    try:
        result = contributions.create_contribution(
            contribution_type=contribution_type,
            content=request.content,
            proposal_id=request.proposal_id,
            session_id=request.session_id,
            metadata=request.metadata,
        )
        return result
    except Exception as e:
        logger.error(f"Contribution creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/contribution/{contribution_id}/submit")
async def submit_contribution(contribution_id: str) -> Dict[str, Any]:
    """
    Submit a draft contribution to Congress.

    Args:
        contribution_id: ID of the contribution

    Returns:
        Updated contribution record
    """
    logger.info(f"Submitting contribution {contribution_id}")

    try:
        result = contributions.submit_contribution(contribution_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Contribution submission failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contribution/{contribution_id}")
async def get_contribution(contribution_id: str) -> Dict[str, Any]:
    """
    Get a specific contribution.

    Args:
        contribution_id: ID of the contribution

    Returns:
        Contribution record
    """
    result = contributions.get_contribution(contribution_id)
    if not result:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return result


@router.get("/contributions/stats")
async def get_contribution_stats() -> Dict[str, Any]:
    """
    Get contribution statistics.

    Returns:
        Contribution statistics
    """
    return contributions.get_contribution_stats()


@router.get("/contributions/session/{session_id}")
async def get_session_contributions(session_id: str) -> Dict[str, Any]:
    """
    Get all contributions for a Congress session.

    Args:
        session_id: Congress session ID

    Returns:
        List of contributions
    """
    results = contributions.get_contributions_by_session(session_id)
    return {
        "session_id": session_id,
        "contributions": results,
        "count": len(results),
    }


# Bill Analysis Endpoints

@router.post("/bill/analyze")
async def analyze_bill(request: BillAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze a bill from Lyra's creative perspective.

    Args:
        request: Bill analysis request

    Returns:
        Analysis with creative assessment
    """
    logger.info(f"Analyzing bill {request.bill_id}")

    try:
        result = bills.analyze_bill(
            bill_id=request.bill_id,
            title=request.title,
            content=request.content,
            domain=request.domain,
            context=request.context,
        )
        return result
    except Exception as e:
        logger.error(f"Bill analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bill/comment")
async def add_bill_comment(request: BillCommentRequest) -> Dict[str, Any]:
    """
    Add a creative comment to a bill.

    Args:
        request: Comment request

    Returns:
        Created comment record
    """
    logger.info(f"Adding comment to bill {request.bill_id}")

    try:
        result = bills.add_comment(
            bill_id=request.bill_id,
            comment_type=request.comment_type,
            content=request.content,
            section=request.section,
            metadata=request.metadata,
        )
        return result
    except Exception as e:
        logger.error(f"Comment creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bill/reframe")
async def suggest_reframe(request: ReframeRequest) -> Dict[str, Any]:
    """
    Suggest conceptual reframes for bill text.

    Args:
        request: Reframe request

    Returns:
        Reframe suggestions
    """
    logger.info(f"Suggesting reframe for bill {request.bill_id}")

    try:
        result = bills.suggest_reframe(
            bill_id=request.bill_id,
            original_text=request.original_text,
            context=request.context,
        )
        return result
    except Exception as e:
        logger.error(f"Reframe suggestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bill/{bill_id}/comments")
async def get_bill_comments(bill_id: str) -> Dict[str, Any]:
    """
    Get all comments for a bill.

    Args:
        bill_id: ID of the bill

    Returns:
        List of comments
    """
    comments = bills.get_bill_comments(bill_id)
    return {
        "bill_id": bill_id,
        "comments": comments,
        "count": len(comments),
    }


@router.get("/bill/stats")
async def get_bill_stats() -> Dict[str, Any]:
    """
    Get bill interface statistics.

    Returns:
        Bill interface statistics
    """
    return bills.get_interface_stats()


# General Congress Status

@router.get("/status")
async def get_congress_status() -> Dict[str, Any]:
    """
    Get overall Congress participation status.

    Returns:
        Combined status from all Congress modules
    """
    return {
        "agent": "Lyra",
        "congress_active": True,
        "voting": voting.get_voting_stats(),
        "contributions": contributions.get_contribution_stats(),
        "bills": bills.get_interface_stats(),
        "guardrails": {
            "restricted_domains": [
                "legal (Sophia)",
                "security (Aegis)",
                "compute/resource (Argus)",
                "health/social (Mercury)",
                "factual (Veritas)",
            ],
            "allowed_domains": [
                "creative",
                "narrative",
                "conceptual",
                "strategic",
            ],
        },
    }
