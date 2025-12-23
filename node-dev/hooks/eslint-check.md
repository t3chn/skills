---
name: eslint-lint-check
event: PreToolUse
tools:
  - Write
  - Edit
match_files: "*.ts"
---

# ESLint Check Hook

Reminds to run ESLint after modifying TypeScript files.

## Instruction

When modifying TypeScript files, remind the user to run linting:

```
After editing TypeScript files, run:
  pnpm eslint . --fix
  pnpm tsc --noEmit
```

This ensures code style consistency and type safety before commit.
