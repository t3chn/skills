---
name: python-essential-libs
description: Essential Python libraries for production applications. Use these battle-tested packages instead of reinventing the wheel or using wrong primitives.
globs: ["**/*.py", "**/pyproject.toml", "**/requirements*.txt"]
---

# Python Essential Libraries

> **Golden Rule**: Use the right tool for the job. These libraries represent thousands of hours of community effort and real-world battle-testing.

## 💰 Decimal & Money (NEVER use float!)

### decimal — Standard Library (Default)
```python
from decimal import Decimal, ROUND_HALF_UP

# WRONG: float for money
price = 19.99
total = price * 3  # 59.97000000000001 — BROKEN!

# CORRECT: Decimal
price = Decimal("19.99")
total = price * 3  # Decimal('59.97') — exact

# From float (when necessary, but prefer strings)
price = Decimal(str(19.99))

# Rounding for display
rounded = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

# Context for precision
from decimal import localcontext
with localcontext() as ctx:
    ctx.prec = 50  # 50 digits precision
    result = Decimal("1") / Decimal("7")
```

### py-moneyed — Currency-Aware
```python
from moneyed import Money, USD, EUR

# Currency-safe operations
price = Money(19.99, USD)
total = price * 3  # Money(59.97, 'USD')

# Access underlying Decimal
amount: Decimal = price.amount

# Currency mismatch protection
try:
    total = Money(10, USD) + Money(10, EUR)  # Error!
except TypeError:
    pass  # Cannot add different currencies

# Formatting
from moneyed.localization import format_money
formatted = format_money(price, locale='en_US')  # '$19.99'
```

### Integer Cents — Simplest Approach
```python
# Store as cents (int) — no precision issues
class Money:
    def __init__(self, cents: int):
        self.cents = cents

    @classmethod
    def from_dollars(cls, dollars: float) -> "Money":
        return cls(int(round(dollars * 100)))

    def to_dollars(self) -> float:
        return self.cents / 100

    def __add__(self, other: "Money") -> "Money":
        return Money(self.cents + other.cents)

# Usage
price = Money.from_dollars(19.99)  # 1999 cents
```

**When to use**:
- `decimal.Decimal`: General purpose, no external deps
- `py-moneyed`: Currency-aware, ISO 4217, formatting
- Integer cents: Simple apps, fixed 2-decimal precision

---

## ✅ Validation & Data Classes

### Pydantic v2 — Validation + Serialization (Default)
```python
from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=18, le=120)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("name")
    @classmethod
    def name_must_be_titlecase(cls, v: str) -> str:
        return v.title()

# Validation
user = User(name="john doe", email="john@example.com", age=25)
# user.name == "John Doe" (validator applied)

# Serialization
user_dict = user.model_dump()
user_json = user.model_dump_json()

# Parsing
user = User.model_validate({"name": "jane", "email": "jane@x.com", "age": 30})
user = User.model_validate_json('{"name": "jane", ...}')
```

### attrs — Performance + Explicit Control
```python
import attrs
from attrs import define, field, validators

@define
class User:
    name: str = field(validator=validators.min_len(1))
    email: str = field(validator=validators.matches_re(r".+@.+\..+"))
    age: int = field(validator=[validators.ge(18), validators.le(120)])

    @age.validator
    def _check_age(self, attribute, value):
        if value < 0:
            raise ValueError("Age cannot be negative")

# Slots by default (40-50% less memory than Pydantic)
user = User(name="John", email="john@example.com", age=25)

# Convert to dict
attrs.asdict(user)
```

### dataclasses — Standard Library (Simple Cases)
```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    name: str
    email: str
    age: int
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        # Manual validation
        if self.age < 0:
            raise ValueError("Age cannot be negative")
```

**When to use**:
- `pydantic`: APIs, user input, JSON, FastAPI (6.5x slower, 2.5x more memory)
- `attrs`: Internal data structures, performance-critical code
- `dataclasses`: Simple cases, no external deps, minimal validation

---

## 🌐 HTTP Client

### httpx — Modern Async/Sync (Recommended)
```python
import httpx

# Sync
response = httpx.get("https://api.example.com/users/1")
user = response.json()

# Async
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com/users/1")
    user = response.json()

# With configuration
client = httpx.Client(
    base_url="https://api.example.com",
    timeout=10.0,
    headers={"Authorization": f"Bearer {token}"},
)

# POST with JSON
response = client.post("/users", json={"name": "John"})
response.raise_for_status()

# HTTP/2 support
client = httpx.Client(http2=True)
```

