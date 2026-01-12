---
name: vi-code-simplifier
description: "Simplify and refine code for clarity, consistency, and maintainability while preserving exact functionality. Use when the user asks to refactor/clean up/simplify code, or after implementing changes to improve readability without changing behavior."
---

# Code Simplifier (No-Behavior-Change Refactors)

Refine code for clarity, consistency, and maintainability while preserving exact functionality. Prefer readable, explicit code over overly compact solutions.

## Core Rules

1. **Preserve functionality**
   - Never change what the code does — only how it is expressed.
   - Keep outputs, side effects, and edge-case behavior intact.

2. **Follow project standards**
   - Read and apply any relevant `AGENTS.md` / `CLAUDE.md` instructions for the files you touch.
   - Preserve existing conventions (imports, naming, error handling, layering, framework patterns).

3. **Enhance clarity**
   - Reduce unnecessary complexity and nesting.
   - Eliminate redundancy and needless abstractions.
   - Improve naming (clear variables/functions) where it increases readability.
   - Consolidate related logic when it improves comprehension.
   - Avoid nested ternary operators; prefer `if/else` chains or `switch` for multi-branch logic.
   - Choose clarity over brevity (avoid dense one-liners and “clever” tricks).

4. **Avoid over-simplification**
   - Don’t merge unrelated concerns into one function/module.
   - Don’t remove helpful abstractions that make the code easier to navigate.
   - Don’t optimize for fewer lines at the expense of readability/debuggability.

5. **Keep scope tight**
   - Default to refining only the code that was recently modified or is directly adjacent to the change.
   - Expand scope only if the user explicitly asks, or if a larger refactor is required to maintain consistency.

## Process

1. Identify the scope (recently changed code / files touched).
2. Scan for simplification opportunities (nesting, duplication, naming, structure).
3. Apply refactors incrementally (small, safe steps).
4. Validate behavior:
   - Prefer running the narrowest relevant tests/commands if available.
   - If you can’t run tests, be conservative and explain assumptions.
5. Summarize only meaningful changes (what improved and why).

