"""
Tests for Lyra Memory System

Phase 4: RAG + Memory integration tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.server import app
from app.rag.embed import _fallback_embedding
from app.rag.ingest import VALID_CATEGORIES, get_valid_categories
from app.rag.query import _cosine_similarity


client = TestClient(app)


class TestMemoryEndpoints:
    """Tests for memory API endpoints."""

    def test_memory_stats(self):
        """Test /memory/stats endpoint."""
        response = client.get("/memory/stats")
        assert response.status_code == 200

        data = response.json()
        assert "categories" in data
        assert "total_items" in data
        assert "valid_categories" in data
        assert isinstance(data["categories"], dict)
        assert isinstance(data["valid_categories"], list)

    def test_memory_categories(self):
        """Test /memory/categories endpoint."""
        response = client.get("/memory/categories")
        assert response.status_code == 200

        data = response.json()
        assert "categories" in data
        assert "descriptions" in data
        assert len(data["categories"]) == 6  # 6 valid categories

    def test_memory_ingest_empty(self):
        """Test ingest with empty items list."""
        response = client.post(
            "/memory/ingest",
            json={"items": []}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["ingested_count"] == 0
        assert data["results"] == []

    def test_memory_ingest_single(self):
        """Test ingesting a single item."""
        response = client.post(
            "/memory/ingest",
            json={
                "items": [
                    {
                        "text": "Test creative concept for memory",
                        "category": "themes",
                        "metadata": {"source": "test"}
                    }
                ]
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["ingested_count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["status"] == "ingested"
        assert data["results"][0]["category"] == "themes"
        assert data["results"][0]["id"] is not None

    def test_memory_ingest_multiple_categories(self):
        """Test ingesting items across multiple categories."""
        response = client.post(
            "/memory/ingest",
            json={
                "items": [
                    {"text": "A narrative arc concept", "category": "narratives"},
                    {"text": "A recurring motif pattern", "category": "motifs"},
                    {"text": "A style guideline", "category": "styles"},
                ]
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["ingested_count"] == 3
        categories = {r["category"] for r in data["results"]}
        assert "narratives" in categories
        assert "motifs" in categories
        assert "styles" in categories

    def test_memory_preview_empty_query(self):
        """Test preview with empty query."""
        response = client.post(
            "/memory/preview",
            json={"top_k": 5}
        )
        # Should work but return empty or minimal results
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "count" in data
        assert isinstance(data["items"], list)

    def test_memory_preview_with_query(self):
        """Test preview with semantic query."""
        # First ingest something
        client.post(
            "/memory/ingest",
            json={
                "items": [
                    {
                        "text": "The hero's journey begins in darkness",
                        "category": "narratives",
                        "metadata": {"type": "test"}
                    }
                ]
            }
        )

        # Then query
        response = client.post(
            "/memory/preview",
            json={
                "query": "hero journey narrative",
                "top_k": 3
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert data["query"] == "hero journey narrative"

    def test_memory_preview_by_category(self):
        """Test preview filtered by category."""
        response = client.post(
            "/memory/preview",
            json={
                "category": "themes",
                "top_k": 5
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert data["category"] == "themes"


class TestEmbedding:
    """Tests for embedding functionality."""

    def test_fallback_embedding_generates_vector(self):
        """Test fallback embedding generates proper vector."""
        embedding = _fallback_embedding("test text")

        assert isinstance(embedding, list)
        assert len(embedding) == 384  # Default dimensions
        assert all(isinstance(x, float) for x in embedding)

    def test_fallback_embedding_deterministic(self):
        """Test fallback embedding is deterministic."""
        text = "same text input"
        emb1 = _fallback_embedding(text)
        emb2 = _fallback_embedding(text)

        assert emb1 == emb2

    def test_fallback_embedding_different_inputs(self):
        """Test different inputs produce different embeddings."""
        emb1 = _fallback_embedding("first text")
        emb2 = _fallback_embedding("second text")

        assert emb1 != emb2

    def test_fallback_embedding_empty_input(self):
        """Test fallback with empty input."""
        embedding = _fallback_embedding("")

        assert isinstance(embedding, list)
        assert len(embedding) == 384
        assert all(x == 0.0 for x in embedding)

    def test_fallback_embedding_normalized(self):
        """Test fallback embedding is normalized (unit length)."""
        import math

        embedding = _fallback_embedding("test normalization")
        magnitude = math.sqrt(sum(x * x for x in embedding))

        assert abs(magnitude - 1.0) < 0.0001  # Close to unit length


class TestCosineSimilarity:
    """Tests for cosine similarity calculation."""

    def test_identical_vectors(self):
        """Test similarity of identical vectors is 1."""
        vec = [1.0, 2.0, 3.0]
        similarity = _cosine_similarity(vec, vec)

        assert abs(similarity - 1.0) < 0.0001

    def test_orthogonal_vectors(self):
        """Test similarity of orthogonal vectors is 0."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0]
        similarity = _cosine_similarity(vec1, vec2)

        assert abs(similarity) < 0.0001

    def test_opposite_vectors(self):
        """Test similarity of opposite vectors is -1."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [-1.0, -2.0, -3.0]
        similarity = _cosine_similarity(vec1, vec2)

        assert abs(similarity - (-1.0)) < 0.0001

    def test_empty_vectors(self):
        """Test similarity of empty vectors is 0."""
        similarity = _cosine_similarity([], [])
        assert similarity == 0.0

    def test_different_length_vectors(self):
        """Test similarity of different length vectors is 0."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [1.0, 2.0]
        similarity = _cosine_similarity(vec1, vec2)

        assert similarity == 0.0


class TestValidCategories:
    """Tests for category validation."""

    def test_valid_categories_list(self):
        """Test VALID_CATEGORIES contains expected categories."""
        expected = [
            "themes",
            "narratives",
            "styles",
            "user_preferences",
            "creative_history",
            "motifs",
        ]
        assert VALID_CATEGORIES == expected

    def test_get_valid_categories_returns_copy(self):
        """Test get_valid_categories returns a copy."""
        cats1 = get_valid_categories()
        cats2 = get_valid_categories()

        # Should be equal but not same object
        assert cats1 == cats2
        assert cats1 is not cats2

    def test_category_count(self):
        """Test correct number of categories."""
        assert len(VALID_CATEGORIES) == 6
