# Configuration (`.pre-commit-config.yaml`)

Use this when editing or designing a `.pre-commit-config.yaml` / `.pre-commit-config.yml`.

## Basics

- Preferred filename: `.pre-commit-config.yaml` (also supports `.yml`).
- Format: YAML, mostly pre-commit compatible.
- In workspace mode, each config file scopes a “project” to its directory tree (see `workspace.md`).

## Repo entry types

- Remote repo (git URL): `repo: https://...`, `rev: ...`, `hooks: [...]`
- Local hooks: `repo: local` (hooks must define `name`, `entry`, `language`)
- Meta hooks: `repo: meta`
- Built-in hooks: `repo: builtin` (prek-only; not compatible with upstream `pre-commit`)

## Common patterns

### Minimal remote repo selection

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
```

### Local hook (repo: local)

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff
        name: ruff
        language: system
        entry: python3 -m ruff check
        files: '\\.py$'
```

### Built-in hooks (offline)

```yaml
repos:
  - repo: builtin
    hooks:
      - id: trailing-whitespace
      - id: check-yaml
```

Notes:

- For `repo: builtin`, `entry` is not allowed and `language` (if set) must be `system`.
- For details and “fast path” behavior, see `builtin.md`.

## Prek-only configuration keys (practical subset)

### `files` / `exclude` as globs

In addition to regex strings, prek supports glob mappings:

```yaml
files:
  glob:
    - src/**/*.py
    - tests/**/*.py
exclude:
  glob:
    - vendor/**
    - dist/**
```

### `minimum_prek_version` (top-level)

Require a minimum prek version:

```yaml
minimum_prek_version: '0.2.0'
```

### `orphan: true` (workspace mode)

Prevent parent projects from also processing files under this project directory:

```yaml
orphan: true
repos: []
```

See `workspace.md` for behavior and gotchas with selectors/skip.

### `env` (hook-level)

Add/override env vars for a hook process:

```yaml
repos:
  - repo: local
    hooks:
      - id: cargo-doc
        name: cargo doc
        language: system
        entry: cargo doc --workspace --no-deps
        pass_filenames: false
        env:
          RUSTDOCFLAGS: -Dwarnings
```

### `priority` (hook-level)

Control scheduling and parallelism (non-negative integer; lower runs earlier; same priority can run concurrently):

```yaml
repos:
  - repo: local
    hooks:
      - id: format
        name: Format
        language: system
        entry: python3 -m ruff format
        always_run: true
        priority: 0
      - id: lint
        name: Lint
        language: system
        entry: python3 -m ruff check
        always_run: true
        priority: 10
```

Avoid putting file-mutating hooks in the same `priority` group.
