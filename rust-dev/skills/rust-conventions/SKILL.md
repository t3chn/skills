---
name: rust-conventions
description: Rust project conventions and best practices for code review context. Use with official feature-dev:code-reviewer agent.
globs: ["**/*.rs", "**/Cargo.toml", "**/Cargo.lock"]
---

# Rust Conventions

Context for code review of Rust projects. These conventions inform the official `feature-dev:code-reviewer` agent.

## 2025 Tooling

| Tool | Purpose | Note |
|------|---------|------|
| **cargo-nextest** | Faster test runner | 3x faster than cargo test |
| **miette** | Pretty error reports | Better than anyhow for CLIs |
| **bacon** | Background checker | Replaces cargo watch |

```bash
# Install modern tooling
cargo install cargo-nextest bacon

# Run tests (faster)
cargo nextest run

# Background checks
bacon  # watches and runs clippy/tests
```

### miette for CLI Error Reports
```rust
use miette::{Diagnostic, SourceSpan};
use thiserror::Error;

#[derive(Error, Diagnostic, Debug)]
#[error("invalid config")]
#[diagnostic(code(config::invalid), help("check the config format"))]
pub struct ConfigError {
    #[source_code]
    src: String,
    #[label("this field is wrong")]
    span: SourceSpan,
}
```

## Error Handling

### Use `thiserror` for Library Errors
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("user not found: {0}")]
    NotFound(String),

    #[error("validation failed: {0}")]
    Validation(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("io error")]
    Io(#[from] std::io::Error),
}
```

### Use `anyhow` for Applications
```rust
use anyhow::{Context, Result};

fn read_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context("failed to read config file")?;

    let config: Config = serde_json::from_str(&content)
        .context("failed to parse config")?;

    Ok(config)
}
```

### Propagate with `?` Operator
```rust
// WRONG
match result {
    Ok(v) => v,
    Err(e) => return Err(e),
}

// CORRECT
let value = result?;
```

## Ownership & Borrowing

### Prefer Borrowing Over Cloning
```rust
// WRONG
fn process(data: String) -> String

// CORRECT
fn process(data: &str) -> String
```

### Use `Cow` for Flexible Ownership
```rust
use std::borrow::Cow;

fn normalize_path(path: &str) -> Cow<'_, str> {
    if path.contains("..") {
        Cow::Owned(sanitize(path))
    } else {
        Cow::Borrowed(path)
    }
}
```

### Lifetime Annotations
```rust
// Explicit when needed
struct Parser<'a> {
    input: &'a str,
}

impl<'a> Parser<'a> {
    fn parse(&self) -> &'a str {
        // Returns reference with same lifetime as input
    }
}
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Types/Structs | PascalCase | `UserService`, `HttpClient` |
| Functions | snake_case | `get_user`, `parse_config` |
| Constants | SCREAMING_SNAKE | `MAX_CONNECTIONS` |
| Modules | snake_case | `user_service`, `http` |
| Traits | PascalCase | `Repository`, `Handler` |
| Type Params | Single uppercase | `T`, `E`, `K`, `V` |

## Project Structure

```
src/
├── main.rs              # Entry point
├── lib.rs               # Library root
├── config.rs            # Configuration
├── error.rs             # Error types
├── domain/              # Business logic
│   ├── mod.rs
│   └── user.rs
├── repository/          # Data access
│   ├── mod.rs
│   └── postgres.rs
└── handler/             # HTTP handlers
    ├── mod.rs
    └── user.rs
```

## Testing Patterns

### Unit Tests in Same File
```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_positive() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, 1), 0);
    }
}
```

### Integration Tests in `tests/`
```rust
// tests/api_test.rs
use myapp::create_app;

#[tokio::test]
async fn test_health_endpoint() {
    let app = create_app().await;
    let response = app
        .oneshot(Request::get("/health").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}
```

### Property-Based Testing
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn parse_roundtrip(s in "\\PC*") {
        let parsed = parse(&s)?;
        let serialized = serialize(&parsed);
        prop_assert_eq!(s, serialized);
    }
}
```

## Async Patterns

### Use `tokio` Runtime
```rust
#[tokio::main]
async fn main() -> Result<()> {
    let server = Server::bind(&addr).serve(app);
    server.await?;
    Ok(())
}
```

### Avoid Blocking in Async
```rust
// WRONG - blocks the runtime
let data = std::fs::read_to_string(path)?;

// CORRECT - async file I/O
let data = tokio::fs::read_to_string(path).await?;

// Or spawn blocking for CPU-bound work
let result = tokio::task::spawn_blocking(|| {
    expensive_computation()
}).await?;
```

## Performance

### Avoid Unnecessary Allocations
```rust
// WRONG
fn contains_word(text: &str, word: &str) -> bool {
    text.split_whitespace().collect::<Vec<_>>().contains(&word)
}

// CORRECT - no allocation
fn contains_word(text: &str, word: &str) -> bool {
    text.split_whitespace().any(|w| w == word)
}
```

### Use Iterators
```rust
// WRONG
let mut results = Vec::new();
for item in items {
    if item.is_valid() {
        results.push(item.transform());
    }
}

// CORRECT
let results: Vec<_> = items
    .into_iter()
    .filter(|item| item.is_valid())
    .map(|item| item.transform())
    .collect();
```

## Security

- Use `secrecy` crate for sensitive data
- Validate all external input
- Use parameterized queries (sqlx does this)
- Audit dependencies with `cargo audit`
- Enable all Clippy lints in CI
- Never use `unsafe` without justification

## Clippy Lints

```toml
# Cargo.toml
[lints.clippy]
pedantic = "warn"
unwrap_used = "warn"
expect_used = "warn"
```

## Code Review Checklist

- [ ] Errors use `thiserror`/`anyhow` appropriately
- [ ] No `.unwrap()` outside tests
- [ ] No unnecessary `.clone()`
- [ ] Async code doesn't block
- [ ] Tests cover error paths
- [ ] Clippy passes with pedantic
- [ ] No `unsafe` without comment
- [ ] Lifetimes explicit where needed
