#!/usr/bin/env python3
"""
Initialize a new backend project with modern best practices.

Usage:
    python init_project.py --name myapp --framework fastapi
    python init_project.py --name myapp --framework nestjs
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

PYTHON_PROJECT_STRUCTURE = {
    "src": ["__init__.py", "main.py", "config.py"],
    "src/api": ["__init__.py", "routes.py", "deps.py"],
    "src/models": ["__init__.py"],
    "src/services": ["__init__.py"],
    "src/repositories": ["__init__.py"],
    "tests": ["__init__.py", "conftest.py"],
    "tests/unit": ["__init__.py"],
    "tests/integration": ["__init__.py"],
}

NODE_PROJECT_STRUCTURE = {
    "src": ["main.ts", "app.module.ts"],
    "src/common": ["filters", "guards", "interceptors", "pipes"],
    "src/config": ["configuration.ts"],
    "src/modules": [],
    "test": ["app.e2e-spec.ts"],
}

PYPROJECT_TOML = """[project]
name = "{name}"
version = "0.1.0"
description = ""
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "sqlalchemy>=2.0.36",
    "asyncpg>=0.30.0",
    "redis>=5.2.0",
    "httpx>=0.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pre-commit>=4.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
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
]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["{name}"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"
"""

RUFF_CONFIG = """# Ruff configuration (fastest Python linter)
target-version = "py312"
line-length = 100

[lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
ignore = ["E501"]

[lint.isort]
known-first-party = ["{name}"]
"""

MAIN_PY_FASTAPI = '''"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "API is running"}
'''

CONFIG_PY = '''"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "FastAPI App"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/db"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Auth
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 15

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
'''


def run_command(cmd: list[str], cwd: Path | None = None) -> bool:
    """Run a shell command."""
    try:
        subprocess.run(cmd, check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(cmd)}: {e}")
        return False


def create_python_project(name: str, path: Path) -> None:
    """Create a FastAPI project with modern tooling."""
    print(f"Creating Python/FastAPI project: {name}")

    # Create directory structure
    for directory, files in PYTHON_PROJECT_STRUCTURE.items():
        dir_path = path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        for file in files:
            (dir_path / file).touch()

    # Write pyproject.toml
    (path / "pyproject.toml").write_text(PYPROJECT_TOML.format(name=name))

    # Write ruff.toml
    (path / "ruff.toml").write_text(RUFF_CONFIG.format(name=name))

    # Write main application files
    (path / "src" / "main.py").write_text(MAIN_PY_FASTAPI)
    (path / "src" / "config.py").write_text(CONFIG_PY)

    # Write .gitignore
    gitignore = """__pycache__/
*.py[cod]
*$py.class
.venv/
.env
.mypy_cache/
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/
dist/
*.egg-info/
"""
    (path / ".gitignore").write_text(gitignore)

    # Initialize with uv
    print("Initializing project with uv...")
    if run_command(["uv", "sync"], cwd=path):
        print("Dependencies installed with uv")

    # Setup pre-commit
    pre_commit_config = """repos:
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
"""
    (path / ".pre-commit-config.yaml").write_text(pre_commit_config)

    print(f"Project created at {path}")
    print("\nNext steps:")
    print(f"  cd {path}")
    print("  uv sync")
    print("  uv run uvicorn src.main:app --reload")


def create_node_project(name: str, path: Path) -> None:
    """Create a NestJS project with modern tooling."""
    print(f"Creating Node.js/NestJS project: {name}")

    # Use NestJS CLI
    if run_command(["npx", "@nestjs/cli", "new", name, "--package-manager", "npm", "--skip-git"]):
        print(f"NestJS project created at {path}")
        print("\nNext steps:")
        print(f"  cd {path}")
        print("  npm run start:dev")


def main():
    parser = argparse.ArgumentParser(description="Initialize a new backend project")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument(
        "--framework",
        choices=["fastapi", "nestjs", "express"],
        default="fastapi",
        help="Framework to use",
    )
    parser.add_argument("--path", default=".", help="Path to create project")

    args = parser.parse_args()

    project_path = Path(args.path) / args.name
    project_path.mkdir(parents=True, exist_ok=True)

    if args.framework == "fastapi":
        create_python_project(args.name, project_path)
    elif args.framework in ("nestjs", "express"):
        create_node_project(args.name, project_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