### requests — Simple Sync (Legacy)
```python
import requests

# Simple and familiar
response = requests.get(
    "https://api.example.com/users/1",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
response.raise_for_status()
user = response.json()

# Session for connection pooling
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {token}"})
```

### aiohttp — High-Performance Async
```python
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get("https://api.example.com/users/1") as response:
        user = await response.json()

# WebSocket support
async with session.ws_connect("wss://example.com/ws") as ws:
    await ws.send_str("Hello")
    async for msg in ws:
        print(msg.data)
```

**When to use**:
- `httpx`: New projects, mixed sync/async, HTTP/2 (recommended)
- `requests`: Simple scripts, sync-only, familiar API
- `aiohttp`: High-concurrency, WebSockets, maximum performance

---

## ⚙️ Configuration

### pydantic-settings — Type-Safe Config (Recommended)
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=False,
    )

    debug: bool = False
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = "redis://localhost:6379"
    api_key: str = Field(min_length=32)

# Load from environment + .env file
settings = Settings()
# APP_DEBUG=true, DATABASE_URL=postgresql://...

# Validation included
# Raises ValidationError if API_KEY is missing or too short
```

### dynaconf — Multi-Format, Multi-Environment
```python
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="APP",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,  # Enable [development], [production] sections
    load_dotenv=True,
)

# settings.toml
"""
[default]
debug = false

[development]
debug = true
database_url = "sqlite:///dev.db"

[production]
database_url = "@format {this.DATABASE_URL}"
"""

# Access
settings.DEBUG
settings.DATABASE_URL
```

### python-decouple — Simple .env
```python
from decouple import config, Csv

DEBUG = config("DEBUG", default=False, cast=bool)
DATABASE_URL = config("DATABASE_URL")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
SECRET_KEY = config("SECRET_KEY")
```

**When to use**:
- `pydantic-settings`: FastAPI, type safety, validation
- `dynaconf`: Complex multi-environment, multiple formats
- `python-decouple`: Simple .env loading

---

## 🧪 Testing

### pytest — The Standard
```python
import pytest

def test_user_creation():
    user = User(name="John", age=25)
    assert user.name == "John"
    assert user.age == 25

class TestUserService:
    @pytest.fixture
    def user_service(self, db_session):
        return UserService(db_session)

    def test_get_user(self, user_service):
        user = user_service.get(1)
        assert user is not None

# Parametrized tests
@pytest.mark.parametrize("age,expected", [
    (17, False),
    (18, True),
    (65, True),
])
def test_is_adult(age, expected):
    assert is_adult(age) == expected

# Async tests
@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data()
    assert result is not None
```

### pytest-asyncio — Async Testing
```python
# pyproject.toml
"""
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
"""

import pytest

@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client

