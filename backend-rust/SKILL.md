---
name: backend-rust
description: |
  Rust backend development with Axum, SQLx, teloxide (Telegram bots).
  Deployment: Shuttle.dev (single app, $0) or VPS + Docker + Caddy (multiple apps, ~€17/mo).
  Triggers: "rust backend", "axum", "teloxide", "telegram bot rust", "shuttle", "caddy", "deploy rust"
---

# Rust Backend Development

Modern Rust backend with Axum, SQLx, teloxide. Cost-optimized deployment.

**For general patterns** (API design, auth, security, architecture): use `backend-core`

## Build & Run

**Compile locally by default** — remote servers may be too weak for Rust compilation. Deploy pre-built binaries unless user explicitly requests remote build.

```bash
# Same architecture (Linux → Linux)
cargo build --release
scp target/release/myapp server:

# Cross-compile (macOS → Linux)
rustup target add x86_64-unknown-linux-gnu
cargo build --release --target x86_64-unknown-linux-gnu
scp target/x86_64-unknown-linux-gnu/release/myapp server:
```

## Deployment Strategy

```
HOW MANY APPS?
│
├─ Single app, zero config → Shuttle.dev ($0)
│
└─ Multiple apps → VPS + Docker + Caddy (~€17/mo)
    └─ Unlimited apps, DBs, bots on one server
```

**Cost comparison:**

| Apps | Per-app PaaS | VPS + Caddy |
|------|--------------|-------------|
| 1 | $0-5 | €17 |
| 3 | $15 | €17 |
| 5 | $25 | €17 |
| 10 | $50 | €17 |

**Recommendation:** Start with Shuttle. Move to VPS + Caddy when you have 2+ apps.

## Project Setup

### Cargo.toml (API Service)

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2024"

[dependencies]
axum = "0.8"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite", "postgres"] }
tower-http = { version = "0.6", features = ["cors", "trace"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
thiserror = "2"
anyhow = "1"

# For Shuttle deployment
shuttle-runtime = "0.51"
shuttle-axum = "0.51"
```

### Cargo.toml (Telegram Bot)

```toml
[package]
name = "mybot"
version = "0.1.0"
edition = "2024"

[dependencies]
teloxide = { version = "0.13", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
tracing = "0.1"
tracing-subscriber = "0.3"
dotenvy = "0.15"
```

### Project Structure

```
src/
├── main.rs           # Entry point
├── lib.rs            # Re-exports for testing
├── config.rs         # Environment config
├── error.rs          # Error types
├── handlers/
│   ├── mod.rs
│   └── users.rs
├── models/
│   ├── mod.rs
│   └── user.rs
├── db/
│   ├── mod.rs
│   └── migrations/
└── services/
    ├── mod.rs
    └── user_service.rs
```

## Axum Patterns

### Basic App Setup

```rust
use axum::{routing::get, Router};
use std::net::SocketAddr;
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    let app = Router::new()
        .route("/health", get(|| async { "OK" }))
        .route("/api/users", get(list_users).post(create_user))
        .route("/api/users/:id", get(get_user))
        .layer(TraceLayer::new_for_http());

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    tracing::info!("Listening on {addr}");

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### Handler Pattern

```rust
use axum::{
    extract::{Path, State, Json},
    http::StatusCode,
    response::IntoResponse,
};
use serde::{Deserialize, Serialize};

#[derive(Clone)]
pub struct AppState {
    pub db: sqlx::SqlitePool,
}

#[derive(Deserialize)]
pub struct CreateUserRequest {
    pub email: String,
    pub name: String,
}

#[derive(Serialize)]
pub struct UserResponse {
    pub id: i64,
    pub email: String,
    pub name: String,
}

pub async fn create_user(
    State(state): State<AppState>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<impl IntoResponse, AppError> {
    let user = sqlx::query_as!(
        UserResponse,
        r#"INSERT INTO users (email, name) VALUES (?, ?) RETURNING id, email, name"#,
        payload.email,
        payload.name
    )
    .fetch_one(&state.db)
    .await?;

    Ok((StatusCode::CREATED, Json(user)))
}

pub async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<impl IntoResponse, AppError> {
    let user = sqlx::query_as!(
        UserResponse,
        r#"SELECT id, email, name FROM users WHERE id = ?"#,
        id
    )
    .fetch_optional(&state.db)
    .await?
    .ok_or(AppError::NotFound)?;

    Ok(Json(user))
}
```

### Error Handling

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Not found")]
    NotFound,

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Internal error")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound => (StatusCode::NOT_FOUND, self.to_string()),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::Database(_) => {
                tracing::error!("Database error: {:?}", self);
                (StatusCode::INTERNAL_SERVER_ERROR, "Database error".into())
            }
            AppError::Internal(_) => {
                tracing::error!("Internal error: {:?}", self);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal error".into())
            }
        };

        (status, Json(json!({ "error": message }))).into_response()
    }
}
```

## SQLx Patterns

### Database Setup

```rust
use sqlx::sqlite::SqlitePoolOptions;

