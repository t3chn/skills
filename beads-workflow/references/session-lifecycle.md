# Session Lifecycle

Detailed guide for managing work sessions with beads.

## Phase 1: Initialization

### Check Environment

```bash
# Verify beads is available
which bd

# Check for .beads directory
ls -d .beads 2>/dev/null || echo "No beads in this project"

# Get project prefix (from config)
bd config get id.prefix
```

### Load Current State

```bash
# Tasks currently being worked on
bd list --status in_progress --json

# Available tasks (unblocked)
bd ready --json

# All open tasks
bd list --status open --json
```

### Task Selection Flow

```
┌─────────────────────────────────────┐
│ Session Start                       │
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
                  ┌─────────────┐
                  │ Start task  │
                  │ in_progress │
                  └─────────────┘
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

**Significant new work:**
```bash
bd create "New discovery" -t task -p 2
bd dep add <new-id> <current-id> --type parent-child
```

**Blocker found:**
```bash
bd create "Blocking issue" -t bug -p 1
bd dep add <current-id> <blocker-id> --type blocked-by
```

### Context Preservation

Maintain in conversation:
- Current task ID
- Task title
- Remaining TodoWrite items
- Any blockers encountered

## Phase 3: Completion

### Verify Completion

Before closing:
1. All TodoWrite items checked
2. Tests pass (if applicable)
3. Code committed (if applicable)

### Close Task

```bash
bd close <id> --reason "Implemented feature X with tests"
bd sync
```

### Transition

After closing:
1. Show updated ready list
2. Suggest next high-priority task
3. Or ask if user wants to continue

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

**Следующие задачи:**
- task-789: Email verification (P1)
- task-012: User profile page (P2)
```
