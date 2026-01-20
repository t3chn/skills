# CLI Reference (Common Tasks)

Use this when a user asks “what command/flag should I run?”.

## `prek run`

Run hooks (defaults to staged files for `pre-commit` stage).

Common forms:

```bash
uvx prek run
uvx prek run --all-files
uvx prek run --files path/a path/b
uvx prek run --directory src --directory docs
uvx prek run --last-commit
uvx prek run --from-ref origin/main --to-ref HEAD
```

Quality-of-life flags:

- Show diffs after failures: `--show-diff-on-failure`
- Stop after first failure: `--fail-fast`
- Pick config file (disables workspace discovery): `-c/--config path`
- Change working dir first: `-C/--cd dir`
- Select/skip hooks or projects: `[HOOK|PROJECT]...` and `--skip ...`
- Choose stage: `--stage/--hook-stage <stage>`

Selectors (`HOOK|PROJECT` and `--skip`):

- `<hook-id>`: match hook id across all projects
- `<project-path>/`: match a project (note trailing `/` matters)
- `<project-path>:<hook-id>`: match one hook in one project

Environment variables:

- `PREK_SKIP` or `SKIP`: comma-delimited list, same syntax as `--skip`

## `prek install` / `prek uninstall`

Wire prek into git hooks.

```bash
uvx prek install
uvx prek install -f            # overwrite existing hook (migration)
uvx prek uninstall
```

Options to know:

- Install specific git hook stage(s): `--hook-type <type>` (repeatable)
- Prep hook envs immediately: `--install-hooks`
- Choose config: `-c/--config path`
- Change working dir: `-C/--cd dir`

## `prek install-hooks`

Prepare hook environments without installing the git hook shim:

```bash
uvx prek install-hooks
```

## `prek validate-config`

Validate one or more config files:

```bash
uvx prek validate-config
uvx prek validate-config path/to/.pre-commit-config.yaml
```

## `prek list`

List configured hooks (useful to discover ids):

```bash
uvx prek list
```

## `prek sample-config`

Generate a starter config (optionally write to a file):

```bash
uvx prek sample-config
uvx prek sample-config -f .pre-commit-config.yaml
```

## `prek auto-update`

Update `rev:` pins in config(s):

```bash
uvx prek auto-update
uvx prek auto-update --dry-run
```

## `prek cache`

Manage caches (repos, envs, toolchains):

```bash
uvx prek cache dir
uvx prek cache gc
uvx prek cache clean
```

## Debug flags (any command)

- More verbosity: `-v`, `-vv`, `-vvv`
- Trace log output file: `--log-file path`
