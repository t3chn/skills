# Code Review

Use the official `code-review:/code-review` skill via Skill tool.

Or use the `feature-dev:code-reviewer` agent for comprehensive review.

**Usage:**
- Run after completing a feature or fix
- Review changes before committing
- Check for YAGNI, KISS, DRY violations
- Get objective feedback on code quality

**Language-specific context:**
The convention skills provide language-specific patterns for the code-reviewer:
- `go-conventions` — Go idioms, error handling, testing
- `ts-conventions` — TypeScript types, Zod validation, Vitest
- `rust-conventions` — Ownership, error handling, async
- `python-conventions` — Type hints, pytest, Pydantic
- `node-conventions` — ES modules, async patterns, logging
