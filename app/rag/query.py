"""
Lyra Agent RAG - Query Module

Knowledge retrieval for the RAG system.
Phase 4: File-based scanning with cosine similarity.

GUARDRAILS:
    Lyra's memory queries are for creative context only:
    - NOT for legal precedent lookup (Sophia)
    - NOT for security threat queries (Aegis)
    - NOT for compute resource queries (Argus)
    - NOT for health record queries (Mercury)
"""

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from app.rag.embed import embed_text, _fallback_embedding


# Base directory for long-term memory
BASE_LONG_TERM_DIR = Path(__file__).parent.parent / "memory" / "long_term"


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        a: First vector
        b: Second vector

    Returns:
        Cosine similarity score (-1 to 1)
    """
    if not a or not b:
        return 0.0

    if len(a) != len(b):
        # Vectors must be same dimension
        return 0.0

    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


async def query_relevant(
    query: str,
    categories: Optional[List[str]] = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Query long-term memory for relevant items.

    Args:
        query: Query string
        categories: Optional list of categories to search (None = all)
        top_k: Number of top results to return

    Returns:
        List of relevant items with structure:
            { "id", "category", "text", "metadata", "score" }
    """
    if not query:
        return []

    # Embed the query
    try:
        query_embedding = await embed_text(query)
    except Exception as e:
        logger.warning(f"Query embedding failed, using fallback: {e}")
        query_embedding = _fallback_embedding(query)

    # Determine which categories to search
    if categories:
        search_categories = categories
    else:
        # Search all subdirectories
        search_categories = [
            d.name for d in BASE_LONG_TERM_DIR.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

    # Collect all candidates with scores
    candidates = []

    for category in search_categories:
        category_dir = BASE_LONG_TERM_DIR / category
        if not category_dir.exists():
            continue

        for file_path in category_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    record = json.load(f)

                embedding = record.get("embedding", [])
                score = _cosine_similarity(query_embedding, embedding)

                candidates.append({
                    "id": record.get("id"),
                    "category": category,
                    "text": record.get("text", ""),
                    "metadata": record.get("metadata", {}),
                    "score": score,
                })
            except Exception as e:
                logger.warning(f"Failed to read {file_path}: {e}")
                continue

    # Sort by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)

    # Return top_k
    return candidates[:top_k]


async def query_by_category(
    category: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Get items from a specific category (no similarity ranking).

    Args:
        category: Category to query
        limit: Maximum items to return

    Returns:
        List of items from the category
    """
    category_dir = BASE_LONG_TERM_DIR / category
    if not category_dir.exists():
        return []

    items = []
    for file_path in list(category_dir.glob("*.json"))[:limit]:
        try:
            with open(file_path, "r") as f:
                record = json.load(f)

            items.append({
                "id": record.get("id"),
                "category": category,
                "text": record.get("text", ""),
                "metadata": record.get("metadata", {}),
            })
        except Exception as e:
            logger.warning(f"Failed to read {file_path}: {e}")
            continue

    return items


def query_relevant_sync(
    query: str,
    categories: Optional[List[str]] = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Synchronous wrapper for query_relevant.

    Args:
        query: Query string
        categories: Optional categories to search
        top_k: Number of results

    Returns:
        List of relevant items
    """
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Use sync implementation
            return _query_relevant_sync_impl(query, categories, top_k)
        return loop.run_until_complete(query_relevant(query, categories, top_k))
    except RuntimeError:
        return asyncio.run(query_relevant(query, categories, top_k))


def _query_relevant_sync_impl(
    query: str,
    categories: Optional[List[str]] = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Pure synchronous implementation of query_relevant.
    """
    from app.rag.embed import embed_text_sync

    if not query:
        return []

    query_embedding = embed_text_sync(query)

    if categories:
        search_categories = categories
    else:
        search_categories = [
            d.name for d in BASE_LONG_TERM_DIR.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

    candidates = []

    for category in search_categories:
        category_dir = BASE_LONG_TERM_DIR / category
        if not category_dir.exists():
            continue

        for file_path in category_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    record = json.load(f)

                embedding = record.get("embedding", [])
                score = _cosine_similarity(query_embedding, embedding)

                candidates.append({
                    "id": record.get("id"),
                    "category": category,
                    "text": record.get("text", ""),
                    "metadata": record.get("metadata", {}),
                    "score": score,
                })
            except Exception:
                continue

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:top_k]


def get_memory_stats() -> Dict[str, Any]:
    """
    Get statistics about stored memory.

    Returns:
        Dict with category counts and total items
    """
    stats = {"total": 0, "categories": {}}

    for category_dir in BASE_LONG_TERM_DIR.iterdir():
        if category_dir.is_dir() and not category_dir.name.startswith("."):
            count = len(list(category_dir.glob("*.json")))
            stats["categories"][category_dir.name] = count
            stats["total"] += count

    return stats
