---
name: backend-core
description: |
  Language-agnostic backend patterns: API design, authentication, security, architecture, DevOps.
  Use with language-specific skills (backend-python, backend-nodejs) for complete coverage.
  Triggers: "API design", "authentication", "security", "architecture", "microservices", "OWASP"
---

# Backend Core Patterns

Language-agnostic backend development patterns. Use with language-specific skills.

## Quick Reference

| Topic | Reference |
|-------|-----------|
| API Design | `references/api-design.md` |
| Authentication | `references/authentication.md` |
| Security | `references/security.md` |
| Architecture | `references/architecture.md` |
| DevOps | `references/devops.md` |
| Observability | `references/observability.md` |

## API Design Principles

### REST
- Use nouns, not verbs: `/users`, not `/getUsers`
- HTTP methods: GET (read), POST (create), PUT/PATCH (update), DELETE
- Status codes: 2xx success, 4xx client error, 5xx server error
- Pagination: `?page=1&limit=20` or cursor-based
- Versioning: `/v1/users` or header `Accept: application/vnd.api+json;version=1`

### GraphQL
- Single endpoint: `/graphql`
- Query for reads, Mutation for writes
- Use DataLoader for N+1 prevention
- Depth limiting to prevent abuse

### gRPC
- Protocol Buffers for schema
- Best for internal microservices
- Streaming support (unary, server, client, bidirectional)

## Authentication Patterns

### OAuth 2.1 + PKCE (recommended)
- Authorization Code flow for web apps
- PKCE required for all clients
- Short-lived access tokens (15-60 min)
- Refresh tokens with rotation

### JWT Best Practices
- Sign with RS256 or ES256 (not HS256 for distributed systems)
- Include: `sub`, `iat`, `exp`, `iss`, `aud`
- Store in httpOnly cookies (not localStorage)
- Validate signature AND claims

### Session Management
- Secure, HttpOnly, SameSite=Strict cookies
- Redis for distributed sessions
- Absolute timeout + idle timeout

## Security (OWASP Top 10)

### Injection Prevention
- **Always** use parameterized queries
- Validate and sanitize all input
- Use ORM with proper escaping

### Authentication Failures
- Argon2id for password hashing (not bcrypt)
- Rate limiting on auth endpoints
- Account lockout after failures
- MFA for sensitive operations

### Security Headers
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

### Rate Limiting
- Token bucket or sliding window
- Per-user and per-IP limits
- Exponential backoff on failures

## Architecture Patterns

### Microservices
- Single responsibility per service
- API Gateway for routing
- Service mesh for observability
- Event-driven communication (Kafka, RabbitMQ)

### Database Patterns
- Connection pooling
- Read replicas for scaling
- Sharding for horizontal scale
- CQRS for complex domains

### Caching Strategy
- Cache-aside (lazy loading)
- Write-through for consistency
- TTL based on data volatility
- Redis for distributed cache

## DevOps Essentials

### CI/CD Pipeline
1. Lint & format
2. Unit tests
3. Build
4. Integration tests
5. Security scan
6. Deploy to staging
7. E2E tests
8. Deploy to production

### Deployment Strategies
- Blue-green: instant rollback
- Canary: gradual rollout (1% → 10% → 50% → 100%)
- Feature flags for controlled releases

### Containers
- Multi-stage builds
- Non-root user
- Health checks
- Specific version tags (not `latest`)

## Observability

### Three Pillars
1. **Logs**: Structured JSON, correlation IDs
2. **Metrics**: RED (Rate, Errors, Duration)
3. **Traces**: Distributed tracing with OpenTelemetry

### Health Checks
- `/health/live` - process alive
- `/health/ready` - ready to serve traffic
- Include dependency checks

### Alerting
- Error rate > threshold
- Latency P99 > SLA
- Resource utilization > 80%