async def test_api_endpoint(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
```

### hypothesis — Property-Based Testing
```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert add(a, b) == add(b, a)

@given(st.text(min_size=1, max_size=100))
def test_encode_decode_roundtrip(text):
    encoded = encode(text)
    decoded = decode(encoded)
    assert decoded == text

# Complex strategies
@given(st.builds(
    User,
    name=st.text(min_size=1, max_size=50),
    age=st.integers(min_value=0, max_value=120),
))
def test_user_validation(user):
    assert user.name
    assert 0 <= user.age <= 120
```

### polyfactory — Test Data Generation
```python
from polyfactory.factories.pydantic_factory import ModelFactory

class User(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserFactory(ModelFactory):
    __model__ = User

# Generate test data
user = UserFactory.build()
users = UserFactory.batch(10)

# With overrides
admin = UserFactory.build(name="Admin", age=30)
```

### pytest-mock — Mocking
```python
def test_user_service(mocker):
    mock_repo = mocker.Mock()
    mock_repo.get.return_value = User(name="John", age=25)

    service = UserService(mock_repo)
    user = service.get_user(1)

    mock_repo.get.assert_called_once_with(1)
    assert user.name == "John"

# Patch
def test_with_patch(mocker):
    mocker.patch("myapp.services.send_email", return_value=True)
    result = register_user(user_data)
    assert result.email_sent
```

---

## 📊 Logging

### structlog — Structured Logging (Recommended)
```python
import structlog

# Configuration
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),  # JSON for production
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Structured logging with context
logger.info("user_created", user_id=123, email="john@example.com")
# {"event": "user_created", "user_id": 123, "email": "john@example.com", ...}

# Bind context
log = logger.bind(request_id="abc-123")
log.info("processing_started")
log.info("processing_completed")
# Both logs have request_id
```

### loguru — Simple + Powerful
```python
from loguru import logger

# Zero config needed
logger.info("Hello, World!")

# Structured data
logger.info("User created", user_id=123, email="john@example.com")

# Configure output
logger.add("app.log", rotation="500 MB", retention="10 days")
logger.add("errors.log", level="ERROR")

# JSON format
logger.add(
    "app.json",
    serialize=True,  # JSON output
    rotation="1 day",
)

# Context binding
with logger.contextualize(request_id="abc-123"):
    logger.info("Processing request")
```

### Standard logging — Built-in
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.info("User created: %s", user_id)
```

**When to use**:
- `structlog`: Production apps, JSON logs, context binding
- `loguru`: Quick setup, file rotation, nice defaults
- `logging`: No deps, integration with stdlib

---

## ⚡ Async & Concurrency

### asyncio — Standard Library
```python
import asyncio

async def fetch_all(urls: list[str]) -> list[str]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.text for r in responses]

# Run
results = asyncio.run(fetch_all(urls))

# Timeout
async def with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=5.0)
    except asyncio.TimeoutError:
        logger.error("Operation timed out")

# Semaphore for limiting concurrency
sem = asyncio.Semaphore(10)

async def limited_fetch(url):
    async with sem:
        return await fetch(url)
```

### anyio — Backend-Agnostic Async
```python
import anyio

async def main():
    # Works with asyncio, trio, or curio
    async with anyio.create_task_group() as tg:
        tg.start_soon(task1)
        tg.start_soon(task2)

    # Structured concurrency
    async with anyio.create_task_group() as tg:
        for url in urls:
            tg.start_soon(fetch, url)

# Cancellation scopes
async def with_timeout():
    with anyio.move_on_after(5.0):
        await slow_operation()
```

### concurrent.futures — Thread/Process Pools
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# I/O-bound tasks
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch, url) for url in urls]
    results = [f.result() for f in futures]

# CPU-bound tasks
with ProcessPoolExecutor() as executor:
    results = list(executor.map(heavy_computation, data))
```

---

## 💉 Dependency Injection

### FastAPI's Depends — Built-in (Recommended for FastAPI)
```python
from fastapi import Depends, FastAPI

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return service.get(user_id)
```

### dependency-injector — Full IoC Container
```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        url=config.database_url,
    )

    user_repository = providers.Factory(
        UserRepository,
        db=db,
    )

    user_service = providers.Factory(
        UserService,
        repository=user_repository,
    )

# Usage
container = Container()
container.config.from_yaml("config.yaml")

service = container.user_service()
```

### Constructor Injection — No Framework
```python
# Just use constructors — simplest approach
class UserService:
    def __init__(self, repo: UserRepository, cache: Cache):
        self.repo = repo
        self.cache = cache

# Wire up in main
def create_app():
    db = Database(url=settings.database_url)
    repo = UserRepository(db)
    cache = RedisCache(settings.redis_url)
    service = UserService(repo, cache)
    return App(service)
```

---

## 🗄️ Caching

### functools.lru_cache — Built-in
```python
from functools import lru_cache, cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    return sum(range(n))

# Python 3.9+: unlimited cache
@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### cachetools — Advanced In-Memory
```python
from cachetools import TTLCache, LRUCache, cached

# TTL cache
cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes

@cached(cache)
def get_user(user_id: int) -> User:
    return db.query(User).get(user_id)

# LRU with custom key
from cachetools.keys import hashkey

@cached(LRUCache(maxsize=1000), key=lambda user: hashkey(user.id))
def get_permissions(user: User) -> list[str]:
    return fetch_permissions(user.id)
```

### aiocache — Async + Redis/Memcached
```python
from aiocache import Cache, cached
from aiocache.serializers import JsonSerializer

# Memory cache
cache = Cache(Cache.MEMORY)
await cache.set("key", "value", ttl=60)
value = await cache.get("key")

# Redis cache
cache = Cache(
    Cache.REDIS,
    endpoint="localhost",
    port=6379,
    serializer=JsonSerializer(),
)

# Decorator
@cached(ttl=300, cache=Cache.REDIS)
async def get_user(user_id: int) -> dict:
    return await fetch_user(user_id)
```

---

## 🕐 Date & Time

### datetime — Standard Library (Default)
```python
from datetime import datetime, timedelta, timezone

# Always use UTC for storage
now = datetime.now(timezone.utc)

# Parse ISO format
dt = datetime.fromisoformat("2024-12-25T10:30:00+00:00")

# Formatting
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

# Arithmetic
tomorrow = now + timedelta(days=1)
```

