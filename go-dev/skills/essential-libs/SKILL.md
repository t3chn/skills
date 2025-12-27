---
name: go-essential-libs
description: Essential Go libraries for production applications. Use these battle-tested packages instead of reinventing the wheel or using wrong primitives.
globs: ["**/*.go", "**/go.mod"]
---

# Go Essential Libraries

> **Golden Rule**: Use the right tool for the job. These libraries represent thousands of hours of community effort and real-world testing.

## 💰 Decimal & Money (NEVER use float64!)

### shopspring/decimal — Arbitrary Precision
```go
import "github.com/shopspring/decimal"

// WRONG: float64 for money
price := 19.99
total := price * 3  // 59.97000000000001 — BROKEN!

// CORRECT: decimal
price := decimal.NewFromFloat(19.99)
total := price.Mul(decimal.NewFromInt(3))  // 59.97 — exact

// From string (safer)
price, _ := decimal.NewFromString("19.99")

// Comparison
if price.GreaterThan(limit) { ... }

// Database scanning
type Product struct {
    Price decimal.Decimal `json:"price" db:"price"`
}
```

**Alternatives**:
| Library | Precision | Performance | Use Case |
|---------|-----------|-------------|----------|
| `shopspring/decimal` | Arbitrary | Moderate | General purpose, correctness-first |
| `govalues/decimal` | 19 digits | High (zero-alloc) | High-throughput financial systems |
| `alpacahq/alpacadecimal` | 12 digits | Highest | Compatible API, trading systems |

### govalues/money — Currency-Aware
```go
import "github.com/govalues/money"

usd, _ := money.NewAmount("USD", 1999, 2)  // $19.99
eur, _ := money.NewAmount("EUR", 1750, 2)  // €17.50

// Currency-safe operations (panics on mismatch in shopspring, errors here)
total, err := usd.Add(usd)  // OK
total, err := usd.Add(eur)  // Error: currency mismatch
```

---

## ✅ Validation

### go-playground/validator — Struct Tags (Simple)
```go
import "github.com/go-playground/validator/v10"

type User struct {
    Email    string `validate:"required,email"`
    Age      int    `validate:"gte=18,lte=120"`
    Password string `validate:"required,min=8"`
}

validate := validator.New()
err := validate.Struct(user)
if err != nil {
    for _, e := range err.(validator.ValidationErrors) {
        fmt.Printf("%s: %s\n", e.Field(), e.Tag())
    }
}
```

### ozzo-validation — Programmatic (Complex)
```go
import validation "github.com/go-ozzo/ozzo-validation/v4"

// Better for complex/conditional validation
func (u User) Validate() error {
    return validation.ValidateStruct(&u,
        validation.Field(&u.Email, validation.Required, is.Email),
        validation.Field(&u.Age, validation.Required, validation.Min(18)),
        validation.Field(&u.Password,
            validation.When(u.IsNew, validation.Required, validation.Length(8, 100)),
        ),
    )
}
```

**When to use which**:
- `validator`: Simple validations, familiar struct tag syntax
- `ozzo-validation`: Conditional logic, compile-time safety, custom rules

---

## 🧪 Testing

### stretchr/testify — Assertions & Mocks
```go
import (
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/mock"
)

func TestUser(t *testing.T) {
    // assert: continues on failure
    assert.Equal(t, expected, actual)
    assert.NoError(t, err)

    // require: stops on failure (use for preconditions)
    require.NotNil(t, user)

    // Mocking
    m := new(MockRepo)
    m.On("GetUser", "123").Return(&User{Name: "John"}, nil)

    svc := NewService(m)
    user, err := svc.GetUser("123")

    m.AssertExpectations(t)
}
```

### vektra/mockery — Auto-Generate Mocks
```bash
# Install
go install github.com/vektra/mockery/v2@latest

# Generate mocks for interfaces
mockery --all --with-expecter
```

```go
// Generated mock with type-safe expectations
m := mocks.NewMockUserRepository(t)
m.EXPECT().GetUser("123").Return(&User{}, nil)
```

### go.uber.org/mock — Uber's GoMock Fork
```bash
# Original gomock is unmaintained, use Uber's fork
go install go.uber.org/mock/mockgen@latest
```

---

## 🌐 HTTP Client

### go-resty/resty — Fluent HTTP Client
```go
import "github.com/go-resty/resty/v2"

client := resty.New().
    SetTimeout(10 * time.Second).
    SetRetryCount(3).
    SetRetryWaitTime(1 * time.Second).
    AddRetryCondition(func(r *resty.Response, err error) bool {
        return r.StatusCode() >= 500
    })

resp, err := client.R().
    SetHeader("Authorization", "Bearer "+token).
    SetBody(payload).
    SetResult(&result).
    Post("https://api.example.com/users")
```

