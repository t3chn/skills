---
name: Rust Deployment
description: This skill should be used when the user asks about "deploy Rust", "Shuttle.dev", "Rust Docker", "Caddy reverse proxy", "Rust production", or needs guidance on deploying Rust applications.
version: 1.0.0
---

# Rust Deployment

Cost-optimized deployment strategies for Rust applications.

## Build Strategy

**Compile locally by default** - remote servers may be too weak for Rust compilation.

```bash
# Same architecture (Linux → Linux)
cargo build --release
scp target/release/myapp server:

# Cross-compile (macOS → Linux)
rustup target add x86_64-unknown-linux-gnu
cargo build --release --target x86_64-unknown-linux-gnu
scp target/x86_64-unknown-linux-gnu/release/myapp server:
```

## Deployment Decision Tree

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

## Option 1: Shuttle.dev

Best for: First app, quick prototypes, $0 budget.

### Setup

```rust
// src/main.rs
use axum::Router;
use shuttle_axum::ShuttleAxum;

#[shuttle_runtime::main]
async fn main() -> ShuttleAxum {
    let router = Router::new()
        .route("/", axum::routing::get(|| async { "Hello from Shuttle!" }));

    Ok(router.into())
}
```

```toml
# Cargo.toml
[dependencies]
axum = "0.8"
shuttle-runtime = "0.51"
shuttle-axum = "0.51"
```

### Deploy

```bash
cargo shuttle deploy
```

### With Database

```rust
use shuttle_runtime::SecretStore;
use sqlx::PgPool;

#[shuttle_runtime::main]
async fn main(
    #[shuttle_shared_db::Postgres] pool: PgPool,
    #[shuttle_runtime::Secrets] secrets: SecretStore,
) -> ShuttleAxum {
    sqlx::migrate!().run(&pool).await.expect("migrations");

    let state = AppState { db: pool };
    let router = create_router(state);

    Ok(router.into())
}
```

## Option 2: VPS + Docker + Caddy

Best for: 2+ apps, telegram bots, full control, predictable costs.

### VPS Providers (EU)

- **OVH Kimsufi**: €17/mo (4c/8t, 32GB RAM, 2x450GB SSD)
- **Hetzner CX22**: €4.5/mo (2 vCPU, 4GB RAM) - lighter workloads

### Dockerfile

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

### Caddyfile

```
myapp.example.com {
    reverse_proxy myapp:3000
}

api.example.com {
    reverse_proxy api:8080
}

# Add more apps as needed
```

### docker-compose.yml

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

### Deploy

```bash
docker compose up -d
```

## Systemd Service (Without Docker)

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Rust App
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/myapp
Restart=on-failure
Environment=RUST_LOG=info
Environment=DATABASE_URL=sqlite:/opt/myapp/data.db

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable myapp
sudo systemctl start myapp
sudo systemctl status myapp
```

## Telegram Bot Deployment

For bots, you don't need a web server - just the binary running:

```yaml
# docker-compose.yml
services:
  bot:
    build: .
    restart: unless-stopped
    environment:
      - TELOXIDE_TOKEN=your_token
      - DATABASE_URL=sqlite:/data/bot.db
    volumes:
      - bot_data:/data

volumes:
  bot_data:
```

## Health Checks

```rust
// Add health endpoint
app.route("/health", get(|| async { "OK" }));
```

```yaml
# docker-compose.yml
services:
  myapp:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Related Skills

- **axum-patterns** - Web framework
- **teloxide** - Telegram bots
