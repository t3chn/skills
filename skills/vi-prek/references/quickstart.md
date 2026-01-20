# Quickstart (Project Setup)

Use this when a repo is adopting prek (new) or migrating from `pre-commit`.

## Migration from `pre-commit`

1. Keep existing `.pre-commit-config.yaml` / `.pre-commit-config.yml` unchanged.
2. Replace `pre-commit` commands in docs/scripts with `prek`.
3. Overwrite the git hook shim once:

```bash
uvx prek install -f
```

4. Verify:

```bash
uvx prek run --all-files
```

## New setup (no config yet)

1. Create `.pre-commit-config.yaml` at the repo root.
2. Start minimal and expand only if asked.

Example:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
```

3. Run once locally:

```bash
uvx prek run --all-files
```

4. Install the git hook:

```bash
uvx prek install
```

5. Undo hook wiring if needed:

```bash
uvx prek uninstall
```

## Common usage patterns

- Run on staged files: `uvx prek run`
- Run on all files: `uvx prek run --all-files`
- Run one hook everywhere: `uvx prek run <hook-id>`
- Run on specific files: `uvx prek run --files path/a path/b`
- Validate configs: `uvx prek validate-config`
