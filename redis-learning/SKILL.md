# Redis Learning Skill

This skill should be used when the user asks about "learning agents", "execution cache", "guidance cache", "agent learning", "pattern caching", "redis learning", or needs guidance on implementing agents that learn from their successes and failures.

## Overview

Learning Agents pattern enables AI agents to:
- Cache successful executions for reuse
- Learn from errors and avoid repeating mistakes
- Reduce token usage by 50-80% on repeated tasks

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LEARNING AGENTS PATTERN                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Query → Check Execution Cache → Hit? → Return cached        │
│                    ↓ Miss                                    │
│          Check Guidance Cache → Apply learnings              │
│                    ↓                                         │
│          Execute with enhanced context                       │
│                    ↓                                         │
│          Success? → Cache execution + result                 │
│          Failure? → Update guidance cache                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Two-Cache System

### Execution Cache
Stores successful query-result pairs:
```python
{
    "query_embedding": [...],  # Vector for semantic matching
    "query_text": "How to implement JWT auth?",
    "result": "...",           # Successful response
    "context": {...},          # Relevant context used
    "success_count": 5,        # Times this worked
    "last_used": "2024-12-24"
}
```

### Guidance Cache
Stores learnings from failures:
```python
{
    "pattern": "JWT implementation",
    "learnings": [
        "Always check token expiration",
        "Use httpOnly cookies for web",
        "Include refresh token flow"
    ],
    "common_errors": [
        "Missing CORS headers",
        "Token not in Authorization header"
    ],
    "success_patterns": [...]
}
```

## Implementation

### 1. Check Execution Cache

```python
def check_execution_cache(query: str, threshold: float = 0.75):
    """Find semantically similar successful executions."""
    embedding = get_embedding(query)

    results = redis.ft("execution_cache").search(
        Query(f"*=>[KNN 3 @embedding $vec AS score]")
        .return_fields("query_text", "result", "score")
        .dialect(2),
        query_params={"vec": embedding}
    )

    for doc in results.docs:
        if float(doc.score) >= threshold:
            return doc.result
    return None
```

### 2. Apply Guidance

```python
def get_guidance(query: str) -> list[str]:
    """Get relevant learnings for the query."""
    # Search guidance cache for related patterns
    results = redis.ft("guidance_cache").search(query)

    guidance = []
    for doc in results.docs:
        guidance.extend(doc.learnings)
        guidance.extend([f"Avoid: {e}" for e in doc.common_errors])

    return guidance
```

### 3. Cache Success

```python
def cache_success(query: str, result: str, context: dict):
    """Cache successful execution for future reuse."""
    doc_id = f"exec:{hash(query)}"

    redis.hset(doc_id, mapping={
        "query_text": query,
        "query_embedding": get_embedding(query),
        "result": result,
        "context": json.dumps(context),
        "success_count": 1,
        "created": datetime.now().isoformat()
    })
```

### 4. Learn from Failure

```python
def learn_from_failure(query: str, error: str, fix: str):
    """Update guidance cache with new learning."""
    pattern = extract_pattern(query)
    doc_id = f"guidance:{hash(pattern)}"

    # Get existing guidance or create new
    existing = redis.hgetall(doc_id)

    learnings = json.loads(existing.get("learnings", "[]"))
    learnings.append(fix)

    errors = json.loads(existing.get("common_errors", "[]"))
    errors.append(error)

    redis.hset(doc_id, mapping={
        "pattern": pattern,
        "learnings": json.dumps(learnings),
        "common_errors": json.dumps(errors),
        "updated": datetime.now().isoformat()
    })
```

## Use Cases

### TDD Pattern Learning
```python
# Cache successful test patterns
cache_success(
    query="Write pytest test for FastAPI endpoint",
    result=test_code,
    context={"framework": "pytest", "pattern": "fastapi"}
)

# Learn from test failures
learn_from_failure(
    query="Write pytest test for FastAPI endpoint",
    error="Missing TestClient import",
    fix="Always import: from fastapi.testclient import TestClient"
)
```

### Code Review Learning
```python
# Cache review patterns
cache_success(
    query="Review authentication code",
    result=review_comments,
    context={"type": "security", "language": "python"}
)

# Learn from missed issues
learn_from_failure(
    query="Review authentication code",
    error="Missed SQL injection vulnerability",
    fix="Always check for parameterized queries in auth code"
)
```

## Benefits

| Metric | Before | After |
|--------|--------|-------|
| Token usage | 100% | 20-50% |
| Response time | 2-5s | <100ms (cache hit) |
| Error repetition | High | Low |
| Consistency | Variable | High |

## Redis Schema

```bash
# Create execution cache index
FT.CREATE execution_cache ON HASH PREFIX 1 exec:
    SCHEMA
        query_text TEXT
        result TEXT
        embedding VECTOR HNSW 6 DIM 1536 DISTANCE_METRIC COSINE

# Create guidance cache index
FT.CREATE guidance_cache ON HASH PREFIX 1 guidance:
    SCHEMA
        pattern TEXT
        learnings TEXT
        common_errors TEXT
```

## Integration with vi-skills

### TDD Enforcer
- Cache successful Red-Green-Refactor cycles
- Learn from common test failures
- Suggest tests based on similar code

### Code Reviewer
- Cache review patterns per language/domain
- Learn from false positives/negatives
- Apply consistent review standards

### Session Checkpoint
- Cache successful recovery patterns
- Learn from failed restorations
- Improve checkpoint quality over time
