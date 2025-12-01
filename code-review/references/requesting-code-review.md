# Requesting Code Review

> **Core principle:** Review early, review often.

## When to Request

**Mandatory:**
- After each task in subagent-driven development
- After major feature completion
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code-reviewer subagent via Task tool:**

Provide:
- `WHAT_WAS_IMPLEMENTED` - What you just built
- `PLAN_OR_REQUIREMENTS` - What it should do
- `BASE_SHA` - Starting commit
- `HEAD_SHA` - Ending commit
- `DESCRIPTION` - Brief summary

**3. Act on feedback:**
- **Critical** - Fix immediately
- **Important** - Fix before proceeding
- **Minor** - Note for later
- **Wrong** - Push back with reasoning

## Example

```
[Completed Task 2: Add verification function]

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code-reviewer subagent]
  WHAT: Verification and repair functions for conversation index
  PLAN: Task 2 from docs/plans/deployment-plan.md
  BASE: a7981ec
  HEAD: 3df7661
  DESC: Added verifyIndex() and repairIndex()

[Subagent returns]:
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100)
  Assessment: Ready to proceed

[Fix progress indicators]
[Continue to Task 3]
```

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