pub async fn init_db(database_url: &str) -> sqlx::SqlitePool {
    SqlitePoolOptions::new()
        .max_connections(5)
        .connect(database_url)
        .await
        .expect("Failed to create pool")
}

// Run migrations
sqlx::migrate!("./migrations")
    .run(&pool)
    .await
    .expect("Failed to run migrations");
```

### Migration (migrations/001_init.sql)

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    due_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Queries with sqlx::query_as!

```rust
// Type-safe query with compile-time checking
let users = sqlx::query_as!(
    User,
    r#"SELECT id, email, name, created_at FROM users WHERE email LIKE ?"#,
    format!("%{}%", search)
)
.fetch_all(&pool)
.await?;

// Insert and return
let task = sqlx::query_as!(
    Task,
    r#"INSERT INTO tasks (user_id, title, due_at)
       VALUES (?, ?, ?)
       RETURNING id, user_id, title, completed as "completed: bool", due_at, created_at"#,
    user_id,
    title,
    due_at
)
.fetch_one(&pool)
.await?;
```

## Teloxide (Telegram Bot)

### Basic Bot

```rust
use teloxide::{prelude::*, utils::command::BotCommands};

#[derive(BotCommands, Clone)]
#[command(rename_rule = "lowercase", description = "Available commands:")]
enum Command {
    #[command(description = "Start the bot")]
    Start,
    #[command(description = "Show help")]
    Help,
    #[command(description = "Add a task")]
    Add(String),
    #[command(description = "List tasks")]
    Tasks,
}

#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();
    tracing_subscriber::fmt::init();

    let bot = Bot::from_env();

    Command::repl(bot, handle_command).await;
}

async fn handle_command(bot: Bot, msg: Message, cmd: Command) -> ResponseResult<()> {
    match cmd {
        Command::Start => {
            bot.send_message(msg.chat.id, "Welcome! Use /help to see commands.").await?;
        }
        Command::Help => {
            bot.send_message(msg.chat.id, Command::descriptions().to_string()).await?;
        }
        Command::Add(task) => {
            // Add task to database
            bot.send_message(msg.chat.id, format!("Task added: {task}")).await?;
        }
        Command::Tasks => {
            // Fetch from database
            bot.send_message(msg.chat.id, "Your tasks:\n1. Example task").await?;
        }
    }
    Ok(())
}
```

### Bot with State and Dialogue

```rust
use teloxide::{
    dispatching::{dialogue, dialogue::InMemStorage, UpdateHandler},
    prelude::*,
};

type MyDialogue = Dialogue<State, InMemStorage<State>>;
type HandlerResult = Result<(), Box<dyn std::error::Error + Send + Sync>>;

#[derive(Clone, Default)]
pub enum State {
    #[default]
    Start,
    ReceiveTaskTitle,
    ReceiveTaskDueDate { title: String },
}

fn schema() -> UpdateHandler<Box<dyn std::error::Error + Send + Sync + 'static>> {
    use dptree::case;

    let command_handler = teloxide::filter_command::<Command, _>()
        .branch(case![Command::Start].endpoint(start))
        .branch(case![Command::Add].endpoint(add_task_start));

    let message_handler = Update::filter_message()
        .branch(command_handler)
        .branch(case![State::ReceiveTaskTitle].endpoint(receive_title))
        .branch(case![State::ReceiveTaskDueDate { title }].endpoint(receive_due_date));

    dialogue::enter::<Update, InMemStorage<State>, State, _>()
        .branch(message_handler)
}

