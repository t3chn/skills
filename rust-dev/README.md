# Rust Development Plugin

Modern Rust backend development toolkit with Axum web framework, SQLx database, teloxide Telegram bots, and deployment patterns.

## Skills

| Skill | Description |
|-------|-------------|
| [essential-libs](./skills/essential-libs/SKILL.md) | **Battle-tested crates** — decimal, errors, validation, HTTP, config, testing |
| [rust-conventions](./skills/rust-conventions/SKILL.md) | Code review context — ownership, error handling, async |
| [axum-patterns](./skills/axum-patterns/SKILL.md) | Axum web framework, handlers, extractors, middleware |
| [sqlx](./skills/sqlx/SKILL.md) | Type-safe SQL with compile-time checking |
| [teloxide](./skills/teloxide/SKILL.md) | Telegram bot framework |
| [deployment](./skills/deployment/SKILL.md) | Shuttle.dev, Docker, Caddy deployment |

## Agents

| Agent | Description |
|-------|-------------|
| [rust-test-generator](./agents/rust-test-generator/AGENT.md) | Generates Rust tests with proper patterns |

> **Code Review:** Use official `feature-dev:code-reviewer` with `rust-conventions` skill for context.

## Commands

| Command | Description |
|---------|-------------|
| `/rust-test` | Run cargo test |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| cargo-fmt-check | PreToolUse | Reminds to run cargo fmt after Rust changes |

## Quick Start

### New API Project

```bash
cargo new myapp && cd myapp
```

```toml
# Cargo.toml
[dependencies]
axum = "0.8"
tokio = { version = "1", features = ["full"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
serde = { version = "1", features = ["derive"] }
tracing = "0.1"
tracing-subscriber = "0.3"
thiserror = "2"
```

### New Bot Project

```bash
cargo new mybot && cd mybot
```

```toml
# Cargo.toml
[dependencies]
teloxide = { version = "0.13", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
dotenvy = "0.15"
```

### Run Tests

```bash
cargo test
cargo test -- --nocapture  # With output
```

### Lint & Format

```bash
cargo fmt
cargo clippy -- -D warnings
```

## Stack

- **Rust 2024 Edition** - Latest features
- **Axum 0.8** - Web framework
- **SQLx 0.8** - Type-safe SQL
- **teloxide 0.13** - Telegram bots
- **tokio** - Async runtime
- **thiserror/anyhow** - Error handling

## Deployment

| Apps | Recommendation |
|------|----------------|
| 1 | Shuttle.dev ($0) |
| 2+ | VPS + Docker + Caddy (€17/mo) |

## Related

- [backend-core](../backend-core/SKILL.md) - Language-agnostic API patterns
- [secrets-guardian](../secrets-guardian/SKILL.md) - Pre-commit security
