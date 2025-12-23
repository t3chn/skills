---
name: Go Testing Patterns
description: This skill should be used when the user asks about "Go testing", "table-driven tests", "testify", "test fixtures", "mocks in Go", "integration tests", "t.Run", "test organization", "Go test coverage", "benchmark tests", "t.Helper", "require vs assert", "test helpers Go", "subtests Go", "parallel tests", or needs guidance on idiomatic Go testing patterns following 2024-2025 best practices.
version: 1.0.0
---

# Go Testing Patterns — Modern Best Practices (2024-2025)

## Core Testing Philosophy

1. **Table-driven tests** — DRY, comprehensive coverage
2. **Subtests with t.Run** — Granular, parallel-friendly
3. **Test what matters** — Behavior, not implementation
4. **Fast feedback** — Unit tests must be fast

## Table-Driven Tests

### Basic Structure

```go
func TestParseID(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    string
        wantErr bool
    }{
        {
            name:  "valid prefix",
            input: "bd-abc123",
            want:  "abc123",
        },
        {
            name:  "uppercase normalized",
            input: "BD-ABC123",
            want:  "abc123",
        },
        {
            name:    "invalid format",
            input:   "invalid",
            wantErr: true,
        },
        {
            name:    "empty string",
            input:   "",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseID(tt.input)

            if tt.wantErr {
                if err == nil {
                    t.Errorf("ParseID(%q) expected error, got nil", tt.input)
                }
                return
            }

            if err != nil {
                t.Errorf("ParseID(%q) unexpected error: %v", tt.input, err)
                return
            }

            if got != tt.want {
                t.Errorf("ParseID(%q) = %q, want %q", tt.input, got, tt.want)
            }
        })
    }
}
```

### Using Maps for Complex Cases

```go
func TestUserValidation(t *testing.T) {
    tests := map[string]struct {
        user    User
        wantErr string
    }{
        "valid user": {
            user: User{Name: "Alice", Email: "alice@example.com"},
        },
        "empty name": {
            user:    User{Name: "", Email: "alice@example.com"},
            wantErr: "name is required",
        },
        "invalid email": {
            user:    User{Name: "Alice", Email: "not-an-email"},
            wantErr: "invalid email format",
        },
    }

    for name, tt := range tests {
        t.Run(name, func(t *testing.T) {
            err := tt.user.Validate()

            if tt.wantErr != "" {
                if err == nil || !strings.Contains(err.Error(), tt.wantErr) {
                    t.Errorf("Validate() error = %v, want containing %q", err, tt.wantErr)
                }
                return
            }

            if err != nil {
                t.Errorf("Validate() unexpected error: %v", err)
            }
        })
    }
}
```

## Using Testify

### require vs assert

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestWithTestify(t *testing.T) {
    // require: stops test on failure (use for preconditions)
    user, err := store.GetUser(ctx, "123")
    require.NoError(t, err)           // Stop if error
    require.NotNil(t, user)           // Stop if nil

    // assert: continues on failure (use for assertions)
    assert.Equal(t, "Alice", user.Name)
    assert.Equal(t, "alice@example.com", user.Email)
    assert.True(t, user.Active)
}
```

### Table-Driven with Testify

```go
func TestCalculatePrice(t *testing.T) {
    tests := []struct {
        name     string
        quantity int
        price    float64
        discount float64
        want     float64
    }{
        {"no discount", 10, 5.0, 0, 50.0},
        {"10% discount", 10, 5.0, 0.1, 45.0},
        {"bulk order", 100, 5.0, 0.2, 400.0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := CalculatePrice(tt.quantity, tt.price, tt.discount)
            assert.InDelta(t, tt.want, got, 0.01, "price calculation mismatch")
        })
    }
}
```

## Test Setup and Fixtures

### Test Helpers

```go
// testutil/testutil.go
package testutil

import (
    "testing"
    "path/filepath"
)

// NewTestStore creates an isolated test database
func NewTestStore(t *testing.T) *storage.SQLiteStore {
    t.Helper()

    tmpDir := t.TempDir() // Automatically cleaned up
    dbPath := filepath.Join(tmpDir, "test.db")

    store, err := storage.NewSQLiteStore(dbPath)
    if err != nil {
        t.Fatalf("failed to create test store: %v", err)
    }

    t.Cleanup(func() {
        store.Close()
    })

    return store
}

