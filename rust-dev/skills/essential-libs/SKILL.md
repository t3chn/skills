---
name: rust-essential-libs
description: Essential Rust libraries for production applications. Use these battle-tested crates instead of reinventing the wheel or using wrong primitives.
globs: ["**/*.rs", "**/Cargo.toml"]
---

# Rust Essential Libraries

> **Golden Rule**: Use the right crate for the job. These libraries represent thousands of hours of community effort and real-world battle-testing.

## 💰 Decimal & Money (NEVER use f64!)

### rust_decimal — 96-bit Mantissa
```rust
use rust_decimal::Decimal;
use rust_decimal_macros::dec;

// WRONG: f64 for money
let price: f64 = 19.99;
let total = price * 3.0;  // 59.97000000000001 — BROKEN!

// CORRECT: rust_decimal
let price = dec!(19.99);
let total = price * dec!(3);  // 59.97 — exact

// From string (safer)
let price: Decimal = "19.99".parse().unwrap();

// Comparison
if price > limit { /* ... */ }

// Rounding for display
let rounded = price.round_dp(2);

// In structs
#[derive(Serialize, Deserialize)]
struct Product {
    #[serde(with = "rust_decimal::serde::str")]
    price: Decimal,
}
```

**Cargo.toml**:
```toml
rust_decimal = { version = "1", features = ["serde", "db-postgres"] }
rust_decimal_macros = "1"
```

**Alternatives**:
| Crate | Precision | Performance | Use Case |
|-------|-----------|-------------|----------|
| `rust_decimal` | 28-29 digits | Good | General purpose, most common |
| `bigdecimal` | Arbitrary | Slower | Scientific computing |
| Integer cents | Perfect | Fastest | Simple, fixed precision |

### Integer Cents — Simplest Approach
```rust
// Store as cents (u64 or i64)
struct Money(i64);

impl Money {
    fn from_dollars(d: i64, cents: i64) -> Self {
        Money(d * 100 + cents)
    }

    fn to_f64(&self) -> f64 {
        self.0 as f64 / 100.0
    }
}
```

---

## ⚠️ Error Handling

### thiserror — Library Errors (Typed)
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user not found: {id}")]
    NotFound { id: String },

    #[error("validation failed: {0}")]
    Validation(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
}

// Usage
fn get_user(id: &str) -> Result<User, UserError> {
    Err(UserError::NotFound { id: id.into() })
}
```

### anyhow — Application Errors (Quick)
```rust
use anyhow::{Context, Result, bail, ensure};

fn read_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context("failed to read config file")?;

    let config: Config = toml::from_str(&content)
        .context("failed to parse config")?;

    // Quick validation
    ensure!(!config.api_key.is_empty(), "API key required");

    Ok(config)
}

fn main() -> Result<()> {
    let config = read_config("config.toml")?;

    if config.debug {
        bail!("debug mode not allowed in production");
    }

    Ok(())
}
```

### eyre — Pretty Errors (CLI)
```rust
use eyre::{eyre, Result, WrapErr};
use color_eyre::eyre::Report;

fn main() -> Result<()> {
    color_eyre::install()?;  // Pretty backtraces

    run().wrap_err("application failed")?;
    Ok(())
}
```

**When to use**:
- `thiserror`: Libraries, public APIs (callers handle specific errors)
- `anyhow`: Applications, binaries (just propagate and report)
- `eyre`: CLIs needing pretty error reports

---

## ✅ Validation

### validator — Derive Macros
```rust
use validator::Validate;

#[derive(Debug, Validate)]
struct User {
    #[validate(length(min = 1, max = 100))]
    name: String,

    #[validate(email)]
    email: String,

    #[validate(range(min = 18, max = 120))]
    age: u8,

    #[validate(url)]
    website: Option<String>,

    #[validate(custom(function = "validate_password"))]
    password: String,
}

fn validate_password(password: &str) -> Result<(), validator::ValidationError> {
    if password.len() < 8 {
        return Err(validator::ValidationError::new("password_too_short"));
    }
    Ok(())
}

// Usage
fn register(user: User) -> Result<(), validator::ValidationErrors> {
    user.validate()?;
    // ...
    Ok(())
}
```

### garde — Compile-Time Safety
```rust
use garde::Validate;

#[derive(Validate)]
struct User {
    #[garde(length(min = 1, max = 100))]
    name: String,

    #[garde(email)]
    email: String,

    #[garde(range(min = 18, max = 120))]
    age: u8,
}

