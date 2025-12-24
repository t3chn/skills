---
description: Review TypeScript code using official code-reviewer with TS conventions
allowed-tools: Task, Glob, Grep, Read
argument-hint: [path] [focus:all|types|tests|security]
---

# TypeScript Code Review

Review TypeScript code at `$1` (default: current changes) with focus on `$2` (default: all).

## Context

- Changed TS files: !`git diff --name-only HEAD 2>/dev/null | grep -E '\.(ts|tsx)$' | head -10 || echo "no changes"`
- tsconfig.json: !`test -f tsconfig.json && echo "found" || echo "not found"`

## Task

Use the `feature-dev:code-reviewer` agent to review TypeScript code.

The `ts-conventions` skill provides TypeScript-specific context:
- Type safety (no `any`, use `unknown`, type guards)
- Error handling (Result pattern, custom error classes)
- Async patterns (no floating promises, Promise.all)
- Zod validation at boundaries
- Modern patterns (discriminated unions, branded types)

### Focus Areas

| Focus | What to Check |
|-------|---------------|
| `all` | Complete review |
| `types` | Type safety, strict mode, generics |
| `tests` | Vitest patterns, mocking, coverage |
| `security` | XSS, injection, secrets, validation |

### Output Format

Report issues with:
- File:line references
- Confidence score (only report ≥80)
- Specific fix suggestions
