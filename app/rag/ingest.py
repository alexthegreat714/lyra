"""
Lyra Agent RAG - Ingest Module

Document and content ingestion for the RAG system.
Phase 4: File-backed storage with embeddings.

GUARDRAILS:
    Lyra's memory is for creative context only:
    - NOT a log of legal rulings (Sophia)
    - NOT a security incident database (Aegis)
    - NOT a compute-performance ledger (Argus)
    - NOT health history (Mercury)

    This keeps memory aligned with Article IV's recognition of
    "strategic & conceptual contributions" as valid AI outputs.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from loguru import logger

from app.rag.embed import embed_text, _fallback_embedding


# Base directory for long-term memory
BASE_LONG_TERM_DIR = Path(__file__).parent.parent / "memory" / "long_term"

# Valid categories for creative memory
VALID_CATEGORIES = [
    "themes",
    "narratives",
    "styles",
    "user_preferences",
    "creative_history",
    "motifs",
]


async def ingest_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ingest multiple items into long-term memory.

    Each item should have:
        - text: str - The content to store
        - category: str - Category for organization
        - metadata: dict - Optional metadata

    For each item:
        - Generate embedding
        - Write JSON file under memory/long_term/<category>/<id>.json
        - Return summary records

    Args:
        items: List of items to ingest

    Returns:
        List of minimal record summaries
    """
    results = []

    for item in items:
        try:
            result = await ingest_item(item)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to ingest item: {e}")
            results.append({
                "id": None,
                "status": "error",
                "error": str(e),
            })

    return results


async def ingest_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ingest a single item into long-term memory.

    Args:
        item: Dict with text, category, and optional metadata

    Returns:
        Summary record with id, category, status
    """
    text = item.get("text", "")
    category = item.get("category", "creative_history")
    metadata = item.get("metadata", {})

    # Validate category
    if category not in VALID_CATEGORIES:
        logger.warning(f"Invalid category '{category}', using 'creative_history'")
        category = "creative_history"

    # Ensure category directory exists
    category_dir = BASE_LONG_TERM_DIR / category
    category_dir.mkdir(parents=True, exist_ok=True)

    # Generate ID and timestamp
    item_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Generate embedding
    try:
        embedding = await embed_text(text)
    except Exception as e:
        logger.warning(f"Embedding failed, using fallback: {e}")
        embedding = _fallback_embedding(text)

    # Build record
    record = {
        "id": item_id,
        "text": text,
        "metadata": {
            **metadata,
            "category": category,
            "timestamp": timestamp,
        },
        "embedding": embedding,
    }

    # Write to file
    file_path = category_dir / f"{item_id}.json"
    with open(file_path, "w") as f:
        json.dump(record, f, indent=2)

    logger.info(f"Ingested item {item_id} into {category}")

    return {
        "id": item_id,
        "category": category,
        "status": "ingested",
        "timestamp": timestamp,
    }


async def ingest_text(
    text: str,
    category: str = "creative_history",
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Convenience function to ingest a single text.

    Args:
        text: Text content to ingest
        category: Category for organization
        metadata: Optional metadata

    Returns:
        Ingestion result
    """
    return await ingest_item({
        "text": text,
        "category": category,
        "metadata": metadata or {},
    })


def ingest_items_sync(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Synchronous wrapper for ingest_items.

    Args:
        items: List of items to ingest

    Returns:
        List of ingestion results
    """
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Can't run async in running loop, use sync implementation
            return _ingest_items_sync_impl(items)
        return loop.run_until_complete(ingest_items(items))
    except RuntimeError:
        return asyncio.run(ingest_items(items))


def _ingest_items_sync_impl(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Pure synchronous implementation of ingest_items.
    """
    from app.rag.embed import embed_text_sync

    results = []

    for item in items:
        try:
            text = item.get("text", "")
            category = item.get("category", "creative_history")
            metadata = item.get("metadata", {})

            if category not in VALID_CATEGORIES:
                category = "creative_history"

            category_dir = BASE_LONG_TERM_DIR / category
            category_dir.mkdir(parents=True, exist_ok=True)

            item_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat() + "Z"

            embedding = embed_text_sync(text)

            record = {
                "id": item_id,
                "text": text,
                "metadata": {**metadata, "category": category, "timestamp": timestamp},
                "embedding": embedding,
            }

            file_path = category_dir / f"{item_id}.json"
            with open(file_path, "w") as f:
                json.dump(record, f, indent=2)

            results.append({
                "id": item_id,
                "category": category,
                "status": "ingested",
                "timestamp": timestamp,
            })
        except Exception as e:
            results.append({"id": None, "status": "error", "error": str(e)})

    return results


def get_valid_categories() -> List[str]:
    """Return list of valid memory categories."""
    return VALID_CATEGORIES.copy()
