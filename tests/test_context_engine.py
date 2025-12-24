"""Unit tests for context_engine module."""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from unittest.mock import patch


class TestGetEmbedding:
    """Tests for get_embedding function."""

    def test_returns_zeros_without_openai(self):
        """Should return zero vector when OpenAI not available."""
        with patch("context_engine.HAS_OPENAI", False):
            from context_engine import get_embedding, EMBEDDING_DIM

            result = get_embedding("test query")
            assert len(result) == EMBEDDING_DIM
            assert all(v == 0.0 for v in result)

    def test_returns_zeros_without_api_key(self):
        """Should return zero vector when API key not set."""
        with patch("context_engine.OPENAI_API_KEY", ""):
            from context_engine import get_embedding, EMBEDDING_DIM

            result = get_embedding("test query")
            assert len(result) == EMBEDDING_DIM
            assert all(v == 0.0 for v in result)

    def test_uses_cache_on_repeated_calls(self):
        """Should return cached embedding on repeated calls."""
        from context_engine import get_embedding, _embedding_cache

        # Pre-populate cache
        test_embedding = [1.0] * 1536
        import hashlib

        cache_key = hashlib.md5("test query".encode()).hexdigest()
        _embedding_cache[cache_key] = test_embedding

        result = get_embedding("test query", use_cache=True)
        assert result == test_embedding

        # Cleanup
        del _embedding_cache[cache_key]


class TestRateLimiting:
    """Tests for rate limiting."""

    def test_check_rate_limit_allows_initial_calls(self):
        """Should allow calls within rate limit."""
        import context_engine

        # Clear state
        context_engine._rate_limit_calls.clear()

        assert context_engine._check_rate_limit() is True
        assert len(context_engine._rate_limit_calls) == 1

    def test_check_rate_limit_blocks_excess_calls(self):
        """Should block calls exceeding rate limit."""
        import time
        import context_engine

        # Fill up rate limit
        context_engine._rate_limit_calls.clear()
        now = time.time()
        context_engine._rate_limit_calls.extend([now] * context_engine.RATE_LIMIT_CALLS)

        assert context_engine._check_rate_limit() is False

        # Cleanup
        context_engine._rate_limit_calls.clear()


class TestExecutionCache:
    """Tests for ExecutionCache class."""

    def test_local_cache_fallback(self):
        """Should use local cache when Redis unavailable."""
        from context_engine import ExecutionCache

        cache = ExecutionCache(redis_client=None)

        # Put should work
        result = cache.put("test query", "test result")
        assert result is True

        # Local cache should have entry
        assert len(cache._local_cache) == 1


class TestGuidanceCache:
    """Tests for GuidanceCache class."""

    def test_local_cache_fallback(self):
        """Should use local cache when Redis unavailable."""
        from context_engine import GuidanceCache

        cache = GuidanceCache(redis_client=None)

        # Put should work
        result = cache.put("test error", "test fix", "python")
        assert result is True

        # Local cache should have entry
        assert len(cache._local_cache) == 1


class TestContextEngine:
    """Tests for ContextEngine class."""

    def test_status_returns_dict(self):
        """Should return status dict."""
        from context_engine import ContextEngine

        engine = ContextEngine()
        status = engine.status()

        assert isinstance(status, dict)
        assert "redis_available" in status
        assert "mode" in status
        assert "memories_count" in status

    def test_get_context_returns_result(self):
        """Should return ContextResult."""
        from context_engine import ContextEngine, ContextResult

        engine = ContextEngine()
        result = engine.get_context("test query", include_cache=False)

        assert isinstance(result, ContextResult)
        assert result.source in ("none", "memory", "cache", "guidance", "combined")


class TestConstants:
    """Tests for configuration constants."""

    def test_thresholds_are_valid(self):
        """Thresholds should be between 0 and 1."""
        from context_engine import SIMILARITY_THRESHOLD, GUIDANCE_THRESHOLD

        assert 0 < SIMILARITY_THRESHOLD <= 1
        assert 0 < GUIDANCE_THRESHOLD <= 1

    def test_embedding_dim_matches_model(self):
        """Embedding dimension should match text-embedding-3-small."""
        from context_engine import EMBEDDING_DIM

        assert EMBEDDING_DIM == 1536

    def test_rate_limits_are_reasonable(self):
        """Rate limits should be reasonable."""
        from context_engine import RATE_LIMIT_CALLS, RATE_LIMIT_WINDOW

        assert RATE_LIMIT_CALLS > 0
        assert RATE_LIMIT_WINDOW > 0
        assert RATE_LIMIT_CALLS <= 100  # Not too high
