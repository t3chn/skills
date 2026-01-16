# Manual Setup

URL: https://www.greptile.com/docs/docker-compose/manual-setup

```
Deploy Greptile on any Linux server AWS, GCP, Azure, on-prem, or air-gapped environments. Uses the [docker/](https://github.com/greptileai/akupara/tree/main/docker) directory from the akupara repository.
```

## Prerequisites

Server Requirements

| Team Size | CPU | RAM | Storage |
| --- | --- | --- | --- |
| 5-10 devs | 4 cores | 16GB | 100GB |
| ~50 devs | 8 cores | 32GB | 200GB |
| 100 devs | 32 cores | 128GB | 500GB |

**OS:** Ubuntu 20.04+, Amazon Linux 2023, Debian 11+, RHEL 8+

Software

* Docker 23.x+ ([install guide](https://docs.docker.com/engine/install/))
* Docker Compose v2.5+ (included with Docker Desktop, or [install separately](https://docs.docker.com/compose/install/))

From Greptile

* Container registry credentials (`CONTAINER_REGISTRY`, `GREPTILE_TAG`)
* Contact [[email protected]](/cdn-cgi/l/email-protection#8af9ebe6eff9caedf8effafee3e6efa4e9e5e7)

Network

**Inbound ports:**

* `3007` SCM webhooks (must be publicly accessible)
* `3000` Web UI
* `8080` Hatchet admin (optional)

**Outbound access:**

* LLM provider APIs
* GitHub/GitLab APIs
* Container registry

## Setup

Clone repository

```
git clone https://github.com/greptileai/akupara.git
cd akupara/docker
```

Configure environment

cp .env.example .env

Edit `.env` with required values (see [Configuration](#configuration) below).

Generate secrets

`./bin/generate-secrets.sh`

Creates `.env.greptile-generated` with `JWT_SECRET`, `TOKEN_ENCRYPTION_KEY`, `LLM_PROXY_KEY`.

Login to registry

`./bin/login-registry.sh`

Authenticates with Docker Hub or AWS ECR based on `REGISTRY_PROVIDER` in `.env`.

Start Hatchet

`./bin/start-hatchet.sh`

Wait ~30 seconds for Hatchet to be healthy.

Generate Hatchet token

`./bin/generate-hatchet-token.sh`

Creates `.env.hatchet-generated` with `HATCHET_CLIENT_TOKEN`.

Start Greptile

`./bin/start-greptile.sh`

Verify

`docker compose ps`

All services should show `running` or `healthy`.

## Access

| Service | URL |
| --- | --- |
```
| Web UI | `http://<IP_ADDRESS>:3000` |
| Hatchet Admin | `http://<IP_ADDRESS>:8080` |
```

## Configuration

### Required Settings

```
# Container registry (from Greptile)
REGISTRY_PROVIDER='dockerhub' # or 'ecr'
CONTAINER_REGISTRY='xxx'
GREPTILE_TAG='xxx'

# Server IP (for webhook callbacks)
IP_ADDRESS='your.server.public.ip'
```

### LLM Provider

Anthropic

```
ANTHROPIC_BASE_URL='https://api.anthropic.com'
ANTHROPIC_KEY='sk-ant-...'
```

OpenAI

```
OPENAI_API_BASE_URL='https://api.openai.com/v1/'
OPENAI_KEY='sk-...'
```

Azure OpenAI

```
AZURE_OPENAI_URL='https://your-resource.openai.azure.com/'
AZURE_OPENAI_KEY='xxx'
AZURE_OPENAI_API_VERSION='2024-07-18'
```

AWS Bedrock

```
AWS_ACCESS_KEY_ID='AKIA...'
AWS_SECRET_ACCESS_KEY='xxx'
AWS_REGION='us-east-1'
```

### GitHub

GitHub Cloud

```
GITHUB_ENABLED='true'
GITHUB_ENTERPRISE_ENABLED='false'
GITHUB_APP_ID='123456'
GITHUB_CLIENT_ID='Iv1.xxx'
GITHUB_CLIENT_SECRET='xxx'
GITHUB_PRIVATE_KEY='-----BEGIN RSA PRIVATE KEY-----...'
WEBHOOK_SECRET='xxx'
```

GitHub Enterprise

```
GITHUB_ENABLED='false'
GITHUB_ENTERPRISE_ENABLED='true'
GITHUB_ENTERPRISE_URL='https://github.yourcompany.com'
GITHUB_ENTERPRISE_API_URL='https://github.yourcompany.com/api/v3/'
GITHUB_APP_ID='123456'
GITHUB_CLIENT_ID='Iv1.xxx'
GITHUB_CLIENT_SECRET='xxx'
GITHUB_PRIVATE_KEY='-----BEGIN RSA PRIVATE KEY-----...'
WEBHOOK_SECRET='xxx'
```

### External Database (Optional)

To use managed PostgreSQL (RDS, Cloud SQL) instead of the bundled container:

```
DB_HOST='your-database-endpoint'
DB_PORT='5432'
DB_USER='greptile'
DB_PASSWORD='xxx'
DB_NAME='greptile'
DB_SSL_DISABLE='false'
```

PostgreSQL 15+ with pgvector extension required. Run `CREATE EXTENSION IF NOT EXISTS vector;`

## Custom Domain & TLS

Point DNS to server IP

Create an A record for your domain pointing to the servers public IP.

Configure Caddy

cp Caddyfile.example Caddyfile

Edit `Caddyfile`:

```
greptile.yourcompany.com {
reverse_proxy greptile-web:3000
}

greptile.yourcompany.com:3007 {
reverse_proxy greptile-webhook:3007
}
```

Update environment

```
IP_ADDRESS='greptile.yourcompany.com'
APP_URL='https://greptile.yourcompany.com'
```

Restart services

`docker compose up -d`

Caddy automatically obtains TLS certificates via Lets Encrypt.

## Auto-Start (Systemd)

```
Install [systemd services](https://github.com/greptileai/akupara/tree/main/docker/systemd) for automatic startup on boot:
```

```
sudo cp systemd/*.service /etc/systemd/system/
sudo cp systemd/*.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable greptile-hatchet greptile-app
sudo systemctl start greptile-hatchet greptile-app
```

| Service | Purpose |
| --- | --- |
| `greptile-hatchet.service` | Starts Hatchet stack |
| `greptile-app.service` | Starts Greptile services |
| `greptile-images.timer` | Periodic image updates |

## Operations

View logs

```
docker compose logs -f # All services
docker compose logs -f greptile-api # Specific service
```

Restart a service

`docker compose restart greptile-api`

Update images

```
./bin/login-registry.sh
docker compose pull
docker compose up -d
```

Check Hatchet workflows

```
Access `http://<IP>:8080` to view workflow status, queue depth, and failures.
```

## Troubleshooting

Services won't start

```
docker compose config # Validate compose file
docker compose logs <service> # Check specific service logs
sudo systemctl status docker # Check Docker daemon
```

Webhooks not receiving

1. Verify `IP_ADDRESS` is publicly accessible
2. Check firewall allows inbound on port 3007
```
3. Confirm GitHub App webhook URL: `http://<IP>:3007/webhook`
```

LLM errors

`docker compose logs greptile-llmproxy`

Verify API keys and endpoint URLs in `.env`.

Hatchet workers not registering

Regenerate token and restart:

```
./bin/generate-hatchet-token.sh
docker compose restart
```

Database connection issues

```
docker compose exec greptile-api nc -zv $DB_HOST 5432
```

## Resources

* [Docker directory](https://github.com/greptileai/akupara/tree/main/docker)
* [.env.example](https://github.com/greptileai/akupara/blob/main/docker/.env.example)
* [Helper scripts](https://github.com/greptileai/akupara/tree/main/docker/bin)
* [Systemd services](https://github.com/greptileai/akupara/tree/main/docker/systemd)
