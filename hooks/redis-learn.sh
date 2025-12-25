#!/usr/bin/env bash
# redis-learn.sh - Learning hooks for Redis context engine
# Handles: PreToolUse (cache lookup), PostToolUse (record), Stop (sync)
#
# Usage:
#   redis-learn.sh pretool   # Check cache before tool use
#   redis-learn.sh posttool  # Record successful tool use
#   redis-learn.sh stop      # Sync local cache to Redis
#
# Dependencies:
# - context_engine.py in scripts/
# - Python 3 with redis + openai packages
#
# Exit 0 = continue
# Exit 2 = block (with reason in stdout)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV="$PROJECT_ROOT/.venv"
CONTEXT_ENGINE="$PROJECT_ROOT/scripts/context_engine.py"

# Check dependencies
if [ ! -f "$CONTEXT_ENGINE" ] || [ ! -d "$VENV" ]; then
  exit 0
fi

MODE="${1:-pretool}"

# Read tool context from stdin (JSON)
TOOL_CONTEXT=""
if [ ! -t 0 ]; then
  TOOL_CONTEXT=$(cat)
fi

# =============================================================================
# PRETOOL: Check execution cache before tool use
# =============================================================================

pretool_hook() {
  # Only check for certain tool types that benefit from caching
  TOOL_NAME=$(echo "$TOOL_CONTEXT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || true)

  case "$TOOL_NAME" in
    Bash|WebSearch|Task)
      # These tools might benefit from cache lookup
      TOOL_INPUT=$(echo "$TOOL_CONTEXT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command','') or d.get('tool_input',{}).get('query','') or d.get('tool_input',{}).get('prompt',''))" 2>/dev/null || true)

      if [ -n "$TOOL_INPUT" ] && [ ${#TOOL_INPUT} -gt 10 ]; then
        # Check cache for similar query
        CACHE_HIT=$(source "$VENV/bin/activate" && python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT/scripts')
from context_engine import ContextEngine
engine = ContextEngine()
result = engine.exec_cache.get('$TOOL_INPUT')
if result and result.score >= 0.95:
    print(f'CACHE_HIT|{result.score}|{result.result[:500]}')
" 2>/dev/null || true)

        if [[ "$CACHE_HIT" == CACHE_HIT* ]]; then
          SCORE=$(echo "$CACHE_HIT" | cut -d'|' -f2)
          RESULT=$(echo "$CACHE_HIT" | cut -d'|' -f3-)
          echo "## 💡 Cache Hit (score: $SCORE)"
          echo ""
          echo "A similar query was executed before with result:"
          echo ""
          echo "\`\`\`"
          echo "$RESULT"
          echo "\`\`\`"
          echo ""
          echo "*Consider reusing this result instead of re-executing.*"
        fi
      fi
      ;;
  esac

  exit 0
}

# =============================================================================
# POSTTOOL: Record successful tool use
# =============================================================================

posttool_hook() {
  # Record successful tool uses for future cache hits
  TOOL_NAME=$(echo "$TOOL_CONTEXT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || true)
  TOOL_INPUT=$(echo "$TOOL_CONTEXT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('tool_input',{})))" 2>/dev/null || true)

  # Only cache meaningful tool outputs (not read/write operations)
  case "$TOOL_NAME" in
    Bash|WebSearch)
      # These are good candidates for caching
      # Note: In practice, we'd need the tool output which isn't available in PostToolUse
      # This hook is more for future integration when output is available
      ;;
  esac

  exit 0
}

# =============================================================================
# STOP: Sync and persist learnings
# =============================================================================

stop_hook() {
  # Check stop_hook_active to prevent infinite loops
  if [ -n "$TOOL_CONTEXT" ]; then
    STOP_ACTIVE=$(echo "$TOOL_CONTEXT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('stop_hook_active', False))" 2>/dev/null || echo "False")
    if [ "$STOP_ACTIVE" = "True" ]; then
      exit 0
    fi
  fi

  # Sync any pending learnings to Redis
  source "$VENV/bin/activate" 2>/dev/null || true

  python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT/scripts')
from context_engine import ContextEngine

engine = ContextEngine()

# Get stats
local_exec_count = len(engine.exec_cache._local_cache)
local_guid_count = len(engine.guidance_cache._local_cache)

if local_exec_count > 0 or local_guid_count > 0:
    print(f'## 🧠 Redis Context Sync')
    print()
    print(f'Local cache: {local_exec_count} executions, {local_guid_count} guidance entries')

    if engine.is_redis_available:
        print('Synced to Redis.')
    else:
        print('Redis unavailable. Local cache preserved.')
" 2>/dev/null || true

  exit 0
}

# =============================================================================
# MAIN
# =============================================================================

case "$MODE" in
  pretool)
    pretool_hook
    ;;
  posttool)
    posttool_hook
    ;;
  stop)
    stop_hook
    ;;
  *)
    echo "Unknown mode: $MODE"
    exit 1
    ;;
esac
