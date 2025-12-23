---
description: Review Go code for best practices and potential issues
allowed-tools: Bash(git:*), Bash(go:*), Bash(golangci-lint:*), Read, Glob, Grep
argument-hint: [path] [focus:all|errors|tests|security]
---

# Review Go Code

## Context

- Working directory: !`pwd`
- Git status: !`git status --short 2>/dev/null | head -20 || echo "not a git repo"`
- Changed Go files: !`git diff --name-only HEAD 2>/dev/null | grep '\.go$' | head -10 || echo "no changes"`
- CLAUDE.md exists: !`test -f CLAUDE.md && echo "yes" || echo "no"`
- golangci-lint available: !`which golangci-lint >/dev/null 2>&1 && echo "yes" || echo "no"`

## Task

Review Go code with:
- **Path:** $1 (default: changed files or current directory)
- **Focus:** $2 (default: all)

### Focus Areas

| Focus | Checks |
|-------|--------|
| `all` | Complete review — errors, tests, structure, security |
| `errors` | Error handling — wrapping, sentinel errors, errors.Is/As |
| `tests` | Testing patterns — table-driven, testify, mocks |
| `structure` | Project layout — cmd/, internal/, interfaces |
| `security` | Security issues — injection, secrets, validation |

## Review Process

1. **Identify scope:**
   - If path specified, review that file/directory
   - Otherwise, review git diff changes
   - If no changes, review current directory

2. **Check CLAUDE.md** for project-specific rules

3. **Run static analysis** (if available):
   ```bash
   golangci-lint run $1 2>&1 | head -30
   ```

4. **Manual review** for:
   - Error handling patterns
   - Testing best practices
   - Go idioms and style
   - Security vulnerabilities

5. **Report findings** with:
   - File:line references
   - Confidence scores (≥80 only)
   - Specific fix suggestions

## Output Format

```
## Go Code Review: [scope]

### [CRITICAL|WARNING] file.go:line — Issue
**Confidence:** X/100
**Fix:** [code example]

### Summary
- Files reviewed: N
- Issues found: N critical, N warnings
- Recommendations: [prioritized list]
```

For comprehensive review, use the `go-code-reviewer` agent.
