#!/usr/bin/env bash
# session-persist.sh - Stop hook for session state persistence
# Syncs beads task state at session end
#
# Input: JSON via stdin with stop_hook_active flag
# Dependencies:
# - beads CLI (bd) for task syncing
#
# Exit 0 = success (non-blocking)

set -e

# =============================================================================
# INFINITE LOOP PROTECTION
# =============================================================================
# Stop hooks can cause infinite loops if they trigger Claude to continue.
# Check stop_hook_active to prevent re-entry.

INPUT=""
if [ ! -t 0 ]; then
  INPUT=$(cat)
fi

if [ -n "$INPUT" ]; then
  STOP_ACTIVE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('stop_hook_active', False))" 2>/dev/null || echo "False")
  if [ "$STOP_ACTIVE" = "True" ]; then
    # Already in a stop hook chain, exit to prevent loop
    exit 0
  fi
fi

# =============================================================================
# BEADS SYNC
# =============================================================================

if command -v bd &> /dev/null; then
  # Sync current task state
  bd sync 2>/dev/null || true
fi

# Note: Serena memory persistence should be done explicitly during the session
# using mcp__serena__write_memory tool, not at session end

exit 0
