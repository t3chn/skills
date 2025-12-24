# Unified Context Engine

Redis-based semantic context management for AI agents.

## Overview

The Unified Context Engine enhances AI agent capabilities through:
- **Long-term Memory**: Serena files with Redis vector search
- **Execution Cache**: Query→Result caching with semantic matching (0.85 threshold)
- **Guidance Cache**: Error→Fix pattern learning

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ContextEngine                             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │  UnifiedMemory   │  │ ExecutionCache │  │ GuidanceCache│ │
│  │  (Serena+Redis)  │  │ (query→result) │  │ (error→fix)  │ │
│  └────────┬─────────┘  └───────┬────────┘  └──────┬───────┘ │
│           │                    │                   │         │
└───────────┼────────────────────┼───────────────────┼─────────┘
            ▼                    ▼                   ▼
     ┌─────────────────────────────────────────────────────────┐
     │                    Redis Stack                          │
     │  • Vector search (HNSW)                                 │
     │  • Semantic similarity (cosine)                         │
     │  • Prefix-based indexing                                │
     └─────────────────────────────────────────────────────────┘
```

## Usage

### CLI Commands

```bash
# Check status
python3 scripts/context_engine.py status

# Initialize Redis indexes (run once)
python3 scripts/context_engine.py init

# Get context for a query
python3 scripts/context_engine.py context "authentication error handling"

# Cache successful result
python3 scripts/context_engine.py cache "auth retry logic" "implement exponential backoff"

# Learn from failure fix
python3 scripts/context_engine.py learn "ConnectionError" "check Redis: docker ps" "redis"
```

### Python API

```python
from scripts.context_engine import ContextEngine

engine = ContextEngine()

# Get unified context
result = engine.get_context("how to handle auth errors")
print(f"Source: {result.source}")
print(f"Cached: {result.cached_result}")
print(f"Memories: {result.memories}")
print(f"Guidance: {result.guidance}")

# Record success for future cache hits
engine.record_success(
    query="auth error handling",
    result="use retry with exponential backoff"
)

# Learn from failure
engine.learn_failure(
    error="ConnectionRefusedError",
    fix="check if Redis is running with docker ps",
    domain="redis"
)
```

## Hooks Integration

The engine integrates with vi-skills hooks:

| Hook | Script | Purpose |
|------|--------|---------|
| SessionStart | `redis-context.sh` | Display status, load cached context |
| Stop | `redis-learn.sh stop` | Sync local cache to Redis |

## Graceful Degradation

```
┌─────────────────────────────────────────────────────────────┐
│ FULL MODE: Redis + Embeddings                               │
│ • Semantic search with vector similarity                    │
│ • 0.85+ threshold for cache hits                            │
├─────────────────────────────────────────────────────────────┤
│ DEGRADED: No OPENAI_API_KEY                                 │
│ • Zero vectors (no semantic matching)                       │
│ • Exact hash-based cache lookup only                        │
├─────────────────────────────────────────────────────────────┤
│ MINIMAL: Redis down                                         │
│ • Local in-memory cache (session-based)                     │
│ • Serena grep fallback for memories                         │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

Environment variables:
- `REDIS_URL`: Redis connection (default: `redis://localhost:6379`)
- `OPENAI_API_KEY`: For embeddings (required for semantic search)
- `SERENA_MEMORIES_PATH`: Memory files path (default: `.serena/memories`)

## Thresholds

| Cache Type | Threshold | Description |
|------------|-----------|-------------|
| Execution | 0.85 | High confidence for reusing results |
| Guidance | 0.75 | Fuzzy matching for similar errors |
| Memory | 0.15 | Broad search for relevant memories |

## Redis Indexes

Created automatically by `python3 scripts/context_engine.py init`:

- `exec_cache_idx`: Prefix `exec_cache:*`, fields: query, result, embedding
- `guidance_idx`: Prefix `guidance:*`, fields: error_pattern, fix, domain, embedding
- `memory_index`: Prefix `memory:*`, managed by UnifiedMemory

## Files

```
scripts/
├── context_engine.py    # Main context engine
├── unified_memory.py    # Serena + Redis memory layer
├── index-memory.py      # Memory indexing script
└── verify-index.py      # Index verification

hooks/
├── redis-context.sh     # SessionStart hook
└── redis-learn.sh       # Learning hooks (stop)

docker/
└── docker-compose.yml   # Redis Stack setup
```

## Troubleshooting

### Redis not available
```bash
# Start Redis Stack
docker compose -f docker/docker-compose.yml up -d

# Verify
docker ps | grep redis
```

### Indexes not found
```bash
# Create indexes
source .venv/bin/activate
python3 scripts/context_engine.py init
```

### No semantic results
```bash
# Check OPENAI_API_KEY
echo $OPENAI_API_KEY

# Verify embeddings work
python3 scripts/verify-index.py
```

### Cache not hitting
- Check similarity threshold (0.85 for exec_cache)
- Verify query is similar enough semantically
- Use `context_engine.py context "query"` to test