// Validation at compile time catches typos
let user = User { /* ... */ };
user.validate(&())?;
```

### nutype — Newtype Validation
```rust
use nutype::nutype;

#[nutype(
    sanitize(trim, lowercase),
    validate(not_empty, len_char_max = 100),
    derive(Debug, Clone, PartialEq, Serialize, Deserialize)
)]
pub struct Username(String);

#[nutype(
    validate(greater_or_equal = 0),
    derive(Debug, Clone, Copy, PartialEq)
)]
pub struct Age(u8);

// Compile-time guaranteed valid types
fn greet(name: Username, age: Age) {
    println!("Hello {}, age {}", name.into_inner(), age.into_inner());
}
```

**When to use**:
- `validator`: Simple struct validation, familiar syntax
- `garde`: Compile-time safety, cleaner error messages
- `nutype`: Domain types that are always valid

---

## 📦 Serialization

### serde — The Standard
```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct User {
    user_id: String,

    #[serde(skip_serializing_if = "Option::is_none")]
    email: Option<String>,

    #[serde(default)]
    is_active: bool,

    #[serde(flatten)]
    metadata: Metadata,
}

#[derive(Debug, Serialize, Deserialize)]
struct Metadata {
    created_at: chrono::DateTime<chrono::Utc>,
}
```

### serde_json — JSON (Default)
```rust
use serde_json::{json, Value};

// Serialize
let json = serde_json::to_string(&user)?;
let pretty = serde_json::to_string_pretty(&user)?;

// Deserialize
let user: User = serde_json::from_str(&json)?;

// Dynamic JSON
let data = json!({
    "name": "John",
    "age": 30,
    "tags": ["admin", "user"]
});
```

### sonic-rs — High Performance (2-3x faster)
```rust
use sonic_rs::{from_str, to_string};

// Drop-in replacement for hot paths
let json = to_string(&user)?;
let user: User = from_str(&json)?;

// Requires SIMD (x86_64, aarch64)
```

```toml
# Cargo.toml
sonic-rs = "0.3"
```

### simd-json — Zero-Copy Fast
```rust
use simd_json::prelude::*;

let mut data = json_string.as_bytes().to_vec();
let parsed: Value = simd_json::to_borrowed_value(&mut data)?;
```

**Performance ranking**: sonic-rs ≈ simd-json > serde_json

---

## 🌐 HTTP Client

### reqwest — Async HTTP (Default)
```rust
use reqwest::Client;

let client = Client::builder()
    .timeout(std::time::Duration::from_secs(10))
    .build()?;

// GET with JSON response
let user: User = client
    .get("https://api.example.com/users/1")
    .bearer_auth(token)
    .send()
    .await?
    .error_for_status()?
    .json()
    .await?;

// POST with JSON body
let response = client
    .post("https://api.example.com/users")
    .json(&new_user)
    .send()
    .await?;
```

### reqwest-middleware — Retry & Tracing
```rust
use reqwest_middleware::{ClientBuilder, ClientWithMiddleware};
use reqwest_retry::{RetryTransientMiddleware, policies::ExponentialBackoff};
use reqwest_tracing::TracingMiddleware;

let retry_policy = ExponentialBackoff::builder().build_with_max_retries(3);
let client: ClientWithMiddleware = ClientBuilder::new(reqwest::Client::new())
    .with(TracingMiddleware::default())
    .with(RetryTransientMiddleware::new_with_policy(retry_policy))
    .build();

let response = client.get("https://api.example.com/data").send().await?;
```

### ureq — Sync HTTP (Simple)
```rust
use ureq;

// Minimal dependencies, no async runtime needed
let body: String = ureq::get("https://api.example.com/data")
    .set("Authorization", &format!("Bearer {}", token))
    .call()?
    .into_string()?;

let user: User = ureq::get("https://api.example.com/users/1")
    .call()?
    .into_json()?;
```

**When to use**:
- `reqwest`: Async apps, full-featured, most common
- `ureq`: Sync apps, CLIs, minimal dependencies
- `hyper`: Low-level control, custom protocols

---

## ⚙️ Configuration

### figment — Layered Config (Recommended)
```rust
use figment::{Figment, providers::{Env, Format, Toml, Serialized}};
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
struct Config {
    port: u16,
    database_url: String,
    debug: bool,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            port: 8080,
            database_url: String::new(),
            debug: false,
        }
    }
}

