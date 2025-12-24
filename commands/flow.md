---
name: flow
description: Show production flow quick reference
---

# Production Flow Quick Reference

Show the user a compact production flow cheatsheet based on what they're trying to do.

## If no arguments, show the overview:

```
PRODUCTION FLOW
===============

1. INIT (new project)
   └─ pre-commit + beads + CLAUDE.md + first commit

2. INIT (existing)
   └─ Clone → check CLAUDE.md → bd init → read context

3. FEATURE
   └─ bd add → /feature-dev → TDD → /code-review → /commit

4. HOTFIX
   └─ branch → TDD fix → /code-review → merge

5. RELEASE
   └─ main clean → tests pass → tag → deploy

Commands:
  /task add "..."   - Create task
  /task done        - Complete task
  /checkpoint       - Save progress
  /commit           - Conventional commit
  /code-review      - Review changes
  /tdd "..."        - Start TDD
  /feature-dev      - Plan feature

Enforcement:
  pre-commit    - Style, types, security
  commit-msg    - Conventional format
  pre-push      - All tests pass
  TDD enforcer  - Red→Green→Refactor
```

## If argument is "new":

Show detailed new project setup steps.

## If argument is "feature":

Show detailed feature development flow.

## If argument is "tdd":

Show TDD Red-Green-Refactor cycle.

Always be concise. This is a quick reference, not documentation.
