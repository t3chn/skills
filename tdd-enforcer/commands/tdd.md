---
name: tdd
description: Start a TDD (Test-Driven Development) workflow for implementing a feature
arguments:
  - name: feature
    description: The feature or behavior to implement using TDD
    required: true
---

# TDD Workflow: $ARGUMENTS.feature

You are guiding the user through Test-Driven Development for: **$ARGUMENTS.feature**

## Current Phase: RED (Write Failing Test)

Follow the strict Red-Green-Refactor cycle:

### Step 1: Understand the Requirement

First, clarify what **$ARGUMENTS.feature** should do:
- What is the expected input?
- What is the expected output?
- What are the error cases?
- What edge cases exist?

### Step 2: Create/Identify Test File

Based on the project structure, determine where the test should go:
- **Go:** `*_test.go` in the same package
- **TypeScript:** `*.test.ts` alongside the source
- **Python:** `test_*.py` in tests/ or same directory
- **Rust:** `#[cfg(test)]` module in the source file

### Step 3: Write ONE Failing Test

Write a minimal test that:
1. Describes the expected behavior in its name
2. Tests exactly ONE behavior
3. Will FAIL until implementation exists

### Step 4: Verify Test Fails

Run the test command:
- **Go:** `go test ./...`
- **TypeScript:** `npm test` or `pnpm vitest run`
- **Python:** `pytest`
- **Rust:** `cargo test`

Confirm it fails for the RIGHT reason (missing function, wrong return value — NOT syntax error).

---

## Use the tdd-coach agent

Invoke the **tdd-coach** agent to guide the full Red-Green-Refactor cycle interactively.

The agent will:
1. Help write the failing test (RED)
2. Guide minimal implementation (GREEN)
3. Suggest refactoring opportunities (REFACTOR)
4. Track progress with TodoWrite
5. Suggest appropriate commits at each phase

## Commit Convention

After each phase, commit with the appropriate prefix:
- `test: add test for <behavior>` — RED phase
- `feat: implement <behavior>` — GREEN phase
- `refactor: improve <aspect>` — REFACTOR phase
