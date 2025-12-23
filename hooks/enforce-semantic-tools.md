---
name: Suggest Semantic Tools
description: Suggests serena semantic tools instead of grep/cat when a serena project is active
hooks:
  - event: PreToolUse
    type: prompt
    matcher:
      tool:
        - Grep
        - Read
---

# Semantic Tools Suggestion

This hook fires when Grep or Read tools are used and a serena project is detected.

## Detection Logic

Check if serena project is active:
```bash
[ -d ".serena" ] || [ -f ".serena/project.yml" ]
```

## When to Suggest

**For Grep with symbol-like patterns:**
- Pattern looks like a function/class name (PascalCase, camelCase, snake_case)
- Searching for "class X", "def X", "func X", "function X"

→ **Suggest:** `mcp__serena__find_symbol` with the symbol name

**For Read on code files:**
- Reading entire source files (.py, .go, .ts, .rs, etc.)
- Likely exploring structure, not reading specific content

→ **Suggest:** `mcp__serena__get_symbols_overview` first, then targeted reads

## Prompt Output

When conditions match, return:

```
💡 Serena Semantic Tools Available

This project has serena configured. Consider using semantic tools for more precise navigation:

| Current Action | Semantic Alternative |
|----------------|---------------------|
| Grep for symbol | `mcp__serena__find_symbol(name_path="<pattern>")` |
| Read entire file | `mcp__serena__get_symbols_overview(relative_path="<file>")` |
| Find usages | `mcp__serena__find_referencing_symbols(name_path="<symbol>", relative_path="<file>")` |

Benefits:
- More precise results (exact symbol bounds)
- Includes type information
- Can navigate inheritance/references
- Results can be used for symbol-level edits

To continue with original tool, proceed as normal.
```

## Non-Blocking

This is a **suggestion only** — does not block tool execution.
Exit code 0 allows the original tool to proceed.

The goal is education and gradual adoption, not enforcement.
