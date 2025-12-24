# Redis Memory Skill

This skill should be used when the user asks about "redis memory", "semantic search", "memory indexing", "unified memory", "agent memory", "redis search", or needs guidance on using Redis for AI agent memory with semantic search capabilities.

## Overview

Redis Memory provides a hybrid architecture for AI agent memory:
- **Serena files** = source of truth + human-readable backup
- **Redis** = semantic search + vector embeddings

## Architecture

```
WRITE PATH:
Agent → Serena File (.md) → Redis Index (embeddings)
         ↓                        ↓
    Git History            Semantic Search

READ PATH:
Query → Redis Search → Results
              ↓ (fallback if Redis down)
        Serena Files (grep)
```

## Quick Start

### 1. Start Redis Stack

```bash
cd ~/projects/skills/docker
docker compose up -d
```

### 2. Index Existing Memories

```bash
python3 scripts/index-memory.py .serena/memories/
```

### 3. Verify Index

```bash
python3 scripts/verify-index.py
```

## UnifiedMemory API

```python
from unified_memory import UnifiedMemory

memory = UnifiedMemory()

# Write memory (to both Serena and Redis)
memory.write("auth-patterns.md", content, {"topics": ["auth", "security"]})

# Search memories (Redis with Serena fallback)
results = memory.search("authentication patterns", limit=5)

# Read specific memory (from Serena - source of truth)
content = memory.read("auth-patterns.md")

# List all memories
memories = memory.list_memories()

# Sync Serena to Redis
stats = memory.sync_to_redis()
```

## CLI Usage

```bash
# Search memories
python3 scripts/unified_memory.py search "authentication"

# List all memories
python3 scripts/unified_memory.py list

# Sync to Redis
python3 scripts/unified_memory.py sync

# Check status
python3 scripts/unified_memory.py status
```

## MCP Servers

Two MCP servers are configured in `~/.claude/settings.json`:

### mcp-redis
Direct Redis access via natural language:
```json
{
  "redis": {
    "command": "uvx",
    "args": ["mcp-redis"],
    "env": { "REDIS_URL": "redis://localhost:6379" }
  }
}
```

### agent-memory-server
AI-powered memory with automatic topic extraction:
```json
{
  "memory": {
    "command": "uvx",
    "args": ["--from", "agent-memory-server", "agent-memory", "mcp"],
    "env": { "REDIS_URL": "redis://localhost:6379" }
  }
}
```

## Best Practices

1. **Always write to Serena first** - it's the source of truth
2. **Use semantic search for discovery** - find related memories
3. **Tag memories with topics** - improves search relevance
4. **Sync periodically** - keep Redis index up to date
5. **Monitor Redis health** - use verify-index.py

## Troubleshooting

### Redis not running
```bash
docker compose -f ~/projects/skills/docker/docker-compose.yml up -d
```

### Index not found
```bash
python3 scripts/index-memory.py .serena/memories/
```

### Search returns no results
```bash
# Check index status
python3 scripts/verify-index.py

# Re-sync if needed
python3 scripts/unified_memory.py sync
```
