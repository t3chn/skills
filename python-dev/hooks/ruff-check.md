---
name: ruff-lint-check
event: PreToolUse
tools:
  - Write
  - Edit
match_files: "*.py"
---

# Ruff Lint Check Hook

Reminds to run ruff after modifying Python files.

## Instruction

When modifying Python files, remind the user to run linting:

```
After editing Python files, run:
  uv run ruff check --fix .
  uv run ruff format .
```

This ensures code style consistency and catches common issues before commit.