### pendulum — Timezone-Aware (Complex Cases)
```python
import pendulum

# Automatic timezone
now = pendulum.now("UTC")
local = pendulum.now("America/New_York")

# Parsing (more forgiving)
dt = pendulum.parse("2024-12-25")
dt = pendulum.parse("Dec 25, 2024")

# Human-readable diffs
diff = pendulum.now().diff_for_humans()  # "2 hours ago"

# Timezone conversion
utc = pendulum.now("UTC")
local = utc.in_timezone("Europe/Paris")

# Period iteration
period = pendulum.period(start, end)
for dt in period.range("days"):
    print(dt)
```

**When to use**:
- `datetime`: Simple cases, no deps
- `pendulum`: Complex timezone handling, human-readable output (18x slower)

---

## 🔐 Security

### Password Hashing — argon2-cffi (Recommended)
```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

# Hash
hash = ph.hash("password123")

# Verify
try:
    ph.verify(hash, "password123")
except VerifyMismatchError:
    raise InvalidCredentialsError()

# Check if rehash needed (params changed)
if ph.check_needs_rehash(hash):
    new_hash = ph.hash("password123")
```

### Password Hashing — bcrypt (Alternative)
```python
import bcrypt

# Hash
password = b"password123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)

# Verify
if bcrypt.checkpw(password, hashed):
    print("Password matches")
```

### Secrets — Secure Random
```python
import secrets

# Token generation
token = secrets.token_urlsafe(32)  # URL-safe base64
hex_token = secrets.token_hex(32)  # Hex string

# Secure comparison (timing attack safe)
if secrets.compare_digest(provided_token, stored_token):
    authenticate()
```

### PyJWT — JSON Web Tokens
```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secret-key"

# Create token
payload = {
    "sub": user_id,
    "exp": datetime.now(timezone.utc) + timedelta(hours=24),
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verify token
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload["sub"]
except jwt.ExpiredSignatureError:
    raise TokenExpiredError()
except jwt.InvalidTokenError:
    raise InvalidTokenError()
```

---

## 🗃️ Database

### SQLAlchemy 2.0 — Async ORM (Recommended)
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)

# Async engine
engine = create_async_engine("postgresql+asyncpg://...")

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

### asyncpg — High-Performance PostgreSQL
```python
import asyncpg

pool = await asyncpg.create_pool(
    "postgresql://user:pass@localhost/db",
    min_size=5,
    max_size=20,
)

async with pool.acquire() as conn:
    user = await conn.fetchrow(
        "SELECT * FROM users WHERE id = $1", user_id
    )

    # Batch insert
    await conn.executemany(
        "INSERT INTO users (name, email) VALUES ($1, $2)",
        [("John", "john@x.com"), ("Jane", "jane@x.com")],
    )
```

---

## 📋 Quick Reference

| Category | Recommended | Alternative |
|----------|-------------|-------------|
| **Decimal** | `decimal.Decimal` | `py-moneyed` (currency) |
| **Validation** | `pydantic` v2 | `attrs` (performance) |
| **HTTP Client** | `httpx` | `aiohttp` (max perf) |
| **Config** | `pydantic-settings` | `dynaconf` (complex) |
| **Testing** | `pytest` + `hypothesis` | `polyfactory` |
| **Mocking** | `pytest-mock` | - |
| **Logging** | `structlog` | `loguru` (simple) |
| **Async** | `asyncio` | `anyio` (portable) |
| **DI** | FastAPI `Depends` | `dependency-injector` |
| **Cache** | `cachetools` | `aiocache` (async) |
| **DateTime** | `datetime` | `pendulum` (complex tz) |
| **Password** | `argon2-cffi` | `bcrypt` |
| **JWT** | `PyJWT` | - |
| **Database** | SQLAlchemy 2.0 + asyncpg | - |

## 🔗 pyproject.toml Example

```toml
[project]
dependencies = [
    # Core
    "pydantic>=2.10",
    "pydantic-settings>=2.6",
    "httpx>=0.28",

    # Database
    "sqlalchemy>=2.0",
    "asyncpg>=0.30",

    # Security
    "argon2-cffi>=23.1",
    "PyJWT>=2.10",

    # Logging
    "structlog>=24.4",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3",
    "pytest-asyncio>=0.24",
    "pytest-mock>=3.14",
    "hypothesis>=6.120",
    "polyfactory>=2.18",
]
```
