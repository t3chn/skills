# Beads CLI Commands Reference

## Viewing Tasks

```bash
# List ready (unblocked) tasks
bd ready

# Ready tasks as JSON (for parsing)
bd ready --json

# Filter by label
bd ready -l project:context8-mcp

# All open issues
bd list --status open

# Show specific issue
bd show <id>
```

## Creating Tasks

```bash
# Create a task
bd create "Title" -t task -p 1

# Create with labels
bd create "Title" -t task -p 1 -l project:myproject -l area:backend

# Types: task, bug, feature, epic
# Priority: 0=critical, 1=high, 2=medium, 3=low
```

## Updating Tasks

```bash
# Change status
bd update <id> --status in_progress
bd update <id> --status done

# Close with reason
bd close <id> --reason "Completed implementation"

# Add dependency (child blocked by parent)
bd dep add <child-id> <parent-id> --type parent-child
```

## Configuration

```bash
# Get config value
bd config get repos.additional

# Set config value
bd config set repos.additional /path/one,/path/two

# View all config
bd config list
```

## Sync

```bash
# Sync beads state with git
bd sync
```

## Project Prefixes

Each project has a unique prefix for issue IDs:
- `plan-` — planner (personal tasks)
- `ctx8mcp-` — context8-mcp
- `ctx8land-` — context8-landing
- `checko-` — checko-mcp
