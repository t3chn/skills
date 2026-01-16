# Kubernetes Deployment

URL: https://www.greptile.com/docs/kubernetes-new

Kubernetes deployment for teams with **100+ developers** or requiring high availability and horizontal scaling.

```
Helm charts are in the [akupara repository](https://github.com/greptileai/akupara/tree/main/greptile-helm).
```

## Prerequisites

**Cluster:**

* Kubernetes 1.21+ (1.25+ recommended)
* `kubectl` configured
* `helm` 3.0+

**From Greptile:**

* Container registry credentials
* License (contact [[email protected]](/cdn-cgi/l/email-protection#cdbeaca1a8be8daabfa8bdb9a4a1a8e3aea2a0))

**External:**

* GitHub App or GitLab OAuth configured

## Setup

Clone repository

```
git clone https://github.com/greptileai/akupara.git
cd akupara/greptile-helm
```

Install Hatchet

Hatchet is the workflow orchestration system. Install it first:

```
helm repo add hatchet https://hatchet-dev.github.io/hatchet-charts
helm install hatchet-stack hatchet/hatchet-stack -f hatchet-values.yaml
```

Wait ~30 seconds, then port-forward to access the admin portal:

`kubectl port-forward svc/caddy 8080:8080`

Generate an API token:

```
1. Open `http://localhost:8080`
2. Login with `[email protected]` / `Admin123!!`
```
3. Go to **Settings > API Tokens > Generate API Token**
4. Copy and save the token

Change the default admin password in Settings > General > Members.

Create registry secret

```
kubectl create secret docker-registry regcred \
--docker-server=https://index.docker.io/v1/ \
--docker-username=greptileai \
--docker-password=<TOKEN_FROM_GREPTILE> \
--docker-email=<YOUR_EMAIL>
```

Configure values.yaml

Open `values.yaml` and configure:**Secrets:**

secrets:
# Generate both with: openssl rand -hex 32
# IMPORTANT: jwtSecret and authSecret must be identical
jwtSecret: "generate-a-random-string"
authSecret: "same-as-jwt-secret"
tokenEncryptionKey: "another-random-string"

# Token from Hatchet portal (Step 2)
hatchetClientToken: "your-hatchet-token"

# LLM API keys (configure the ones you use)
anthropicKey: "sk-ant-..."
openaiKey: "sk-..."
azureOpenaiKey: ""

# GitHub credentials
githubWebhookSecret: "your-webhook-secret"
githubPrivateKey: |
-----BEGIN RSA PRIVATE KEY-----
...your private key...
-----END RSA PRIVATE KEY-----

**Global settings:**

```
global:
externalUrl: "https://greptile.yourcompany.com"
authGithubId: "Iv1.xxx"
authGithubSecret: "xxx"

ai:
# Override default proxy URLs to use direct APIs
anthropic:
baseUrl: "https://api.anthropic.com"
openai:
apiBaseUrl: "https://api.openai.com/v1"

refiner:
modelProvider: "anthropic"
model: "claude-sonnet-4-20250514"
chat:
modelProvider: "anthropic"
model: "claude-sonnet-4-20250514"
summarizer:
modelProvider: "openai"
model: "gpt-4o-mini"
embeddings:
modelProvider: "openai"
model: "text-embedding-ada-002"

web:
config:
externalUrl: "https://greptile.yourcompany.com"
```

Default values.yaml uses Helicone proxy URLs. Update `anthropic.baseUrl` and `openai.apiBaseUrl` to use direct provider APIs as shown above.

```
See [values.yaml](https://github.com/greptileai/akupara/blob/main/greptile-helm/values.yaml) for all options.
```

Deploy

```
helm dependency update
helm install greptile . -f values.yaml
```

Verify

`kubectl get pods`

```
All pods should be `Running`. Verify Hatchet shows 4 registered workers at `http://localhost:8080`.Access the web UI:
```

```
kubectl port-forward svc/greptile-web 3000:3000
```

---

## Infrastructure by Cloud Provider

If you dont already have a Kubernetes cluster, use these guides to create one.

### AWS (EKS)

```
[Terraform configurations](https://github.com/greptileai/akupara/tree/main/kubernetes/terraform/aws) are provided:
```

cd kubernetes/terraform/aws
cp terraform.tfvars.example terraform.tfvars

Edit `terraform.tfvars` with your GitHub App credentials and LLM API keys, then:

```
terraform init
terraform apply
```

After deployment, configure kubectl:

```
aws eks update-kubeconfig --region <region> --name <cluster-name>
```

### GCP (GKE)

```
[Terraform configuration](https://github.com/greptileai/akupara/tree/main/kubernetes/terraform/gcp) creates full infrastructure:
```

* VPC with private/public subnets
* Cloud SQL (PostgreSQL 16)
* Memorystore (Redis)
* GKE cluster with node pool
* Secret Manager secrets
* Service account with Vertex AI access

cd kubernetes/terraform/gcp

Create a `terraform.tfvars` with required variables:

```
project_id = "your-gcp-project"
region = "us-central1"
db_username = "greptile"
db_password = "your-secure-password"

# LLM keys
openai_api_key = "sk-..."
anthropic_api_key = "sk-ant-..."

# GitHub App
github_client_id = "Iv1.xxx"
github_client_secret = "xxx"
github_webhook_secret = "xxx"
github_private_key = "-----BEGIN RSA PRIVATE KEY-----..."

# Secrets (generate with: openssl rand -hex 32)
jwt_secret = "xxx"
```

Deploy:

```
terraform init
terraform apply
```

Configure kubectl:

```
gcloud container clusters get-credentials greptile --region <region>
```

### Azure (AKS)

No Terraform provided for Azure. Create a cluster manually:

```
az group create --name greptile-rg --location eastus

az aks create \
--resource-group greptile-rg \
--name greptile-prod \
--node-count 3 \
--node-vm-size Standard_D4s_v3 \
--enable-cluster-autoscaler \
--min-count 3 --max-count 10
```

Configure kubectl:

```
az aks get-credentials --resource-group greptile-rg --name greptile-prod
```

For Azure OpenAI, add to `values.yaml`:

```
global:
ai:
azure:
openaiUrl: "https://your-resource.openai.azure.com/"
openaiSummarizerDeploymentName: "gpt-4o-mini"
openaiEmbeddingsDeploymentName: "text-embedding-ada-002"
summarizer:
modelProvider: "azure"
embeddings:
modelProvider: "azure"

secrets:
azureOpenaiKey: "your-key"
```

### Other Environments

For on-prem, k3s, Rancher, or OpenShift:

* Kubernetes 1.21+ required
* The Helm chart deploys PostgreSQL by default
* Redis is optional (disabled by default)
* Configure an ingress controller or load balancer for external access

---

## Resource Sizing

Production recommendations (adjust based on team size):

| Service | CPU Request | CPU Limit | Memory | Replicas |
| --- | --- | --- | --- | --- |
| API | 100m | 2000m | 2-4Gi | 20 |
| Chunker | 4000m | 8000m | 24-48Gi | 10 |
| Summarizer | 1000m | 2000m | 2-4Gi | 50 |
| Reviews | 500m | 1000m | 1-2Gi | 36 |
| Webhook | 500m | 1000m | 1-2Gi | 5 |
| Web | 500m | 1000m | 512Mi-1Gi | 3 |

---

## Operations

### Scaling

```
kubectl scale deployment greptile-api --replicas=10
```

### Updating

```
helm upgrade greptile . -f values.yaml --set image.tag=<new_version>
kubectl rollout status deployment/greptile-api

# Rollback if needed
helm rollback greptile 1
```

### Viewing Logs

```
kubectl logs -l app=greptile-api --tail=100 -f
kubectl logs -l app=greptile-webhook --tail=100 -f
```

### Monitoring

* **Hatchet dashboard** (`http://localhost:8080`): Workflow status, queue depth, worker health
* **Pod health** : `kubectl get pods`
* **Resource usage** : `kubectl top pods`
* **Events** : `kubectl get events --sort-by='.lastTimestamp'`

---

## Troubleshooting

### Pods Not Starting

```
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp' | head -20
```

| Symptom | Cause | Fix |
| --- | --- | --- |
| `ImagePullBackOff` | Registry auth failed | Verify `regcred` secret |
| `CrashLoopBackOff` | App error | Check logs: `kubectl logs <pod>` |
| `Pending` | No resources | Scale cluster or reduce resource requests |

### Hatchet Workers Not Registering

If Hatchet portal shows 0 workers:

1. Verify `secrets.hatchetClientToken` matches the token from Hatchet portal
```
2. Check worker logs: `kubectl logs -l app=greptile-reviews`
```
3. Regenerate token if needed and redeploy: `helm upgrade greptile . -f values.yaml`

### Database Connection Issues

Test connectivity:

```
kubectl run -it --rm debug --image=postgres:14 --restart=Never -- \
psql -h <db-host> -U <username> -d <database>
```

Ensure pgvector is installed: `CREATE EXTENSION IF NOT EXISTS vector;`

### Webhooks Not Working

1. Verify `global.externalUrl` is publicly accessible
```
2. Check webhook URL in GitHub App matches `https://<externalUrl>/webhook`
3. Check logs: `kubectl logs -l app=greptile-webhook --tail=100`
```

### LLM Errors

Check LLM proxy logs:

```
kubectl logs -l app=greptile-llmproxy --tail=100
```

Verify API keys and model names in `values.yaml`.

---

## Resources

* [Helm charts](https://github.com/greptileai/akupara/tree/main/greptile-helm)
* [values.yaml](https://github.com/greptileai/akupara/blob/main/greptile-helm/values.yaml)
* [Terraform configs](https://github.com/greptileai/akupara/tree/main/kubernetes/terraform)
