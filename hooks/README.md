# vi-skills Hooks

Hooks for automatic context injection and workflow automation in Claude Code sessions.

## Hook Overview

| Event | Hook | Purpose |
|-------|------|---------|
| SessionStart | `flow-check.sh` | Check production flow compliance |
| SessionStart | `skill-suggester.sh` | Auto-detect project and suggest skills |
| SessionStart | `session-context.sh` | Inject beads + serena context |
| SessionStart | `redis-context.sh` | Load Redis context engine (timeout: 120s) |
| PreToolUse | `suggest-semantic-tools.sh` | Suggest serena for Grep/Read |
| PreCompact | `precompact-context.sh` | Save task context before compaction |
| Stop | `redis-learn.sh stop` | Sync Redis cache after response |
| SessionEnd | `session-end.sh` | Final beads + Redis sync |

## Installation

**Automatic** — hooks are included in vi-skills plugin.

When plugin is installed, hooks load from `hooks/hooks.json`. No manual configuration required.

## Hook Details

### SessionStart Hooks

#### flow-check.sh
Checks if project follows production flow:
- CLAUDE.md exists
- Pre-commit hooks installed
- Beads task tracking configured
- Tests directory present

#### skill-suggester.sh
Detects project type and suggests relevant skills:

| Trigger | Skills suggested |
|---------|------------------|
| `Cargo.toml` | backend-rust, backend-core |
| `pyproject.toml` / `requirements.txt` | backend-python, backend-core |
| `package.json` | backend-nodejs, backend-core |
| `tests/` directory | python-testing |
| `src/components/` or frontend framework | frontend-design |
| MCP/FastMCP in dependencies | mcp-builder |
| `.beads/` directory | beads-workflow |
| gitleaks in `.pre-commit-config.yaml` | secrets-guardian |

#### session-context.sh
Injects:
- Current date (AI models confuse years)
- Beads task context (`bd prime`)
- Serena project awareness
- Memory recovery hints

#### redis-context.sh
- Auto-starts Redis via Docker if available
- Reports Redis context engine status
- Shows available APIs

### PreToolUse Hook

#### suggest-semantic-tools.sh
When Claude uses `Grep` or `Read` on a serena-enabled project, suggests semantic alternatives:
- `find_symbol` instead of Grep
- `get_symbols_overview` instead of Read

### PreCompact Hook

#### precompact-context.sh
Before Claude compacts conversation:
- Saves current task context (`bd prime`)
- Notes available checkpoints
- Context survives compaction

### Stop Hook

#### redis-learn.sh stop
After each Claude response:
- Syncs local Redis cache
- Checks `stop_hook_active` to prevent loops

### SessionEnd Hook

#### session-end.sh
When session closes (logout, clear, exit):
- Final `bd sync` for beads
- Force sync Redis context to persistent storage

## Adding New Hooks

1. Create script in `hooks/` directory
2. Add to `hooks/hooks.json`:
```json
{
  "EventName": [{
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/hooks/your-hook.sh",
      "description": "What it does"
    }]
  }]
}
```

3. For PreToolUse/PostToolUse, add `matcher`:
```json
{
  "matcher": "Bash|Write",
  "hooks": [...]
}
```

## Best Practices

1. **Read stdin JSON** — hooks receive input via stdin, not env vars
2. **Check `stop_hook_active`** — Stop hooks must check this flag
3. **Exit 0** — stdout becomes context injection
4. **Exit 2** — stderr becomes blocking error
5. **Set timeouts** — for slow operations (Docker, network)
6. **Graceful degradation** — exit silently if deps missing

## Plain Text vs JSON Output

**Use plain text** (current approach) when:
- Injecting context for Claude to see
- Simple informational output
- Easier to read and debug

**Use JSON output** when you need:
- `systemMessage` — show warning to user (not Claude)
- `suppressOutput` — hide stdout from verbose mode
- `permissionDecision` — block/allow/modify tool (PreToolUse)
- `updatedInput` — modify tool parameters

JSON format example:
```json
{
  "systemMessage": "Warning shown to user",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "Context for Claude",
    "permissionDecision": "allow"
  }
}
```

For vi-skills hooks, plain text is optimal — we want Claude to see suggestions.
