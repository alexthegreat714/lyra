"""
Lyra Agent RAG - Embed Module

Text embedding for the RAG system.
Phase 4: Simple HTTP client for embedding service.

GUARDRAILS:
    Lyra's embeddings are for creative context only:
    - NOT for legal document embeddings (Sophia)
    - NOT for security incident embeddings (Aegis)
    - NOT for compute/performance metrics (Argus)
    - NOT for health records (Mercury)
"""

import os
import math
from typing import List

import httpx
from loguru import logger


# Configuration from environment
EMBEDDING_MODEL = os.getenv("LYRA_EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_ENDPOINT = os.getenv(
    "LYRA_EMBEDDING_ENDPOINT", "http://localhost:11434/api/embeddings"
)
EMBEDDING_TIMEOUT = float(os.getenv("LYRA_EMBEDDING_TIMEOUT", "30.0"))


async def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Given a list of texts, return list of embedding vectors.

    Phase 4: Simple HTTP client; no batching complexity.
    Uses Ollama-compatible endpoint by default.

    Args:
        texts: List of text strings to embed

    Returns:
        List of embedding vectors (list of floats)
    """
    if not texts:
        return []

    embeddings = []

    async with httpx.AsyncClient(timeout=EMBEDDING_TIMEOUT) as client:
        for text in texts:
            try:
                embedding = await _embed_single(client, text)
                embeddings.append(embedding)
            except Exception as e:
                logger.warning(f"Embedding failed for text, using fallback: {e}")
                # Fallback: return simple hash-based pseudo-embedding
                embeddings.append(_fallback_embedding(text))

    return embeddings


async def embed_text(text: str) -> List[float]:
    """
    Embed a single text string.

    Args:
        text: Text to embed

    Returns:
        Embedding vector
    """
    results = await embed_texts([text])
    return results[0] if results else _fallback_embedding(text)


async def _embed_single(client: httpx.AsyncClient, text: str) -> List[float]:
    """
    Embed a single text using the configured endpoint.

    Args:
        client: HTTP client
        text: Text to embed

    Returns:
        Embedding vector
    """
    try:
        response = await client.post(
            EMBEDDING_ENDPOINT,
            json={
                "model": EMBEDDING_MODEL,
                "prompt": text,
            },
        )
        response.raise_for_status()
        data = response.json()

        # Ollama format returns {"embedding": [...]}
        if "embedding" in data:
            return data["embedding"]

        # OpenAI format returns {"data": [{"embedding": [...]}]}
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]["embedding"]

        logger.warning("Unknown embedding response format")
        return _fallback_embedding(text)

    except httpx.HTTPStatusError as e:
        logger.warning(f"HTTP error during embedding: {e}")
        raise
    except httpx.RequestError as e:
        logger.warning(f"Request error during embedding: {e}")
        raise


def _fallback_embedding(text: str, dimensions: int = 384) -> List[float]:
    """
    Generate a simple fallback pseudo-embedding when the embedding service
    is unavailable. Uses hash-based approach for consistency.

    This is NOT a real embedding - just ensures the system doesn't crash
    when the embedding service is down.

    Args:
        text: Text to create pseudo-embedding for
        dimensions: Number of dimensions

    Returns:
        Pseudo-embedding vector
    """
    if not text:
        return [0.0] * dimensions

    # Use hash for deterministic output
    hash_val = hash(text)

    # Generate pseudo-embedding from hash
    embedding = []
    for i in range(dimensions):
        # Create varied values based on hash and position
        val = ((hash_val + i * 31) % 1000) / 1000.0 - 0.5
        embedding.append(val)

    # Normalize
    magnitude = math.sqrt(sum(x * x for x in embedding))
    if magnitude > 0:
        embedding = [x / magnitude for x in embedding]

    return embedding


def embed_texts_sync(texts: List[str]) -> List[List[float]]:
    """
    Synchronous wrapper for embed_texts.
    Useful for contexts where async isn't available.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, use fallback
            return [_fallback_embedding(t) for t in texts]
        return loop.run_until_complete(embed_texts(texts))
    except RuntimeError:
        # No event loop, create one
        return asyncio.run(embed_texts(texts))


def embed_text_sync(text: str) -> List[float]:
    """
    Synchronous wrapper for embed_text.

    Args:
        text: Text to embed

    Returns:
        Embedding vector
    """
    results = embed_texts_sync([text])
    return results[0] if results else _fallback_embedding(text)
