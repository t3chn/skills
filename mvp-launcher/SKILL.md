---
name: mvp-launcher
description: |
  Portable MVP workflow for rapid product development. Start sprints, manage context, handle session handoffs.
  Triggers: "start mvp", "resume mvp", "mvp sprint", "mvp handoff", "launch mvp", "mvp status"
---

# mvp-launcher

Portable skill for rapid MVP development with context persistence across sessions.

## Configuration

Paths can be overridden via environment or defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| MVP_ROOT | ~/mvps | Where context files live |
| MVP_PROJECTS | ~/projects | Where code repos live |

## Tech Stack Reference

| Type | Stack | Hosting | Cost |
|------|-------|---------|------|
| telegram-bot | Rust + teloxide | Fly.io | $0 |
| api-service | Rust + Axum | Shuttle.dev | $0 |
| cli-tool | Rust + clap | crates.io | $0 |
| mcp-server | Python + FastMCP | Railway | $5 |
| web-app | Vite + React | Vercel | $0 |
| web-app-complex | Next.js + Supabase | Vercel | $0 |

---

## Procedures

### start — Start New MVP Sprint

**Triggers:** "start mvp", "new mvp", "begin mvp"

**Actions:**

1. AskUserQuestion:

   **Q1: "What are we building?"**
   - header: "Name"
   - Free text via "Other"

   **Q2: "What scope?"**
   - header: "Scope"
   - Options:
     - "Minimal (5 days)" — Core only, no polish
     - "Lean (7 days)" — Core + basic error handling
     - "Solid (10-14 days)" — Full feature set + tests

   **Q3: "Project type?"**
   - header: "Type"
   - Options:
     - "telegram-bot" — Rust + teloxide
     - "api-service" — Rust + Axum
     - "mcp-server" — Python + FastMCP
     - "web-app" — Vite + React
     - "cli-tool" — Rust + clap

   **Q4: "Hours per day?"**
   - header: "Hours"
   - Options:
     - "1-2 hours" — Part-time
     - "3-4 hours" — Half-day
     - "5-6 hours" — Most of day
     - "7-8 hours" — Full-time

2. Create MVP context:
   - Create `$MVP_ROOT/{slug}/`
   - Create `context.md` with business context
   - Generate `sprint.md` based on scope and hours

3. Create project repo if needed:
   - `mkdir -p $MVP_PROJECTS/{slug}`
   - Init beads: `bd init`
   - Create initial CLAUDE.md

4. Create beads tasks for Day 1:
   ```bash
   cd $MVP_PROJECTS/{slug}
   bd create --title="Day 1: Project setup" --type=task --priority=1
   ```

5. Output summary with next steps

---

### resume — Resume Session on MVP

**Triggers:** "resume mvp", "continue mvp", "back to mvp"

**Actions:**

1. Find active MVPs:
   - Read all `$MVP_ROOT/*/context.md`
   - Filter by `Status: active-sprint`

2. If multiple, AskUserQuestion which one

3. Load context:
   - Read `context.md`
   - Read last 2-3 session notes
   - Get `bd ready` from project repo

4. Calculate sprint day from start date

5. Output summary:
   ```markdown
   # Resuming: {MVP Name}

   **Sprint:** Day {N} of {total}
   **Last Session:** {date}

   ## Where We Left Off
   {from last session notes}

   ## Today's Focus (Day {N})
   {from sprint.md}

   ## Ready Tasks
   {from bd ready}

   What should we focus on first?
   ```

---

### sprint — View Sprint Progress

**Triggers:** "sprint status", "mvp progress", "sprint"

**Actions:**

1. Load active MVP context

2. Calculate metrics:
   - Sprint day (Day N of M)
   - Tasks done vs total (from beads)
   - Pace: ahead / on-track / behind

3. Output progress table and blockers

---

### handoff — End Session with State Save

**Triggers:** "mvp handoff", "end session", "save progress"

**Actions:**

1. Get active MVP context

2. AskUserQuestion:
   - What did you do?
   - Any blockers?
   - What's next?

3. Update context.md:
   - Add session to Session Log
   - Update Current State
   - Update Blockers if any

4. Sync beads: `cd $MVP_PROJECTS/{slug} && bd sync`

5. Output confirmation

---

### launch — Execute Launch Checklist

**Triggers:** "launch mvp", "deploy mvp", "ship it"

**Actions:**

1. Load active MVP context

2. Check/create launch checklist based on project type

3. Show completion progress

4. If ready, update status to `launched`

---

### list — MVP Dashboard

**Triggers:** "mvp list", "show mvps", "mvp dashboard"

**Actions:**

1. Scan all `$MVP_ROOT/*/context.md`

2. Parse status, sprint info, last session date

3. Output dashboard with active, paused, and launched MVPs

---

## Context File Format

```markdown
# MVP: {Project Name}

**Status:** planning | active-sprint | launched | paused
**Sprint:** W{N} of {total}
**Last Session:** {date}
**Repo:** ~/projects/{path}

---

## Business Context

**Problem:** {what we're solving}
**Target User:** {who will use this}
**Success Metrics:** {measurable goals}
**Monetization:** {how we make money}

---

## Technical Decisions

| Area | Decision | Rationale | Date |
|------|----------|-----------|------|
| Stack | | | |
| Hosting | | | |

---

## Current State

### Done
- [x] {completed task}

### In Progress
- [ ] {current task}

### Next Up
- {upcoming task}

---

## Session Log

### {YYYY-MM-DD}
**Done:** {what was done}
**Blockers:** {if any}
**Next:** {what's next}
```

---

## Rules

1. **Context is king** — always update context.md
2. **Handoff required** — never end session without saving state
3. **One active sprint** — focus on one MVP at a time
4. **Ship ugly first** — MVP over polish
5. **Daily chunks** — plan only 1 day ahead in detail
6. **Cost-aware** — prefer Rust/free hosting for new projects
