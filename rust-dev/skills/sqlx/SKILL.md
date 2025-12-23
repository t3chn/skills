---
name: SQLx
description: This skill should be used when the user asks about "SQLx", "Rust database", "Rust SQL", "Rust migrations", "Rust postgres", "Rust sqlite", or needs guidance on SQLx database patterns.
version: 1.0.0
---

# SQLx

Type-safe SQL for Rust with compile-time checked queries.

## Setup

```toml
# Cargo.toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite", "postgres"] }
```

## Database Connection

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

## Migrations

```sql
-- migrations/001_init.sql
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

## Type-Safe Queries

### query_as! Macro

```rust
use sqlx::FromRow;

#[derive(FromRow)]
pub struct User {
    pub id: i64,
    pub email: String,
    pub name: String,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

// Type-safe query with compile-time checking
let users = sqlx::query_as!(
    User,
    r#"SELECT id, email, name, created_at FROM users WHERE email LIKE ?"#,
    format!("%{}%", search)
)
.fetch_all(&pool)
.await?;
```

### Insert and Return

```rust
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

### Type Overrides

```rust
// For nullable columns
let user = sqlx::query_as!(
    User,
    r#"SELECT id, email, name as "name?", bio as "bio?" FROM users WHERE id = ?"#,
    id
)
.fetch_one(&pool)
.await?;

// For boolean conversion
let task = sqlx::query_as!(
    Task,
    r#"SELECT completed as "completed: bool" FROM tasks"#
)
.fetch_one(&pool)
.await?;
```

## Dynamic Queries

```rust
use sqlx::QueryBuilder;

let mut query = QueryBuilder::new("SELECT * FROM users WHERE 1=1");

if let Some(email) = email_filter {
    query.push(" AND email LIKE ");
    query.push_bind(format!("%{}%", email));
}

if let Some(name) = name_filter {
    query.push(" AND name LIKE ");
    query.push_bind(format!("%{}%", name));
}

let users = query
    .build_query_as::<User>()
    .fetch_all(&pool)
    .await?;
```

## Transactions

```rust
let mut tx = pool.begin().await?;

let user = sqlx::query_as!(
    User,
    "INSERT INTO users (email, name) VALUES (?, ?) RETURNING *",
    email,
    name
)
.fetch_one(&mut *tx)
.await?;

sqlx::query!(
    "INSERT INTO user_profiles (user_id) VALUES (?)",
    user.id
)
.execute(&mut *tx)
.await?;

tx.commit().await?;
```

## Batch Operations

```rust
// Batch insert
let values = vec![
    ("user1@example.com", "User 1"),
    ("user2@example.com", "User 2"),
];

let mut query = QueryBuilder::new("INSERT INTO users (email, name) ");
query.push_values(values.iter(), |mut b, (email, name)| {
    b.push_bind(email).push_bind(name);
});

query.build().execute(&pool).await?;
```

## PostgreSQL Specific

```rust
// Array types
let tags = vec!["rust", "axum"];
sqlx::query!(
    "INSERT INTO posts (title, tags) VALUES ($1, $2)",
    title,
    &tags as &[&str]
)
.execute(&pool)
.await?;

// JSON
use sqlx::types::Json;
#[derive(Serialize, Deserialize)]
struct Metadata { views: i64 }

sqlx::query!(
    "INSERT INTO posts (metadata) VALUES ($1)",
    Json(Metadata { views: 0 }) as _
)
.execute(&pool)
.await?;
```

## CLI Commands

```bash
# Create database
sqlx database create

# Run migrations
sqlx migrate run

# Revert migration
sqlx migrate revert

# Generate offline data (for CI)
cargo sqlx prepare

# Check queries
cargo sqlx prepare --check
```

## Related Skills

- **axum-patterns** - Web framework integration
- **deployment** - Database in production
