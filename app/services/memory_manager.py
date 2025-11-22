"""
Lyra Agent - Memory Manager Service

Thin layer over Lyra's long-term memory & RAG.
Phase 4: File-backed memory with embeddings.

GUARDRAILS:
    Lyra's memory is for creative context only:
    - No cross-agent access
    - No law/security data (Sophia/Aegis domains)
    - No compute/resource metrics (Argus domain)
    - No health/social records (Mercury domain)

    This keeps memory aligned with Article IV's recognition of
    "strategic & conceptual contributions" as valid AI outputs.
"""

from typing import Any, Dict, List, Optional

from loguru import logger

from app.rag.ingest import ingest_items, get_valid_categories
from app.rag.query import query_relevant, query_by_category, get_memory_stats


class LyraMemoryManager:
    """
    Memory manager for Lyra's creative context.

    Provides:
        - Ingestion of creative snippets, themes, narratives
        - Retrieval of relevant context for creative tasks
        - Category-based organization

    GUARDRAILS:
        - No cross-agent access
        - No law/security data storage
        - No compute metrics storage
        - No health records storage
    """

    def __init__(self):
        """Initialize the memory manager."""
        logger.info("LyraMemoryManager initialized")

    async def ingest_creative_snippets(
        self, items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Ingest creative snippets into long-term memory.

        Args:
            items: List of items with text, category, metadata

        Returns:
            List of ingestion results
        """
        logger.info(f"Ingesting {len(items)} creative snippets")
        return await ingest_items(items)

    async def retrieve_context(
        self,
        prompt: str,
        task_type: Optional[str] = None,
        categories: Optional[List[str]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context for a creative task.

        Args:
            prompt: Query prompt
            task_type: Optional task type for category hints
            categories: Optional specific categories to search
            top_k: Number of results to return

        Returns:
            List of relevant memory items
        """
        # If no categories specified, infer from task type
        if categories is None and task_type:
            categories = self._get_categories_for_task(task_type)

        logger.info(
            f"Retrieving context for prompt (task_type={task_type}, "
            f"categories={categories}, top_k={top_k})"
        )

        return await query_relevant(
            query=prompt,
            categories=categories,
            top_k=top_k
        )

    def _get_categories_for_task(self, task_type: str) -> Optional[List[str]]:
        """
        Map task types to relevant memory categories.

        Args:
            task_type: The creative task type

        Returns:
            List of relevant categories or None for all
        """
        category_mapping = {
            "narrative_design": ["narratives", "themes", "motifs"],
            "idea_generation": ["themes", "creative_history", "motifs"],
            "analogy_exploration": ["motifs", "themes", "styles"],
            "reframe": ["themes", "styles", "creative_history"],
            "counterfactual_analysis": ["themes", "narratives"],
            "tone_mapping": ["styles", "themes"],
            "mixed_creative": None,  # Search all categories
        }

        return category_mapping.get(task_type)

    async def get_by_category(
        self, category: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get items from a specific category.

        Args:
            category: Category name
            limit: Maximum items to return

        Returns:
            List of items
        """
        return await query_by_category(category, limit)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics.

        Returns:
            Dict with category counts
        """
        return get_memory_stats()

    def get_valid_categories(self) -> List[str]:
        """
        Get list of valid memory categories.

        Returns:
            List of category names
        """
        return get_valid_categories()