**Key features**:
- Built-in retry with backoff
- Automatic JSON marshaling
- Request/response middleware
- File uploads, form data
- Debug mode

---

## 🛣️ HTTP Router

### go-chi/chi — Lightweight & Idiomatic (Recommended)
```go
import (
    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

r := chi.NewRouter()

// Built-in middleware
r.Use(middleware.Logger)
r.Use(middleware.Recoverer)
r.Use(middleware.RequestID)

// Routes
r.Get("/", handleHome)
r.Route("/api/users", func(r chi.Router) {
    r.Get("/", listUsers)
    r.Post("/", createUser)
    r.Route("/{id}", func(r chi.Router) {
        r.Get("/", getUser)
        r.Put("/", updateUser)
        r.Delete("/", deleteUser)
    })
})

// URL params
userID := chi.URLParam(r, "id")

http.ListenAndServe(":8080", r)
```

**Why chi over others**:
- ~1000 LOC, zero dependencies
- 100% compatible with `net/http`
- Context-based middleware chain
- No magic, explicit routing

**Alternatives**:
| Router | Style | Use Case |
|--------|-------|----------|
| `chi` | Minimal | APIs, microservices |
| `gin` | Feature-rich | Rapid prototyping |
| `echo` | Fast | High-performance APIs |
| stdlib `http.ServeMux` | Zero deps | Simple services (Go 1.22+) |

---

## ⚙️ Configuration

### knadh/koanf — Modern Config (Recommended)
```go
import (
    "github.com/knadh/koanf/v2"
    "github.com/knadh/koanf/parsers/yaml"
    "github.com/knadh/koanf/providers/file"
    "github.com/knadh/koanf/providers/env"
)

var k = koanf.New(".")

// Load from file
k.Load(file.Provider("config.yaml"), yaml.Parser())

// Override with env vars (APP_DATABASE_HOST -> database.host)
k.Load(env.Provider("APP_", ".", func(s string) string {
    return strings.Replace(strings.ToLower(
        strings.TrimPrefix(s, "APP_")), "_", ".", -1)
}), nil)

// Unmarshal to struct
var cfg Config
k.Unmarshal("", &cfg)
```

**Why koanf over viper**:
- 313% smaller binary
- No forced key lowercasing
- Modular dependencies
- Cleaner abstractions

### caarlos0/env — Env-Only (Modern)
```go
import "github.com/caarlos0/env/v11"

type Config struct {
    Port     int      `env:"PORT" envDefault:"8080"`
    Database string   `env:"DATABASE_URL,required"`
    Debug    bool     `env:"DEBUG" envDefault:"false"`
    Hosts    []string `env:"HOSTS" envSeparator:":"`
}

var cfg Config
err := env.Parse(&cfg)

// Or with generics (Go 1.18+)
cfg, err := env.ParseAs[Config]()
```

**Key features**:
- Zero dependencies, modern API
- Generics support (`ParseAs[T]()`)
- Rich tag options: `,required`, `,notEmpty`, `,expand`, `,file`
- File content: `env:"SECRET,file"` reads content from file path

---

## 🆔 UUID

### google/uuid — Simple & Maintained
```go
import "github.com/google/uuid"

id := uuid.New()              // v4 random
id := uuid.NewString()        // string directly
id, err := uuid.Parse(str)    // from string
```

### gofrs/uuid — Full-Featured (Fork of satori)
```go
import "github.com/gofrs/uuid/v5"

id, _ := uuid.NewV4()         // Random
id, _ := uuid.NewV7()         // Time-ordered (better for DBs)
id := uuid.Must(uuid.NewV4()) // Panic on error
```

**Recommendation**:
- `google/uuid` for simplicity
- `gofrs/uuid` for v7 (time-ordered) or more versions

---

## 🕐 Time & Date

### Standard Library First
```go
import "time"

// Always use UTC for storage
now := time.Now().UTC()

// Parse with location
loc, _ := time.LoadLocation("America/New_York")
t, _ := time.ParseInLocation("2006-01-02", "2024-12-25", loc)

// Duration
timeout := 30 * time.Second
```

### dromara/carbon — Fluent API (Optional)
```go
import "github.com/dromara/carbon/v2"

// More readable for complex operations
carbon.Now().SubDays(7).StartOfDay()
carbon.Parse("2024-12-25").IsWeekend()
carbon.Now().DiffInDays(carbon.Parse("2025-01-01"))
```

---

## 🔐 Security

