#!/usr/bin/env bash
# session-end.sh - SessionEnd hook for final cleanup
# Syncs beads and Redis state when session closes
#
# Unlike Stop hook (called after each Claude response), SessionEnd is called
# once when the session actually ends (logout, clear, exit).
#
# Exit 0 = success

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV="$PROJECT_ROOT/.venv"
CONTEXT_ENGINE="$PROJECT_ROOT/scripts/context_engine.py"

# =============================================================================
# BEADS FINAL SYNC
# =============================================================================

if command -v bd &> /dev/null; then
  bd sync 2>/dev/null || true
fi

# =============================================================================
# REDIS CONTEXT FINAL SYNC
# =============================================================================

if [ -f "$CONTEXT_ENGINE" ] && [ -d "$VENV" ]; then
  source "$VENV/bin/activate" 2>/dev/null || true

  python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT/scripts')
try:
    from context_engine import ContextEngine
    engine = ContextEngine()
    # Force sync any pending local cache to Redis
    if engine.is_redis_available:
        engine.exec_cache._sync_to_redis()
        engine.guidance_cache._sync_to_redis()
except Exception:
    pass  # Silent failure - don't block session end
" 2>/dev/null || true
fi

exit 0
