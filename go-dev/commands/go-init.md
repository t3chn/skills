---
description: Initialize a new Go project with modern structure
allowed-tools: Bash(go:*), Bash(task:*), Bash(mkdir:*), Bash(ls:*), Write, Edit, Read
argument-hint: <project-name> [cli|http|library]
---

# Initialize Go Project

## Context

- Current directory: !`pwd`
- Go version: !`go version 2>/dev/null || echo "Go not installed"`
- Directory contents: !`ls -la 2>/dev/null | head -10`
- Existing go.mod: !`test -f go.mod && cat go.mod | head -3 || echo "none"`

## Task

Create a new Go project with the following parameters:
- **Project name:** $1
- **Project type:** $2 (default: cli)

### Project Types
- `cli` — Command-line application with flag handling
- `http` — HTTP service with graceful shutdown
- `library` — Reusable package with examples

## Requirements

1. **Validate environment**
   - Verify Go is installed
   - Check current directory is suitable (empty or confirm overwrite)

2. **Create structure** based on project type:
   ```
   # CLI
   cmd/<name>/main.go
   internal/app/app.go

   # HTTP
   cmd/server/main.go
   internal/handler/handler.go
   internal/service/service.go

   # Library
   pkg/<name>/<name>.go
   examples/basic/main.go
   ```

3. **Generate files:**
   - `go.mod` — Initialize module
   - `Taskfile.yml` — Build automation
   - `.golangci.yml` — Linter config
   - `.gitignore` — Ignore patterns
   - `README.md` — Basic documentation

4. **Initialize and verify:**
   ```bash
   go mod init <module-path>
   go mod tidy
   task --list
   ```

## Output

After creation, display:
- Directory tree
- Available task commands
- Next steps for development

Use the `go-project-init` agent if complex scaffolding is needed.
