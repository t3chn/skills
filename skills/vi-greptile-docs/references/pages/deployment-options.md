# Deployment Options

URL: https://www.greptile.com/docs/deployment-options

## Quick Decision

**Use Cloud** if you want Greptile running in minutes with zero infrastructure management.
**Use Self-Hosted** if you need data sovereignty, air-gapped environments, or custom LLM providers.
For self-hosted, choose based on team size:

* **Docker Compose** : Up to 100 developers. Single VM, simpler operations.
* **Kubernetes** : 100+ developers. Horizontal scaling, high availability.

## Self-Hosted: Docker Compose

Runs all services on a single Linux VM using Docker Compose.

### Two Setup Paths

**AWS with Terraform** If youre on AWS and want automated provisioning:

* Terraform creates VPC, EC2, RDS PostgreSQL, ElastiCache Redis
* Bootstraps the EC2 with Docker Compose and starts Greptile
* Single `terraform apply` gets you running

**Manual Setup** If youre on GCP, Azure, on-prem, or want control over infrastructure:

* You provision a Linux VM and any external databases
* Clone the repo, configure `.env`, run Docker Compose
* Works anywhere Docker runs

### Requirements

**VM Sizing:**

| Team Size | CPU | RAM | Storage |
| --- | --- | --- | --- |
| 5-10 devs | 4 cores | 16GB | 100GB |
| ~50 devs | 8 cores | 32GB | 200GB |
| 100 devs | 32 cores | 128GB | 500GB |

**Software:** Linux (Ubuntu 20.04+, Amazon Linux 2023), Docker 23.x+, Docker Compose v2.5+
**Network:** Inbound access on port 3007 for SCM webhooks. Outbound HTTPS to LLM and SCM providers.

## Self-Hosted: Kubernetes

Runs services across a Kubernetes cluster using Helm charts. Provides horizontal scaling, rolling updates, and high availability.

### Requirements

**Cluster:** Kubernetes 1.21+ (1.25+ recommended), Helm 3.0+
**External Services:** PostgreSQL with pgvector (RDS recommended), Redis (ElastiCache recommended)
**Sizing:**

| Team Size | Nodes | Per Node | Total |
| --- | --- | --- | --- |
| 50 devs | 3-5 | 8c / 32GB | 24-40 cores |
| 100-500 devs | 5-10 | 16c / 64GB | 80-160 cores |
| 500+ devs | 10-20+ | 16-32c / 64-128GB | 160-640+ cores |

[Go to Kubernetes guide ](/docs/kubernetes-new)

## External Dependencies

### LLM Providers

You need three model types configured:

| Model Type | Used For | Options |
| --- | --- | --- |
| Smart (reasoning) | Code review, agent tasks | Claude 3.5 Sonnet+, GPT-4o |
| Fast | Summarization, quick tasks | GPT-4o-mini, Claude Haiku |
| Embeddings | Code indexing | text-embedding-3-small, Titan V2 |

Supported providers: OpenAI, Anthropic, AWS Bedrock, Azure OpenAI, GCP Vertex AI.

### Source Code Management

| Platform | Setup Required |
| --- | --- |
| GitHub / GitHub Enterprise | GitHub App with webhook URL |
| GitLab | OAuth app configuration |
| Perforce | P4USER, P4PASSWD, P4PORT, P4CLIENT env vars |

### Container Registry

Access to Greptiles Docker images. Contact Greptile for registry credentials.

## Migration

Docker Compose to Kubernetes migration is supported via parallel deployments. Run both simultaneously, then switch traffic at the load balancer or DNS level.

## Pricing

Self-hosted requires a license. Contact [[email protected]](/cdn-cgi/l/email-protection#d9aab8b5bcaa99beabbca9adb0b5bcf7bab6b4).