async fn start(bot: Bot, dialogue: MyDialogue, msg: Message) -> HandlerResult {
    dialogue.update(State::Start).await?;
    bot.send_message(msg.chat.id, "Welcome!").await?;
    Ok(())
}

async fn add_task_start(bot: Bot, dialogue: MyDialogue, msg: Message) -> HandlerResult {
    dialogue.update(State::ReceiveTaskTitle).await?;
    bot.send_message(msg.chat.id, "What's the task title?").await?;
    Ok(())
}

async fn receive_title(bot: Bot, dialogue: MyDialogue, msg: Message) -> HandlerResult {
    if let Some(title) = msg.text() {
        dialogue.update(State::ReceiveTaskDueDate { title: title.into() }).await?;
        bot.send_message(msg.chat.id, "When is it due? (YYYY-MM-DD)").await?;
    }
    Ok(())
}
```

### Inline Keyboards

```rust
use teloxide::types::{InlineKeyboardButton, InlineKeyboardMarkup};

fn task_keyboard(task_id: i64) -> InlineKeyboardMarkup {
    InlineKeyboardMarkup::new(vec![
        vec![
            InlineKeyboardButton::callback("✅ Done", format!("done_{task_id}")),
            InlineKeyboardButton::callback("🗑 Delete", format!("delete_{task_id}")),
        ],
        vec![
            InlineKeyboardButton::callback("⏰ Snooze 1h", format!("snooze_{task_id}_1h")),
            InlineKeyboardButton::callback("📅 Tomorrow", format!("snooze_{task_id}_1d")),
        ],
    ])
}

// Handle callback
async fn handle_callback(bot: Bot, q: CallbackQuery) -> HandlerResult {
    if let Some(data) = q.data {
        if data.starts_with("done_") {
            let task_id: i64 = data.strip_prefix("done_").unwrap().parse()?;
            // Mark as done in database
            bot.answer_callback_query(&q.id).await?;
            if let Some(msg) = q.message {
                bot.edit_message_text(msg.chat.id, msg.id, "✅ Task completed!").await?;
            }
        }
    }
    Ok(())
}
```

## Deployment

### Option 1: Shuttle.dev (Single App, Zero Config)

Best for: First app, quick prototypes, $0 budget.

```rust
// src/main.rs for Shuttle
use axum::Router;
use shuttle_axum::ShuttleAxum;

#[shuttle_runtime::main]
async fn main() -> ShuttleAxum {
    let router = Router::new()
        .route("/", axum::routing::get(|| async { "Hello from Shuttle!" }));

    Ok(router.into())
}
```

```bash
cargo shuttle deploy
```

### Option 2: VPS + Docker + Caddy (Multiple Apps)

Best for: 2+ apps, telegram bots, full control, predictable costs.

**VPS Providers (EU):**
- OVH Kimsufi: €17/mo (4c/8t, 32GB RAM, 2x450GB SSD)
- Hetzner CX22: €4.5/mo (2 vCPU, 4GB RAM) — lighter workloads

**Dockerfile (universal):**

```dockerfile
FROM rust:1.83-slim AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && cargo build --release && rm -rf src
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/myapp /usr/local/bin/
ENV RUST_LOG=info
CMD ["myapp"]
```

**Caddyfile:**

```
myapp.example.com {
    reverse_proxy myapp:3000
}

api.example.com {
    reverse_proxy api:8080
}

# Add more apps as needed
```

**docker-compose.yml:**

```yaml
services:
  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config

  myapp:
    build: .
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/app
      - RUST_LOG=info

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  caddy_data:
  caddy_config:
  pgdata:
```

```bash
docker compose up -d
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use axum::http::StatusCode;
    use axum_test::TestServer;

    #[tokio::test]
    async fn test_create_user() {
        let pool = init_test_db().await;
        let app = create_app(pool);
        let server = TestServer::new(app).unwrap();

        let response = server
            .post("/api/users")
            .json(&serde_json::json!({
                "email": "test@example.com",
                "name": "Test User"
            }))
            .await;

        assert_eq!(response.status_code(), StatusCode::CREATED);
    }
}
```

## Anti-patterns

- `unwrap()` in production → `?` with proper error types
- `clone()` everywhere → `Arc<T>` for shared state
- Blocking in async → `tokio::task::spawn_blocking`
- Raw SQL strings → `sqlx::query_as!` for type safety
- `println!` → `tracing::info!`
- `.env` in git → use secrets management
