"""
Lyra Agent Memory Routes

API endpoints for memory ingestion and retrieval.
Phase 4: RAG + Memory integration.

GUARDRAILS:
    Lyra's memory is for creative context only:
    - No cross-agent access
    - No law/security data (Sophia/Aegis domains)
    - No compute/resource metrics (Argus domain)
    - No health/social records (Mercury domain)
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.models.schema import (
    IngestRequest,
    IngestResponse,
    IngestResult,
    MemoryPreviewRequest,
    MemoryPreviewResponse,
    MemoryPreviewItem,
    MemoryStatsResponse,
)
from app.rag.ingest import ingest_items, get_valid_categories
from app.rag.query import query_relevant, query_by_category, get_memory_stats


router = APIRouter(prefix="/memory", tags=["memory"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest_memory(request: IngestRequest) -> IngestResponse:
    """
    Ingest creative snippets into Lyra's long-term memory.

    Each item should have:
        - text: The content to store
        - category: One of themes, narratives, styles, user_preferences,
                    creative_history, motifs
        - metadata: Optional additional data

    Args:
        request: IngestRequest with list of items

    Returns:
        IngestResponse with per-item results
    """
    logger.info(f"Memory ingest request: {len(request.items)} items")

    # Convert Pydantic models to dicts for ingestion
    items_data = [
        {
            "text": item.text,
            "category": item.category,
            "metadata": item.metadata,
        }
        for item in request.items
    ]

    try:
        results = await ingest_items(items_data)

        # Convert to response format
        result_models = [
            IngestResult(
                id=r.get("id"),
                category=r.get("category"),
                status=r.get("status", "unknown"),
                timestamp=r.get("timestamp"),
                error=r.get("error"),
            )
            for r in results
        ]

        ingested_count = sum(1 for r in results if r.get("status") == "ingested")

        return IngestResponse(
            ingested_count=ingested_count,
            results=result_models,
        )

    except Exception as e:
        logger.error(f"Memory ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview", response_model=MemoryPreviewResponse)
async def preview_memory(request: MemoryPreviewRequest) -> MemoryPreviewResponse:
    """
    Preview/query items from Lyra's long-term memory.

    Supports:
        - Semantic search via query parameter
        - Category filtering
        - Result limiting via top_k

    Args:
        request: MemoryPreviewRequest with query, category, and top_k

    Returns:
        MemoryPreviewResponse with matching items
    """
    logger.info(
        f"Memory preview request: query={request.query is not None}, "
        f"category={request.category}, top_k={request.top_k}"
    )

    try:
        if request.query:
            # Semantic search
            categories = [request.category] if request.category else None
            results = await query_relevant(
                query=request.query,
                categories=categories,
                top_k=request.top_k,
            )
        elif request.category:
            # Category-based retrieval
            results = await query_by_category(
                category=request.category,
                limit=request.top_k,
            )
        else:
            # No query or category - return recent from all categories
            results = await query_relevant(
                query="",
                categories=None,
                top_k=request.top_k,
            )

        # Convert to response format
        items = [
            MemoryPreviewItem(
                id=r.get("id", ""),
                text=r.get("text", ""),
                category=r.get("category", r.get("metadata", {}).get("category", "unknown")),
                similarity=r.get("score"),
                metadata=r.get("metadata", {}),
            )
            for r in results
        ]

        return MemoryPreviewResponse(
            items=items,
            count=len(items),
            query=request.query,
            category=request.category,
        )

    except Exception as e:
        logger.error(f"Memory preview failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=MemoryStatsResponse)
async def memory_stats() -> MemoryStatsResponse:
    """
    Get statistics about Lyra's long-term memory.

    Returns:
        MemoryStatsResponse with category counts and totals
    """
    try:
        stats = get_memory_stats()
        categories = stats.get("categories", {})
        total = sum(categories.values())

        return MemoryStatsResponse(
            categories=categories,
            total_items=total,
            valid_categories=get_valid_categories(),
        )

    except Exception as e:
        logger.error(f"Memory stats failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def list_categories() -> dict:
    """
    List valid memory categories.

    Returns:
        Dict with list of valid categories
    """
    return {
        "categories": get_valid_categories(),
        "descriptions": {
            "themes": "Core themes and concepts explored",
            "narratives": "Narrative structures and story elements",
            "styles": "Creative styles and approaches",
            "user_preferences": "User-specific preferences and patterns",
            "creative_history": "History of creative outputs",
            "motifs": "Recurring motifs and patterns",
        },
    }
