# Task Operations

Complete reference for beads CLI commands.

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
```

## Creating Tasks

```bash
# Basic task
bd create "Task title" -t task -p 1

# With labels
bd create "Task title" -t task -p 1 -l area:backend -l component:auth

# Types
-t task     # Regular task
-t bug      # Bug fix
-t feature  # New feature
-t epic     # Parent for multiple tasks

# Priority
-p 0  # Critical
-p 1  # High
-p 2  # Medium
-p 3  # Low
```

## Updating Tasks

```bash
# Change status
bd update <id> --status in_progress
bd update <id> --status done

# Update title
bd update <id> --title "New title"

# Add labels
bd update <id> --add-label area:frontend

# Remove labels
bd update <id> --remove-label area:backend
```

## Closing Tasks

```bash
# Close with reason
bd close <id> --reason "Implemented and tested"

# Close as not needed
bd close <id> --reason "Not relevant anymore"
```

## Dependencies

```bash
# Parent-child (subtask)
bd dep add <child-id> <parent-id> --type parent-child

# Blocked-by (blocker)
bd dep add <blocked-id> <blocker-id> --type blocked-by

# View dependencies
bd show <id>  # Shows in task details
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

## Sync

```bash
# Sync with git
bd sync

# Force sync
bd sync --force
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

### Create subtask
```bash
bd create "Subtask" -t task -p 1
bd dep add <subtask-id> <parent-id> --type parent-child
```
