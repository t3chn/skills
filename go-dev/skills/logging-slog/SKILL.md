---
name: Go Structured Logging
description: This skill should be used when the user asks about "Go logging", "slog", "structured logging Go", "log/slog", "JSON logging Go", "logging best practices Go", "logger injection", "log levels Go", "zerolog", "zap logging", or needs guidance on modern structured logging patterns in Go (2024-2025).
version: 1.0.0
---

# Go Structured Logging — Modern Best Practices (2024-2025)

## Why Structured Logging?

- **Machine-readable**: JSON format for log aggregation (ELK, Datadog, etc.)
- **Queryable**: Filter by fields, not regex
- **Context-rich**: Attach request IDs, user IDs, etc.
- **Performance**: Zero-allocation in hot paths (slog, zap, zerolog)

## Standard Library: log/slog (Go 1.21+)

### Basic Setup

```go
package main

import (
    "log/slog"
    "os"
)

func main() {
    // JSON handler for production
    logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    }))

    // Set as default
    slog.SetDefault(logger)

    // Usage
    slog.Info("server started", "port", 8080)
    slog.Error("request failed", "error", err, "path", "/api/users")
}
```

**Output:**
```json
{"time":"2024-01-15T10:30:00Z","level":"INFO","msg":"server started","port":8080}
{"time":"2024-01-15T10:30:01Z","level":"ERROR","msg":"request failed","error":"connection refused","path":"/api/users"}
```

### Text Handler for Development

```go
// Human-readable for local development
logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelDebug,
}))
```

**Output:**
```
time=2024-01-15T10:30:00Z level=INFO msg="server started" port=8080
```

### Handler Options

```go
opts := &slog.HandlerOptions{
    Level:     slog.LevelDebug,           // Minimum level
    AddSource: true,                       // Include file:line
    ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
        // Customize attribute names
        if a.Key == slog.TimeKey {
            a.Key = "timestamp"
        }
        return a
    },
}
```

## Logger Injection Pattern

### Service with Logger

```go
// internal/service/user.go
package service

import "log/slog"

type UserService struct {
    logger *slog.Logger
    repo   UserRepository
}

func NewUserService(logger *slog.Logger, repo UserRepository) *UserService {
    return &UserService{
        logger: logger.With("service", "user"),  // Add context
        repo:   repo,
    }
}

func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    s.logger.DebugContext(ctx, "getting user", "id", id)

    user, err := s.repo.Get(ctx, id)
    if err != nil {
        s.logger.ErrorContext(ctx, "failed to get user", "id", id, "error", err)
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }

    return user, nil
}
```

### HTTP Handler with Request Context

```go
// internal/middleware/logging.go
package middleware

import (
    "log/slog"
    "net/http"
    "time"
)

func Logging(logger *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()

            // Add request context to logger
            reqLogger := logger.With(
                "method", r.Method,
                "path", r.URL.Path,
                "request_id", r.Header.Get("X-Request-ID"),
            )

            // Store logger in context for handlers
            ctx := context.WithValue(r.Context(), loggerKey, reqLogger)

            // Wrap response writer to capture status
            rw := &responseWriter{ResponseWriter: w, status: 200}

            next.ServeHTTP(rw, r.WithContext(ctx))

            reqLogger.Info("request completed",
                "status", rw.status,
                "duration_ms", time.Since(start).Milliseconds(),
            )
        })
    }
}

// Get logger from context
func LoggerFromContext(ctx context.Context) *slog.Logger {
    if logger, ok := ctx.Value(loggerKey).(*slog.Logger); ok {
        return logger
    }
    return slog.Default()
}
```

## Log Levels

| Level | When to Use |
|-------|-------------|
| `Debug` | Detailed troubleshooting info (disabled in prod) |
| `Info` | Normal operations, milestones |
| `Warn` | Unexpected but recoverable situations |
| `Error` | Failures requiring attention |

```go
slog.Debug("cache miss", "key", key)
slog.Info("user logged in", "user_id", userID)
slog.Warn("retry attempt", "attempt", 3, "max", 5)
slog.Error("database connection failed", "error", err)
```

## Grouping Attributes

```go
// Group related fields
slog.Info("request processed",
    slog.Group("request",
        "method", "POST",
        "path", "/api/users",
    ),
    slog.Group("response",
        "status", 201,
        "body_size", 256,
    ),
)
```

**Output:**
```json
{
  "level": "INFO",
  "msg": "request processed",
  "request": {"method": "POST", "path": "/api/users"},
  "response": {"status": 201, "body_size": 256}
}
```

## Environment-Based Configuration

```go
func NewLogger(env string) *slog.Logger {
    var handler slog.Handler

    switch env {
    case "production":
        handler = slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
            Level: slog.LevelInfo,
        })
    case "development":
        handler = slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
            Level:     slog.LevelDebug,
            AddSource: true,
        })
    default:
        handler = slog.NewTextHandler(os.Stdout, nil)
    }

    return slog.New(handler)
}
```

## Context-Aware Logging

```go
// Always use *Context variants when context is available
func (s *Service) Process(ctx context.Context, id string) error {
    // Good: includes trace ID, request ID from context
    s.logger.InfoContext(ctx, "processing", "id", id)

    // Avoid: loses context information
    s.logger.Info("processing", "id", id)
}
```

## Alternatives to slog

### zerolog (Zero-allocation)

```go
import "github.com/rs/zerolog"

logger := zerolog.New(os.Stdout).With().Timestamp().Logger()
logger.Info().Str("user", "alice").Msg("logged in")
```

### zap (Uber)

```go
import "go.uber.org/zap"

logger, _ := zap.NewProduction()
defer logger.Sync()
logger.Info("logged in", zap.String("user", "alice"))
```

## Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| `log.Printf("%v", err)` | `slog.Error("msg", "error", err)` |
| Log and return error | Choose one: log OR return |
| String concatenation | Use structured attributes |
| Global logger everywhere | Inject logger into services |
| Logging sensitive data | Redact passwords, tokens, PII |

## Testing with Logs

```go
func TestServiceLogging(t *testing.T) {
    var buf bytes.Buffer
    logger := slog.New(slog.NewJSONHandler(&buf, nil))

    svc := NewService(logger)
    svc.DoSomething()

    // Verify log output
    assert.Contains(t, buf.String(), `"msg":"operation completed"`)
}
```

## Related Skills

- **Error Handling** — Logging errors properly
- **Project Structure** — Where to configure logger

## References

- [Go Blog: Structured Logging with slog](https://go.dev/blog/slog)
- [slog Package Documentation](https://pkg.go.dev/log/slog)
