---
name: Backend Core Patterns
description: This skill should be used when the user asks about "API design", "REST API", "GraphQL", "gRPC", "authentication", "OAuth", "JWT", "security headers", "OWASP", "microservices", "caching", "rate limiting", "CI/CD", "health checks", "observability", or needs language-agnostic backend architecture guidance.
version: 1.0.0
---

# Backend Core Patterns

Language-agnostic backend development patterns. Use with language-specific skills (backend-python, backend-nodejs, backend-rust).

## API Design

### REST Best Practices

```
GET    /users           # List users (with pagination)
GET    /users/:id       # Get single user
POST   /users           # Create user
PUT    /users/:id       # Full update
PATCH  /users/:id       # Partial update
DELETE /users/:id       # Delete user
```

**Pagination:**
```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "next": "/users?page=2&limit=20"
  }
}
```

**Error Response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "field": "email"
  }
}
```

### GraphQL Essentials

```graphql
type Query {
  user(id: ID!): User
  users(limit: Int = 20, cursor: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}
```

- Use DataLoader for N+1 prevention
- Depth limiting to prevent abuse
- Persisted queries for production

### gRPC

```protobuf
service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (stream User);
}
```

Best for internal microservices communication.

## Authentication

### OAuth 2.1 + PKCE (Recommended)

```
1. Client generates code_verifier + code_challenge
2. Redirect to /authorize?code_challenge=...
3. User authenticates
4. Redirect back with authorization code
5. Exchange code + code_verifier for tokens
```

### JWT Structure

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-123",
    "iss": "https://auth.example.com",
    "aud": "https://api.example.com",
    "exp": 1704067200,
    "iat": 1704063600
  }
}
```

- Sign with RS256/ES256 (not HS256 for distributed)
- Store in httpOnly cookies (not localStorage)
- Short-lived access tokens (15-60 min)
- Refresh tokens with rotation

### Password Hashing

```
Argon2id > scrypt > bcrypt
```

Parameters for Argon2id:
- Memory: 64 MB
- Iterations: 3
- Parallelism: 4

## Security (OWASP Top 10)

### Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Referrer-Policy: strict-origin-when-cross-origin
```

### Rate Limiting

```
Token Bucket Algorithm:
- Bucket capacity: 100 requests
- Refill rate: 10 requests/second
- Per-user AND per-IP limits
```

### Input Validation

```
Always:
1. Validate type and format
2. Sanitize special characters
3. Use parameterized queries
4. Limit input length
5. Reject unexpected fields
```

## Architecture

### Database Patterns

```
Connection Pooling:
- min: 5, max: 20
- idle timeout: 30s
- connection timeout: 5s

Read Replicas:
- Writes → Primary
- Reads → Replica (with lag tolerance)

Caching:
- Cache-aside (lazy loading)
- TTL based on data volatility
- Redis for distributed cache
```

### Microservices

```
┌─────────────┐
│ API Gateway │
└──────┬──────┘
       │
┌──────┴──────┐
│             │
▼             ▼
┌─────┐    ┌─────┐
│Svc A│    │Svc B│
└──┬──┘    └──┬──┘
   │          │
   └────┬─────┘
        ▼
   ┌─────────┐
   │  Queue  │
   └─────────┘
```

- Single responsibility per service
- Event-driven communication (Kafka, RabbitMQ)
- Service mesh for observability

## DevOps

### CI/CD Pipeline

```yaml
stages:
  - lint          # Format, lint, type check
  - test          # Unit tests
  - build         # Compile/bundle
  - integration   # Integration tests
  - security      # Dependency scan, SAST
  - deploy-stage  # Staging deployment
  - e2e           # End-to-end tests
  - deploy-prod   # Production (with approval)
```

### Deployment Strategies

| Strategy | Rollback | Risk | Use Case |
|----------|----------|------|----------|
| Blue-Green | Instant | Low | Critical services |
| Canary | Fast | Medium | Gradual rollout |
| Rolling | Slow | Medium | Standard deploys |

### Container Best Practices

```dockerfile
# Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
USER node
COPY --from=builder /app/node_modules ./node_modules
COPY . .
HEALTHCHECK --interval=30s CMD curl -f http://localhost:3000/health
```

## Observability

### Three Pillars

| Pillar | Tool | Format |
|--------|------|--------|
| Logs | ELK, Loki | Structured JSON |
| Metrics | Prometheus | RED (Rate, Errors, Duration) |
| Traces | Jaeger, Tempo | OpenTelemetry |

### Health Endpoints

```
GET /health/live   → 200 if process alive
GET /health/ready  → 200 if can serve traffic
GET /health/startup → 200 after initialization
```

### Alerting Thresholds

```
Error Rate: > 1% for 5 min
Latency P99: > 500ms for 5 min
CPU Usage: > 80% for 10 min
Memory: > 85% for 5 min
```

## Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| `SELECT *` | Explicit column list |
| No pagination | Cursor or offset pagination |
| HS256 for distributed JWT | RS256 or ES256 |
| Secrets in code/env | Secrets manager (Vault, AWS Secrets) |
| No rate limiting | Token bucket per user + IP |
| Polling for updates | WebSockets or SSE |
| No health checks | /health/live + /health/ready |
| Single DB instance | Connection pooling + read replicas |

## Related Skills

- **backend-python** — FastAPI, SQLAlchemy, async patterns
- **backend-nodejs** — NestJS, Drizzle, TypeScript
- **backend-rust** — Axum, SQLx, deployment
- **secrets-guardian** — Pre-commit security hooks
