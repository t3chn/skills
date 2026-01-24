---
name: vi-rust-cli-dev
description: "Build and refactor Rust command-line tools: Cargo scaffolding, `clap` argument parsing, stdin/stdout IO, error handling and exit codes, logging/config, integration tests (`assert_cmd`), and packaging/distribution. Use when requests mention Rust CLI apps, `clap`, `assert_cmd`, shell completions, man pages, `cargo install`, or releasing Rust binaries."
---

# Vi Rust Cli Dev

## Overview

Build production-quality Rust CLIs with strong UX, composability, and testability.

## Default approach (adjust to context)

- Define a clear CLI contract (inputs, outputs, exit codes).
- Keep core logic in `src/lib.rs` and CLI wiring in `src/main.rs`.
- Use `clap` derive for args + subcommands.
- Use `anyhow` for app-level error wiring; use `thiserror` for typed library errors.
- Keep stdout for primary output; use stderr for diagnostics/logs/progress.
- Add integration tests with `assert_cmd` (+ `predicates`) and fixtures.

## Workflow

1) Clarify the CLI contract
   - Define subcommands/flags, defaults, and validation rules.
   - Decide input sources (files, stdin, network) and output formats (human vs machine).
   - Define stable exit codes and what goes to stdout vs stderr.

2) Scaffold for testability
   - Split logic from IO: keep parsing/formatting and domain logic in library code.
   - Pass `Read`/`Write`/`BufRead` into core functions instead of touching globals.

3) Implement the CLI surface
   - Model args as structs/enums; prefer subcommands to mode flags when it improves clarity.
   - Validate at parse time where possible (ranges, enums, file paths).

4) Implement IO and output
   - Stream input; avoid reading unbounded data into memory.
   - Print primary output to stdout; print errors/logs/progress to stderr.
   - Provide `--json`/`--quiet`/`--no-color` style controls when relevant.

5) Handle errors and exit codes
   - Use `?` and attach context to failures; avoid panics for user-facing errors.
   - Map domain errors to stable exit codes (document them).

6) Test and iterate
   - Unit-test core logic and formatting.
   - Integration-test the compiled binary (fixtures, temp dirs, golden output).

7) Package and ship
   - Ensure `cargo install` works; optionally publish to crates.io.
   - For binaries, build release artifacts and include completions/man pages if needed.

## References (load as needed)

- Decision-making checklist: `references/cli-design.md`
- Project structure patterns: `references/project-structure.md`
- `clap` recipes (derive, subcommands, completions, man pages): `references/clap.md`
- IO + output conventions (stdout vs stderr, JSON, progress): `references/io-output.md`
- Error handling + exit codes: `references/errors-exitcodes.md`
- Config files and precedence: `references/config-files.md`
- Testing patterns (unit + integration): `references/testing.md`
- Tooling and quality gates: `references/tooling.md`
- Packaging and release options: `references/packaging-release.md`
- Crate index by concern: `references/crates.md`
- Upstream reading map: `references/upstream-reading.md`

## Guardrails

- Do not break existing flags or output formats without a migration plan.
- Keep stdout stable for scripts; send diagnostics to stderr.
- Prefer small, composable subcommands over one giant mode switch.
