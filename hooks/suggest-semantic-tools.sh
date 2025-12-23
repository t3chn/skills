#!/usr/bin/env bash
# suggest-semantic-tools.sh - PreToolUse hook for serena tool suggestions
# Suggests semantic navigation tools when serena project is active
#
# This script checks the tool input to determine if serena tools would be better.
# Exit 0 = allow with suggestion (output becomes prompt)

set -e

# Check if serena project is active
if [ ! -d ".serena" ] && [ ! -f ".serena/project.yml" ]; then
  # No serena project, exit silently
  exit 0
fi

# Get tool name from environment (set by Claude Code)
TOOL_NAME="${CLAUDE_TOOL_NAME:-}"

# Only suggest for Grep and Read tools
case "$TOOL_NAME" in
  Grep|Read)
    ;;
  *)
    exit 0
    ;;
esac

# Output suggestion
cat << 'EOF'
💡 **Serena Semantic Tools Available**

This project has serena configured. Consider using semantic tools:

| Current Action | Semantic Alternative |
|----------------|---------------------|
| Grep for symbol | `mcp__serena__find_symbol(name_path="<pattern>")` |
| Read entire file | `mcp__serena__get_symbols_overview(relative_path="<file>")` |
| Find usages | `mcp__serena__find_referencing_symbols(...)` |

**Benefits:** Precise symbol bounds, type info, inheritance navigation.

To continue with original tool, proceed as normal.
EOF

exit 0
