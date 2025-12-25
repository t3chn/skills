---
description: Initialize project for production workflow (beads + serena + CLAUDE.md)
---

# /init-project

Initialize the current project with production workflow tools.

## What This Does

1. **Beads** — Task tracking with `bd` CLI
2. **Serena** — Code memory and semantic navigation
3. **CLAUDE.md** — AI quick reference (always loaded)
4. **Pre-commit** — Code quality hooks

## Usage

Run the initialization script:

```bash
# Full setup (recommended)
bash ${CLAUDE_PLUGIN_ROOT}/scripts/init-project.sh

# With custom name
bash ${CLAUDE_PLUGIN_ROOT}/scripts/init-project.sh --name "My Project"

# Minimal (beads + CLAUDE.md only)
bash ${CLAUDE_PLUGIN_ROOT}/scripts/init-project.sh --minimal
```

## After Initialization

1. Review `CLAUDE.md` and customize for your project
2. Update `.serena/memories/overview.md` with architecture details
3. Create first task: `bd create --title "..." --type task`
4. Commit: `git add -A && git commit -m "chore: init production workflow"`
5. Sync: `bd sync`

## Checklist

```
[ ] .beads/ exists (bd init)
[ ] .serena/project.yml exists
[ ] .serena/memories/overview.md written
[ ] CLAUDE.md with quick start
[ ] .pre-commit-config.yaml configured
[ ] pre-commit install executed
[ ] First commit made
[ ] bd sync executed
```
