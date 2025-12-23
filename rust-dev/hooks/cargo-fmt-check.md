---
name: cargo-fmt-check
event: PreToolUse
tools:
  - Write
  - Edit
match_files: "*.rs"
---

# Cargo Format Check Hook

Reminds to run cargo fmt and clippy after modifying Rust files.

## Instruction

When modifying Rust files, remind the user to run formatting and linting:

```
After editing Rust files, run:
  cargo fmt
  cargo clippy -- -D warnings
```

This ensures code style consistency and catches common issues before commit.
