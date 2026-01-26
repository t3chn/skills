# Config discovery (runtime vs setup)

Use this when you need to find the right configuration key, decide whether it belongs to runtime config (`--config`) or setup steps (`--steps`), and apply changes without touching ZITADEL source code.

## Source of truth

Prefer these files from the ZITADEL repo you are operating against:

- Runtime defaults: `~/contrib/zitadel/cmd/defaults.yaml`
- Setup steps defaults: `~/contrib/zitadel/cmd/setup/steps.yaml`

Both files also show the corresponding environment variable names in `# ZITADEL_...` comments.

If you do not have the repo locally, use the upstream equivalents:

- https://github.com/zitadel/zitadel/blob/main/cmd/defaults.yaml
- https://github.com/zitadel/zitadel/blob/main/cmd/setup/steps.yaml

## Fast search recipes

- List all runtime env vars: `rg -n \"#\\s*ZITADEL_[A-Z0-9_]+\" ~/contrib/zitadel/cmd/defaults.yaml`
- List all setup-step env vars: `rg -n \"#\\s*ZITADEL_[A-Z0-9_]+\" ~/contrib/zitadel/cmd/setup/steps.yaml`
- Jump to external access keys: `rg -n \"^External(Domain|Port|Secure):\" ~/contrib/zitadel/cmd/defaults.yaml`
- Jump to database keys: `rg -n \"^Database:\" ~/contrib/zitadel/cmd/defaults.yaml`
- Jump to first admin user defaults: `rg -n \"^FirstInstance:\" ~/contrib/zitadel/cmd/setup/steps.yaml`

## Runtime vs steps: what goes where

- **Runtime config (`--config`)**: networking (`ExternalDomain/...`), TLS, database connection (ZITADEL DB user), logging/metrics/tracing, quotas/limits defaults, etc.
- **Setup steps (`--steps`)**: first-instance bootstrap (initial org/admin, machine users, PAT outputs), data initialization steps and migrations.

Rule of thumb: if it affects "how the server runs", it is runtime; if it affects "what to create during bootstrap/migrations", it is steps.

## Config layering (recommended)

ZITADEL merges multiple `--config` and `--steps` files. Use this to keep secrets out of git.

- Put public, non-secret values in `config.public.yaml`
- Put secrets in `config.secrets.yaml` from a secret manager (mounted file) or generated at deploy time
- Pass both: `zitadel start --config config.public.yaml --config config.secrets.yaml ...`

Do the same for setup steps:

- `zitadel setup --steps steps.public.yaml --steps steps.secrets.yaml ...`

## Masterkey handling (critical)

The masterkey is the root secret used to encrypt other keys. It must be exactly 32 bytes.

Prefer one of:

- `--masterkeyFile /path/to/masterkey` (best for ops)
- `--masterkeyFromEnv` with `ZITADEL_MASTERKEY` (acceptable if your platform secures env vars)

Avoid committing or logging the masterkey. Treat it like a database encryption root key.

## Useful offline docs in the repo

If `~/contrib/zitadel` exists, the self-hosting docs include examples and explanations:

- `~/contrib/zitadel/docs/docs/self-hosting/manage/configure/`
- `~/contrib/zitadel/docs/docs/self-hosting/manage/updating_scaling.md`
- `~/contrib/zitadel/docs/docs/self-hosting/manage/productionchecklist.md`
