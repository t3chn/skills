#!/usr/bin/env bash
# redis-context.sh - SessionStart hook for Redis unified context
# Loads cached context and reports Redis status
#
# Dependencies:
# - context_engine.py in scripts/
# - Python 3 with redis + openai packages
#
# Exit 0 = context injection

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV="$PROJECT_ROOT/.venv"
CONTEXT_ENGINE="$PROJECT_ROOT/scripts/context_engine.py"

output=""

# =============================================================================
# REDIS CONTEXT ENGINE STATUS
# =============================================================================

# Check if context engine exists
if [ ! -f "$CONTEXT_ENGINE" ]; then
  exit 0
fi

# Check if venv exists
if [ ! -d "$VENV" ]; then
  exit 0
fi

# =============================================================================
# ENSURE REDIS IS RUNNING (auto-start if Docker available)
# =============================================================================

DOCKER_COMPOSE_FILE="$PROJECT_ROOT/docker/docker-compose.yml"

if command -v docker &> /dev/null && [ -f "$DOCKER_COMPOSE_FILE" ]; then
  # Check if Redis container is running
  if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -q "redis-ai-memory"; then
    # Try to start Redis (silent, non-blocking)
    docker compose -f "$DOCKER_COMPOSE_FILE" up -d 2>/dev/null &
    # Give it a moment to start
    sleep 1
  fi
fi

# Get status from context engine
STATUS=$(source "$VENV/bin/activate" && python3 "$CONTEXT_ENGINE" status 2>/dev/null || true)

if [ -z "$STATUS" ]; then
  exit 0
fi

# Parse status
REDIS_AVAILABLE=$(echo "$STATUS" | grep "redis_available" | cut -d: -f2 | tr -d ' ')
MODE=$(echo "$STATUS" | grep "mode" | cut -d: -f2 | tr -d ' ')
MEMORIES=$(echo "$STATUS" | grep "memories_count" | cut -d: -f2 | tr -d ' ')

# =============================================================================
# ENSURE INDEXES EXIST (auto-recovery after Redis restart)
# =============================================================================

if [ "$REDIS_AVAILABLE" = "True" ]; then
  # Silently ensure indexes exist (creates if missing)
  source "$VENV/bin/activate" && python3 "$CONTEXT_ENGINE" init >/dev/null 2>&1 || true
fi

# =============================================================================
# BUILD OUTPUT
# =============================================================================

if [ "$REDIS_AVAILABLE" = "True" ]; then
  output="${output}## 🧠 Redis Context Engine Active"$'\n'
  output="${output}"$'\n'
  output="${output}**Status:** \`${MODE}\` mode | **Memories:** ${MEMORIES}"$'\n'
  output="${output}"$'\n'
  output="${output}**Available APIs:**"$'\n'
  output="${output}"$'\n'
  output="${output}"'| Action | Command |'$'\n'
  output="${output}"'|--------|---------|'$'\n'
  output="${output}"'| Search context | `python3 scripts/context_engine.py context "query"` |'$'\n'
  output="${output}"'| Cache success | `python3 scripts/context_engine.py cache "query" "result"` |'$'\n'
  output="${output}"'| Learn failure | `python3 scripts/context_engine.py learn "error" "fix" "domain"` |'$'\n'
  output="${output}"$'\n'
  output="${output}"'**Best practice:** Use `record_success()` after successful operations, `learn_failure()` after fixes.'$'\n'
  output="${output}"$'\n'
else
  output="${output}## ⚠️ Redis Context Engine (Degraded)"$'\n'
  output="${output}"$'\n'
  output="${output}"'Redis not available. Operating in degraded mode with local cache fallback.'$'\n'
  output="${output}"$'\n'
  output="${output}"'To enable full mode: `docker compose -f docker/docker-compose.yml up -d`'$'\n'
  output="${output}"$'\n'
fi

# =============================================================================
# OUTPUT
# =============================================================================

if [ -n "$output" ]; then
  echo "$output"
fi

exit 0
