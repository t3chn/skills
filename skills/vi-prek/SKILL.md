---
name: vi-prek
description: "Set up and configure prek (Rust drop-in replacement for pre-commit) in repositories: create/update `.pre-commit-config.yaml`, install/uninstall git hooks (`uvx prek install` / `uvx prek uninstall`), migrate from `pre-commit`, and add minimal CI (e.g., GitHub Actions). Use when a project needs pre-commit-style hooks wired up via prek."
---

# Prek Setup

Set up prek in a repo with minimal, reviewable changes.

## Workflow

### 1) Identify the scenario

- **Migration**: repo already has `.pre-commit-config.yaml` / `.pre-commit-config.yml`.
- **New setup**: no pre-commit config yet.

### 2) Ensure prek is available

Always run prek via `uvx` (so commands look like `uvx prek ...`).

Verify with `uvx prek --version`. If `uvx` is missing, install `uv` first.

### 3) Create or keep the config

Prefer `.pre-commit-config.yaml` at the repo root.

If migrating, keep the existing config unchanged unless the user asks to modify hooks.

Optional generator: `uvx prek sample-config -f .pre-commit-config.yaml`.

### 4) Run hooks and wire into git

- Run locally: `uvx prek run` (staged files) or `uvx prek run --all-files`.
- Install git hook: `uvx prek install`.
- Migration from `pre-commit`: run `uvx prek install -f` once to overwrite the existing hook.
- Undo: `uvx prek uninstall`.

### 5) Add minimal CI (GitHub Actions)

If the repo uses GitHub Actions, add a minimal workflow (see `references/ci.md`).

### 6) Monorepos (only if relevant)

Use workspace mode (see `references/workspace.md`).

### 7) Sanity checks

- Validate config(s): `uvx prek validate-config`.
- Keep diffs minimal and explicit; do not add extra hooks unless requested.

## References (load only if needed)

- `references/quickstart.md` — Migration vs new setup checklist
- `references/installation.md` — Install/update/completions
- `references/configuration.md` — Config patterns + prek-only keys
- `references/cli.md` — Commands, flags, selectors
- `references/workspace.md` — Monorepos + workspace discovery
- `references/ci.md` — GitHub Actions + Docker usage
- `references/languages.md` — `language` / `language_version` / toolchains
- `references/builtin.md` — `repo: builtin` and fast path
- `references/debugging.md` — Verbose mode + log file
- `references/faq.md` — `prek install --install-hooks` explanation

## Skill maintenance

- Validate this skill locally: `uvx --from pyyaml python /Users/vi/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/vi-prek`
