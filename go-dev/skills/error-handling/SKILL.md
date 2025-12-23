---
name: Go Error Handling
description: This skill should be used when the user asks about "Go error handling", "error wrapping", "sentinel errors", "errors.Is", "errors.As", "custom error types", "error context", "fmt.Errorf %w", "error best practices Go", "when to wrap errors", "Go error patterns", "handling errors in Go", "error messages Go", or needs guidance on idiomatic Go error patterns following 2024-2025 best practices.
version: 1.0.0
---

# Go Error Handling — Modern Best Practices (2024-2025)

## Core Principles

1. **Errors are values** — Handle them explicitly, don't ignore
2. **Add context when wrapping** — Make errors actionable
3. **Use `errors.Is` and `errors.As`** — Never compare with `==`
4. **Don't over-wrap** — Add context only when meaningful

## Error Creation Patterns

### Simple Errors

```go
import "errors"

// For simple cases
var ErrNotFound = errors.New("not found")

// With formatting
return fmt.Errorf("user %s not found", userID)
```

### Sentinel Errors

```go
// internal/storage/errors.go
package storage

import "errors"

// Sentinel errors — exported, start with Err
var (
    ErrNotFound      = errors.New("storage: item not found")
    ErrAlreadyExists = errors.New("storage: item already exists")
    ErrInvalidID     = errors.New("storage: invalid ID format")
)
```

**Usage:**
```go
if errors.Is(err, storage.ErrNotFound) {
    // Handle not found case
}
```

### Custom Error Types

```go
// For errors needing additional context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}

// Usage with errors.As
var valErr *ValidationError
if errors.As(err, &valErr) {
    log.Printf("Field %s failed: %s", valErr.Field, valErr.Message)
}
```

### Domain Error Wrapper

```go
// internal/errors/errors.go
package errors

import (
    "errors"
    "fmt"
)

// DomainError wraps errors with operation context
type DomainError struct {
    Op      string // Operation that failed
    Kind    Kind   // Category of error
    Err     error  // Underlying error
}

type Kind int

const (
    KindNotFound Kind = iota + 1
    KindInvalid
    KindPermission
    KindInternal
)

func (e *DomainError) Error() string {
    return fmt.Sprintf("%s: %v", e.Op, e.Err)
}

func (e *DomainError) Unwrap() error {
    return e.Err
}

// E creates a new DomainError
func E(op string, kind Kind, err error) error {
    return &DomainError{Op: op, Kind: kind, Err: err}
}
```

## Error Wrapping

### When to Wrap

```go
// GOOD: Add meaningful context
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}

// BAD: Redundant wrapping
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("error getting user: %w", err) // "error" is redundant
    }
    return user, nil
}
```

### When NOT to Wrap

```go
// DON'T wrap if no context to add
func (r *Repo) FindByID(ctx context.Context, id string) (*User, error) {
    // Just return the error as-is
    return r.db.QueryRow(ctx, query, id).Scan(&user)
}

// DON'T expose internal errors in public APIs
func (s *Service) Login(email, password string) (*Token, error) {
    user, err := s.repo.FindByEmail(email)
    if err != nil {
        // Don't leak "sql: no rows" to clients
        return nil, ErrInvalidCredentials
    }
}
```

## Error Checking Patterns

### Using errors.Is (Sentinel Errors)

```go
// CORRECT
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrNotFound
}

// WRONG - doesn't work with wrapped errors
if err == sql.ErrNoRows {
    return nil, ErrNotFound
}
```

### Using errors.As (Custom Types)

```go
var pgErr *pgconn.PgError
if errors.As(err, &pgErr) {
    if pgErr.Code == "23505" { // unique violation
        return ErrAlreadyExists
    }
}
```

## CLI Error Patterns

```go
// cmd/myapp/errors.go

// FatalError exits with message
func FatalError(format string, args ...interface{}) {
    fmt.Fprintf(os.Stderr, "Error: "+format+"\n", args...)
    os.Exit(1)
}

// FatalErrorWithHint provides actionable guidance
func FatalErrorWithHint(message, hint string) {
    fmt.Fprintf(os.Stderr, "Error: %s\n", message)
    fmt.Fprintf(os.Stderr, "Hint: %s\n", hint)
    os.Exit(1)
}

// WarnError for non-fatal issues
func WarnError(format string, args ...interface{}) {
    fmt.Fprintf(os.Stderr, "Warning: "+format+"\n", args...)
}
```

**Usage:**
```go
// Pattern A: Fatal for user input / critical errors
if err := store.CreateIssue(ctx, issue); err != nil {
    FatalError("failed to create issue: %v", err)
}

// Pattern B: Warn for optional operations
if err := createGitHook(); err != nil {
    WarnError("failed to install git hook: %v", err)
    // Continue execution
}
```

## HTTP API Error Responses

```go
type APIError struct {
    Code    string `json:"code"`
    Message string `json:"message"`
}

func handleError(w http.ResponseWriter, err error) {
    var status int
    var apiErr APIError

    switch {
    case errors.Is(err, ErrNotFound):
        status = http.StatusNotFound
        apiErr = APIError{Code: "NOT_FOUND", Message: "Resource not found"}
    case errors.Is(err, ErrInvalidInput):
        status = http.StatusBadRequest
        apiErr = APIError{Code: "INVALID_INPUT", Message: err.Error()}
    default:
        status = http.StatusInternalServerError
        apiErr = APIError{Code: "INTERNAL_ERROR", Message: "An error occurred"}
        // Log actual error internally
        log.Printf("internal error: %v", err)
    }

    w.WriteHeader(status)
    json.NewEncoder(w).Encode(apiErr)
}
```

## Error Message Style

```go
// GOOD: lowercase, no punctuation, concise
return fmt.Errorf("parse config: %w", err)
return fmt.Errorf("user %s not found", id)
return errors.New("invalid input")

// BAD: uppercase, punctuation, verbose
return fmt.Errorf("Error parsing config: %w.", err)
return fmt.Errorf("Failed to find user with ID %s!", id)
```

## Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| `if err.Error() == "not found"` | `errors.Is(err, ErrNotFound)` |
| `return errors.New("error: " + err.Error())` | `return fmt.Errorf("context: %w", err)` |
| Ignoring errors `_ = file.Close()` | `defer func() { _ = file.Close() }()` with comment |
| Logging and returning | Choose one: log OR return |
| Generic `errors.New("failed")` | Specific: `errors.New("open config: permission denied")` |

## Related Skills

- **Testing Patterns** — Testing error conditions with table-driven tests
- **Project Structure** — Where to put error definitions (`internal/errors/`)

## References

- [Go Blog: Working with Errors in Go 1.13](https://go.dev/blog/go1.13-errors)
- [Dave Cheney: Don't just check errors, handle them gracefully](https://dave.cheney.net/2016/04/27/dont-just-check-errors-handle-them-gracefully)
