---
name: Go Context Patterns
description: This skill should be used when the user asks about "Go context", "context.Context", "context cancellation", "context timeout", "context deadline", "context values", "WithCancel", "WithTimeout", "context best practices", "passing context", or needs guidance on proper context usage in Go.
version: 1.0.0
---

# Go Context Patterns — Modern Best Practices (2024-2025)

## What Context Solves

- **Cancellation**: Stop work when caller is gone (HTTP client disconnects)
- **Deadlines**: Set maximum time for operations
- **Request-scoped values**: Trace IDs, auth tokens (use sparingly)

## Core Rules

1. **Context is the first parameter** — Always `func Foo(ctx context.Context, ...)`
2. **Don't store context** — Pass it through, don't put in structs
3. **Don't pass nil** — Use `context.Background()` or `context.TODO()`
4. **Values for request-scoped data only** — Not for function options

## Creating Contexts

### Background vs TODO

```go
// context.Background() — Root context for main, init, tests
func main() {
    ctx := context.Background()
    server.Run(ctx)
}

// context.TODO() — Placeholder when unsure what context to use
func legacyFunction() {
    ctx := context.TODO() // Will be updated when caller passes context
    doWork(ctx)
}
```

### Cancellation

```go
func processWithCancel(ctx context.Context) error {
    ctx, cancel := context.WithCancel(ctx)
    defer cancel() // Always call cancel to release resources

    // Start worker goroutine
    errCh := make(chan error, 1)
    go func() {
        errCh <- doWork(ctx)
    }()

    select {
    case err := <-errCh:
        return err
    case <-ctx.Done():
        return ctx.Err() // context.Canceled or context.DeadlineExceeded
    }
}
```

### Timeout

```go
func fetchWithTimeout(ctx context.Context, url string) (*Response, error) {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }

    return http.DefaultClient.Do(req)
}
```

### Deadline

```go
func processBeforeDeadline(ctx context.Context) error {
    deadline := time.Now().Add(30 * time.Second)
    ctx, cancel := context.WithDeadline(ctx, deadline)
    defer cancel()

    // Check remaining time
    if d, ok := ctx.Deadline(); ok {
        fmt.Printf("Time remaining: %v\n", time.Until(d))
    }

    return doWork(ctx)
}
```

## Checking for Cancellation

### In Long Operations

```go
func processItems(ctx context.Context, items []Item) error {
    for _, item := range items {
        // Check cancellation before each item
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
        }

        if err := processItem(ctx, item); err != nil {
            return err
        }
    }
    return nil
}
```

### Non-Blocking Check

```go
func doWork(ctx context.Context) error {
    // Quick non-blocking check
    if ctx.Err() != nil {
        return ctx.Err()
    }

    // Proceed with work
    return nil
}
```

## Context Values (Use Sparingly)

### Request-Scoped Data Pattern

```go
// Define unexported key type to avoid collisions
type contextKey string

const (
    requestIDKey contextKey = "request_id"
    userIDKey    contextKey = "user_id"
)

// Setter
func WithRequestID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, requestIDKey, id)
}

// Getter
func RequestIDFromContext(ctx context.Context) string {
    if id, ok := ctx.Value(requestIDKey).(string); ok {
        return id
    }
    return ""
}
```

### Middleware Example

```go
func RequestIDMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := r.Header.Get("X-Request-ID")
        if requestID == "" {
            requestID = uuid.New().String()
        }

        ctx := WithRequestID(r.Context(), requestID)
        w.Header().Set("X-Request-ID", requestID)

        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

## HTTP Handlers

```go
func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context() // Already has deadline from http.Server

    user, err := h.service.GetUser(ctx, chi.URLParam(r, "id"))
    if err != nil {
        if errors.Is(err, context.Canceled) {
            // Client disconnected
            return
        }
        if errors.Is(err, context.DeadlineExceeded) {
            http.Error(w, "request timeout", http.StatusGatewayTimeout)
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    json.NewEncoder(w).Encode(user)
}
```

## Database Operations

```go
func (r *Repository) GetUser(ctx context.Context, id string) (*User, error) {
    // Context automatically cancels query if client disconnects
    row := r.db.QueryRowContext(ctx, "SELECT id, name FROM users WHERE id = $1", id)

    var user User
    if err := row.Scan(&user.ID, &user.Name); err != nil {
        if errors.Is(err, context.Canceled) {
            return nil, fmt.Errorf("query canceled: %w", err)
        }
        return nil, err
    }

    return &user, nil
}
```

## Graceful Shutdown

```go
func main() {
    ctx, cancel := context.WithCancel(context.Background())

    // Handle shutdown signals
    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

    go func() {
        <-sigCh
        cancel() // Signal all operations to stop
    }()

    // Run server with context
    if err := server.Run(ctx); err != nil && !errors.Is(err, context.Canceled) {
        log.Fatal(err)
    }
}
```

## Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| `ctx context.Context` as struct field | Pass as first function parameter |
| `context.WithValue` for options | Use function parameters or options struct |
| Ignoring `ctx.Done()` in loops | Check cancellation periodically |
| `context.Background()` in handlers | Use `r.Context()` |
| Long-lived contexts with values | Create child contexts for specific operations |

## Testing with Context

```go
func TestServiceTimeout(t *testing.T) {
    // Create context that times out immediately
    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Nanosecond)
    defer cancel()

    time.Sleep(1 * time.Millisecond) // Ensure timeout

    err := service.Process(ctx)
    assert.ErrorIs(t, err, context.DeadlineExceeded)
}

func TestServiceCancellation(t *testing.T) {
    ctx, cancel := context.WithCancel(context.Background())
    cancel() // Cancel immediately

    err := service.Process(ctx)
    assert.ErrorIs(t, err, context.Canceled)
}
```

## Related Skills

- **Error Handling** — Handling context errors
- **Logging** — Using LoggerContext methods

## References

- [Go Blog: Context](https://go.dev/blog/context)
- [context Package Documentation](https://pkg.go.dev/context)
