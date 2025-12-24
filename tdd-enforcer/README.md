# TDD Enforcer Plugin

Cross-language Test-Driven Development enforcement for Go, TypeScript, Python, and Rust.

## Overview

This plugin enforces the **Red-Green-Refactor** TDD workflow by:
1. Detecting when code is modified without running tests
2. Warning (or blocking) session completion until tests pass
3. Guiding developers through the TDD cycle with specialized agents

## Features

### Stop Hook Enforcement

When you try to stop a session after modifying code:
- **Warning Mode (default):** Shows a reminder to run tests
- **Strict Mode:** Blocks until tests are executed

### TDD Agents

| Agent | Purpose |
|-------|---------|
| `tdd-coach` | Guides Red-Green-Refactor workflow step by step |
| `test-analyzer` | Analyzes test coverage and quality |

### Commands

| Command | Purpose |
|---------|---------|
| `/tdd <feature>` | Start TDD workflow for a feature |
| `/tdd-status` | Check TDD compliance status |

## Supported Languages

| Language | Test Pattern | Test Command |
|----------|-------------|--------------|
| Go | `*_test.go` | `go test ./...` |
| TypeScript | `*.test.ts`, `*.spec.ts` | `npm test` / `pnpm vitest` |
| Python | `test_*.py`, `*_test.py` | `pytest` |
| Rust | `#[cfg(test)]` / `tests/*.rs` | `cargo test` |

## Configuration

Create `.claude/tdd-enforcer.local.md` in your project:

```yaml
---
strictMode: false     # true = block, false = warn (default)
testCommand: null     # auto-detect or override (e.g., "npm test")
---

## Project-specific TDD Notes

Add any project-specific testing conventions here.
```

## Red-Green-Refactor Cycle

```
┌─────────┐     ┌─────────┐     ┌───────────┐
│   RED   │ ──► │  GREEN  │ ──► │ REFACTOR  │ ──┐
│  Write  │     │ Minimal │     │  Improve  │   │
│ Failing │     │  Code   │     │   Code    │   │
│  Test   │     │ to Pass │     │  Safely   │   │
└─────────┘     └─────────┘     └───────────┘   │
     ▲                                          │
     └──────────────────────────────────────────┘
```

### Commit Conventions

- `test:` — RED phase (write failing test)
- `feat:` — GREEN phase (minimal implementation)
- `refactor:` — REFACTOR phase (improve code)

## How It Works

### 1. Session Start Hook

Detects project language and sets:
- `TDD_LANGUAGE` (go, typescript, python, rust)
- `TDD_TEST_CMD` (appropriate test command)

### 2. Stop Hook

When session ends:
1. Reads session transcript (`$TRANSCRIPT_PATH`)
2. Detects code modifications (Write, Edit tools)
3. Checks if test commands were executed
4. Returns warning or block based on configuration

### 3. Transcript Analysis

The `core/transcript_analyzer.py` module:
- Identifies test file patterns per language
- Detects test execution commands
- Determines TDD compliance status

## File Structure

```
tdd-enforcer/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   ├── hooks.json
│   ├── stop_tdd_check.py      # Main enforcement
│   └── session_start.sh       # Language detection
├── core/
│   ├── __init__.py
│   └── transcript_analyzer.py # Analysis logic
├── agents/
│   ├── tdd-coach/AGENT.md     # TDD guidance
│   └── test-analyzer/AGENT.md # Coverage analysis
├── commands/
│   ├── tdd.md                 # /tdd command
│   └── tdd-status.md          # /tdd-status command
├── skills/
│   └── tdd-workflow/SKILL.md  # TDD patterns
└── README.md
```

## Integration with Test Generators

Works with language-specific test generators:
- `go-test-generator` (go-dev)
- `ts-test-generator` (ts-dev)
- `python-test-writer` (python-dev)
- `rust-test-generator` (rust-dev)

The `tdd-coach` agent delegates to these generators for language-specific test patterns.

## Examples

### Start TDD for a feature

```
/tdd user authentication

# tdd-coach guides:
# 1. Write failing test for login
# 2. Implement minimal login
# 3. Refactor if needed
# 4. Repeat for each behavior
```

### Check TDD status

```
/tdd-status

# Shows:
# - Modified files
# - Tests executed
# - Compliance status
# - Recommendations
```

### Enable strict mode

```yaml
# .claude/tdd-enforcer.local.md
---
strictMode: true
---
```

Now the session will block until tests are run.
