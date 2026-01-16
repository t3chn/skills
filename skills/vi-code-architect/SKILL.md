---
name: vi-code-architect
description: "Design a concrete architecture and implementation blueprint for a new feature that fits an existing codebase (files to change, components, data flow, error handling, tests). Use after codebase exploration when you need a decisive plan to implement."
---

# Code Architect (Implementation Blueprint)

Design a complete, actionable architecture blueprint by first understanding the existing codebase and then making confident decisions that integrate cleanly with current patterns.

## Workflow

1. **Analyze codebase patterns**
   - Identify the stack, module boundaries, layering, error-handling patterns, and testing strategy.
   - Read any repo guidance (`AGENTS.md`, `CONTRIBUTING.md`, etc.) that applies to the files you will touch.
   - Find and study similar features to reuse established approaches.

2. **Make an architecture decision**
   - Pick an approach and commit to it (don’t present endless options).
   - Call out key trade-offs and why this approach fits the repo and the specific task.

3. **Deliver the blueprint**
   - Specify exactly what to create/modify and how it fits together.

## Output checklist

Include:

- **Patterns & conventions found**: key findings with file paths (and line numbers when available).
- **Architecture decision**: chosen approach + rationale + explicit trade-offs.
- **Component design**: components/modules with responsibilities, dependencies, and interfaces.
- **Implementation map**: specific files to create/modify with what changes go where.
- **Data flow**: end-to-end flow from entry points through transformations to outputs.
- **Build sequence**: phased checklist to implement safely in order.
- **Critical details**: error handling, state management, security, performance, testing, and rollout/migration notes (as relevant).

Be specific and actionable (paths, symbols, and concrete steps), not generic guidance.
