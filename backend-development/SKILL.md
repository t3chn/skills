---
name: backend-development
description: Production-ready backend development with Node.js/Python/Go/Rust, APIs (REST/GraphQL/gRPC), databases, security (OWASP), testing, DevOps, and AI/LLM integration. Use when working on: (1) API design and implementation (REST/GraphQL/gRPC), (2) Authentication/authorization (OAuth 2.1, JWT, RBAC), (3) Database optimization and schema design, (4) Security hardening (OWASP Top 10), (5) Performance tuning and caching (Redis), (6) CI/CD pipelines and Docker/K8s deployment, (7) Microservices architecture, (8) Debugging production systems, (9) AI/LLM backend integration, (10) Testing strategies. Always enforces modern tooling: uv/ruff for Python (NOT pip/poetry/flake8), Vitest for Node.js (NOT Jest), latest stable versions.
---

# Backend Development Skill

**Core principle:** Always use latest stable versions and modern tooling.

## Quick Reference

| Task | Reference |
|------|-----------|
| **Modern tooling (uv, ruff)** | `references/backend-modern-tooling.md` |
| **API Design** | `references/backend-api-design.md` |
| **Authentication** | `references/backend-authentication.md` |
| **Security (OWASP)** | `references/backend-security.md` |
| **Performance** | `references/backend-performance.md` |
| **Architecture** | `references/backend-architecture.md` |
| **Testing** | `references/backend-testing.md` |
| **DevOps** | `references/backend-devops.md` |
| **Observability** | `references/backend-observability.md` |
| **AI/LLM Integration** | `references/backend-ai-integration.md` |
| **Debugging** | `references/debugging/` |

## Modern Tooling Standards (2025)

**Python:**
- Package manager: **uv** (NOT pip/poetry)
- Linting/formatting: **ruff** (NOT flake8/black/isort)
- Type checking: **mypy** or **pyright**
- Testing: **pytest** with pytest-asyncio
- Version: **Python 3.12+**

**Node.js/TypeScript:**
- Runtime: **Node 22+** or **Bun**
- Testing: **Vitest** (NOT Jest)
- Linting: **ESLint 9+** flat config or **Biome**
- Build: **esbuild** or **tsup**

**General:**
- Always use **lockfiles** (uv.lock, package-lock.json)
- Always use **specific versions** in Dockerfiles (NOT `latest`)
- Always run as **non-root** in containers
- Always use **parameterized queries** (prevent SQL injection)
- Always use **Argon2id** for password hashing (NOT bcrypt)

## Technology Selection Guide

**Languages:**
- Node.js/TypeScript: Full-stack, real-time apps
- Python: Data/ML integration, FastAPI
- Go: High concurrency, microservices
- Rust: Maximum performance, memory safety

**Frameworks:**
- NestJS (Node.js enterprise)
- FastAPI (Python async, auto-docs)
- Gin (Go performance)
- Axum (Rust ergonomic)

**Databases:**
- PostgreSQL: ACID, complex queries
- MongoDB: Flexible schema
- Redis: Caching, sessions

**APIs:**
- REST: Simple CRUD, public APIs
- GraphQL: Flexible data fetching
- gRPC: Internal microservices, performance

## Templates & Scripts

**Templates** (`templates/`):
- `Dockerfile` - Multi-stage Node.js build
- `Dockerfile.python` - Python with uv
- `docker-compose.yml` - Local dev stack
- `.github/workflows/ci.yml` - GitHub Actions CI/CD
- `.env.example` - Environment variables template

**Scripts** (`scripts/`):
- `init_project.py` - Initialize new project with best practices
- `security_check.sh` - Run security scanners

## Key Best Practices

**Security:**
- Argon2id passwords
- Parameterized queries (98% SQL injection reduction)
- OAuth 2.1 + PKCE
- Rate limiting
- Security headers (CSP, HSTS)

**Performance:**
- Redis caching (90% DB load reduction)
- Database indexing (30% I/O reduction)
- CDN (50%+ latency cut)
- Connection pooling

**Testing:**
- 70-20-10 pyramid (unit-integration-E2E)
- Vitest 50% faster than Jest
- Contract testing for microservices

**DevOps:**
- Blue-green/canary deployments
- Feature flags (90% fewer failures)
- Kubernetes + Helm
- OpenTelemetry for observability

## Implementation Checklist

**New Project:**
- [ ] Use latest language version (Python 3.12+, Node 22+)
- [ ] Use modern package manager (uv, npm with lockfile)
- [ ] Use modern linter (ruff, ESLint 9+)
- [ ] Setup pre-commit hooks
- [ ] Configure CI/CD pipeline
- [ ] Add health check endpoints
- [ ] Setup structured logging
- [ ] Configure OpenTelemetry

**API:**
- [ ] Choose style (REST/GraphQL/gRPC)
- [ ] Design schema
- [ ] Validate input
- [ ] Add auth
- [ ] Rate limiting
- [ ] Documentation (OpenAPI)
- [ ] Error handling

**Security:**
- [ ] OWASP Top 10 review
- [ ] Parameterized queries
- [ ] OAuth 2.1 + JWT
- [ ] Security headers
- [ ] Input validation
- [ ] Argon2id passwords
- [ ] Dependency scanning

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OAuth 2.1: https://oauth.net/2.1/
- OpenTelemetry: https://opentelemetry.io/
- uv: https://docs.astral.sh/uv/
- ruff: https://docs.astral.sh/ruff/
