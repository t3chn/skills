---
description: Save session progress to serena memory
allowed-tools: mcp__plugin_serena_serena__*, Bash(bd:*), Bash(date:*), Bash(git:*)
argument-hint: [restore|<custom-name>]
---

# Checkpoint Command

Save or restore session progress using serena memories.

## Context

- Serena status: !`[ -d ".serena" ] && echo "active" || echo "not active"`
- Active beads task: !`bd show 2>/dev/null | head -3 || echo "none"`
- Recent memories: !`ls -t .serena/memories/*.md 2>/dev/null | head -3 || echo "none"`

## Commands

### No arguments: Create checkpoint
Save current session state with timestamp.

1. Gather context:
   - Current beads task (if any)
   - TodoWrite state
   - Recent files modified
   - Current working state

2. Create memory:
   ```
   mcp__serena__write_memory(
     memory_file_name="checkpoint-<YYYY-MM-DD-HHMM>.md",
     content="<checkpoint content>"
   )
   ```

3. Confirm to user with memory name and restore instructions.

### `restore`: List and restore checkpoints
1. List available checkpoints:
   ```
   mcp__serena__list_memories()
   ```

2. Filter for `checkpoint-*` prefix
3. Show recent checkpoints with dates
4. Ask user which to restore (AskUserQuestion)
5. Read and summarize checkpoint
6. Offer to continue from that state

### `<custom-name>`: Create named checkpoint
Create checkpoint with descriptive name:
```
mcp__serena__write_memory(
  memory_file_name="checkpoint-<custom-name>.md",
  content="<checkpoint content>"
)
```

Useful for: `pre-refactor`, `before-migration`, `feature-complete`

## Checkpoint Content Template

```markdown
# Session Checkpoint: <timestamp or name>

## Task Context
- **Beads Task:** <id> - <title> (or "None")
- **Goal:** <what we're working on>
- **Status:** <in progress / near completion / blocked>

## Completed
- [x] Step 1
- [x] Step 2

## Remaining
- [ ] Step 3
- [ ] Step 4

## Current State
- **Last modified:** <file>
- **Tests passing:** <yes/no>
- **Blockers:** <any issues>

## Key Files
- `path/to/main.py` — <what's there>
- `path/to/test.py` — <test status>

## Next Steps
1. <immediate next action>
2. <following action>

## Recovery
To continue: read this checkpoint, open key files, proceed with next steps.
```

## Integration

- Uses `session-checkpoint` agent for complex checkpoints
- Works with beads task tracking
- Persists in `.serena/memories/`

## Examples

```bash
# Quick checkpoint
/checkpoint

# Named checkpoint before risky operation
/checkpoint pre-refactor

# Restore from previous checkpoint
/checkpoint restore
```
