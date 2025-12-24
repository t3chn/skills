#!/usr/bin/env python3
"""
Context Engine - Unified context management for AI agents.

Combines:
- UnifiedMemory: Long-term semantic memory (Serena + Redis)
- ExecutionCache: Query→Result caching with semantic matching
- GuidanceCache: Error→Fix pattern learning

Usage:
    engine = ContextEngine()

    # Get context for a query
    context = engine.get_context("how to handle auth errors")

    # Record successful execution for future cache hits
    engine.record_success(query="auth error handling", result="use retry with backoff")

    # Learn from failures
    engine.learn_failure(error="ConnectionError", fix="check Redis connection", domain="redis")
"""

import struct
import hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

# Import UnifiedMemory from same directory
from unified_memory import UnifiedMemory, MemoryResult, HAS_OPENAI, OPENAI_API_KEY

# Configuration
CACHE_PREFIX = "exec_cache:"
GUIDANCE_PREFIX = "guidance:"
SIMILARITY_THRESHOLD = 0.85  # High threshold for execution cache
GUIDANCE_THRESHOLD = 0.75  # Lower threshold for guidance (more fuzzy matching)
EMBEDDING_DIM = 1536  # text-embedding-3-small dimension
EMBEDDING_MAX_CHARS = 8000  # Safe limit for embedding input

# Shared embedding cache to avoid duplicate API calls
_embedding_cache: dict[str, list[float]] = {}


def get_embedding(text: str, use_cache: bool = True) -> list[float]:
    """
    Generate embedding using OpenAI with caching.

    Args:
        text: Text to embed (truncated to EMBEDDING_MAX_CHARS)
        use_cache: Whether to use in-memory cache

    Returns:
        Embedding vector (EMBEDDING_DIM floats)
    """
    if not HAS_OPENAI or not OPENAI_API_KEY:
        return [0.0] * EMBEDDING_DIM

    # Truncate and hash for cache key
    text_truncated = text[:EMBEDDING_MAX_CHARS]
    cache_key = hashlib.md5(text_truncated.encode()).hexdigest()

    # Check cache
    if use_cache and cache_key in _embedding_cache:
        return _embedding_cache[cache_key]

    # Generate embedding
    import openai

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-small", input=text_truncated
    )
    embedding = response.data[0].embedding

    # Cache result
    if use_cache:
        _embedding_cache[cache_key] = embedding

    return embedding


@dataclass
class CacheHit:
    """Result from execution cache lookup."""

    query: str
    result: str
    score: float
    cached_at: str
    hits: int = 0


@dataclass
class GuidanceHit:
    """Result from guidance cache lookup."""

    error_pattern: str
    fix: str
    domain: str
    score: float
    success_count: int = 0


@dataclass
class ContextResult:
    """Combined context from all sources."""

    memories: list[MemoryResult] = field(default_factory=list)
    cached_result: Optional[CacheHit] = None
    guidance: list[GuidanceHit] = field(default_factory=list)
    source: str = "none"  # "cache", "memory", "guidance", "combined"


