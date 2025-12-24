#!/usr/bin/env python3
"""
Unified Memory API for AI Agents.

Enhanced Hybrid Architecture:
- Serena files = source of truth + human-readable backup
- Redis = semantic search + vector embeddings

Write Path: Agent → Serena File → Redis Index (async)
Read Path: Query → Redis Search → (fallback if down) → Serena Files
"""

import os
import struct
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

try:
    import redis
    from redis.commands.search.query import Query

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

try:
    import openai

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERENA_MEMORIES_PATH = os.getenv("SERENA_MEMORIES_PATH", ".serena/memories")
INDEX_NAME = "memory_index"
EMBEDDING_DIM = 1536


@dataclass
class MemoryResult:
    """Result from memory search."""

    filename: str
    filepath: str
    content: str
    score: float = 0.0
    title: str = ""
    topics: list[str] = None

    def __post_init__(self):
        if self.topics is None:
            self.topics = []


class UnifiedMemory:
    """
    Unified memory layer with Redis semantic search and Serena file backup.

    Usage:
        memory = UnifiedMemory()

        # Write memory (to both Serena and Redis)
        memory.write("auth-patterns.md", content, {"topics": ["auth", "security"]})

        # Search memories (Redis with Serena fallback)
        results = memory.search("authentication patterns", limit=5)

        # Read specific memory (from Serena - source of truth)
        content = memory.read("auth-patterns.md")
    """

    def __init__(self, serena_path: str = None, redis_url: str = None):
        self.serena_path = Path(serena_path or SERENA_MEMORIES_PATH)
        self.redis_url = redis_url or REDIS_URL
        self._redis_client = None
        self._redis_available = None

    @property
    def redis(self) -> Optional["redis.Redis"]:
        """Lazy Redis connection with availability check."""
        if not HAS_REDIS:
            return None

        if self._redis_client is None:
            try:
                self._redis_client = redis.from_url(self.redis_url)
                self._redis_client.ping()
                self._redis_available = True
            except (redis.ConnectionError, Exception):
                self._redis_available = False
                self._redis_client = None

        return self._redis_client

    @property
    def is_redis_available(self) -> bool:
        """Check if Redis is available."""
        if self._redis_available is None:
            _ = self.redis  # Trigger connection check
        return self._redis_available or False

    def write(self, filename: str, content: str, metadata: dict = None) -> bool:
        """
        Write memory to Serena file and index to Redis.

        Args:
            filename: Memory filename (e.g., "auth-patterns.md")
            content: Memory content
            metadata: Optional metadata (topics, project, etc.)

        Returns:
            True if successful
        """
        metadata = metadata or {}
        filepath = self.serena_path / filename

        # 1. Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # 2. Write to Serena file (primary source of truth)
        filepath.write_text(content, encoding="utf-8")

        # 3. Index to Redis (async/best-effort)
        if self.is_redis_available:
            try:
                self._index_to_redis(str(filepath), content, metadata)
            except Exception as e:
                # Log but don't fail - Serena file is saved
                print(f"Warning: Redis indexing failed: {e}")

        return True

    def search(
        self, query: str, limit: int = 5, threshold: float = 0.15
    ) -> list[MemoryResult]:
        """
        Search memories using Redis semantic search with Serena fallback.

        Args:
            query: Search query
            limit: Maximum results to return
            threshold: Minimum similarity score (0-1)

        Returns:
            List of MemoryResult objects
        """
        # Try Redis first
        if self.is_redis_available:
            try:
                results = self._redis_search(query, limit, threshold)
                if results:
                    return results
            except Exception as e:
                print(f"Warning: Redis search failed: {e}")

        # Fallback to Serena grep
        return self._serena_search(query, limit)

    def read(self, filename: str) -> Optional[str]:
        """
        Read memory from Serena file (source of truth).

        Args:
            filename: Memory filename

        Returns:
            Memory content or None if not found
        """
        filepath = self.serena_path / filename
        if filepath.exists():
            return filepath.read_text(encoding="utf-8")
        return None

    def delete(self, filename: str) -> bool:
        """
        Delete memory from both Serena and Redis.

        Args:
            filename: Memory filename

        Returns:
            True if deleted
        """
        filepath = self.serena_path / filename
        deleted = False

        # Delete from Serena
        if filepath.exists():
            filepath.unlink()
            deleted = True

        # Delete from Redis
        if self.is_redis_available:
            try:
                import hashlib

                doc_id = f"memory:{hashlib.md5(str(filepath).encode()).hexdigest()}"
                self.redis.delete(doc_id)
            except Exception:
                pass

        return deleted

    def list_memories(self) -> list[str]:
        """List all memory files."""
        if not self.serena_path.exists():
            return []
        return [f.name for f in self.serena_path.glob("**/*.md")]

    def sync_to_redis(self) -> dict:
        """
        Sync all Serena memories to Redis.

        Returns:
            Stats dict with indexed/failed counts
        """
        if not self.is_redis_available:
            return {"error": "Redis not available"}

        stats = {"indexed": 0, "failed": 0, "skipped": 0}

        for filepath in self.serena_path.glob("**/*.md"):
            try:
                content = filepath.read_text(encoding="utf-8")
                if not content.strip():
                    stats["skipped"] += 1
                    continue

                self._index_to_redis(str(filepath), content, {})
                stats["indexed"] += 1
            except Exception as e:
                print(f"Failed to index {filepath}: {e}")
                stats["failed"] += 1

        return stats

    def _get_embedding(self, text: str) -> list[float]:
        """Generate embedding using OpenAI."""
        if not HAS_OPENAI or not OPENAI_API_KEY:
            return [0.0] * EMBEDDING_DIM

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.embeddings.create(
            model="text-embedding-3-small", input=text[:8000]
        )
        return response.data[0].embedding

    def _index_to_redis(self, filepath: str, content: str, metadata: dict):
        """Index a memory to Redis."""
        import hashlib

        doc_id = f"memory:{hashlib.md5(filepath.encode()).hexdigest()}"
        content_hash = hashlib.md5(content.encode()).hexdigest()

        # Check if already indexed with same content
        existing = self.redis.hget(doc_id, "content_hash")
        if existing and existing.decode() == content_hash:
            return  # Already indexed

        # Generate embedding
        embedding = self._get_embedding(content)

        # Extract title from content
        title = Path(filepath).stem
        for line in content.split("\n")[:10]:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # Store in Redis
        doc = {
            "content": content,
            "content_hash": content_hash,
            "filename": Path(filepath).name,
            "filepath": filepath,
            "title": title,
            "topics": ",".join(metadata.get("topics", [])),
            "project": metadata.get("project", ""),
            "created": datetime.now().isoformat(),
            "embedding": struct.pack(f"{len(embedding)}f", *embedding),
        }

        self.redis.hset(doc_id, mapping=doc)

    def _redis_search(
        self, query: str, limit: int, threshold: float
    ) -> list[MemoryResult]:
        """Search using Redis vector similarity."""
        # Generate query embedding
        query_embedding = self._get_embedding(query)

        # Build vector search query
        query_vector = struct.pack(f"{len(query_embedding)}f", *query_embedding)

        # Use KNN search
        q = (
            Query(f"*=>[KNN {limit} @embedding $vec AS score]")
            .return_fields(
                "filename", "filepath", "content", "title", "topics", "score"
            )
            .sort_by("score")
            .dialect(2)
        )

        results = self.redis.ft(INDEX_NAME).search(
            q, query_params={"vec": query_vector}
        )

        memories = []
        for doc in results.docs:
            score = float(doc.score) if hasattr(doc, "score") else 0.0
            # Convert distance to similarity (cosine distance to similarity)
            similarity = 1 - score

            if similarity >= threshold:
                memories.append(
                    MemoryResult(
                        filename=doc.filename,
                        filepath=doc.filepath,
                        content=doc.content,
                        score=similarity,
                        title=getattr(doc, "title", ""),
                        topics=doc.topics.split(",") if doc.topics else [],
                    )
                )

        return memories

    def _serena_search(self, query: str, limit: int) -> list[MemoryResult]:
        """Fallback search using grep on Serena files."""
        results = []

        if not self.serena_path.exists():
            return results

        # Simple case-insensitive search
        query_lower = query.lower()

        for filepath in self.serena_path.glob("**/*.md"):
            try:
                content = filepath.read_text(encoding="utf-8")
                if query_lower in content.lower():
                    # Extract title
                    title = filepath.stem
                    for line in content.split("\n")[:10]:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            break

                    results.append(
                        MemoryResult(
                            filename=filepath.name,
                            filepath=str(filepath),
                            content=content,
                            score=0.5,  # Arbitrary score for text match
                            title=title,
                            topics=[],
                        )
                    )

                    if len(results) >= limit:
                        break
            except Exception:
                continue

        return results


# CLI interface
if __name__ == "__main__":
    import sys

    memory = UnifiedMemory()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  unified_memory.py search <query>    - Search memories")
        print("  unified_memory.py list              - List all memories")
        print("  unified_memory.py sync              - Sync Serena to Redis")
        print("  unified_memory.py status            - Check Redis status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "search" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        results = memory.search(query)
        for r in results:
            print(f"[{r.score:.2f}] {r.title} ({r.filename})")
            print(f"  {r.content[:200]}...")
            print()

    elif command == "list":
        for m in memory.list_memories():
            print(m)

    elif command == "sync":
        stats = memory.sync_to_redis()
        print(f"Sync complete: {stats}")

    elif command == "status":
        print(f"Redis available: {memory.is_redis_available}")
        print(f"Serena path: {memory.serena_path}")
        print(f"Memories count: {len(memory.list_memories())}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
