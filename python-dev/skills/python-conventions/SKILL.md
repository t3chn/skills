---
name: python-conventions
description: Python project conventions and best practices for code review context. Use with official feature-dev:code-reviewer agent.
globs: ["**/*.py", "**/pyproject.toml", "**/requirements.txt"]
---

# Python Conventions

Context for code review of Python projects. These conventions inform the official `feature-dev:code-reviewer` agent.

## 2025 Tooling (Required)

| Tool | Purpose | Replaces |
|------|---------|----------|
| **uv** | Package manager, venv | pip, poetry, pipenv |
| **Ruff** | Linter + formatter | flake8, black, isort |
| **pytest** | Testing | unittest |
| **Pydantic v2** | Validation | dataclasses for API |

```bash
# Modern project setup
uv init myproject && cd myproject
uv add fastapi uvicorn pydantic
uv add --dev pytest ruff
```

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "UP", "B", "SIM"]
```

## Type Hints (Required)

### Function Signatures
```python
def get_user(user_id: str) -> User | None:
    """Fetch user by ID."""
    ...

async def fetch_data(
    url: str,
    timeout: float = 30.0,
    *,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    ...
```

### Use Modern Syntax (Python 3.10+)
```python
# Use built-in generics
list[str]  # not List[str]
dict[str, int]  # not Dict[str, int]

# Use union operator
str | None  # not Optional[str]
int | str  # not Union[int, str]
```

### TypedDict for Dictionaries
```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    id: str
    email: str
    name: NotRequired[str]  # Optional field
```

## Error Handling

### Custom Exceptions
```python
class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, code: str = "UNKNOWN"):
        self.message = message
        self.code = code
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", "NOT_FOUND")

class ValidationError(AppError):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("; ".join(errors), "VALIDATION")
```

### Catch Specific Exceptions
```python
# WRONG
try:
    process()
except:  # bare except
    pass

# WRONG
try:
    process()
except Exception:  # too broad
    pass

# CORRECT
try:
    result = await client.fetch(url)
except httpx.TimeoutException:
    logger.warning("Request timed out", url=url)
    raise
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        return None
    raise
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `UserService`, `HTTPClient` |
| Functions | snake_case | `get_user`, `parse_config` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `API_URL` |
| Modules | snake_case | `user_service`, `http_client` |
| Private | `_` prefix | `_internal_method` |

## Project Structure

```
src/
├── app/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── config.py         # Settings
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   ├── repositories/     # Data access
│   └── api/              # HTTP handlers
│       ├── __init__.py
│       ├── routes.py
│       └── deps.py       # Dependencies
tests/
├── conftest.py           # Fixtures
├── test_services.py
└── test_api.py
pyproject.toml
```

## Testing with pytest

### Structure Tests with Classes
```python
import pytest
from unittest.mock import AsyncMock, patch

class TestUserService:
    @pytest.fixture
    def service(self, mock_repo: AsyncMock) -> UserService:
        return UserService(repository=mock_repo)

    @pytest.fixture
    def mock_repo(self) -> AsyncMock:
        return AsyncMock(spec=UserRepository)

    async def test_get_user_found(
        self,
        service: UserService,
        mock_repo: AsyncMock,
    ) -> None:
        expected = User(id="1", email="test@example.com")
        mock_repo.find_by_id.return_value = expected

        result = await service.get_user("1")

        assert result == expected
        mock_repo.find_by_id.assert_called_once_with("1")

    async def test_get_user_not_found(
        self,
        service: UserService,
        mock_repo: AsyncMock,
    ) -> None:
        mock_repo.find_by_id.return_value = None

        with pytest.raises(NotFoundError):
            await service.get_user("1")
```

### Parametrized Tests
```python
@pytest.mark.parametrize(
    "input_data,expected",
    [
        ({"email": "test@example.com"}, True),
        ({"email": "invalid"}, False),
        ({"email": ""}, False),
    ],
)
def test_validate_email(input_data: dict, expected: bool) -> None:
    result = validate_email(input_data["email"])
    assert result == expected
```

## Async Patterns

### Use `asyncio` Correctly
```python
import asyncio

# Parallel execution
results = await asyncio.gather(
    fetch_user(user_id),
    fetch_orders(user_id),
)

# With error handling
results = await asyncio.gather(
    *tasks,
    return_exceptions=True,
)
```

### Avoid Blocking Async
```python
# WRONG - blocks event loop
def sync_operation():
    time.sleep(1)  # Blocking!

# CORRECT - use async sleep
async def async_operation():
    await asyncio.sleep(1)

# Or run in executor
result = await asyncio.get_event_loop().run_in_executor(
    None,  # Default executor
    blocking_function,
)
```

## Pydantic Models

```python
from pydantic import BaseModel, Field, field_validator

class CreateUserRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    name: str = Field(..., min_length=1, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

    model_config = {"from_attributes": True}
```

## Logging with structlog

```python
import structlog

logger = structlog.get_logger()

# Structured logging
logger.info(
    "user_created",
    user_id=user.id,
    email=user.email,
)

# With context
logger = logger.bind(request_id=request_id)
logger.info("processing_request")
```

## Security

- Never log sensitive data (passwords, tokens)
- Use `secrets` module for random tokens
- Validate all input with Pydantic
- Use parameterized queries (SQLAlchemy does this)
- Set appropriate timeouts on HTTP clients
- Hash passwords with `bcrypt` or `argon2`

## Code Review Checklist

- [ ] All functions have type hints
- [ ] Specific exceptions caught (not bare except)
- [ ] Tests use pytest fixtures properly
- [ ] No blocking calls in async code
- [ ] Pydantic models for API boundaries
- [ ] Structured logging with context
- [ ] No hardcoded secrets
- [ ] Input validated at entry points