### Password Hashing — Argon2 (Recommended)
```go
import "golang.org/x/crypto/argon2"

// Argon2id (winner of Password Hashing Competition)
func HashPassword(password string) (string, error) {
    salt := make([]byte, 16)
    crypto_rand.Read(salt)

    hash := argon2.IDKey([]byte(password), salt, 1, 64*1024, 4, 32)

    return fmt.Sprintf("$argon2id$v=%d$m=%d,t=%d,p=%d$%s$%s",
        argon2.Version, 64*1024, 1, 4,
        base64.RawStdEncoding.EncodeToString(salt),
        base64.RawStdEncoding.EncodeToString(hash),
    ), nil
}
```

### Password Hashing — bcrypt (Simpler)
```go
import "golang.org/x/crypto/bcrypt"

hash, _ := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
err := bcrypt.CompareHashAndPassword(hash, []byte(password))
```

**Argon2 vs bcrypt**:
- Argon2: More secure, memory-hard, no 72-byte limit
- bcrypt: Simpler, battle-tested, FIPS-140 (if needed)

### Tokens — PASETO over JWT
```go
import "github.com/o1egl/paseto"

// PASETO v2 (safer than JWT — no algorithm confusion attacks)
token, _ := paseto.NewV2().Encrypt(key, payload, footer)
```

### JWT (if required)
```go
import "github.com/golang-jwt/jwt/v5"
```

---

## 📦 JSON Performance

### Standard Library — Default Choice
```go
import "encoding/json"
// Good enough for most cases
```

### jsoniter — Drop-in Replacement (3-6x faster)
```go
import jsoniter "github.com/json-iterator/go"

var json = jsoniter.ConfigCompatibleWithStandardLibrary

// Same API as encoding/json
json.Marshal(v)
json.Unmarshal(data, &v)
```

### mailru/easyjson — Fastest (Code Gen)
```bash
go install github.com/mailru/easyjson/...@latest
easyjson -all types.go
```

**Performance ranking**: easyjson > jsoniter > go-json > sonic > stdlib

---

## ⚡ Concurrency

### golang.org/x/sync/errgroup — Goroutine Groups
```go
import "golang.org/x/sync/errgroup"

g, ctx := errgroup.WithContext(ctx)

for _, url := range urls {
    url := url
    g.Go(func() error {
        return fetch(ctx, url)
    })
}

if err := g.Wait(); err != nil {
    // First error from any goroutine
}
```

### golang.org/x/sync/semaphore — Limit Concurrency
```go
import "golang.org/x/sync/semaphore"

sem := semaphore.NewWeighted(10)  // Max 10 concurrent

for _, item := range items {
    sem.Acquire(ctx, 1)
    go func(item Item) {
        defer sem.Release(1)
        process(item)
    }(item)
}
```

### sourcegraph/conc — Higher-Level Patterns
```go
import "github.com/sourcegraph/conc/pool"

p := pool.New().WithMaxGoroutines(10).WithContext(ctx)
for _, item := range items {
    p.Go(func(ctx context.Context) error {
        return process(ctx, item)
    })
}
err := p.Wait()
```

---

## 🗄️ Caching

### dgraph-io/ristretto — High-Performance
```go
import "github.com/dgraph-io/ristretto"

cache, _ := ristretto.NewCache(&ristretto.Config{
    NumCounters: 1e7,     // 10M counters for admission
    MaxCost:     1 << 30, // 1GB max
    BufferItems: 64,
})

cache.Set("key", value, cost)
value, found := cache.Get("key")
```

### allegro/bigcache — Low GC Overhead
```go
import "github.com/allegro/bigcache/v3"

cache, _ := bigcache.New(context.Background(), bigcache.DefaultConfig(10*time.Minute))
cache.Set("key", []byte(value))
data, _ := cache.Get("key")
```

**When to use**:
- `ristretto`: Best hit ratio, high concurrency
- `bigcache`: Lowest GC pause, large datasets
- `freecache`: Fixed size, per-entry TTL

---

## 🔧 Error Handling

### Standard Library (Go 1.13+)
```go
// Wrap with context
return fmt.Errorf("fetch user %s: %w", id, err)

// Check error types
if errors.Is(err, sql.ErrNoRows) { ... }

var pathErr *os.PathError
if errors.As(err, &pathErr) { ... }
```

### hashicorp/go-multierror — Accumulate Errors
```go
import "github.com/hashicorp/go-multierror"

var result *multierror.Error
for _, item := range items {
    if err := validate(item); err != nil {
        result = multierror.Append(result, err)
    }
}
return result.ErrorOrNil()
```

### cockroachdb/errors — Distributed Systems
```go
import "github.com/cockroachdb/errors"

// Drop-in replacement for pkg/errors with:
// - Network portability
// - Sentry integration
// - PII-safe details
```

---

## 💉 Dependency Injection

