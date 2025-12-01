# Modern Backend Tooling (2025)

Always use the latest stable versions of tools and libraries. This guide covers modern tooling that should be the default choice for new projects.

## Core Principle

**Always prefer modern, actively maintained tools over legacy options.** Check release dates and community activity before adopting any tool.

## Python Tooling

### Package Management: uv (NOT pip/poetry/pipenv)

**uv** is the modern Python package manager - 10-100x faster than pip.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init myproject
cd myproject

# Add dependencies
uv add fastapi uvicorn pydantic

# Add dev dependencies
uv add --dev pytest ruff mypy

# Sync dependencies (install from lock file)
uv sync

# Run commands in venv
uv run python main.py
uv run pytest

# Update all dependencies
uv lock --upgrade
```

**pyproject.toml (modern standard):**
```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "sqlalchemy>=2.0.36",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "ruff>=0.8.0",
]
```

### Linting & Formatting: Ruff (NOT flake8/black/isort)

**Ruff** replaces flake8, black, isort, pyupgrade, and more. 10-100x faster.

```bash
# Install
uv add --dev ruff

# Lint
ruff check .

# Lint and fix
ruff check --fix .

# Format (replaces black)
ruff format .
```

**ruff.toml:**
```toml
target-version = "py312"
line-length = 100

[lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "S",      # flake8-bandit (security)
    "ASYNC",  # flake8-async
]
ignore = ["E501"]  # line too long (handled by formatter)

[lint.per-file-ignores]
"tests/**" = ["S101"]  # allow assert in tests

[format]
quote-style = "double"
indent-style = "space"
```

### Type Checking: mypy or Pyright

```bash
# mypy (traditional)
uv add --dev mypy
mypy src/

# pyright (faster, VSCode integration)
uv add --dev pyright
pyright
```

**pyproject.toml mypy config:**
```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
```

### Testing: pytest (with modern plugins)

```bash
uv add --dev pytest pytest-asyncio pytest-cov pytest-xdist

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run in parallel
uv run pytest -n auto
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.0]

  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.5.0
    hooks:
      - id: uv-lock
```

## Node.js/TypeScript Tooling

### Package Management: npm/pnpm (with lockfile)

```bash
# Use specific Node version (via fnm or nvm)
fnm use 22

# Install with lockfile
npm ci  # NOT npm install

# pnpm (faster, disk efficient)
pnpm install --frozen-lockfile
```

### Runtime: Bun or Node 22+

```bash
# Bun (faster runtime, built-in bundler)
bun run src/index.ts
bun test

# Node 22+ (native TypeScript support coming)
node --experimental-strip-types src/index.ts
```

### Linting: ESLint 9+ with flat config

```javascript
// eslint.config.js (flat config - new standard)
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/no-explicit-any': 'error',
    },
  }
);
```

### Formatting: Prettier or Biome

```bash
# Biome (faster, replaces ESLint + Prettier)
npx @biomejs/biome init
npx @biomejs/biome check --write .
```

### Testing: Vitest (NOT Jest)

**Vitest** is 50% faster than Jest, native ESM support, better DX.

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

```bash
# Run tests
npx vitest

# Run with coverage
npx vitest --coverage

# Watch mode
npx vitest --watch
```

### Build: esbuild or tsup

```bash
# tsup (esbuild wrapper, zero config)
npx tsup src/index.ts --format esm,cjs --dts

# esbuild (raw, fastest)
npx esbuild src/index.ts --bundle --platform=node --outfile=dist/index.js
```

## Go Tooling

### Modern Go Setup

```bash
# Always use latest Go (1.23+)
go version

# Module management
go mod init myapp
go mod tidy
go mod verify

# Build with optimizations
go build -ldflags="-s -w" -o bin/app ./cmd/app
```

### Linting: golangci-lint

```yaml
# .golangci.yml
linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gosec        # security
    - prealloc     # performance
    - misspell

linters-settings:
  gosec:
    severity: medium
    confidence: medium
```

### Testing

```bash
# Run tests with race detection
go test -race ./...

# With coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Rust Tooling

### Modern Rust Setup

```bash
# Install via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Use latest stable
rustup default stable
rustup update

# Faster builds with mold linker
cargo install cargo-binstall
cargo binstall mold
```

### Linting & Formatting

```bash
# Clippy (linter)
cargo clippy -- -W clippy::pedantic

# Format
cargo fmt

# Check without building
cargo check
```

### Testing

```bash
# Run tests
cargo test

# With output
cargo test -- --nocapture

# Specific test
cargo test test_name
```

## Database Tools

### Migrations

**Node.js:**
```bash
# Drizzle (type-safe, fast)
npx drizzle-kit generate
npx drizzle-kit migrate

# Prisma
npx prisma migrate dev
```

**Python:**
```bash
# Alembic (SQLAlchemy)
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Database Clients

```bash
# pgcli (better psql)
pip install pgcli
pgcli postgresql://user:pass@localhost/db

# usql (universal SQL client)
go install github.com/xo/usql@latest
usql pg://user:pass@localhost/db
```

## Docker & Containers

### Modern Dockerfile Practices

```dockerfile
# Use specific versions, not 'latest'
FROM node:22-alpine AS builder

# Use multi-stage builds
# Use non-root users
# Use health checks
# Use .dockerignore
```

### Container Tools

```bash
# Docker Compose v2 (not v1)
docker compose up -d

# Podman (rootless alternative)
podman run -d myimage

# Container scanning
trivy image myimage:latest
```

## CI/CD

### GitHub Actions (Modern)

```yaml
# Use latest action versions
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
- uses: actions/setup-python@v5

# Use caching
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

## Version Checklist

Always verify you're using recent versions:

| Tool | Minimum Version | Check Command |
|------|-----------------|---------------|
| Python | 3.12+ | `python --version` |
| Node.js | 22+ | `node --version` |
| Go | 1.23+ | `go version` |
| Rust | 1.82+ | `rustc --version` |
| uv | 0.5+ | `uv --version` |
| Ruff | 0.8+ | `ruff --version` |
| Docker | 27+ | `docker --version` |

## Anti-patterns to Avoid

**Python:**
- ❌ pip install without lockfile
- ❌ requirements.txt (use pyproject.toml)
- ❌ flake8 + black + isort (use ruff)
- ❌ Python < 3.11

**Node.js:**
- ❌ npm install in CI (use npm ci)
- ❌ CommonJS for new projects (use ESM)
- ❌ Jest (use Vitest)
- ❌ Node < 20

**General:**
- ❌ Docker 'latest' tag
- ❌ Running as root in containers
- ❌ No lockfiles in git
- ❌ Manual dependency updates (use Dependabot/Renovate)
