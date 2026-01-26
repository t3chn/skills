---
name: vi-zitadel-admin
description: "Reliable self-hosted ZITADEL administration and day-2 operations with configuration-only changes: initial setup (`zitadel init/setup/start`), hardening (TLS, HTTP/2, masterkey, SMTP), upgrades/scaling, backups, observability, and common troubleshooting. Use when working with ZITADEL deployment config (Helm, Docker Compose, Linux service), ZITADEL config/steps YAML, or diagnosing self-hosted ZITADEL runtime issues."
---

# Vi Zitadel Admin

Administer ZITADEL (self-hosted) via configuration and operational workflows. Avoid patching ZITADEL source unless explicitly requested.

## Quick intake (ask first)

- Deployment: Kubernetes (Helm), Docker Compose, or Linux/service
- Version/DB: ZITADEL major version (v2 vs v3), Postgres vs CockroachDB (v2 only)
- External access: `ExternalDomain`, TLS termination (`--tlsMode`), reverse proxy/WAF/CDN, HTTP/2/h2c
- Config delivery: where `--config` and `--steps` files live; how `--masterkey*` is provided

## Source of truth (local)

Prefer using the checked-out ZITADEL repo as the authoritative config catalog:

- Runtime defaults + env var mapping: `~/contrib/zitadel/cmd/defaults.yaml`
- Setup steps defaults + env var mapping: `~/contrib/zitadel/cmd/setup/steps.yaml`
- Self-hosting docs (offline): `~/contrib/zitadel/docs/docs/self-hosting/manage/`

If the repo isn’t available, fall back to https://zitadel.com/docs and the upstream GitHub paths referenced above.

## Recommended workflow

1) Locate current runtime config (`--config`) and setup steps (`--steps`).
2) Compare against the production checklist and close gaps (TLS/HTTP/2, non-default credentials, SMTP, backups, observability).
3) Apply changes as configuration-only:
   - Use multiple `--config` / `--steps` files to separate public config from secrets.
   - Keep secrets out of git (masterkey, DB creds, SMTP creds, TLS private key).
4) For installs/upgrades, follow the phase separation:
   - First install: `zitadel init` (once) → `zitadel setup` → `zitadel start`
   - Upgrade: run `zitadel setup` with the new version, then roll out `zitadel start`
5) Verify with health endpoints and logs:
   - Ready: `/debug/ready`
   - Health: `/debug/healthz`
   - Metrics: `/debug/metrics`

## Common tasks (short recipes)

- **Find config keys**: search `~/contrib/zitadel/cmd/defaults.yaml` and `~/contrib/zitadel/cmd/setup/steps.yaml` (look for `# ZITADEL_...` comments).
- **Fix “Instance not found”**: validate `ExternalDomain/Port/Secure`, reverse proxy host headers, then rerun `zitadel setup`.
- **Prepare for production**: follow `references/production-hardening.md` and cross-check upstream `productionchecklist.md`.
- **Plan upgrades and scaling**: use `references/upgrade-scaling.md` (init/setup/start separation, probes, zero downtime).
- **Validate database posture**: use `references/database.md` (supported versions, credential rotation, v2→v3 CRDB migration notes).
- **Verify HTTP/2 + TLS**: use `references/networking-http2-tls.md`.

## Resources

- Config discovery and file layout: `references/config-discovery.md`
- Production hardening checklist: `references/production-hardening.md`
- Init/setup/start + upgrades + scaling: `references/upgrade-scaling.md`
- Database operations and credential rotation: `references/database.md`
- HTTP/2, h2c, TLS modes, reverse proxies: `references/networking-http2-tls.md`
- Observability: readiness/liveness/metrics/logging: `references/observability.md`
- Optional migration (v2 CockroachDB → Postgres): `references/migration-crdb-to-pg.md`
