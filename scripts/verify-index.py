#!/usr/bin/env python3
"""
Verify Redis memory index integrity.

Usage:
    python3 verify-index.py
"""

import os
import sys
from pathlib import Path

try:
    import redis

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
SERENA_MEMORIES_PATH = os.getenv("SERENA_MEMORIES_PATH", ".serena/memories")
INDEX_NAME = "memory_index"


def verify():
    if not HAS_REDIS:
        print("Error: redis-py not installed")
        sys.exit(1)

    # Connect to Redis
    r = redis.from_url(REDIS_URL)
    try:
        r.ping()
        print("✓ Redis connection OK")
    except redis.ConnectionError:
        print("✗ Redis connection FAILED")
        sys.exit(1)

    # Check index exists
    try:
        info = r.ft(INDEX_NAME).info()
        num_docs = info.get("num_docs", 0)
        print(f"✓ Index '{INDEX_NAME}' exists ({num_docs} documents)")
    except redis.ResponseError:
        print(f"✗ Index '{INDEX_NAME}' does not exist")
        print("  Run: python3 scripts/index-memory.py .serena/memories/")
        sys.exit(1)

    # Count Serena files
    serena_path = Path(SERENA_MEMORIES_PATH)
    if serena_path.exists():
        serena_count = len(list(serena_path.glob("**/*.md")))
        print(f"✓ Sync OK: {num_docs} documents in Redis, {serena_count} in Serena")
        if num_docs < serena_count:
            print(f"  Warning: {serena_count - num_docs} files not indexed")
    else:
        print(f"  Serena path not found: {serena_path}")

    # Test search
    try:
        result = r.ft(INDEX_NAME).search("*")
        print(f"✓ Search works: found {len(result.docs)} results for '*'")
    except Exception as e:
        print(f"✗ Search failed: {e}")

    print("\nVerification complete!")


if __name__ == "__main__":
    verify()
