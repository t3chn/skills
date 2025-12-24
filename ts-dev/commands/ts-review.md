---
description: Review TypeScript code for type safety, patterns, and best practices
allowed-tools: Bash(git:*), Bash(pnpm:*), Bash(biome:*), Read, Glob, Grep
argument-hint: [path] [types|tests|performance|security|all]
---

# Review TypeScript Code

## Context

- Current directory: !`pwd`
- Git status: !`git status --short 2>/dev/null | head -10 || echo "Not a git repo"`
- Changed files: !`git diff --name-only 2>/dev/null | head -15 || echo "No changes"`
- TypeScript config: !`test -f tsconfig.json && echo "tsconfig.json found" || echo "No tsconfig.json"`
- Biome config: !`test -f biome.json && echo "biome.json found" || echo "No biome.json"`

## Task

Review TypeScript code with focus on:
- **Path:** $1 (default: current unstaged changes from `git diff`)
- **Focus area:** $2 (default: all)

### Focus Areas
- `types` — Type safety, strict mode compliance, type guards
- `tests` — Test coverage, testing patterns, mocking
- `performance` — Bundle size, memory, async patterns
- `security` — XSS, injection, secrets, validation
- `all` — Comprehensive review of all areas

## Requirements

1. **Gather information**
   ```bash
   git diff --name-only              # Files changed
   git diff HEAD                     # Actual changes
   cat tsconfig.json | head -30      # TypeScript settings
   ```

2. **Check project rules**
   - Look for CLAUDE.md in project root
   - Review tsconfig.json strict settings
   - Check biome.json rules

3. **Review for:**
   - Type safety violations (`any`, assertions, non-null)
   - Modern TypeScript patterns
   - Error handling
   - Async code issues
   - Security vulnerabilities
   - Performance problems

4. **Confidence scoring**
   - Only report issues with confidence >= 80
   - Avoid false positives from linters
   - Skip pre-existing issues

## Output Format

```
## TypeScript Code Review: [scope]

### [CRITICAL|WARNING] file.ts:line — Issue
**Confidence:** X/100
**Category:** [Type Safety|Security|Bug|Performance]

**Issue:** Description
**Fix:** Code suggestion
```

## Summary

Provide:
- Overall score (1-10)
- Critical issues count
- Positive patterns found
- Prioritized recommendations

Use the `ts-code-reviewer` agent for comprehensive review.
