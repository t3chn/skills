---
name: daily-planner
description: Use when user asks for daily/weekly plan, wants to plan their day, or says "план на день/неделю", "что делаем сегодня". Integrates with beads (bd) issue tracker to show ready tasks from configured projects.
---

# Daily Planner Skill

This skill helps create daily work plans by aggregating tasks from multiple projects using the beads issue tracker.

## Workflow

### Step 1: Get Available Projects

Run this command in `~/planner` to get hydrated projects:

```bash
cd ~/planner && bd config get repos.additional
```

Parse the comma-separated paths. Always include `~/planner` as the base project for personal tasks.

### Step 2: Ask Which Projects Are in Focus

Use AskUserQuestion with multiSelect to let user choose projects for today:

```
Question: "Какие проекты в фокусе сегодня?"
Options: [parsed project names from Step 1]
multiSelect: true
```

Extract project name from path (last directory component).

### Step 3: Ask About Available Time

Use AskUserQuestion:

```
Question: "Сколько времени на работу сегодня?"
Options:
  - "Пара часов" (2-3 hours)
  - "Полдня" (4-5 hours)
  - "Полный день" (6-8 hours)
  - "Вечер" (1-2 hours)
```

### Step 4: Fetch Ready Tasks

For each selected project, run:

```bash
cd <project_path> && bd ready --json
```

Collect all tasks, noting their:
- ID (with project prefix)
- Title
- Priority (0=critical, 1=high, 2=medium, 3=low)
- Labels

### Step 5: Create the Plan

Generate a daily plan with:

1. **Header** with date and focus projects
2. **Priority tasks** (P0-P1) — must do today
3. **If time allows** (P2-P3) — nice to have
4. **Checklist format** for easy tracking

Example output:

```markdown
# План на [date]

## Фокус
- **project-a** — краткое описание
- **project-b** — краткое описание
- Время: [selected time]

---

## Обязательно сделать (P0-P1)

### project-a
- [ ] [id] Task title

### project-b
- [ ] [id] Task title

---

## Если останется время (P2-P3)

- [ ] [id] Task title
```

## Notes

- Tasks are worked on in separate sessions per project
- Use `bd update <id> --status in_progress` when starting a task
- Use `bd close <id> --reason "Done"` when completing
- Run `bd sync` after significant changes to sync with git