class ExecutionCache:
    """
    Cache for query→result pairs with semantic matching.

    Stores successful query executions and retrieves them
    when similar queries are made (threshold 0.85).
    """

    def __init__(self, redis_client=None):
        self._redis = redis_client
        self._local_cache = {}  # Fallback when Redis unavailable

    @property
    def redis(self):
        return self._redis

    @redis.setter
    def redis(self, client):
        self._redis = client

    def get(
        self, query: str, threshold: float = SIMILARITY_THRESHOLD
    ) -> Optional[CacheHit]:
        """
        Look up cached result for similar query.

        Args:
            query: The query to look up
            threshold: Minimum similarity score (default 0.85)

        Returns:
            CacheHit if found, None otherwise
        """
        if not self._redis:
            # Fallback: exact match in local cache
            query_hash = hashlib.md5(query.lower().encode()).hexdigest()
            if query_hash in self._local_cache:
                entry = self._local_cache[query_hash]
                return CacheHit(
                    query=entry["query"],
                    result=entry["result"],
                    score=1.0,
                    cached_at=entry["cached_at"],
                    hits=entry.get("hits", 0),
                )
            return None

        try:
            # Semantic search in Redis
            from redis.commands.search.query import Query

            embedding = get_embedding(query)
            query_vector = struct.pack(f"{len(embedding)}f", *embedding)

            q = (
                Query("*=>[KNN 1 @embedding $vec AS score]")
                .return_fields("query", "result", "cached_at", "hits", "score")
                .sort_by("score")
                .dialect(2)
            )

            results = self._redis.ft("exec_cache_idx").search(
                q, query_params={"vec": query_vector}
            )

            if results.docs:
                doc = results.docs[0]
                similarity = 1 - float(doc.score)

                if similarity >= threshold:
                    # Increment hit counter
                    doc_id = doc.id
                    self._redis.hincrby(doc_id, "hits", 1)

                    return CacheHit(
                        query=doc.query,
                        result=doc.result,
                        score=similarity,
                        cached_at=doc.cached_at,
                        hits=int(doc.hits) + 1,
                    )
        except Exception as e:
            print(f"ExecutionCache.get error: {e}")

        return None

    def put(self, query: str, result: str) -> bool:
        """
        Store query→result pair in cache.

        Args:
            query: The original query
            result: The successful result

        Returns:
            True if stored successfully
        """
        query_hash = hashlib.md5(query.lower().encode()).hexdigest()
        cached_at = datetime.now().isoformat()

        entry = {"query": query, "result": result, "cached_at": cached_at, "hits": 0}

        # Always store locally
        self._local_cache[query_hash] = entry

        if not self._redis:
            return True

        try:
            doc_id = f"{CACHE_PREFIX}{query_hash}"
            embedding = get_embedding(query)

            self._redis.hset(
                doc_id,
                mapping={
                    **entry,
                    "embedding": struct.pack(f"{len(embedding)}f", *embedding),
                },
            )
            return True
        except Exception as e:
            print(f"ExecutionCache.put error: {e}")
            return False


class GuidanceCache:
    """
    Cache for error→fix patterns.

    Learns from failures and provides guidance for similar errors.
    Organized by domain (python, go, typescript, redis, etc.)
    """

    def __init__(self, redis_client=None):
        self._redis = redis_client
        self._local_cache = {}  # Fallback

    @property
    def redis(self):
        return self._redis

    @redis.setter
    def redis(self, client):
        self._redis = client

    def get(
        self, error: str, domain: str = "", threshold: float = GUIDANCE_THRESHOLD
    ) -> list[GuidanceHit]:
        """
        Look up guidance for error.

        Args:
            error: The error message or pattern
            domain: Optional domain filter (python, go, etc.)
            threshold: Minimum similarity score

        Returns:
            List of matching guidance entries
        """
        if not self._redis:
            # Fallback: keyword matching
            results = []
            error_lower = error.lower()
            for key, entry in self._local_cache.items():
                if domain and entry.get("domain") != domain:
                    continue
                if error_lower in entry["error_pattern"].lower():
                    results.append(
                        GuidanceHit(
                            error_pattern=entry["error_pattern"],
                            fix=entry["fix"],
                            domain=entry.get("domain", ""),
                            score=0.5,
                            success_count=entry.get("success_count", 0),
                        )
                    )
            return results[:5]

        try:
            from redis.commands.search.query import Query

            embedding = get_embedding(error)
            query_vector = struct.pack(f"{len(embedding)}f", *embedding)

            # Build query with optional domain filter
            filter_str = f"@domain:{{{domain}}}" if domain else "*"
            q = (
                Query(f"{filter_str}=>[KNN 5 @embedding $vec AS score]")
                .return_fields(
                    "error_pattern", "fix", "domain", "success_count", "score"
                )
                .sort_by("score")
                .dialect(2)
            )

            results = self._redis.ft("guidance_idx").search(
                q, query_params={"vec": query_vector}
            )

            hits = []
            for doc in results.docs:
                similarity = 1 - float(doc.score)
                if similarity >= threshold:
                    hits.append(
                        GuidanceHit(
                            error_pattern=doc.error_pattern,
                            fix=doc.fix,
                            domain=getattr(doc, "domain", ""),
                            score=similarity,
                            success_count=int(getattr(doc, "success_count", 0)),
                        )
                    )
            return hits
        except Exception as e:
            print(f"GuidanceCache.get error: {e}")
            return []

    def put(self, error: str, fix: str, domain: str = "") -> bool:
        """
        Store error→fix pattern.

        Args:
            error: The error message or pattern
            fix: The fix that worked
            domain: Category (python, go, typescript, etc.)

        Returns:
            True if stored successfully
        """
        error_hash = hashlib.md5(error.lower().encode()).hexdigest()

        entry = {
            "error_pattern": error,
            "fix": fix,
            "domain": domain,
            "success_count": 1,
            "created_at": datetime.now().isoformat(),
        }

        # Always store locally
        self._local_cache[error_hash] = entry

        if not self._redis:
            return True

        try:
            doc_id = f"{GUIDANCE_PREFIX}{error_hash}"

            # Check if exists, increment success_count
            existing = self._redis.hget(doc_id, "success_count")
            if existing:
                entry["success_count"] = int(existing) + 1

            embedding = get_embedding(error)
            self._redis.hset(
                doc_id,
                mapping={
                    **entry,
                    "embedding": struct.pack(f"{len(embedding)}f", *embedding),
                },
            )
            return True
        except Exception as e:
            print(f"GuidanceCache.put error: {e}")
            return False


