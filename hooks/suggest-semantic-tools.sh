#!/usr/bin/env bash
# suggest-semantic-tools.sh - PreToolUse hook for serena tool suggestions
# Suggests semantic navigation tools when serena project is active
#
# Input: JSON via stdin with tool_name, tool_input, etc.
# Exit 0 = allow with suggestion (output becomes context)

set -e

# Check if serena project is active
if [ ! -d ".serena" ] && [ ! -f ".serena/project.yml" ]; then
  # No serena project, exit silently
  exit 0
fi

# Read JSON input from stdin (required by Claude Code hooks API)
INPUT=""
if [ ! -t 0 ]; then
  INPUT=$(cat)
fi

# Exit if no input (shouldn't happen, but be safe)
if [ -z "$INPUT" ]; then
  exit 0
fi

# Parse tool_name from JSON using Python (more portable than jq)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || true)

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
