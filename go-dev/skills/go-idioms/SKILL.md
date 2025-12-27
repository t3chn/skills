---
name: go-idioms
description: Core Go idioms from Effective Go. Essential patterns for developers coming from other languages. Covers data allocation, methods, interfaces, embedding, and Go-specific control flow.
globs: ["**/*.go", "**/go.mod"]
---

# Go Idioms

> Patterns that make Go code idiomatic. Based on [Effective Go](https://go.dev/doc/effective_go).

---

## Data Allocation: new vs make

```go
// new(T) — allocates zeroed memory, returns *T
p := new(int)      // *int, points to 0
user := new(User)  // *User, all fields zero-valued

// make(T, args) — initializes slices, maps, channels
s := make([]int, 0, 10)  // slice: len=0, cap=10
m := make(map[string]int) // map: ready to use
ch := make(chan int, 5)   // buffered channel
```

**Rule**: `new` = allocation, `make` = initialization of slice/map/chan

---

## Slices: The Most Important Type

```go
// Slice = pointer to array + length + capacity
// Passing slice is cheap (24 bytes), but SHARES underlying array!

func modify(s []int) {
    s[0] = 999  // MODIFIES original!
}

// Append may reallocate
s := make([]int, 0, 2)
s = append(s, 1, 2)     // fits in capacity
s = append(s, 3)        // reallocates! new backing array

// Preallocate when size known
users := make([]User, 0, len(ids))
for _, id := range ids {
    users = append(users, fetchUser(id))
}

// Slice a slice (shares memory!)
original := []int{1, 2, 3, 4, 5}
slice := original[1:3]  // [2, 3] — same backing array
slice[0] = 999          // original is now [1, 999, 3, 4, 5]

// Copy to avoid sharing
clone := make([]int, len(original))
copy(clone, original)
```

---

## Maps

```go
// Nil map reads OK, writes PANIC
var m map[string]int
_ = m["key"]      // OK: returns zero value
m["key"] = 1      // PANIC: assignment to nil map

// Always initialize
m := make(map[string]int)
m := map[string]int{}  // equivalent

// Comma-ok idiom
value, ok := m["key"]
if !ok {
    // key not present
}

// Delete is safe on nil
delete(m, "key")  // OK even if m is nil or key missing

// Maps are not safe for concurrent use!
// Use sync.Map or mutex for concurrent access
```

---

## Methods: Pointer vs Value Receivers

```go
type User struct {
    Name string
    Age  int
}

// Value receiver — works on COPY
func (u User) String() string {
    return u.Name
}

// Pointer receiver — can MODIFY original
func (u *User) SetAge(age int) {
    u.Age = age  // modifies the actual struct
}
```

### The Rule

| If method needs to... | Use |
|----------------------|-----|
| Modify receiver | `*T` pointer |
| Avoid copy (large struct) | `*T` pointer |
| Be consistent with other methods | Match existing |
| Work with nil receiver | `*T` pointer |
| None of above | `T` value is fine |

**Golden rule**: If ANY method uses pointer receiver, ALL should use pointer receiver for consistency.

```go
// Common pattern: constructor returns pointer
func NewUser(name string) *User {
    return &User{Name: name}
}
```

---

## Interfaces

### Implicit Implementation
```go
// No "implements" keyword — just have the methods
type Reader interface {
    Read(p []byte) (n int, err error)
}

// MyBuffer implements Reader automatically
type MyBuffer struct { data []byte }

func (b *MyBuffer) Read(p []byte) (int, error) {
    n := copy(p, b.data)
    return n, nil
}

// Compile-time check (blank identifier pattern)
var _ Reader = (*MyBuffer)(nil)
```

### Interface Design
```go
// GOOD: Small, focused interfaces
type Reader interface { Read([]byte) (int, error) }
type Writer interface { Write([]byte) (int, error) }
type ReadWriter interface { Reader; Writer }  // composition

// BAD: Large "god" interfaces
type Repository interface {
    GetUser(id int) (*User, error)
    CreateUser(u *User) error
    UpdateUser(u *User) error
    DeleteUser(id int) error
    GetAllUsers() ([]*User, error)
    // ... 20 more methods
}

// GOOD: Define interface where USED, not where implemented
// In consumer package:
type UserGetter interface {
    GetUser(id int) (*User, error)
}

func NewService(repo UserGetter) *Service { ... }
```

### Type Assertions & Switches
```go
// Type assertion
r, ok := val.(io.Reader)
if ok {
    // val implements io.Reader
}

// Type switch
switch v := val.(type) {
case string:
    fmt.Println("string:", v)
case int:
    fmt.Println("int:", v)
case io.Reader:
    fmt.Println("reader")
default:
    fmt.Println("unknown type")
}
```

---

## Embedding

### Struct Embedding (Composition)
```go
type Engine struct {
    Power int
}

func (e *Engine) Start() { fmt.Println("Engine started") }

type Car struct {
    Engine  // embedded — Car "has an" Engine
    Brand string
}

// Car gets Engine's methods automatically
car := &Car{Engine: Engine{Power: 200}, Brand: "Tesla"}
car.Start()       // works! promoted method
car.Power = 300   // works! promoted field
car.Engine.Start() // also works, explicit
```

### Interface Embedding
```go
type ReadCloser interface {
    io.Reader  // embed Reader interface
    io.Closer  // embed Closer interface
}

// Equivalent to:
type ReadCloser interface {
    Read(p []byte) (n int, err error)
    Close() error
}
```

### Embedding vs Inheritance
```go
// Embedding is NOT inheritance!
type Base struct{}
func (Base) Method() { fmt.Println("Base") }

type Derived struct { Base }
func (Derived) Method() { fmt.Println("Derived") }

d := Derived{}
d.Method()       // "Derived"
d.Base.Method()  // "Base" — base is still accessible
```

---

## Control Flow Idioms

### Labeled Break/Continue
```go
outer:
for _, row := range matrix {
    for _, val := range row {
        if val == target {
            break outer  // breaks OUTER loop
        }
    }
}
```

### If with Init Statement
```go
if err := doSomething(); err != nil {
    return err
}
// err not in scope here — cleaner!

// Compare to:
err := doSomething()
if err != nil {
    return err
}
// err still in scope, pollutes namespace
```

### Switch without Expression
```go
// Cleaner than if-else chains
switch {
case n < 0:
    return "negative"
case n == 0:
    return "zero"
default:
    return "positive"
}
```

---

## Initialization

### const + iota
```go
// iota resets to 0 at each const block
const (
    Sunday = iota  // 0
    Monday         // 1
    Tuesday        // 2
)

// Skip values
const (
    _ = iota       // 0 (discarded)
    KB = 1 << (10 * iota)  // 1 << 10
    MB                      // 1 << 20
    GB                      // 1 << 30
)

// Bitmask pattern
const (
    FlagRead  = 1 << iota  // 1
    FlagWrite              // 2
    FlagExec               // 4
)
```

### init() Function
```go
// Runs automatically before main()
// Multiple init() in same file run in order
// init() across files: undefined order within package

func init() {
    // Setup code: register drivers, init globals
    sql.Register("mysql", &MySQLDriver{})
}

// AVOID init() when possible:
// - Hard to test
// - Hidden dependencies
// - Order surprises
// Prefer explicit initialization in main()
```

---

## Blank Identifier Patterns

```go
// Discard unwanted values
for _, v := range slice { ... }  // discard index
result, _ := strconv.Atoi(s)     // discard error (careful!)

// Import for side effects only
import _ "image/png"  // registers PNG decoder

// Compile-time interface check
var _ io.Reader = (*MyType)(nil)

// Silence "unused variable" during development
_ = unusedVar
```

---

## Defer

```go
// Executes when function returns (LIFO order)
func process() error {
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close()  // guaranteed cleanup

    // ... work with file
    return nil
}

// Arguments evaluated immediately!
func trace(msg string) func() {
    start := time.Now()
    log.Println("enter:", msg)
    return func() { log.Println("exit:", msg, time.Since(start)) }
}

func foo() {
    defer trace("foo")()  // note the () — calls trace NOW, defers return value
}

// Loop gotcha
for _, f := range files {
    defer f.Close()  // ALL close at function end, not loop iteration!
}
// Fix: use anonymous function
for _, f := range files {
    func(f *os.File) {
        defer f.Close()
        // process f
    }(f)
}
```

---

## Quick Reference

| Idiom | Pattern |
|-------|---------|
| Allocation | `new(T)` → `*T` zeroed; `make(T)` → initialized slice/map/chan |
| Nil map | Read OK, write panics |
| Comma-ok | `v, ok := m[key]` or `v, ok := x.(T)` |
| Receivers | Pointer if modify/large/nil-safe; else value OK |
| Interfaces | Small, define at consumer, implicit impl |
| Embedding | Composition, not inheritance; methods promoted |
| Type switch | `switch v := x.(type) { case T: }` |
| Interface check | `var _ Interface = (*Type)(nil)` |
| iota | Auto-increment in const blocks |
| defer | LIFO, args eval immediately |
