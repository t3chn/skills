# go-dev Plugin

Modern Go development toolkit for Claude Code with skills, agents, and commands for building Go projects with consistent, idiomatic patterns (2024-2025 best practices).

## Features

### Skills (Knowledge Modules)

Auto-triggered based on conversation context:

| Skill | Triggers On |
|-------|-------------|
| **Project Structure** | "Go project layout", "internal/ vs pkg/", "organize Go packages", "clean architecture Go" |
| **Error Handling** | "Go error handling", "errors.Is", "error wrapping", "sentinel errors", "fmt.Errorf %w" |
| **Testing Patterns** | "Go testing", "table-driven tests", "testify", "mocks in Go", "require vs assert" |
| **Taskfile Automation** | "Taskfile", "go-task", "alternative to Makefile", "task --watch" |
| **Structured Logging** | "slog", "Go logging", "structured logging", "JSON logging Go" |
| **Context Patterns** | "context.Context", "WithTimeout", "WithCancel", "context values" |

### Agents (Autonomous Subagents)

| Agent | Purpose | Color |
|-------|---------|-------|
| **go-code-reviewer** | Review Go code for best practices, security, error handling | Red |
| **go-project-init** | Scaffold new Go projects with proper structure | Green |
| **go-test-generator** | Generate table-driven tests for existing code | Cyan |

Each agent includes:
- Comprehensive system prompts (800-1500 words)
- `<example>` blocks for auto-triggering
- Confidence-based filtering (≥80 threshold)
- Specific output formats

### Commands (Slash Commands)

| Command | Description |
|---------|-------------|
| `/go-init <name> [type]` | Create new Go project (cli/http/library) |
| `/go-review [path] [focus]` | Review code (all/errors/tests/structure/security) |
| `/go-test <file> [style]` | Generate tests (table/testify/benchmark) |

All commands include:
- `allowed-tools` for controlled execution
- Dynamic context injection with `` !`command` `` syntax
- `argument-hint` for better UX

### Hook

| Hook | Event | Action |
|------|-------|--------|
| **go-lint-check** | PostToolUse (Edit/Write *.go) | Check formatting with gofmt |

## Installation

### Prerequisites

```bash
# Go (required)
go version  # Go 1.21+

# Task runner
brew install go-task  # or: go install github.com/go-task/task/v3/cmd/task@latest

# Linter
brew install golangci-lint  # or: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Optional: Code formatting
go install golang.org/x/tools/cmd/goimports@latest

# Optional: Testing
go get github.com/stretchr/testify
```

### Plugin Setup

This plugin is auto-discovered from `~/.claude/plugins/local/go-dev/`.

## Usage Examples

### Create a new CLI project
```
/go-init myapp cli
```

### Create an HTTP service
```
/go-init api-server http
```

### Review error handling in a directory
```
/go-review ./internal/service errors
```

### Generate tests for a file
```
/go-test ./internal/user/service.go testify
```

### Using agents directly
```
Use the go-code-reviewer agent to check my changes before commit
```

## Best Practices Enforced

### Project Structure
- `cmd/` for application entry points (minimal main.go)
- `internal/` for private packages (compiler-enforced)
- `pkg/` only for truly reusable libraries
- Interfaces defined where consumed, not implemented

### Error Handling
- Wrap errors with context: `fmt.Errorf("operation: %w", err)`
- Use `errors.Is()` and `errors.As()` for checking
- Sentinel errors for expected conditions (`ErrNotFound`)
- Don't leak internal errors in public APIs

### Testing
- Table-driven tests with `t.Run()` subtests
- `require` for preconditions (stops on failure)
- `assert` for assertions (continues on failure)
- Test helpers use `t.Helper()`
- No `time.Sleep()` — use channels/conditions

### Structured Logging
- Use `log/slog` (Go 1.21+)
- JSON format for production
- Inject logger into services
- Use `*Context` methods when context available

### Context
- Context as first parameter
- Don't store context in structs
- Check cancellation in long operations
- Use `WithTimeout` for external calls

### Build Automation
- Taskfile.yml over Makefile (cross-platform)
- Source tracking for incremental builds
- Standard tasks: build, test, lint, fmt, clean
- golangci-lint v2 configuration

## Directory Structure

```
go-dev/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── go-code-reviewer/
│   │   └── AGENT.md
│   ├── go-project-init/
│   │   └── AGENT.md
│   └── go-test-generator/
│       └── AGENT.md
├── commands/
│   ├── go-init.md
│   ├── go-review.md
│   └── go-test.md
├── hooks/
│   └── go-lint-check.md
├── skills/
│   ├── context-patterns/
│   │   └── SKILL.md
│   ├── error-handling/
│   │   └── SKILL.md
│   ├── logging-slog/
│   │   └── SKILL.md
│   ├── project-structure/
│   │   └── SKILL.md
│   ├── taskfile-automation/
│   │   └── SKILL.md
│   └── testing-patterns/
│       └── SKILL.md
├── templates/
│   ├── gitignore.txt
│   └── golangci.yml
└── README.md
```

## Version

1.0.0 — Modern Go development patterns (2024-2025)

## References

- [Taskfile.dev](https://taskfile.dev/)
- [golangci-lint](https://golangci-lint.run/)
- [Go Project Layout](https://github.com/golang-standards/project-layout)
- [Effective Go](https://go.dev/doc/effective_go)
