---
description: Quick beads task management
allowed-tools: Bash(bd:*)
argument-hint: [add <desc>|done|block <reason>|show|list]
---

# Task Management

Quick interface to beads task tracker.

## Context

- Beads status: !`command -v bd &>/dev/null && echo "installed" || echo "not installed"`
- Current task: !`bd prime 2>/dev/null | head -5 || echo "none"`
- Available tasks: !`bd ready --json 2>/dev/null | head -3 || echo "[]"`

## Commands

### No arguments: Show current context
Display current task with full details:
```bash
bd list --status in_progress
bd show <id>
```

### `add <description>`: Create new task
```bash
bd create --title "$*" --type task
```
Then offer to start it immediately with `bd update <id> --status in_progress`.

### `done`: Complete current task
```bash
bd close <id> --reason "completed"
```
Show success confirmation and offer next task from ready list.

### `defer <reason>`: Put task on ice
```bash
bd defer <id>
bd comments add <id> "Reason: $*"
```
Explain why deferred and offer next task.

### `show [id]`: Show task details
```bash
bd show <id>
```

### `list`: List all tasks
```bash
bd list
bd ready  # Show only ready to work
```

### `mol <proto>`: Spawn molecule from proto
```bash
bd mol spawn <proto> --var key=value
```

### `wisp <proto>`: Spawn ephemeral wisp
```bash
bd wisp create <proto>
```

## Error Handling

- **bd not installed**: Inform user to install beads CLI
- **No daemon running**: Suggest `bd init` to initialize project
- **No task in progress**: Show ready tasks and offer to start one

## Integration

This command works with:
- `session-context.sh` hook — injects `bd prime` at session start
- `session-persist.sh` hook — runs `bd sync` at session end
- `task-tracker` agent — for complex task lifecycle automation