// MustCreateUser creates a test user or fails
func MustCreateUser(t *testing.T, store *storage.Store, name string) *User {
    t.Helper()

    user := &User{Name: name, Email: name + "@test.com"}
    err := store.CreateUser(context.Background(), user)
    if err != nil {
        t.Fatalf("failed to create test user: %v", err)
    }
    return user
}
```

### Golden Files

```go
var update = flag.Bool("update", false, "update golden files")

func TestRenderTemplate(t *testing.T) {
    data := TemplateData{Title: "Test", Items: []string{"a", "b", "c"}}

    got, err := RenderTemplate(data)
    require.NoError(t, err)

    golden := filepath.Join("testdata", t.Name()+".golden")

    if *update {
        os.WriteFile(golden, []byte(got), 0644)
    }

    want, err := os.ReadFile(golden)
    require.NoError(t, err)

    assert.Equal(t, string(want), got)
}
```

## Mocking Patterns

### Interface-Based Mocking

```go
// Define interface where it's used
type UserRepository interface {
    Get(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// Mock implementation
type MockUserRepo struct {
    GetFunc  func(ctx context.Context, id string) (*User, error)
    SaveFunc func(ctx context.Context, user *User) error
}

func (m *MockUserRepo) Get(ctx context.Context, id string) (*User, error) {
    return m.GetFunc(ctx, id)
}

func (m *MockUserRepo) Save(ctx context.Context, user *User) error {
    return m.SaveFunc(ctx, user)
}

// Usage in test
func TestUserService_UpdateName(t *testing.T) {
    mockRepo := &MockUserRepo{
        GetFunc: func(ctx context.Context, id string) (*User, error) {
            return &User{ID: id, Name: "Old Name"}, nil
        },
        SaveFunc: func(ctx context.Context, user *User) error {
            assert.Equal(t, "New Name", user.Name)
            return nil
        },
    }

    svc := NewUserService(mockRepo)
    err := svc.UpdateName(context.Background(), "123", "New Name")
    require.NoError(t, err)
}
```

## Integration Tests

### Build Tags

```go
//go:build integration

package storage_test

import (
    "testing"
)

func TestDatabaseIntegration(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }

    // Real database tests...
}
```

Run: `go test -tags=integration ./...`

### Test Containers (Docker)

```go
func TestWithPostgres(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping container test")
    }

    ctx := context.Background()
    container, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: testcontainers.ContainerRequest{
            Image:        "postgres:15",
            ExposedPorts: []string{"5432/tcp"},
            Env: map[string]string{
                "POSTGRES_PASSWORD": "test",
                "POSTGRES_DB":       "testdb",
            },
            WaitingFor: wait.ForListeningPort("5432/tcp"),
        },
        Started: true,
    })
    require.NoError(t, err)
    defer container.Terminate(ctx)

    // Use container...
}
```

## Test Organization

```
project/
├── internal/
│   ├── user/
│   │   ├── service.go
│   │   ├── service_test.go      # Unit tests
│   │   └── repository.go
│   └── storage/
│       ├── sqlite.go
│       └── sqlite_test.go
├── tests/
│   ├── integration/             # Integration tests
│   │   └── api_test.go
│   └── testdata/                # Shared test fixtures
│       └── fixtures.json
```

## Running Tests

```bash
# All tests
go test ./...

# Short mode (skip slow tests)
go test -short ./...

# Specific package
go test ./internal/user/...

# With coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Verbose with race detection
go test -v -race ./...

# Run specific test
go test -run TestUserService_UpdateName ./internal/user/

# Parallel tests
go test -parallel 4 ./...
```

## Anti-Patterns

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Testing private functions | Test through public API |
| Large test functions | Split into subtests |
| Shared mutable state | Use `t.Parallel()` with isolated state |
| Sleep in tests | Use channels, conditions, or polling |
| Ignoring `t.Helper()` | Always mark helper functions |

## Related Skills

- **Error Handling** — Testing error conditions
- **Project Structure** — Test file organization

## References

- [Go Wiki: TableDrivenTests](https://go.dev/wiki/TableDrivenTests)
- [Dave Cheney: Prefer table driven tests](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests)
- [Testify Documentation](https://github.com/stretchr/testify)