class ContextEngine:
    """
    Unified context engine combining all context sources.

    Orchestrates:
    - UnifiedMemory (Serena + Redis semantic search)
    - ExecutionCache (query→result caching)
    - GuidanceCache (error→fix patterns)

    Provides graceful degradation when Redis unavailable.
    """

    def __init__(self, serena_path: str = None, redis_url: str = None):
        self.memory = UnifiedMemory(serena_path=serena_path, redis_url=redis_url)
        self.exec_cache = ExecutionCache()
        self.guidance_cache = GuidanceCache()

        # Share Redis connection
        if self.memory.is_redis_available:
            self.exec_cache.redis = self.memory.redis
            self.guidance_cache.redis = self.memory.redis

    def ensure_indexes(self) -> dict:
        """
        Create Redis search indexes for execution and guidance caches.

        Returns:
            Dict with creation status for each index
        """
        if not self.is_redis_available:
            return {"error": "Redis not available"}

        results = {}
        r = self.memory.redis

        # Execution cache index
        try:
            r.ft("exec_cache_idx").info()
            results["exec_cache_idx"] = "exists"
        except Exception:
            try:
                from redis.commands.search.field import (
                    TextField,
                    NumericField,
                    VectorField,
                )
                from redis.commands.search.index_definition import (
                    IndexDefinition,
                    IndexType,
                )

                schema = (
                    TextField("query"),
                    TextField("result"),
                    TextField("cached_at"),
                    NumericField("hits"),
                    VectorField(
                        "embedding",
                        "HNSW",
                        {"TYPE": "FLOAT32", "DIM": 1536, "DISTANCE_METRIC": "COSINE"},
                    ),
                )
                r.ft("exec_cache_idx").create_index(
                    schema,
                    definition=IndexDefinition(
                        prefix=["exec_cache:"], index_type=IndexType.HASH
                    ),
                )
                results["exec_cache_idx"] = "created"
            except Exception as e:
                results["exec_cache_idx"] = f"error: {e}"

        # Guidance cache index
        try:
            r.ft("guidance_idx").info()
            results["guidance_idx"] = "exists"
        except Exception:
            try:
                from redis.commands.search.field import (
                    TextField,
                    NumericField,
                    TagField,
                    VectorField,
                )
                from redis.commands.search.index_definition import (
                    IndexDefinition,
                    IndexType,
                )

                schema = (
                    TextField("error_pattern"),
                    TextField("fix"),
                    TagField("domain"),
                    NumericField("success_count"),
                    TextField("created_at"),
                    VectorField(
                        "embedding",
                        "HNSW",
                        {"TYPE": "FLOAT32", "DIM": 1536, "DISTANCE_METRIC": "COSINE"},
                    ),
                )
                r.ft("guidance_idx").create_index(
                    schema,
                    definition=IndexDefinition(
                        prefix=["guidance:"], index_type=IndexType.HASH
                    ),
                )
                results["guidance_idx"] = "created"
            except Exception as e:
                results["guidance_idx"] = f"error: {e}"

        return results

    @property
    def is_redis_available(self) -> bool:
        """Check if Redis is available."""
        return self.memory.is_redis_available

    def get_context(
        self,
        query: str,
        include_cache: bool = True,
        include_guidance: bool = True,
        include_memories: bool = True,
        memory_limit: int = 3,
        guidance_limit: int = 3,
    ) -> ContextResult:
        """
        Get unified context for a query.

        Checks (in order):
        1. Execution cache (fast path if high-confidence match)
        2. Guidance cache (for error-related queries)
        3. Long-term memories (semantic search)

        Args:
            query: The query to find context for
            include_cache: Whether to check execution cache
            include_guidance: Whether to check guidance cache
            include_memories: Whether to search memories
            memory_limit: Max memories to return
            guidance_limit: Max guidance entries to return

        Returns:
            ContextResult with all relevant context
        """
        result = ContextResult()
        sources = []

        # 1. Check execution cache first (fast path)
        if include_cache:
            cache_hit = self.exec_cache.get(query)
            if cache_hit:
                result.cached_result = cache_hit
                sources.append("cache")
                # High confidence cache hit - can skip other sources
                if cache_hit.score >= 0.95:
                    result.source = "cache"
                    return result

        # 2. Check guidance (especially for error messages)
        if include_guidance:
            # Detect if query looks like an error
            error_keywords = [
                "error",
                "exception",
                "failed",
                "cannot",
                "unable",
                "traceback",
            ]
            is_error = any(kw in query.lower() for kw in error_keywords)

            if is_error:
                guidance = self.guidance_cache.get(query)[:guidance_limit]
                if guidance:
                    result.guidance = guidance
                    sources.append("guidance")

        # 3. Search long-term memories
        if include_memories:
            memories = self.memory.search(query, limit=memory_limit)
            if memories:
                result.memories = memories
                sources.append("memory")

        # Set source
        if len(sources) > 1:
            result.source = "combined"
        elif sources:
            result.source = sources[0]

        return result

    def record_success(self, query: str, result: str) -> bool:
        """
        Record successful query execution for future cache hits.

        Args:
            query: The original query
            result: The successful result

        Returns:
            True if recorded successfully
        """
        return self.exec_cache.put(query, result)

    def learn_failure(self, error: str, fix: str, domain: str = "") -> bool:
        """
        Learn from a failure for future guidance.

        Args:
            error: The error message or pattern
            fix: The fix that worked
            domain: Category (python, go, typescript, etc.)

        Returns:
            True if learned successfully
        """
        return self.guidance_cache.put(error, fix, domain)

    def write_memory(self, filename: str, content: str, metadata: dict = None) -> bool:
        """
        Write a long-term memory (delegates to UnifiedMemory).

        Args:
            filename: Memory filename
            content: Memory content
            metadata: Optional metadata

        Returns:
            True if written successfully
        """
        return self.memory.write(filename, content, metadata)

    def search_memories(self, query: str, limit: int = 5) -> list[MemoryResult]:
        """
        Search long-term memories (delegates to UnifiedMemory).

        Args:
            query: Search query
            limit: Max results

        Returns:
            List of matching memories
        """
        return self.memory.search(query, limit=limit)

    def status(self) -> dict:
        """Get engine status."""
        return {
            "redis_available": self.is_redis_available,
            "serena_path": str(self.memory.serena_path),
            "memories_count": len(self.memory.list_memories()),
            "mode": "full" if self.is_redis_available else "degraded",
        }


