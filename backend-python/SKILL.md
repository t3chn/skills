---
name: Python Backend
description: This skill should be used when the user asks about "Python backend", "FastAPI", "SQLAlchemy", "uv package manager", "ruff linter", "async Python", "Pydantic", "Python API", or needs Python-specific backend development guidance (2024-2025 best practices).
version: 1.0.0
---

# Python Backend Development

Modern Python backend with FastAPI, SQLAlchemy, uv, ruff.

**For general patterns** (API design, auth, security, architecture): use `backend-core`

## Modern Tooling (2025)

### Package Manager: uv (NOT pip/poetry)

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

### pyproject.toml

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
testpaths = ["tests"]

[tool.mypy]
python_version = "3.12"
strict = true
```

### Linting: ruff (NOT flake8/black)

```bash
ruff check .          # Lint
ruff check --fix .    # Lint + fix
ruff format .         # Format
```

## FastAPI Patterns

### Project Structure

```
src/
├── myapp/
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── dependencies.py   # DI
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── repositories/     # Data access
tests/
├── conftest.py
├── test_users.py
```

### App Setup

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(
    title="My API",
    version="1.0.0",
    lifespan=lifespan,
)
```

### Router Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Dependency Injection

```python
from functools import lru_cache
from typing import Annotated
from fastapi import Depends

@lru_cache
def get_settings() -> Settings:
    return Settings()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserService:
    return UserService(db)
```

### Pydantic Schemas

```python
from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    email: str = Field(..., examples=["user@example.com"])
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
```

## SQLAlchemy 2.0 Patterns

### Async Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=False,
    pool_size=5,
    max_overflow=10,
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass
```

### Models

```python
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))

    items: Mapped[list["Item"]] = relationship(back_populates="owner")
```

### Repository Pattern

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
```

## Security

### Password Hashing (Argon2id)

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hash: str) -> bool:
    try:
        ph.verify(hash, password)
        return True
    except VerifyMismatchError:
        return False
```

### JWT with python-jose

```python
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError

SECRET_KEY = "your-secret-key"
ALGORITHM = "RS256"  # or ES256

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    expire = datetime.now(UTC) + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

## Testing

### Async Testing with pytest

```python
import pytest
from httpx import AsyncClient, ASGITransport
from myapp.main import app

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    response = await client.get("/users/1")
    assert response.status_code == 200
```

### Database Testing

```python
@pytest.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

## Anti-patterns

❌ `pip install` without lockfile → ✅ `uv add`
❌ `requirements.txt` → ✅ `pyproject.toml`
❌ `flake8 + black + isort` → ✅ `ruff`
❌ `bcrypt` → ✅ `argon2-cffi`
❌ Python < 3.11 → ✅ Python 3.12+
❌ sync SQLAlchemy → ✅ async with asyncpg

## Related Skills

- **backend-core** — Language-agnostic patterns (API design, auth, security)
- **python-testing** — Pytest patterns, fixtures, mocking
- **secrets-guardian** — Pre-commit security hooks
