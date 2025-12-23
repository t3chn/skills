#!/usr/bin/env bash
# session-persist.sh - Stop hook for session state persistence
# Syncs beads task state at session end
#
# Dependencies:
# - beads CLI (bd) for task syncing
#
# Exit 0 = success (non-blocking)

set -e

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