### google/wire — Compile-Time (Recommended)
```go
// wire.go
//go:build wireinject

func InitializeApp() (*App, error) {
    wire.Build(
        NewDatabase,
        NewUserRepo,
        NewUserService,
        NewApp,
    )
    return nil, nil
}
```

```bash
wire ./...  # Generates wire_gen.go
```

### uber-go/fx — Runtime (Large Apps)
```go
import "go.uber.org/fx"

app := fx.New(
    fx.Provide(NewDatabase, NewUserRepo, NewUserService),
    fx.Invoke(StartServer),
)
app.Run()
```

**When to use**:
- `wire`: Type safety, zero runtime overhead, smaller apps
- `fx`: Lifecycle management, module composition, large services

---

## 📊 Logging

### log/slog — Standard Library (Go 1.21+)
```go
import "log/slog"

logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
logger.Info("user created",
    slog.String("user_id", id),
    slog.Int("age", 25),
)
```

### High-Performance Alternatives
```go
// uber-go/zap — Fastest structured logging
import "go.uber.org/zap"

// rs/zerolog — Zero allocation
import "github.com/rs/zerolog"
```

---

## 🗃️ Database

### pgx — PostgreSQL Driver (Recommended)
```go
import "github.com/jackc/pgx/v5"

conn, _ := pgx.Connect(ctx, os.Getenv("DATABASE_URL"))
rows, _ := conn.Query(ctx, "SELECT * FROM users WHERE id = $1", id)
```

### sqlc — Type-Safe SQL (Recommended)
```sql
-- query.sql
-- name: GetUser :one
SELECT * FROM users WHERE id = $1;

-- name: ListUsers :many
SELECT * FROM users ORDER BY created_at;
```

```bash
sqlc generate  # Generates type-safe Go code
```

### uptrace/bun — SQL-First ORM (Recommended)
```go
import (
    "github.com/uptrace/bun"
    "github.com/uptrace/bun/dialect/pgdialect"
    "github.com/uptrace/bun/driver/pgdriver"
)

// Connect
sqldb := sql.OpenDB(pgdriver.NewConnector(pgdriver.WithDSN(dsn)))
db := bun.NewDB(sqldb, pgdialect.New())

// Model
type User struct {
    bun.BaseModel `bun:"table:users"`
    ID            int64  `bun:",pk,autoincrement"`
    Name          string `bun:",notnull"`
    Email         string `bun:",unique"`
}

// CRUD
db.NewInsert().Model(&user).Exec(ctx)
db.NewSelect().Model(&user).Where("id = ?", id).Scan(ctx)
db.NewUpdate().Model(&user).Set("name = ?", name).Where("id = ?", id).Exec(ctx)
db.NewDelete().Model(&user).Where("id = ?", id).Exec(ctx)

// Raw SQL when needed
db.QueryContext(ctx, "SELECT * FROM users WHERE age > ?", 18)
```

**Why bun over GORM**:
- SQL-first: you control the queries
- Lighter: built on `database/sql`, minimal overhead
- Better for complex queries: CTEs, subqueries, window functions
- Explicit relationships via struct tags

### GORM — ORM (Use Carefully)
```go
import "gorm.io/gorm"

// ⚠️ Prefer bun or sqlc for new projects
// ⚠️ Disable auto-migrate in production!
// ⚠️ Always review generated SQL with db.Debug()
```

---

## 📋 Quick Reference

| Category | Recommended | Alternative |
|----------|-------------|-------------|
| **Decimal** | `shopspring/decimal` | `govalues/decimal` (perf) |
| **Validation** | `go-playground/validator` | `ozzo-validation` (complex) |
| **Testing** | `testify` + `mockery` | `go.uber.org/mock` |
| **HTTP Client** | `go-resty/resty` | stdlib `net/http` |
| **HTTP Router** | `go-chi/chi` | `gin`, `echo` |
| **Config** | `knadh/koanf` | `caarlos0/env` |
| **UUID** | `google/uuid` | `gofrs/uuid` (v7) |
| **Hashing** | `argon2` | `bcrypt` (simpler) |
| **Tokens** | `paseto` | `golang-jwt` (if required) |
| **JSON** | stdlib | `jsoniter` (performance) |
| **Concurrency** | `errgroup` + `semaphore` | `sourcegraph/conc` |
| **Cache** | `ristretto` | `bigcache` (low GC) |
| **Errors** | stdlib + `multierror` | `cockroachdb/errors` |
| **DI** | `google/wire` | `uber-go/fx` (large apps) |
| **Logging** | `log/slog` | `zap`, `zerolog` |
| **PostgreSQL** | `pgx` + `sqlc` | `bun` (ORM) |
