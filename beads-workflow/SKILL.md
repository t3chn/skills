---
name: beads-workflow
description: |
  Proactive workflow for projects using beads issue tracker.
  ACTIVATE AUTOMATICALLY when session starts in directory with .beads/.
  Use when: starting work session, selecting tasks, completing tasks, creating subtasks.
  Triggers: "какие задачи", "что делать", "готово", "done", "следующая задача", "создай задачу", "tasks", "next task", "pick task", "обнови задачи", "refresh", "sync".
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
  bd create "Subtask title" -t task -p 1
  bd dep add <new-id> <parent-id> --type parent-child
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
bd create "Implement user auth API" -t task -p 1 -l "skill:backend-rust"

# Without skill (general task)
bd create "Write documentation" -t task -p 2
```

Priority: 0=critical, 1=high, 2=medium, 3=low

For subtasks, link to parent:
```bash
bd dep add <child-id> <parent-id> --type parent-child
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

## Reference Files

- For detailed session lifecycle: See [references/session-lifecycle.md](references/session-lifecycle.md)
- For all bd commands: See [references/task-operations.md](references/task-operations.md)