fn load_config() -> Result<Config, figment::Error> {
    Figment::new()
        .merge(Serialized::defaults(Config::default()))
        .merge(Toml::file("config.toml"))
        .merge(Env::prefixed("APP_").split("_"))
        .extract()
}
```

### config-rs — Alternative
```rust
use config::{Config, File, Environment};

let settings = Config::builder()
    .add_source(File::with_name("config"))
    .add_source(Environment::with_prefix("APP"))
    .build()?;

let port: u16 = settings.get("port")?;
```

### dotenvy — .env Files
```rust
use dotenvy::dotenv;

fn main() {
    dotenv().ok();  // Load .env file

    let db_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
}
```

**When to use**:
- `figment`: Complex layered configs, profiles
- `config-rs`: Simple file + env loading
- `dotenvy`: Just .env files (dev environments)

---

## 🧪 Testing

### Built-in + assert Macros
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_ne!(add(2, 3), 6);
        assert!(is_valid("test"));
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn test_divide_by_zero() {
        divide(1, 0);
    }
}
```

### rstest — Fixtures & Parametrized
```rust
use rstest::{rstest, fixture};

#[fixture]
fn db() -> TestDb {
    TestDb::new()
}

#[rstest]
fn test_user_creation(db: TestDb) {
    let user = db.create_user("test@example.com");
    assert!(user.is_ok());
}

#[rstest]
#[case(2, 3, 5)]
#[case(0, 0, 0)]
#[case(-1, 1, 0)]
fn test_add(#[case] a: i32, #[case] b: i32, #[case] expected: i32) {
    assert_eq!(add(a, b), expected);
}
```

### mockall — Mocking
```rust
use mockall::{automock, predicate::*};

#[automock]
trait UserRepository {
    fn find(&self, id: &str) -> Option<User>;
    fn save(&self, user: &User) -> Result<(), Error>;
}

#[test]
fn test_user_service() {
    let mut mock = MockUserRepository::new();
    mock.expect_find()
        .with(eq("123"))
        .times(1)
        .returning(|_| Some(User { name: "John".into() }));

    let service = UserService::new(Box::new(mock));
    let user = service.get_user("123").unwrap();
    assert_eq!(user.name, "John");
}
```

### proptest — Property-Based Testing
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_parse_roundtrip(s in "\\PC{0,100}") {
        let encoded = encode(&s);
        let decoded = decode(&encoded)?;
        prop_assert_eq!(s, decoded);
    }

    #[test]
    fn test_add_commutative(a in any::<i32>(), b in any::<i32>()) {
        prop_assert_eq!(add(a, b), add(b, a));
    }
}
```

### fake — Test Data Generation
```rust
use fake::{Fake, Faker};
use fake::faker::name::en::*;
use fake::faker::internet::en::*;

let name: String = Name().fake();
let email: String = SafeEmail().fake();
let user: User = Faker.fake();
```

### cargo-nextest — Fast Test Runner
```bash
cargo install cargo-nextest

# Run tests (3x faster than cargo test)
cargo nextest run

# With retries for flaky tests
cargo nextest run --retries 2
```

---

## 📊 Logging & Tracing

### tracing — Structured (Recommended)
```rust
use tracing::{info, warn, error, debug, instrument, span, Level};

#[instrument(skip(password))]
async fn login(username: &str, password: &str) -> Result<User, Error> {
    info!(username, "login attempt");

    let user = db.find_user(username).await?;

    if !verify_password(&user, password) {
        warn!(username, "invalid password");
        return Err(Error::InvalidCredentials);
    }

    info!(user.id, "login successful");
    Ok(user)
}

// Custom spans
fn process_batch(items: &[Item]) {
    let span = span!(Level::INFO, "batch_process", count = items.len());
    let _enter = span.enter();

    for item in items {
        debug!(item.id, "processing");
        // ...
    }
}
```

### tracing-subscriber — Output Setup
```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

fn init_tracing() {
    tracing_subscriber::registry()
        .with(EnvFilter::try_from_default_env().unwrap_or_else(|_| "info".into()))
        .with(tracing_subscriber::fmt::layer().json())  // JSON for production
        .init();
}

// Or simple setup
fn init_simple() {
    tracing_subscriber::fmt()
        .with_env_filter("info,my_app=debug")
        .init();
}
```

### tracing-opentelemetry — Distributed Tracing
```rust
use tracing_opentelemetry::OpenTelemetryLayer;
use opentelemetry::sdk::trace::TracerProvider;

