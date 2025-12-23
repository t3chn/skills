---
name: Python Modern Tooling
description: This skill should be used when the user asks about "uv package manager", "ruff linter", "pyproject.toml", "Python project setup", "Python dependencies", or needs guidance on modern Python tooling (2024-2025 best practices).
version: 1.0.0
---

# Python Modern Tooling

Modern Python development with uv, ruff, and pyproject.toml (2025 standards).

## Package Manager: uv (NOT pip/poetry)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init myproject && cd myproject

# Add dependencies
uv add fastapi uvicorn pydantic sqlalchemy

# Add dev dependencies
uv add --dev pytest ruff mypy pytest-asyncio

# Run
uv run python -m myapp
uv run pytest
```

## pyproject.toml

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
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM", "S", "ASYNC"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]

[tool.mypy]
python_version = "3.12"
strict = true
```

## Linting: ruff (NOT flake8/black)

```bash
ruff check .          # Lint
ruff check --fix .    # Lint + fix
ruff format .         # Format
```

### Ruff Rule Categories

| Code | Category | Description |
|------|----------|-------------|
| E, W | pycodestyle | Style errors and warnings |
| F | Pyflakes | Logical errors |
| I | isort | Import sorting |
| B | flake8-bugbear | Bug-prone patterns |
| C4 | flake8-comprehensions | Comprehension style |
| UP | pyupgrade | Python upgrade suggestions |
| ARG | flake8-unused-arguments | Unused arguments |
| SIM | flake8-simplify | Code simplification |
| S | flake8-bandit | Security issues |
| ASYNC | flake8-async | Async issues |

## Type Checking: mypy

```bash
mypy src/
```

### mypy Configuration

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
exclude = ["tests/", "migrations/"]

[[tool.mypy.overrides]]
module = "third_party_lib.*"
ignore_missing_imports = true
```

## Testing Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
    "--strict-config",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

## Anti-patterns

| Wrong | Right |
|-------|-------|
| `pip install` without lockfile | `uv add` |
| `requirements.txt` | `pyproject.toml` |
| `flake8 + black + isort` | `ruff` |
| `bcrypt` | `argon2-cffi` |
| Python < 3.11 | Python 3.12+ |
| sync SQLAlchemy | async with asyncpg |

## Project Structure

```
myproject/
├── pyproject.toml          # All config here
├── uv.lock                  # Lockfile (auto-generated)
├── .python-version          # Python version
├── src/
│   └── myapp/
│       ├── __init__.py
│       └── main.py
└── tests/
    ├── conftest.py
    └── test_main.py
```

## Common Commands

```bash
# Development
uv run python -m myapp          # Run app
uv run uvicorn myapp.main:app --reload  # Dev server

# Testing
uv run pytest                   # Run tests
uv run pytest --cov            # With coverage

# Linting
uv run ruff check .            # Lint
uv run ruff format .           # Format
uv run mypy src/               # Type check

# Dependencies
uv add <package>               # Add dependency
uv add --dev <package>         # Add dev dependency
uv remove <package>            # Remove dependency
uv sync                        # Sync from lockfile
uv lock                        # Update lockfile
```

## Related Skills

- **fastapi-patterns** - FastAPI application architecture
- **testing-pytest** - Pytest patterns and fixtures
