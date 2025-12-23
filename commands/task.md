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
bd show
```

### `add <description>`: Create new task
```bash
bd add "$*"
```
Then offer to start it immediately.

### `done`: Complete current task
```bash
bd done
```
Show success confirmation and offer next task from ready list.

### `block <reason>`: Mark task blocked
```bash
bd block "$*"
```
Explain what's blocking and offer next task.

### `show [id]`: Show task details
```bash
bd show $1
```

### `list`: List all tasks
```bash
bd list
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
