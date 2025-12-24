---
name: go-conventions
description: Go project conventions and best practices for code review context. Use with official feature-dev:code-reviewer agent.
globs: ["**/*.go", "**/go.mod", "**/go.sum"]
---

# Go Conventions

Context for code review of Go projects. These conventions inform the official `feature-dev:code-reviewer` agent.

## 2025 Tooling

| Tool | Purpose | Note |
|------|---------|------|
| **sqlc** | Type-safe SQL | Generates Go from SQL |
| **templ** | Type-safe HTML | Replaces html/template |
| **Task** | Build automation | Replaces Makefile |

### sqlc for Type-Safe Database
```yaml
# sqlc.yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "query.sql"
    schema: "schema.sql"
    gen:
      go:
        package: "db"
        out: "internal/db"
```

```sql
-- query.sql
-- name: GetUser :one
SELECT * FROM users WHERE id = $1;
```

### Go 1.23+ Iterator Pattern
```go
// Range over function (Go 1.23+)
func (s *Store) All() iter.Seq[Item] {
    return func(yield func(Item) bool) {
        for _, item := range s.items {
            if !yield(item) {
                return
            }
        }
    }
}

// Usage
for item := range store.All() {
    process(item)
}
```

## Error Handling

### Always Check Errors
```go
// WRONG
file, _ := os.Open(path)

// CORRECT
file, err := os.Open(path)
if err != nil {
    return fmt.Errorf("open config: %w", err)
}
```

### Wrap Errors with Context
```go
// Use %w for wrappable errors
if err != nil {
    return fmt.Errorf("process user %s: %w", userID, err)
}

// Use errors.Is/As for checking
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrNotFound
}
```

### Sentinel Errors
```go
var (
    ErrNotFound    = errors.New("not found")
    ErrInvalidData = errors.New("invalid data")
)
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Interfaces | `-er` suffix | `Reader`, `Writer`, `Stringer` |
| Unexported | camelCase | `userID`, `httpClient` |
| Exported | PascalCase | `UserService`, `HTTPClient` |
| Acronyms | ALL CAPS | `HTTP`, `URL`, `ID` |
| Package | lowercase, short | `user`, `http`, `auth` |

## Package Structure

```
cmd/
├── api/main.go           # Entry points
├── worker/main.go
internal/
├── domain/               # Business logic
├── repository/           # Data access
├── service/              # Application services
├── handler/              # HTTP handlers
pkg/                      # Public libraries (if any)
```

## Testing Patterns

### Table-Driven Tests
```go
func TestParseConfig(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    *Config
        wantErr bool
    }{
        {
            name:  "valid config",
            input: `{"port": 8080}`,
            want:  &Config{Port: 8080},
        },
        {
            name:    "invalid json",
            input:   `{invalid}`,
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseConfig(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Test Helpers
```go
func newTestServer(t *testing.T) *httptest.Server {
    t.Helper()
    // Setup...
    t.Cleanup(func() { /* cleanup */ })
    return srv
}
```

## Context Usage

### Always Pass Context First
```go
func (s *Service) GetUser(ctx context.Context, id string) (*User, error)
```

### Respect Cancellation
```go
select {
case <-ctx.Done():
    return ctx.Err()
case result := <-ch:
    return result, nil
}
```

## Concurrency

### Use sync Package Correctly
```go
var mu sync.Mutex  // Protect shared state
var wg sync.WaitGroup  // Wait for goroutines

// Prefer channels for communication
ch := make(chan Result, bufSize)
```

### Avoid Goroutine Leaks
```go
// Always ensure goroutines can exit
go func() {
    select {
    case <-ctx.Done():
        return
    case ch <- value:
    }
}()
```

## Performance

### Preallocate Slices
```go
// When size is known
users := make([]User, 0, len(ids))
```

### Avoid String Concatenation in Loops
```go
var b strings.Builder
for _, s := range items {
    b.WriteString(s)
}
result := b.String()
```

## Security

- Never log sensitive data (passwords, tokens, PII)
- Use `crypto/rand` not `math/rand` for security
- Validate all external input
- Use parameterized queries (no string SQL)
- Set appropriate timeouts on HTTP clients

## Code Review Checklist

- [ ] All errors handled and wrapped with context
- [ ] No naked goroutines (all have exit path)
- [ ] Context passed and respected
- [ ] Tests use table-driven pattern
- [ ] No sensitive data in logs
- [ ] Interfaces defined where consumed
- [ ] Package names are lowercase and short
