---
name: Production Flow
description: This skill should be used when the user asks about "production flow", "project setup", "new project", "init project", "add feature", "development workflow", "how to start", "best practices", or needs guidance on following the unified production flow for reliable code delivery.
version: 1.0.0
---

# Production Flow — Unified Development Workflow

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION FLOW STAGES                        │
├─────────────────────────────────────────────────────────────────┤
│  1. INIT      → pre-commit, beads, serena, CLAUDE.md            │
│  2. PLAN      → /feature-dev or EnterPlanMode                   │
│  3. DEVELOP   → TDD (Red→Green→Refactor), convention skills     │
│  4. VERIFY    → pre-commit, type check, SAST, tests             │
│  5. REVIEW    → /code-review, address feedback                  │
│  6. SHIP      → /commit, PR, merge to main                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. New Project Setup

### Step 1.1: Initialize Project Structure

```bash
# Create project
mkdir my-project && cd my-project
git init

# Language-specific init (choose one)
/go-init           # Go project
/ts-init           # TypeScript project
uv init            # Python project
cargo init         # Rust project
```

### Step 1.2: Setup Quality Gates

```bash
# Copy pre-commit config from vi-skills
cp ~/.claude/plugins/cache/vi-skills/vi-skills/*/templates/.pre-commit-config.yaml .

# Or create minimal config
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
EOF

# Install hooks
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

### Step 1.3: Create CLAUDE.md

```bash
cat > CLAUDE.md << 'EOF'
# Project: my-project

## Overview
[Brief description]

## Tech Stack
- Language: [Go/TypeScript/Python/Rust]
- Framework: [if applicable]
- Database: [if applicable]

## Project Structure
```
src/           # Source code
tests/         # Test files
docs/          # Documentation
```

## Development Commands
```bash
# Run tests
[test command]

# Run linter
[lint command]

# Build
[build command]
```

## Conventions
- [Key convention 1]
- [Key convention 2]
EOF
```

### Step 1.4: Initialize Beads Task Tracking

```bash
# Create beads directory
bd init

# Add initial task
bd add "Initial project setup"
bd start 1
```

### Step 1.5: Initialize Serena (if using)

```bash
# Serena will auto-detect on first use
# Memories stored in .serena/memories/
```

### Step 1.6: First Commit

```bash
git add -A
git commit -m "chore: initial project setup

- Add pre-commit hooks
- Add CLAUDE.md
- Initialize beads task tracking"
```

---

## 2. Existing Project Setup

### Step 2.1: Clone and Assess

```bash
git clone <repo>
cd <repo>

# Check what exists
ls -la .pre-commit-config.yaml CLAUDE.md .beads/ 2>/dev/null
```

### Step 2.2: Add Missing Components

```bash
# If no CLAUDE.md - create one (see above)

# If no pre-commit - add it
pre-commit install

# If no beads - initialize
bd init
```

### Step 2.3: Read Project Context

```bash
# Let Claude read the project
cat CLAUDE.md

# Or use Serena for deep understanding
# (Serena auto-activates on project open)
```

---

## 3. Feature Development Flow

### Step 3.1: Create Task

```bash
# Add to beads
bd add "Implement user authentication"
bd start <id>

# Or use /task command
/task add "Implement user authentication"
```

### Step 3.2: Plan the Feature

```
Option A: Use feature-dev skill
/feature-dev

Option B: Use plan mode
EnterPlanMode → Research → Create plan → Get approval
```

### Step 3.3: Develop with TDD

```
RED PHASE:
1. Write failing test first
2. Run tests - confirm failure
3. Commit: "test: add failing test for X"

GREEN PHASE:
1. Write minimal code to pass
2. Run tests - confirm passing
3. Commit: "feat: implement X"

REFACTOR PHASE:
1. Improve code quality
2. Run tests - confirm still passing
3. Commit: "refactor: clean up X"
```

### Step 3.4: Checkpoint Progress

```bash
# After significant progress
/checkpoint

# Or manually
bd note "Completed auth service, starting endpoints"
```

### Step 3.5: Review Before Commit

```bash
# Run code review
/code-review

# Or language-specific
/go-review
/ts-review
```

### Step 3.6: Commit and Push

```bash
# Use commit command
/commit

# Or manual with conventional format
git add -A
git commit -m "feat: implement user authentication"
git push
```

---

## 4. Code Review Process

### Reviewer Workflow

```bash
# Review PR
/code-review <PR-number>

# Check Greptile comments
# (if Greptile integration enabled)
```

### Author Response

```bash
# Address each comment
# Re-run review after fixes
/code-review

# Update PR
git add -A
git commit -m "fix: address review feedback"
git push
```

---

## 5. Hotfix Flow

```bash
# Create hotfix branch
git checkout -b hotfix/critical-bug

# Fix with TDD
# 1. Write test that exposes bug
# 2. Fix the bug
# 3. Verify test passes

# Commit
git commit -m "fix: resolve critical auth bypass"

# Fast-track review + merge
/code-review
git push
# Create PR → merge to main
```

---

## 6. Release Flow

```bash
# Ensure main is clean
git checkout main
git pull

# All tests pass
pre-commit run --all-files

# Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push --tags

# Deploy (project-specific)
```

---

## Enforcement Mechanisms

### Automatic (Hooks)

| Hook | Stage | What it enforces |
|------|-------|------------------|
| Ruff/Biome/golangci-lint | pre-commit | Code style |
| mypy/tsc | pre-commit | Type safety |
| Bandit | pre-commit | Python security |
| Gitleaks | pre-commit | No secrets |
| Conventional commits | commit-msg | Commit format |
| Tests | pre-push | All tests pass |
| Semgrep | CI | Security scan |

### Manual Checkpoints

| When | What to check |
|------|---------------|
| Before feature start | Task created in beads? |
| Before coding | Plan approved? |
| Before commit | Tests passing? Review done? |
| Before merge | CI green? PR approved? |

### Session Reminders

- SessionStart hook injects beads context
- TDD enforcer validates Red-Green-Refactor
- Context engineering skill guides context usage

---

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `/task add "..."` | Create beads task |
| `/task start <id>` | Start working on task |
| `/task done` | Complete current task |
| `/checkpoint` | Save session progress |
| `/commit` | Create conventional commit |
| `/code-review` | Review current changes |
| `/tdd "feature"` | Start TDD workflow |
| `/feature-dev` | Plan feature development |
| `/go-init` | Initialize Go project |
| `/ts-init` | Initialize TypeScript project |

---

## Troubleshooting

### Pre-commit failing?

```bash
# See what's failing
pre-commit run --all-files

# Skip temporarily (emergencies only!)
git commit --no-verify -m "..."
```

### Tests failing?

```bash
# Run specific test
pytest tests/test_auth.py -v

# With debugger
pytest --pdb
```

### Context overflow?

```bash
# Create checkpoint
/checkpoint

# Then ask Claude to summarize and continue
```

### Lost progress?

```bash
# Check Serena memories
ls .serena/memories/checkpoint-*

# Read latest
cat .serena/memories/checkpoint-latest.md
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| Skip tests | Bugs in prod | Always TDD |
| No task tracking | Lost context | Use beads |
| Giant commits | Hard to review | Small, focused |
| Skip review | Miss issues | Always review |
| Force push to main | Lose history | Never |
| Secrets in code | Security breach | Use .env + gitleaks |
| No CLAUDE.md | Context loss | Always create |

---

## Related Skills

- **context-engineering** — Managing AI context
- **reliable-execution** — Session persistence
- **beads-workflow** — Task tracking
- **tdd-workflow** — TDD patterns
