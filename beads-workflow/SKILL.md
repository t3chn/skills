---
name: Beads Workflow
description: This skill should be used when the user asks about "beads", "task management", "bd command", "issue tracker", "какие задачи", "что делать", "готово", "done", "следующая задача", "создай задачу", "tasks", "next task", "pick task", or needs guidance on beads-based project task management. ACTIVATE AUTOMATICALLY when session starts in directory with .beads/.
version: 1.0.0
---

# Beads Workflow

Proactive task management for projects using beads issue tracker.

## Session Start (PROACTIVE)

When starting a session in a project directory:

### 1. Check for beads

```bash
ls -d .beads 2>/dev/null
```

If `.beads/` does not exist — this skill is not applicable.

### 2. Self-Install in CLAUDE.md (MANDATORY)

**YOU MUST ALWAYS CHECK AND OFFER TO CREATE CLAUDE.md:**

```bash
# Check if CLAUDE.md exists and has Beads Workflow section
if [ -f CLAUDE.md ]; then
  grep -q "## Beads Workflow" CLAUDE.md && echo "configured" || echo "needs_section"
else
  echo "no_claude_md"
fi
```

**If "no_claude_md" or "needs_section":**
1. ALWAYS ask user: "В проекте есть beads, но CLAUDE.md не настроен. Создать/обновить?"
2. If agreed, create or append the section below
3. DO NOT SKIP THIS STEP

**CLAUDE.md content to add:**

```markdown
# CLAUDE.md

## Beads Workflow

При старте сессии используй скилл `beads-workflow` для:
1. Показать текущую задачу (in_progress) или выбрать из ready
2. Отслеживать прогресс через TodoWrite
3. При завершении — закрыть задачу через bd close

## Project Info

<!-- Add project-specific instructions here -->
```

### 3. Get Current Context

```bash
bd list --status in_progress --json
bd ready --json
```

### 4. Present Status

**If task in_progress exists:**
> "Продолжаем работу над **[id]** [title]"
> Show task details with `bd show <id>`

**If no in_progress:**
Use AskUserQuestion with ready tasks as options (max 4, sorted by priority).

### 5. Start Selected Task

```bash
bd update <id> --status in_progress
bd show <id>
```

Use TodoWrite to break down the task into subtasks.

## During Work

- Track current task ID in conversation context
- Use TodoWrite for subtask tracking within the beads task
- When discovering subtasks that should be tracked separately:
  ```bash
  bd create --title "Subtask title" -t task -p 1 --parent <parent-id>
  ```

## Task Completion

When user says "готово", "done", "сделал", "закрой задачу":

1. Confirm which task (if ambiguous)
2. Ask for brief reason via AskUserQuestion:
   - "Реализовано" (Implemented)
   - "Исправлено" (Fixed)
   - "Не актуально" (Not relevant)
   - Other (custom input)

3. Close and sync:
   ```bash
   bd close <id> --reason "<reason>"
   bd sync
   ```

4. Offer next task from ready list

## Creating Tasks

When user says "создай задачу", "новая задача", "create task":

**Task description must include:**
1. **Clear title** — what needs to be done (action + object)
2. **Recommended skill** — if applicable, add label `skill:<name>`

Available skills for labeling:
- `skill:backend-rust` — Rust backend (Axum, SQLx, teloxide)
- `skill:backend-python` — Python backend (FastAPI, Django)
- `skill:backend-nodejs` — Node.js backend (Express, Fastify)
- `skill:frontend-design` — Frontend UI/UX
- `skill:mcp-builder` — MCP server development
- `skill:python-testing` — Python tests (pytest)

```bash
# With skill recommendation
bd create --title "Implement user auth API" -t task -p 1 -l "skill:backend-rust"

# Without skill (general task)
bd create --title "Write documentation" -t task -p 2

# Quick capture (returns only ID)
bd q "Fix login bug"
```

Priority: 0=critical (P0), 1=high (P1), 2=medium (P2), 3=low (P3), 4=backlog (P4)

For subtasks, link to parent:
```bash
bd create --title "Subtask" --parent <parent-id>
```

## Refresh Tasks

When user says "обнови задачи", "refresh", "sync":

```bash
bd sync
bd ready --json
```

Show what changed:
- New tasks added
- Tasks closed by others
- Priority changes

If current in_progress task was modified, warn user.

## Switching Tasks

Before showing ready list for next task selection, ALWAYS sync first:

```bash
bd sync
bd ready --json
```

This ensures task list is current before user picks.

## Session End

If task is still in_progress when session ends:
1. Ask: keep in_progress or close?
2. Run `bd sync` to save state
3. Brief summary of what was done

## Claude Code Integration

### Automatic Context Injection

The `session-context.sh` hook automatically injects beads context at session start:

1. **`bd prime` output** — If a task is in progress, its full context is injected
2. **Available tasks notification** — If no in-progress task, notifies about ready tasks

This means you don't need to manually call `bd ready` at session start — context is already there.

### Session Persistence

The `session-persist.sh` Stop hook runs `bd sync` when session ends, ensuring:
- Task status is saved
- Progress is not lost on context reset
- Other team members see updates

### Task Tracker Agent

For complex implementation work, the `task-tracker` agent automates the full lifecycle:

```
User: "Implement dark mode"
       │
       ▼
task-tracker agent:
  1. Checks bd ready --json
  2. Creates task if none exists (bd create)
  3. Starts task with bd update --status in_progress
  4. Creates TodoWrite subtasks
  5. Completes with bd close
```

Invoke with: `Task(subagent_type="task-tracker", prompt="Track implementation of dark mode")`

### Quick Commands

Use `/task` command for quick operations:
- `/task` — Show current task context
- `/task add "description"` — Create new task (bd create)
- `/task done` — Mark current complete (bd close)
- `/task defer "reason"` — Put on ice (bd defer)

## Molecules & Wisps (v0.33+)

### Molecules — Reusable Work Templates

For repeated workflows, create a **proto** (template) and spawn **molecules**:

```bash
# List available protos
bd mol catalog

# Spawn a molecule from proto
bd mol spawn <proto-id> --var feature="dark mode"

# Execute steps with auto-advance
bd close <step-id> --continue

# Show current position
bd mol current
```

### Wisps — Ephemeral Molecules

Wisps live in `.beads-wisp/` (gitignored) — perfect for operational loops:

```bash
# Create wisp (not synced to git)
bd wisp create <proto-id>

# When done, either:
bd mol squash <id>  # Create digest, delete wisp
bd mol burn <id>    # Delete with no trace
```

### Chemistry Metaphor

```
Proto (solid)  →  Mol (liquid)  →  Wisp (vapor)
template          real issues      ephemeral
reusable          tracked          local only
```

## Reference Files

- For detailed session lifecycle: See [references/session-lifecycle.md](references/session-lifecycle.md)
- For all bd commands: See [references/task-operations.md](references/task-operations.md)
