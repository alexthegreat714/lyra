"""
Lyra Agent Congress Module

Phase 5: Congress integration for multi-agent collaboration.

GUARDRAILS:
    Lyra participates in Congress for creative strategy only:
    - No voting on legal matters (Sophia's domain)
    - No voting on security protocols (Aegis's domain)
    - No voting on resource allocation (Argus's domain)
    - No voting on health/social matters (Mercury's domain)

    Lyra's Congress role is to provide:
    - Creative perspectives on proposals
    - Strategic narrative analysis
    - Conceptual reframing suggestions
"""

from app.congress.voting import VotingModule
from app.congress.contributions import ContributionTracker
from app.congress.bill_interface import BillInterface

__all__ = ["VotingModule", "ContributionTracker", "BillInterface"]
