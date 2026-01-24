# Config files and precedence

## When to add config support

- Add config files when the tool has many options or is used repeatedly in the same environment.
- Avoid config files when the CLI is intentionally “one-shot” and simple.

## Recommended precedence (predictable)

1. Built-in defaults
2. Config file (optional)
3. Environment variables (optional)
4. CLI flags (highest precedence)

Document the precedence and keep it stable.

## Config file discovery

- Prefer explicit `--config /path/to/config.toml` for deterministic behavior.
- If you support auto-discovery, pick one well-defined location (and document it):
  - OS-specific config directories via the `directories` crate
  - Or a project-local config file for repo tools (e.g., `tool.toml`)

## Formats and parsing

- Prefer TOML or YAML for human-authored config.
- Parse with `serde` and a typed config struct.
- Validate after merge (some rules depend on multiple fields).

## Merging sources

- Use `figment` or `config` when you need layered config merging and env overrides.
- Keep conversion logic in one place (e.g., `Config` -> `RunPlan`).

## Security notes

- Avoid storing secrets in plain config files unless the tool is explicitly designed for it.
- If secrets are required, prefer environment variables or secret managers and avoid logging them.

