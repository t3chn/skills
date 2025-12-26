#!/usr/bin/env bash
# precompact-context.sh - PreCompact hook for context preservation
# Saves current task context before Claude compacts the conversation
#
# Exit 0 = inject context into compacted conversation

set -e

output=""

# =============================================================================
# BEADS TASK CONTEXT
# =============================================================================

if command -v bd &> /dev/null; then
  # Get current task context to preserve across compaction
  BD_PRIME=$(bd prime 2>/dev/null || true)

  if [ -n "$BD_PRIME" ]; then
    output="${output}# Context Preserved from Pre-Compact"$'\n\n'
    output="${output}${BD_PRIME}"$'\n\n'
  fi
fi

# =============================================================================
# SERENA MEMORY HINT
# =============================================================================

if [ -d ".serena/memories" ]; then
  CHECKPOINT=$(ls -t .serena/memories/checkpoint-*.md 2>/dev/null | head -1)
  if [ -n "$CHECKPOINT" ]; then
    CHECKPOINT_NAME=$(basename "$CHECKPOINT")
    output="${output}**Session checkpoint available:** \`read_memory('$CHECKPOINT_NAME')\`"$'\n'
  fi
fi

# =============================================================================
# OUTPUT
# =============================================================================

if [ -n "$output" ]; then
  echo "$output"
fi

exit 0
