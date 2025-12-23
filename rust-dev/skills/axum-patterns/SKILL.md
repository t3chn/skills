---
name: Axum Patterns
description: This skill should be used when the user asks about "Axum", "Rust web", "Rust API", "Rust handlers", "Rust routing", "tower", or needs guidance on Axum web framework patterns.
version: 1.0.0
---

# Axum Patterns

Production-ready Rust web APIs with Axum.

## Project Structure

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

## Cargo.toml

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
```

## Basic App Setup

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

## Handler Pattern

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

## Error Handling

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

## Middleware & Layers

```rust
use axum::{middleware, Router};
use tower_http::{
    cors::{CorsLayer, Any},
    trace::TraceLayer,
    compression::CompressionLayer,
};

let app = Router::new()
    .route("/api/users", get(list_users))
    .layer(TraceLayer::new_for_http())
    .layer(CompressionLayer::new())
    .layer(
        CorsLayer::new()
            .allow_origin(Any)
            .allow_methods(Any)
            .allow_headers(Any)
    );
```

## Extractors

```rust
use axum::extract::{Path, Query, State, Json, Extension};
use serde::Deserialize;

// Path parameters
async fn get_user(Path(id): Path<i64>) -> String {
    format!("User {id}")
}

// Multiple path params
async fn get_item(Path((user_id, item_id)): Path<(i64, i64)>) -> String {
    format!("User {user_id}, Item {item_id}")
}

// Query parameters
#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    limit: Option<u32>,
}

async fn list_users(Query(params): Query<Pagination>) -> String {
    let page = params.page.unwrap_or(1);
    let limit = params.limit.unwrap_or(20);
    format!("Page {page}, limit {limit}")
}

// JSON body
async fn create_user(Json(payload): Json<CreateUserRequest>) -> impl IntoResponse {
    Json(json!({ "created": payload.name }))
}
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

## Related Skills

- **sqlx** - Database patterns
- **deployment** - Shuttle and Docker
