---
name: Reliable Execution
description: This skill should be used when the user asks about "reliable execution", "session persistence", "context recovery", "checkpoint patterns", "handoff protocol", "agent reliability", "preventing context loss", or needs guidance on ensuring work survives context resets and session handoffs.
version: 1.0.0
---

# Reliable Execution — Patterns for Persistent Agent Work

## The Problem

Claude Code sessions have limited context. Long tasks risk:
- Context resets mid-implementation
- Lost progress after interruptions
- Incomplete handoffs between sessions
- Forgotten decisions and discoveries

## The Solution

A layered approach to persistence:

```
┌─────────────────────────────────────────────┐
│              Session Layer                   │
│  TodoWrite — visible progress tracking      │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│              Task Layer                      │
│  Beads — high-level task lifecycle          │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│            Knowledge Layer                   │
│  Serena Memories — persistent discoveries   │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│              Code Layer                      │
│  Git commits — permanent artifacts          │
└─────────────────────────────────────────────┘
```

## Pre-Flight Checklist

Before starting significant work:

### 1. Task Tracking Active?
```bash
# Check beads
bd show 2>/dev/null || echo "No beads task"
```
→ If no task, create one: `bd create --title "Task description"`

### 2. Context Loaded?
- SessionStart hook injected `bd prime`?
- Serena memories available? `list_memories()`

### 3. TodoWrite Initialized?
Create subtasks for the implementation.

### 4. Checkpoint Plan?
Identify when to save progress:
- After each major step
- Before risky operations
- When context feels full

## During Execution

### Track Progress Visibly
```
TodoWrite([
  {content: "Implement UserService", status: "completed"},
  {content: "Add unit tests", status: "in_progress"},
  {content: "Update documentation", status: "pending"}
])
```

### Save Discoveries
When you learn something important:
```
write_memory(
  memory_file_name="auth-patterns.md",
  content="# Auth Patterns\n\n..."
)
```

### Commit Incrementally
After completing logical units:
```bash
git add -A && git commit -m "feat: implement UserService"
```

### Create Checkpoints
Before context gets full or before risky changes:
```
Task(subagent_type="session-checkpoint", prompt="Save progress")
```

## Checkpoint Triggers

Create checkpoints when:

| Trigger | Action |
|---------|--------|
| Major step completed | `/checkpoint` |
| Before refactoring | `/checkpoint` with rollback notes |
| Context feeling full | `/checkpoint` with full state |
| Session ending | `/checkpoint` with handoff notes |
| Complex bug found | `/checkpoint` with debug state |

## Session Handoff Protocol

When session is ending or context is resetting:

### 1. Sync Beads
```bash
bd sync
```

### 2. Create Handoff Checkpoint
Include:
- Current task state
- Completed vs remaining work
- Key discoveries
- Immediate next step
- Any blockers

### 3. Commit Pending Changes
```bash
git add -A && git commit -m "WIP: <current state>"
```

### 4. Report Checkpoint Location
Tell user:
```
Session checkpoint saved to `checkpoint-<timestamp>.md`.
To continue: Read this memory and resume from step X.
```

## Recovery Flow

When starting a new session:

### 1. Check for Checkpoints
```
list_memories()
```
Look for `checkpoint-*.md` files.

### 2. Read Most Recent
```
read_memory("checkpoint-<latest>.md")
```

### 3. Resume from State
Follow "Next Steps" from checkpoint.

### 4. Update Task Status
```bash
bd update <task-id> --status in_progress  # Resume beads task
```

## Tool Integration

### Hooks
- `session-context.sh` — Injects beads/serena context at start
- `session-persist.sh` — Syncs beads at session end
- `suggest-semantic-tools.sh` — Reminds about serena tools

### Agents
- `task-tracker` — Manages beads task lifecycle
- `code-navigator` — Explores code with serena, saves discoveries
- `session-checkpoint` — Creates recovery checkpoints

### Commands
- `/task` — Quick beads task management
- `/checkpoint` — Save session progress

## Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| No task tracking | Start with `bd create` or `/task add` |
| Discoveries in conversation only | Use `write_memory()` |
| No progress visibility | Use `TodoWrite` |
| Waiting until end to save | Checkpoint after each major step |
| Large uncommitted changes | Commit incrementally |

## Example: Full Reliable Flow

```
User: "Implement user authentication"

1. Create task:
   bd create --title "Implement user authentication" -t feature -p 1
   bd update <id> --status in_progress

2. Plan with TodoWrite:
   - Research existing auth patterns
   - Implement UserService
   - Add login/logout endpoints
   - Write tests
   - Update documentation

3. Research (save discoveries):
   - Use serena to explore codebase
   - write_memory("auth-research.md", findings)

4. Implement (checkpoint after each):
   - Complete UserService → checkpoint + commit
   - Complete endpoints → checkpoint + commit
   - Complete tests → checkpoint + commit

5. Finish:
   bd close <id> --reason "Implemented with tests"
   bd sync
   Final checkpoint with summary
```

## Related Skills

- **beads-workflow** — Task tracking details
- **serena-navigation** — Code exploration and memory
