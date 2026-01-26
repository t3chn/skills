# Database operations (Postgres vs CockroachDB)

Use this when configuring the database, rotating credentials, planning backups, or migrating between database vendors.

Upstream reference (recommended):

- Local: `~/contrib/zitadel/docs/docs/self-hosting/manage/database/`
- Online: https://zitadel.com/docs/self-hosting/manage/database

## Pick the right database for your ZITADEL version

- **ZITADEL v3**: Postgres only (CockroachDB support removed).
- **ZITADEL v2**: Postgres or CockroachDB (depending on your deployment and version).

Confirm by checking the runtime defaults in `~/contrib/zitadel/cmd/defaults.yaml` for your exact version.

## Postgres (recommended)

Supported versions (per upstream docs): 14 to 17.

Key config area: `Database.postgres.*` in `~/contrib/zitadel/cmd/defaults.yaml`.

If you want to avoid storing admin DB credentials in ZITADEL config, pre-provision DB + user:

```sql
CREATE ROLE zitadel LOGIN;
CREATE DATABASE zitadel;
GRANT CONNECT, CREATE ON DATABASE zitadel TO zitadel;
```

Then ensure authentication/permissions are correct (for example `pg_hba.conf`) and run `zitadel setup` using only the unprivileged ZITADEL user.

## Credential rotation (important behavior)

`zitadel init` creates the database/user if missing, but it does not rotate passwords or migrate object ownership.

- Rotating the password for the existing ZITADEL DB user is the simplest path; update all places where the password is supplied.
- Switching to a new DB user requires manual reassignment of ownership and privileges for all objects ZITADEL needs (schemas, tables, sequences).

Do not rely on rerunning `init` to "fix" permissions after changing users.

## Backups and restore tests

ZITADEL is event-sourced; the database is the source of truth.

- Back up the database using your DB vendor's recommended approach (base backups + WAL, snapshots, managed backups).
- Regularly test restores to a staging environment.
- After restore/cutover, ensure the deployed ZITADEL version runs `setup` before serving traffic.

## Migrating CockroachDB -> Postgres (v2 to v3 path)

Use the ZITADEL `mirror` command to copy data between databases.

See `references/migration-crdb-to-pg.md` and the upstream mirror guide:

- Local: `~/contrib/zitadel/docs/docs/self-hosting/manage/cli/mirror.mdx`
- Online: https://zitadel.com/docs/self-hosting/manage/cli/mirror
