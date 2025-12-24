---
description: Review Go code using official code-reviewer with Go conventions
allowed-tools: Task, Glob, Grep, Read
argument-hint: [path] [focus:all|errors|tests|security]
---

# Go Code Review

Review Go code at `$1` (default: current changes) with focus on `$2` (default: all).

## Context

- Changed Go files: !`git diff --name-only HEAD 2>/dev/null | grep '\.go$' | head -10 || echo "no changes"`
- CLAUDE.md exists: !`test -f CLAUDE.md && echo "yes" || echo "no"`

## Task

Use the `feature-dev:code-reviewer` agent to review Go code.

The `go-conventions` skill provides Go-specific context:
- Error handling (wrapping, sentinel errors, errors.Is/As)
- Naming conventions (interfaces with -er suffix, package names)
- Testing patterns (table-driven, t.Run, testify)
- Context usage and cancellation
- Concurrency patterns (goroutine leaks, sync package)

### Focus Areas

| Focus | What to Check |
|-------|---------------|
| `all` | Complete review |
| `errors` | Error handling, wrapping, checking |
| `tests` | Table-driven tests, test helpers, coverage |
| `security` | Input validation, SQL injection, secrets |

### Output Format

Report issues with:
- File:line references
- Confidence score (only report ≥80)
- Specific fix suggestions
