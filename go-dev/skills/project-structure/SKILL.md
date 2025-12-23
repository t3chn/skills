---
name: Go Project Structure
description: This skill should be used when the user asks to "create a Go project", "structure Go code", "organize Go packages", "set up Go project layout", "use internal/ or pkg/", "Go module structure", "cmd/ directory pattern", "where to put main.go", "Go clean architecture", "hexagonal architecture Go", "Go project best practices", "Go monorepo structure", or needs guidance on idiomatic Go project organization following 2024-2025 best practices.
version: 1.0.0
---

# Go Project Structure — Modern Best Practices (2024-2025)

## Core Principle

**Simplicity first, complexity when necessary.** Start with what you need today, refactor as your project grows. Go's minimalist philosophy extends to project organization.

## Standard Directory Layout

```
project/
├── cmd/                    # Application entry points
│   └── myapp/
│       └── main.go         # main package, minimal code
├── internal/               # Private packages (compiler-enforced)
│   ├── config/             # Configuration loading
│   ├── storage/            # Data layer interfaces + implementations
│   │   ├── storage.go      # Interface definitions
│   │   └── sqlite/         # Concrete implementation
│   ├── types/              # Domain types, enums, validation
│   └── <feature>/          # Feature-specific packages
├── pkg/                    # Public reusable packages (optional)
├── api/                    # OpenAPI specs, proto files
├── web/                    # Static assets, templates
├── scripts/                # Build, install, CI scripts
├── docs/                   # Documentation
├── tests/                  # Additional test data, integration tests
├── .golangci.yml           # Linter configuration
├── Taskfile.yml            # Task runner (preferred over Makefile)
├── go.mod
├── go.sum
├── README.md
└── CLAUDE.md               # AI agent instructions
```

## Key Directories Explained

### `cmd/` — Entry Points
Each subdirectory is a separate binary. Keep main.go minimal:

```go
// cmd/myapp/main.go
package main

import (
    "os"
    "myapp/internal/app"
)

func main() {
    if err := app.Run(os.Args[1:]); err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }
}
```

### `internal/` — Private Packages
**Compiler-enforced privacy.** Code here cannot be imported by external projects. Perfect for:
- Business logic
- Domain types
- Storage implementations
- Utilities not meant for reuse

### `pkg/` — Public Libraries
**Only use if you're building a library** that others will import. Many projects don't need this.

## Architecture Patterns

### Group-by-Feature (Recommended for most projects)

```
internal/
├── user/
│   ├── handler.go      # HTTP handlers
│   ├── service.go      # Business logic
│   ├── repository.go   # Data access
│   └── user.go         # Types
├── order/
│   ├── handler.go
│   ├── service.go
│   └── order.go
└── shared/             # Cross-cutting concerns
    ├── middleware/
    └── errors/
```

### Clean/Hexagonal Architecture (For complex systems)

```
internal/
├── domain/             # Core business logic (no external deps)
│   ├── user.go
│   └── order.go
├── application/        # Use cases, orchestration
│   ├── user_service.go
│   └── order_service.go
├── infrastructure/     # External concerns
│   ├── persistence/    # Database implementations
│   ├── http/           # HTTP handlers
│   └── messaging/      # Queue implementations
└── interfaces/         # Port definitions
    ├── repository.go
    └── notifier.go
```

## Interface Design

### Define Interfaces Where They're Used

```go
// internal/user/service.go
package user

// Repository defines what the service needs (consumer-side interface)
type Repository interface {
    Get(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, u *User) error
}

type Service struct {
    repo Repository
}
```

### Storage Interface Pattern

```go
// internal/storage/storage.go
package storage

type Storage interface {
    // Core operations
    Create(ctx context.Context, item *types.Item) error
    Get(ctx context.Context, id string) (*types.Item, error)
    Update(ctx context.Context, id string, updates map[string]interface{}) error
    Delete(ctx context.Context, id string) error

    // Transactions
    RunInTransaction(ctx context.Context, fn func(tx Transaction) error) error

    // Lifecycle
    Close() error
}

type Transaction interface {
    Create(ctx context.Context, item *types.Item) error
    Get(ctx context.Context, id string) (*types.Item, error)
    // ... subset of Storage methods
}
```

## Package Naming

| Pattern | Example | Use |
|---------|---------|-----|
| Singular nouns | `user`, `order` | Domain packages |
| Descriptive | `storage`, `config` | Infrastructure |
| Avoid stutter | `user.User` not `user.UserModel` | Types |
| No `util`, `common` | Split into specific packages | Always |

## Anti-Patterns to Avoid

1. **Over-engineering early** — Don't create 10 packages for a 500-line app
2. **`pkg/` for everything** — Only for truly reusable libraries
3. **Circular imports** — Design clear dependency direction
4. **God packages** — Split large packages by responsibility
5. **`utils/` or `helpers/`** — Be specific: `stringutil`, `httputil`

## Migration Strategy

**Starting small:**
```
project/
├── main.go
├── handlers.go
├── storage.go
└── types.go
```

**Growing:**
```
project/
├── cmd/myapp/main.go
├── internal/
│   ├── handler/
│   ├── storage/
│   └── types/
```

## Related Skills

- **Error Handling** — Patterns for error types in your packages
- **Testing Patterns** — Test file organization and fixtures
- **Taskfile Automation** — Build automation for your structure

## References

- [golang-standards/project-layout](https://github.com/golang-standards/project-layout) (community convention)
- [bxcodec/go-clean-arch](https://github.com/bxcodec/go-clean-arch) (clean architecture example)