let provider = TracerProvider::builder()
    .with_simple_exporter(exporter)
    .build();

tracing_subscriber::registry()
    .with(OpenTelemetryLayer::new(provider.tracer("my-app")))
    .init();
```

**When to use**:
- `tracing`: Async apps, spans, structured logging
- `log` + `env_logger`: Simple sync apps
- `tracing-opentelemetry`: Distributed systems

---

## 🔐 Security

### Password Hashing — argon2
```rust
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2
};

fn hash_password(password: &str) -> Result<String, argon2::password_hash::Error> {
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    let hash = argon2.hash_password(password.as_bytes(), &salt)?;
    Ok(hash.to_string())
}

fn verify_password(password: &str, hash: &str) -> bool {
    let parsed = PasswordHash::parse(hash, argon2::password_hash::Encoding::B64)
        .expect("invalid hash");
    Argon2::default()
        .verify_password(password.as_bytes(), &parsed)
        .is_ok()
}
```

### secrecy — Secret Handling
```rust
use secrecy::{ExposeSecret, SecretString};

struct Config {
    api_key: SecretString,  // Won't print in Debug
}

fn use_secret(config: &Config) {
    // Must explicitly expose
    let key = config.api_key.expose_secret();
    client.set_header("X-API-Key", key);
}

// Debug output: Config { api_key: SecretString([REDACTED]) }
```

### JWT — jsonwebtoken
```rust
use jsonwebtoken::{encode, decode, Header, Validation, EncodingKey, DecodingKey};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    exp: usize,
}

fn create_token(user_id: &str, secret: &[u8]) -> Result<String, jsonwebtoken::errors::Error> {
    let claims = Claims {
        sub: user_id.into(),
        exp: (chrono::Utc::now() + chrono::Duration::hours(24)).timestamp() as usize,
    };
    encode(&Header::default(), &claims, &EncodingKey::from_secret(secret))
}

fn verify_token(token: &str, secret: &[u8]) -> Result<Claims, jsonwebtoken::errors::Error> {
    let data = decode::<Claims>(token, &DecodingKey::from_secret(secret), &Validation::default())?;
    Ok(data.claims)
}
```

---

## ⚡ Async & Concurrency

### tokio — Runtime (Standard)
```rust
#[tokio::main]
async fn main() -> Result<()> {
    // Full runtime with all features
    run_server().await
}

// Or minimal
#[tokio::main(flavor = "current_thread")]
async fn main() { /* ... */ }
```

```toml
# Cargo.toml - only enable what you need
tokio = { version = "1", features = ["rt-multi-thread", "macros", "net", "time", "sync"] }
```

### tokio::spawn — Concurrent Tasks
```rust
use tokio::task::JoinSet;

async fn fetch_all(urls: Vec<String>) -> Vec<Result<String, Error>> {
    let mut set = JoinSet::new();

    for url in urls {
        set.spawn(async move {
            reqwest::get(&url).await?.text().await
        });
    }

    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        results.push(res.unwrap());
    }
    results
}
```

### tokio::sync — Channels & Primitives
```rust
use tokio::sync::{mpsc, oneshot, Mutex, RwLock, Semaphore};

// Bounded channel
let (tx, mut rx) = mpsc::channel::<Message>(100);

// One-shot for request/response
let (tx, rx) = oneshot::channel::<Response>();

// Semaphore for limiting concurrency
let sem = Arc::new(Semaphore::new(10));
let permit = sem.acquire().await?;
```

### rayon — Parallel Iterators (CPU-bound)
```rust
use rayon::prelude::*;

// Parallel map
let results: Vec<_> = items
    .par_iter()
    .map(|item| expensive_computation(item))
    .collect();

// Parallel for_each
items.par_iter().for_each(|item| {
    process(item);
});
```

---

## 🆔 UUID

### uuid — Standard
```rust
use uuid::Uuid;

let id = Uuid::new_v4();        // Random
let id = Uuid::now_v7();        // Time-ordered (better for DBs)
let id = Uuid::parse_str("...")?;

// In structs
#[derive(Serialize, Deserialize)]
struct User {
    #[serde(default = "Uuid::new_v4")]
    id: Uuid,
}
```

```toml
uuid = { version = "1", features = ["v4", "v7", "serde"] }
```

---

## 🕐 Date & Time

### chrono — Full-Featured
```rust
use chrono::{DateTime, Utc, Duration, NaiveDate};

