# Workspace mode (Monorepos)

Use this when a repo has multiple `.pre-commit-config.yaml` files (monorepo / nested projects).

## What it is

- Workspace root: the first `.pre-commit-config.yaml` found while walking upward from your current directory.
- Projects: every directory containing a `.pre-commit-config.yaml` under the workspace root (can be nested).

## Discovery rules (default behavior)

When you run without `--config`:

1. Find workspace root by walking upward from CWD until a config file is found.
2. From that root, recursively discover nested configs in subdirectories.
3. Stop at the git repo boundary (`.git`).

Discovery also:

- Respects `.gitignore` (including `.git/info/exclude` and global gitignore).
- Supports `.prekignore` (gitignore syntax) to exclude additional paths from discovery.
- Ignores dot-directories (like `.venv`) and cookiecutter template dirs.

If you pass `-c/--config`, workspace discovery is disabled and only that config is used.

## Execution model (important constraints)

- Each project only sees files under its own directory tree.
- Projects run deepest-to-shallowest (more specific configs first).
- By default, files in subprojects can be processed multiple times (by the subproject and its parents).

### `orphan: true`

Set `orphan: true` in a nested project to “consume” files in that subtree so parent configs don’t also process them.

Gotcha: in workspace mode, an orphan project still claims its files even if you skip it via selectors; files do not fall back to parent projects.

## Targeting hooks/projects (selectors)

Selectors work for `prek run`, `prek install`, `prek install-hooks`, and `--skip`:

- `<hook-id>`: match hook id across all projects
- `<project-path>/`: match a project (trailing `/` matters)
- `<project-path>:<hook-id>`: match one hook in one project

Examples:

```bash
uvx prek run black
uvx prek run frontend/
uvx prek run frontend:lint src/backend:black
uvx prek run --skip frontend/ --all-files
```

`<project-path>` is resolved relative to the current working directory. Use `-C/--cd <dir>` to change CWD for discovery/selector resolution.

## Installing hooks in a workspace

When using `prek install` in workspace mode, only the workspace root config’s `default_install_hook_types` is honored.
