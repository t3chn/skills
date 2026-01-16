# Overview

URL: https://www.greptile.com/docs/security/selfhost

# Overview

Greptile is AI that understands your codebase and can do things like review PRs, generate documentation, and more. The entirety of Greptiles service can be self-hosted in an air-gapped environment.

# Deployment

* Runs on any compute node (EC2 or equivalent) with `docker-compose`
* Compatible with major cloud providers:
+ Amazon Web Services (AWS)
+ Google Cloud Platform (GCP)
+ Microsoft Azure
+ Other major providers supported
* More information on the deployment method can be found in the [akupara](https://github.com/greptileai/akupara) repository.

# LLM Configuration

* Flexible LLM integration supporting:
+ Any OpenAI-compatible API
+ Custom LLM implementations
+ Recommended: Anthropic Claude 3.7 Sonnet (as of Feb 2025) and OpenAI Embeddings
+ AWS Bedrock integration available

# Database Requirements

* PostgreSQL database required
+ AWS RDS recommended
+ Uses pgvector as the vector database
+ Customer provisions and maintains database
* Redis cache recommended
+ AWS Elasticache recommended
+ Customer provisions and maintains cache

# Version Management

* Regular update notifications
* New Docker image URLs provided
* Maximum 30-day version delta from cloud
* Seamless upgrade path

# Code Host Support

* GitHub integration
+ GitHub Cloud (github.com)
+ GitHub Enterprise Server (self-hosted) - email [[email protected]](/cdn-cgi/l/email-protection#640c0108080b2403160114100d08014a070b09) for access
+ GitHub Enterprise Cloud
* GitLab integration
+ GitLab Cloud (gitlab.com)
+ GitLab Self-Managed
+ GitLab Enterprise Edition
* Support for multiple code hosts simultaneously
* Custom code host integrations available on request

# Pricing Structure

* Annual contracts with monthly payments
* 15% discount for upfront annual payment
* Trial Policy:
+ No free trials
+ 100% refund available within first 30 days
+ Pro-rated refunds available months 2-4 (upfront payments only)

# Getting Started

```
To get started with Greptile self-hosted, you can book time with our engineering team [here](https://cal.com/team/greptile/demo)!
```
