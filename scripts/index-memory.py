#!/usr/bin/env python3
"""
Index Serena memories to Redis for semantic search.

Usage:
    python3 index-memory.py <memory_file_or_directory>
    python3 index-memory.py .serena/memories/
    python3 index-memory.py .serena/memories/auth-patterns.md
"""

import os
import sys
import hashlib
import struct
from pathlib import Path
from datetime import datetime

try:
    import redis
    from redis.commands.search.field import TextField, VectorField, TagField
    from redis.commands.search.index_definition import IndexDefinition, IndexType

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False
    print("Warning: redis-py not installed. Run: pip install redis")

try:
    import openai

    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
INDEX_NAME = "memory_index"
EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small


def get_embedding(text: str) -> list[float]:
    """Generate embedding using OpenAI API."""
    if not HAS_OPENAI or not OPENAI_API_KEY:
        # Return zero vector if no OpenAI
        return [0.0] * EMBEDDING_DIM

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:8000],  # Truncate to token limit
    )
    return response.data[0].embedding


def extract_metadata(content: str, filepath: str) -> dict:
    """Extract metadata from memory content."""
    lines = content.split("\n")
    metadata = {
        "filename": os.path.basename(filepath),
        "filepath": filepath,
        "created": datetime.now().isoformat(),
        "topics": [],
        "entities": [],
    }

    # Extract from frontmatter or headers
    for line in lines[:20]:
        line = line.strip()
        if line.startswith("# "):
            metadata["title"] = line[2:]
        elif line.startswith("## Tags:") or line.startswith("## tags:"):
            tags = line.split(":", 1)[1].strip()
            metadata["topics"] = [t.strip() for t in tags.split(",")]
        elif line.startswith("## Project:"):
            metadata["project"] = line.split(":", 1)[1].strip()

    return metadata


def content_hash(content: str) -> str:
    """Generate hash for deduplication."""
    return hashlib.md5(content.encode()).hexdigest()


def index_memory(r: "redis.Redis", filepath: str) -> bool:
    """Index a single memory file to Redis."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    # Skip empty files
    if not content.strip():
        print(f"Skipping empty file: {filepath}")
        return False

    # Generate document ID from filepath
    doc_id = f"memory:{content_hash(filepath)}"

    # Check if already indexed with same content
    existing = r.hget(doc_id, "content_hash")
    current_hash = content_hash(content)
    if existing and existing.decode() == current_hash:
        print(f"Already indexed (unchanged): {filepath}")
        return True

    # Extract metadata
    metadata = extract_metadata(content, filepath)

    # Generate embedding
    print(f"Generating embedding for: {filepath}")
    embedding = get_embedding(content)

    # Store in Redis
    doc = {
        "content": content,
        "content_hash": current_hash,
        "filename": metadata["filename"],
        "filepath": metadata["filepath"],
        "title": metadata.get("title", metadata["filename"]),
        "topics": ",".join(metadata.get("topics", [])),
        "project": metadata.get("project", ""),
        "created": metadata["created"],
        "embedding": struct.pack(f"{len(embedding)}f", *embedding),
    }

    r.hset(doc_id, mapping=doc)
    print(f"Indexed: {filepath}")
    return True


def create_index(r: "redis.Redis"):
    """Create RediSearch index if not exists."""
    try:
        r.ft(INDEX_NAME).info()
        print(f"Index '{INDEX_NAME}' already exists")
        return
    except redis.ResponseError:
        pass

    schema = (
        TextField("content"),
        TextField("title"),
        TextField("filename"),
        TagField("topics"),
        TagField("project"),
        VectorField(
            "embedding",
            "HNSW",
            {
                "TYPE": "FLOAT32",
                "DIM": EMBEDDING_DIM,
                "DISTANCE_METRIC": "COSINE",
            },
        ),
    )

    definition = IndexDefinition(prefix=["memory:"], index_type=IndexType.HASH)

    r.ft(INDEX_NAME).create_index(schema, definition=definition)
    print(f"Created index: {INDEX_NAME}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 index-memory.py <memory_file_or_directory>")
        sys.exit(1)

    if not HAS_REDIS:
        print("Error: redis-py required. Install with: pip install redis")
        sys.exit(1)

    path = Path(sys.argv[1])

    # Connect to Redis
    r = redis.from_url(REDIS_URL)
    try:
        r.ping()
    except redis.ConnectionError:
        print(f"Error: Cannot connect to Redis at {REDIS_URL}")
        print("Start Redis with: docker compose up -d")
        sys.exit(1)

    # Create index
    create_index(r)

    # Index files
    if path.is_file():
        index_memory(r, str(path))
    elif path.is_dir():
        count = 0
        for file in path.glob("**/*.md"):
            if index_memory(r, str(file)):
                count += 1
        print(f"\nIndexed {count} memories")
    else:
        print(f"Error: Path not found: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
