# Production hardening checklist (condensed)

Use this as a day-2 checklist to close common reliability and security gaps in a self-hosted ZITADEL deployment.

Upstream reference (recommended to cross-check):

- Local: `~/contrib/zitadel/docs/docs/self-hosting/manage/productionchecklist.md`
- Online: https://zitadel.com/docs/self-hosting/manage/productionchecklist

## Infrastructure

- Provision infra via IaC (Terraform/Pulumi/etc) and keep manual changes to a minimum.
- Store secrets in a secret manager (masterkey, DB passwords, SMTP creds, TLS private key).
- Enforce least-privilege access for operators and CI/CD.

## High availability

- Run multiple ZITADEL runtimes (stateless), ideally behind an orchestrator (Kubernetes/Knative/Cloud Run).
- Separate phases for production:
  - `zitadel init` runs once (installation)
  - `zitadel setup` runs per version and controlled (migration job)
  - `zitadel start` runs as the fast, scalable runtime
- Run the database in HA mode, including:
  - backups and periodic restore tests
  - connection and query monitoring
  - network isolation (private subnet / firewall rules)

## Networking

- Ensure end-to-end HTTP/2 support (ZITADEL uses gRPC and gRPC-Web).
- Put a Layer 7 WAF / reverse proxy in front that supports HTTP/2 and (if needed) h2c to ZITADEL.
- Configure rate limits per endpoint group (API vs UI) and ensure IPv6 is covered.
- Use a CDN for static assets if it improves latency and shields the runtime.

## ZITADEL configuration (must-haves)

- Set external access correctly:
  - `ExternalDomain`, `ExternalPort`, `ExternalSecure`
  - Rerun `zitadel setup` after changing any of these.
- Do not ship defaults:
  - First instance admin credentials (`FirstInstance.Org.Human.*`)
  - Database credentials (`Database.*.User.*`, `Database.*.Admin.*`)
- Configure email delivery:
  - Configure SMTP in the instance defaults or via the console and test deliverability.
- Store and protect the masterkey (32 bytes) and ensure it is available to init/setup/start consistently.
- Consider expressing desired state via the ZITADEL Terraform provider for repeatability.

## Security

- Use a FQDN and valid certificates for external access (or terminate TLS in a trusted upstream component).
- Use service accounts for API integrations instead of reusing human admin accounts.
- Keep admin UI access restricted (SSO, network controls, dedicated operator group).
- Run periodic vulnerability scans against the public endpoints (WAF rules and TLS posture included).

## Monitoring

- Scrape metrics (`/debug/metrics`) and alert on:
  - readiness failures (`/debug/ready`)
  - liveness failures (`/debug/healthz`)
  - elevated error rate / latency
  - database connection saturation
  - TLS certificate expiry
- Centralize logs and keep enough retention for incident response.
