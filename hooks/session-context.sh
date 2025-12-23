#!/usr/bin/env bash
# session-context.sh - SessionStart hook for beads + serena integration
# Injects task context from beads and serena project awareness
#
# Dependencies:
# - beads CLI (bd) for task tracking
# - serena MCP for code navigation (detected via .serena/)
#
# Exit 0 = context injection

set -e

output=""

# =============================================================================
# BEADS INTEGRATION
# =============================================================================

if command -v bd &> /dev/null; then
  # Try to get current task context
  BD_PRIME=$(bd prime 2>/dev/null || true)

  if [ -n "$BD_PRIME" ]; then
    output="${output}${BD_PRIME}"$'\n\n'
  else
    # Check for available tasks
    BD_READY=$(bd ready --json 2>/dev/null || true)
    if [ -n "$BD_READY" ] && [ "$BD_READY" != "[]" ] && [ "$BD_READY" != "null" ]; then
      output="${output}## 📋 Beads Tasks Available"$'\n'
      output="${output}"$'\n'
      output="${output}Run \`bd ready\` to see available work items, or \`bd start <id>\` to begin a task."$'\n'
      output="${output}"$'\n'
    fi
  fi
fi

# =============================================================================
# SERENA PROJECT DETECTION
# =============================================================================

if [ -d ".serena" ] || [ -f ".serena/project.yml" ]; then
  output="${output}## 🔍 Serena Project Active"$'\n'
  output="${output}"$'\n'
  output="${output}**Use semantic tools for code navigation:**"$'\n'
  output="${output}"$'\n'
  output="${output}| Instead of | Use |"$'\n'
  output="${output}|------------|-----|"$'\n'
  output="${output}"'| `Grep` for symbols | `mcp__serena__find_symbol` |'$'\n'
  output="${output}"'| `Read` entire file | `mcp__serena__get_symbols_overview` |'$'\n'
  output="${output}"'| Searching references | `mcp__serena__find_referencing_symbols` |'$'\n'
  output="${output}"$'\n'
  output="${output}"'**Persistence:** Use `mcp__serena__write_memory` to save discoveries across sessions.'$'\n'
  output="${output}"$'\n'

  # Check for existing memories
  MEMORIES_DIR=".serena/memories"
  if [ -d "$MEMORIES_DIR" ]; then
    MEMORY_COUNT=$(find "$MEMORIES_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$MEMORY_COUNT" -gt 0 ]; then
      output="${output}"'**Available memories:** Run `mcp__serena__list_memories` to see '$MEMORY_COUNT' saved memories.'$'\n'
      output="${output}"$'\n'
    fi
  fi
fi

# =============================================================================
# OUTPUT
# =============================================================================

if [ -n "$output" ]; then
  echo "$output"
fi

exit 0