let now: DateTime<Utc> = Utc::now();
let tomorrow = now + Duration::days(1);

// Parsing
let dt = DateTime::parse_from_rfc3339("2024-01-15T10:30:00Z")?;

// Formatting
let formatted = now.format("%Y-%m-%d %H:%M:%S").to_string();

// In structs (with serde)
#[derive(Serialize, Deserialize)]
struct Event {
    #[serde(with = "chrono::serde::ts_seconds")]
    created_at: DateTime<Utc>,
}
```

### time — Lighter Alternative
```rust
use time::{OffsetDateTime, Duration};

let now = OffsetDateTime::now_utc();
let later = now + Duration::hours(1);
```

---

## 🗃️ Database

### SQLx — Compile-Time Checked SQL (Recommended)
```rust
use sqlx::postgres::PgPoolOptions;

#[derive(sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    email: String,
}

async fn get_user(pool: &PgPool, id: i64) -> Result<User, sqlx::Error> {
    sqlx::query_as!(User, "SELECT id, name, email FROM users WHERE id = $1", id)
        .fetch_one(pool)
        .await
}

async fn create_pool() -> PgPool {
    PgPoolOptions::new()
        .max_connections(5)
        .connect(&std::env::var("DATABASE_URL").unwrap())
        .await
        .unwrap()
}
```

### SeaORM — ORM (If Needed)
```rust
use sea_orm::entity::prelude::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i64,
    pub name: String,
    pub email: String,
}
```

**When to use**:
- `sqlx`: Direct SQL, compile-time checks, most control
- `sea-orm`: Active Record pattern, migrations
- `diesel`: Sync apps, very type-safe

---

## 🗄️ Caching

### moka — High-Performance Cache
```rust
use moka::sync::Cache;
use std::time::Duration;

let cache: Cache<String, User> = Cache::builder()
    .max_capacity(10_000)
    .time_to_live(Duration::from_secs(300))
    .build();

// Get or compute
let user = cache.get_with(user_id, || {
    db.fetch_user(user_id).unwrap()
});

// Async version
use moka::future::Cache;
```

### quick_cache — Simple & Fast
```rust
use quick_cache::sync::Cache;

let cache: Cache<String, String> = Cache::new(1000);
cache.insert("key".into(), "value".into());
let value = cache.get(&"key".into());
```

---

## 💉 Dependency Injection

### Constructor Pattern (Recommended)
```rust
// No framework needed — just constructor injection
struct UserService {
    repo: Box<dyn UserRepository>,
    cache: Arc<dyn Cache>,
}

impl UserService {
    pub fn new(repo: Box<dyn UserRepository>, cache: Arc<dyn Cache>) -> Self {
        Self { repo, cache }
    }
}

// In main
fn main() {
    let repo = Box::new(PostgresUserRepo::new(pool));
    let cache = Arc::new(RedisCache::new(redis));
    let service = UserService::new(repo, cache);
}
```

### shaku — Compile-Time DI (Complex Apps)
```rust
use shaku::{module, Component, Interface};

trait UserRepository: Interface { /* ... */ }

#[derive(Component)]
#[shaku(interface = UserRepository)]
struct PostgresUserRepo {
    #[shaku(inject)]
    pool: Arc<dyn DbPool>,
}

module! {
    AppModule {
        components = [PostgresUserRepo, UserService],
        providers = []
    }
}
```

---

## 📋 Quick Reference

| Category | Recommended | Alternative |
|----------|-------------|-------------|
| **Decimal** | `rust_decimal` | Integer cents |
| **Errors (lib)** | `thiserror` | - |
| **Errors (app)** | `anyhow` | `eyre` (pretty) |
| **Validation** | `validator` | `garde`, `nutype` |
| **Serialization** | `serde` + `serde_json` | `sonic-rs` (perf) |
| **HTTP Client** | `reqwest` | `ureq` (sync) |
| **Config** | `figment` | `config-rs` |
| **Testing** | `rstest` + `mockall` | `proptest` |
| **Logging** | `tracing` | `log` + `env_logger` |
| **Password** | `argon2` | `bcrypt` |
| **JWT** | `jsonwebtoken` | - |
| **Async** | `tokio` | - |
| **Parallelism** | `rayon` | - |
| **UUID** | `uuid` | - |
| **DateTime** | `chrono` | `time` |
| **Database** | `sqlx` | `sea-orm` |
| **Cache** | `moka` | `quick_cache` |
| **DI** | Constructor | `shaku` |
