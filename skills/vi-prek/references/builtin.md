# Built-in fast hooks

Use this when a user wants offline/zero-setup hooks or asks about prek’s “fast path”.

## Automatic fast path (no config changes)

If your config uses:

```yaml
repo: https://github.com/pre-commit/pre-commit-hooks
```

prek may run Rust-native implementations for some hook ids for speed.

- Detection is based on the repo URL; `rev` is ignored for fast-path detection.
- prek may still clone the repo / set up envs for compatibility, even if execution uses the fast path.

Disable fast path (for debugging / parity checks):

```bash
PREK_NO_FAST_PATH=1 uvx prek run
```

## Explicit offline mode (`repo: builtin`)

Use `repo: builtin` to avoid network and avoid env setup.

```yaml
repos:
  - repo: builtin
    hooks:
      - id: trailing-whitespace
      - id: check-yaml
```

Notes:

- Not compatible with upstream `pre-commit`.
- `entry` is not allowed; `language` (if set) must be `system`.
- Configure with `args: [...]`, `files`, `exclude`, `stages`, etc.

## Common built-in hook ids

These ids are commonly available as built-ins (also often accelerated via fast path):

- `trailing-whitespace`
- `end-of-file-fixer`
- `check-added-large-files`
- `check-yaml`
- `check-json` / `check-json5`
- `check-toml`
- `check-xml`
- `check-merge-conflict`
- `detect-private-key`
- `mixed-line-ending`
