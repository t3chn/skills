# Init/setup/start, upgrades, and scaling

Use this when planning installs, upgrades, or horizontal scaling, and when diagnosing slow startups or failed migrations.

Upstream reference (recommended):

- Local: `~/contrib/zitadel/docs/docs/self-hosting/manage/updating_scaling.md`
- Online: https://zitadel.com/docs/self-hosting/manage/updating_scaling

## Phases

ZITADEL separates lifecycle phases:

- **Init**: `zitadel init` (run once per installation)
- **Setup**: `zitadel setup` (run once per deployed version; performs migrations/projections setup)
- **Runtime**: `zitadel start` (serves traffic; fastest startup)

For dev/prototyping you can combine phases with `zitadel start-from-init`, but production ops are simpler and safer when phases are separated.

## First install (recommended sequence)

1) Run `zitadel init` once (admin DB credentials required unless you pre-provisioned DB/user).
2) Run `zitadel setup` (uses the unprivileged ZITADEL DB user; performs migrations and instance bootstrap).
3) Run `zitadel start` as the long-running runtime.

## Upgrades (zero-downtime friendly)

1) Deploy the new binary/image.
2) Run exactly one `zitadel setup` job for the new version (migrations).
3) Roll out `zitadel start` runtimes (multiple replicas are fine).
4) Gate traffic on readiness: `/debug/ready`.

Avoid running multiple setup jobs in parallel for the same database.

## When you must rerun setup

- After upgrading to a new ZITADEL version.
- After changing external access settings: `ExternalDomain`, `ExternalPort`, `ExternalSecure`.

## Scaling

- The runtime is stateless; shared state lives in the database.
- Scale horizontally by increasing `zitadel start` replicas.
- Ensure the database is provisioned and tuned for the target request rate (connections, CPU, memory, IO).
- If you use an autoscaler (scale-to-zero), keep startup times low by separating init/setup from runtime.

## Probes and endpoints

- **Readiness**: `GET /debug/ready` (traffic gate; also indicates migrations in progress)
- **Liveness**: `GET /debug/healthz` (process health)
- **Metrics**: `GET /debug/metrics`

Use these for Kubernetes `readinessProbe` and `livenessProbe`.
