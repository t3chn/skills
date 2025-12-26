# Python Development Plugin

Modern Python development toolkit with FastAPI patterns, pytest testing, async SQLAlchemy, and modern tooling (uv, ruff).

## Skills

| Skill | Description |
|-------|-------------|
| [essential-libs](./skills/essential-libs/SKILL.md) | **Battle-tested libraries** — decimal, validation, HTTP, config, testing, logging |
| [fastapi-patterns](./skills/fastapi-patterns/SKILL.md) | FastAPI application architecture, DI, Pydantic, SQLAlchemy async |
| [testing-pytest](./skills/testing-pytest/SKILL.md) | Pytest patterns, fixtures, mocking, async testing |
| [modern-tooling](./skills/modern-tooling/SKILL.md) | uv, ruff, pyproject.toml configuration |

## Agents

| Agent | Description |
|-------|-------------|
| [python-test-writer](./agents/python-test-writer/AGENT.md) | Generates comprehensive pytest tests for Python code |

## Commands

| Command | Description |
|---------|-------------|
| `/py-test` | Run pytest with coverage |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| ruff-check | PreToolUse | Reminds to run ruff after Python file changes |

## Quick Start

### New Project

```bash
uv init myproject && cd myproject
uv add fastapi uvicorn pydantic sqlalchemy httpx
uv add --dev pytest pytest-asyncio pytest-mock pytest-cov ruff mypy
```

### Run Tests

```bash
uv run pytest --cov --cov-report=term-missing
```

### Lint & Format

```bash
uv run ruff check --fix .
uv run ruff format .
```

## Stack

- **Python 3.12+** - Modern Python with latest features
- **FastAPI** - Async web framework
- **Pydantic v2** - Data validation
- **SQLAlchemy 2.0** - Async ORM with asyncpg
- **pytest** - Testing framework
- **uv** - Fast package manager
- **ruff** - Linting and formatting

## Related

- [backend-core](../backend-core/SKILL.md) - Language-agnostic API patterns
- [secrets-guardian](../secrets-guardian/SKILL.md) - Pre-commit security
