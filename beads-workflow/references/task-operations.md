# Task Operations

Complete reference for beads CLI commands (v0.35.0+).

## Viewing Tasks

```bash
# Ready (unblocked) tasks
bd ready
bd ready --json

# Filter by label
bd ready -l project:myproject

# All open issues
bd list --status open
bd list --status open --json

# In progress tasks
bd list --status in_progress

# Show specific task
bd show <id>

# Show blocked tasks
bd blocked

# Show deferred tasks
bd list --status open  # deferred tasks have ❄️ marker
```

## Creating Tasks

```bash
# Basic task
bd create --title "Task title" -t task -p 1

# Quick capture (returns only ID)
bd q "Fix login bug"

# With labels
bd create --title "Task title" -t task -p 1 -l area:backend -l component:auth

# With parent (subtask)
bd create --title "Subtask" -t task -p 1 --parent <parent-id>

# Types
-t task      # Regular task
-t bug       # Bug fix
-t feature   # New feature
-t epic      # Parent for multiple tasks
-t molecule  # Workflow instance

# Priority (0-4 or P0-P4)
-p 0 / -p P0  # Critical
-p 1 / -p P1  # High
-p 2 / -p P2  # Medium (default)
-p 3 / -p P3  # Low
-p 4 / -p P4  # Backlog
```

## Updating Tasks

```bash
# Change status
bd update <id> --status in_progress
bd update <id> --status open

# Update title
bd update <id> --title "New title"

# Add labels
bd update <id> --add-label area:frontend

# Remove labels
bd update <id> --remove-label area:backend

# Add comment
bd comments add <id> "Progress note"
```

## Closing Tasks

```bash
# Close with reason
bd close <id> --reason "Implemented and tested"

# Close multiple at once
bd close <id1> <id2> <id3> --reason "Sprint complete"

# Close and auto-advance (molecules)
bd close <id> --continue

# Defer (put on ice)
bd defer <id>
bd undefer <id>  # Resume
```

## Dependencies

```bash
# Blocking dependency (A blocks B)
bd dep add <blocked-id> <blocker-id>  # default type: blocks

# Parent-child (subtask)
bd create --title "Subtask" --parent <parent-id>
# Or manually:
bd dep add <child-id> <parent-id> --type parent-child

# Related (no blocking)
bd dep add <id1> <id2> --type related

# Cross-project dependency
bd dep add <id> external:<project>:<capability>

# View dependencies
bd show <id>        # Shows in task details
bd dep tree <id>    # Show dependency tree
bd dep cycles       # Detect circular dependencies
```

## Molecules & Wisps (v0.33+)

```bash
# List available protos (templates)
bd mol catalog

# Spawn molecule from proto
bd mol spawn <proto-id> --var key=value

# Show current position in molecule
bd mol current

# Close step and auto-advance
bd close <step-id> --continue

# Bond protos/molecules together
bd mol bond <id1> <id2>

# Distill proto from existing epic
bd mol distill <epic-id>
```

### Wisps (ephemeral molecules)

```bash
# Create wisp (not synced to git)
bd wisp create <proto-id>

# List all wisps
bd wisp list

# Squash wisp to digest
bd mol squash <wisp-id>

# Burn wisp (delete with no trace)
bd mol burn <wisp-id>

# Garbage collect orphaned wisps
bd wisp gc
```

## Configuration

```bash
# Get config value
bd config get id.prefix
bd config get repos.additional

# Set config value
bd config set id.prefix myprefix
bd config set repos.additional /path/one,/path/two

# List all config
bd config list
```

## Sync & Maintenance

```bash
# Sync with git
bd sync

# Check sync status
bd sync --status

# Project health check
bd doctor
bd doctor --fix

# Database migration
bd migrate

# Activity stream
bd activity                # Last 100 events
bd activity --follow       # Real-time
bd activity --mol <id>     # Filter by molecule
```

## Output Formats

Most commands support `--json` for machine-readable output:

```bash
bd ready --json
bd list --status open --json
bd show <id> --json
```

## Common Patterns

### Start work session
```bash
bd list --status in_progress --json  # Check current
bd ready --json                       # See available
bd update <id> --status in_progress  # Pick task
```

### Complete task and pick next
```bash
bd close <id> --reason "Done"
bd sync
bd ready --json
bd update <next-id> --status in_progress
```

### Create subtask (preferred)
```bash
bd create --title "Subtask" -t task -p 1 --parent <parent-id>
```

### Molecule workflow
```bash
bd mol spawn feature-template --var name="dark-mode"
# Work on steps...
bd close <step-id> --continue  # Auto-advance
```
