---
description: Generate idiomatic Go tests for a file or function
allowed-tools: Read, Write, Edit, Bash(go:*), Glob, Grep
argument-hint: <file.go> [table|testify|benchmark]
---

# Generate Go Tests

## Context

- Target file: !`test -f "$1" && echo "exists: $1" || echo "file not found: $1"`
- Package: !`test -f "$1" && head -5 "$1" | grep "^package" || echo "unknown"`
- Existing tests: !`test -f "${1%.go}_test.go" && echo "yes: ${1%.go}_test.go" || echo "no"`
- Testify available: !`grep -q "testify" go.mod 2>/dev/null && echo "yes" || echo "no"`

## Task

Generate tests for:
- **Target:** $1 (Go file or function name)
- **Style:** $2 (default: table)

### Test Styles

| Style | Description | Use When |
|-------|-------------|----------|
| `table` | Standard library table-driven | Default, no dependencies |
| `testify` | With github.com/stretchr/testify | Better assertions, existing testify usage |
| `benchmark` | Include performance benchmarks | Performance-critical code |

## Generation Process

1. **Read target file** and identify:
   - Public functions and methods
   - Input/output types
   - Dependencies (interfaces to mock)

2. **Generate test cases** for each function:
   - Happy path (valid input → expected output)
   - Error cases (invalid input → error)
   - Edge cases (empty, nil, boundary values)

3. **Create mocks** for interface dependencies

4. **Write test file:**
   - Place adjacent to source: `foo.go` → `foo_test.go`
   - Use same package or `_test` suffix

5. **Verify tests compile:**
   ```bash
   go test -v ./path/to/... -run TestNone
   ```

## Test Template (Table-Driven)

```go
func TestFunctionName(t *testing.T) {
    tests := []struct {
        name    string
        input   Type
        want    Type
        wantErr bool
    }{
        {"valid", validInput, expectedOutput, false},
        {"empty", "", Type{}, true},
        {"edge case", edgeInput, edgeOutput, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := FunctionName(tt.input)
            // assertions...
        })
    }
}
```

## Output

After generation:
```
## Tests Generated: [file_test.go]

### Coverage
- FunctionA: 4 test cases
- FunctionB: 3 test cases

### Run Tests
go test -v ./path/...
go test -cover ./path/...
```

For complex test generation, use the `go-test-generator` agent.
