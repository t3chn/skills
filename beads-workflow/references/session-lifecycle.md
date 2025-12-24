# Session Lifecycle

Detailed guide for managing work sessions with beads (v0.35.0+).

## Phase 1: Initialization

### Check Environment

```bash
# Verify beads is available
which bd
bd --version

# Check for .beads directory
ls -d .beads 2>/dev/null || echo "No beads in this project"

# Get project prefix (from config)
bd config get id.prefix

# Check health
bd doctor
```

### Load Current State

```bash
# Get optimized context (auto-detects MCP mode)
bd prime

# Tasks currently being worked on
bd list --status in_progress --json

# Available tasks (unblocked)
bd ready --json

# All open tasks
bd list --status open --json

# Check for deferred tasks
bd list --status open  # ❄️ marks deferred
```

### Task Selection Flow

```
┌─────────────────────────────────────┐
│ Session Start                       │
│ (bd prime auto-injected by hooks)   │
└─────────────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────┐
        │ in_progress     │
        │ exists?         │
        └────────┬────────┘
                 │
         ┌───────┴───────┐
         │               │
        YES             NO
         │               │
         ▼               ▼
   ┌───────────┐  ┌─────────────┐
   │ Continue  │  │ Show ready  │
   │ task      │  │ tasks       │
   └───────────┘  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ User picks  │
                  │ task        │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────────────────┐
                  │ bd update <id>          │
                  │   --status in_progress  │
                  └─────────────────────────┘
```

## Phase 2: Active Work

### Track Progress

Use TodoWrite to break down the beads task:

```
Beads Task: "Implement user auth" (id: abc-123)
├── [ ] Research existing auth patterns
├── [ ] Create auth middleware
├── [ ] Add login endpoint
├── [ ] Add logout endpoint
└── [ ] Write tests
```

### Handle Discoveries

When new work is discovered during implementation:

**Minor subtask (same scope):**
- Add to TodoWrite list
- Complete within current task

**Significant new work (create as child):**
```bash
bd create --title "New discovery" -t task -p 2 --parent <current-id>
```

**Blocker found:**
```bash
bd create --title "Blocking issue" -t bug -p 1
bd dep add <current-id> <blocker-id>  # current blocked by blocker
```

**Put aside for later:**
```bash
bd defer <id>
bd comments add <id> "Reason: waiting for API spec"
```

### Context Preservation

Maintain in conversation:
- Current task ID
- Task title
- Remaining TodoWrite items
- Any blockers encountered

### Progress Notes

```bash
# Add progress comment
bd comments add <id> "Completed middleware, starting endpoints"
```

## Phase 3: Completion

### Verify Completion

Before closing:
1. All TodoWrite items checked
2. Tests pass (if applicable)
3. Code committed (if applicable)

### Close Task

```bash
# Single task
bd close <id> --reason "Implemented feature X with tests"

# Multiple tasks at once
bd close <id1> <id2> --reason "Sprint complete"

# For molecules: close and auto-advance
bd close <id> --continue
```

### Transition

After closing:
1. Show updated ready list
2. Suggest next high-priority task
3. Or ask if user wants to continue

```bash
bd sync
bd ready --json
```

## Phase 4: Session End

### Clean State

```bash
# Sync all changes
bd sync

# Verify state
bd list --status in_progress
```

### Summary Format

```
## Сессия завершена

**Выполнено:**
- [x] task-123: Implement user auth

**В процессе:**
- [ ] task-456: Add password reset (60% done)

**Отложено (❄️):**
- task-999: Research OAuth providers

**Следующие задачи:**
- task-789: Email verification (P1)
- task-012: User profile page (P2)
```

## Molecule Workflow (v0.33+)

For repeated workflows, use molecules:

```
┌────────────────────────────────────┐
│ bd mol spawn feature-template      │
│   --var name="dark-mode"           │
└─────────────────┬──────────────────┘
                  │
                  ▼
        ┌─────────────────┐
        │ Step 1: Design  │
        └────────┬────────┘
                 │ bd close <id> --continue
                 ▼
        ┌─────────────────┐
        │ Step 2: Impl    │
        └────────┬────────┘
                 │ bd close <id> --continue
                 ▼
        ┌─────────────────┐
        │ Step 3: Test    │
        └────────┬────────┘
                 │ bd close <id> --continue
                 ▼
        ┌─────────────────┐
        │ Complete ✓      │
        └─────────────────┘
```

### Wisps for Ephemeral Work

For one-off workflows that shouldn't clutter history:

```bash
# Create wisp (not synced to git)
bd wisp create patrol-template

# Work through steps...
bd close <id> --continue

# When done:
bd mol squash <wisp-id>  # Create digest
# or
bd mol burn <wisp-id>    # Delete with no trace
```