# CLI interface
if __name__ == "__main__":
    import sys

    engine = ContextEngine()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  context_engine.py context <query>     - Get context for query")
        print("  context_engine.py cache <query> <result> - Cache execution result")
        print("  context_engine.py learn <error> <fix> [domain] - Learn from failure")
        print("  context_engine.py status              - Show engine status")
        print("  context_engine.py init                - Create Redis indexes")
        sys.exit(1)

    command = sys.argv[1]

    if command == "context" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        result = engine.get_context(query)

        print(f"Source: {result.source}")

        if result.cached_result:
            print(f"\nCached result (score: {result.cached_result.score:.2f}):")
            print(f"  {result.cached_result.result[:200]}...")

        if result.guidance:
            print(f"\nGuidance ({len(result.guidance)} entries):")
            for g in result.guidance:
                print(f"  [{g.domain}] {g.error_pattern[:50]} -> {g.fix[:50]}")

        if result.memories:
            print(f"\nMemories ({len(result.memories)} entries):")
            for m in result.memories:
                print(f"  [{m.score:.2f}] {m.title}")

    elif command == "cache" and len(sys.argv) > 3:
        query = sys.argv[2]
        result = sys.argv[3]
        success = engine.record_success(query, result)
        print(f"Cached: {success}")

    elif command == "learn" and len(sys.argv) > 3:
        error = sys.argv[2]
        fix = sys.argv[3]
        domain = sys.argv[4] if len(sys.argv) > 4 else ""
        success = engine.learn_failure(error, fix, domain)
        print(f"Learned: {success}")

    elif command == "status":
        status = engine.status()
        for key, value in status.items():
            print(f"{key}: {value}")

    elif command == "init":
        results = engine.ensure_indexes()
        print("Redis index initialization:")
        for idx, status in results.items():
            print(f"  {idx}: {status}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
