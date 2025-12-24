---
name: tdd-workflow
description: |
  Test-Driven Development workflow patterns and practices for Go, TypeScript, Python, and Rust.
  Use this skill when writing tests first, following Red-Green-Refactor, or enforcing TDD discipline.
globs:
  - "**/*.go"
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.py"
  - "**/*.rs"
  - "**/test_*.py"
  - "**/*_test.go"
  - "**/*.test.ts"
  - "**/*.spec.ts"
---

# Test-Driven Development Workflow

## The Red-Green-Refactor Cycle

TDD follows a strict three-phase cycle that must be repeated for each behavior:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────┐     ┌─────────┐     ┌───────────┐            │
│   │   RED   │ ──► │  GREEN  │ ──► │ REFACTOR  │ ──┐        │
│   │  Write  │     │ Minimal │     │  Improve  │   │        │
│   │ Failing │     │  Code   │     │   Code    │   │        │
│   │  Test   │     │ to Pass │     │  Safely   │   │        │
│   └─────────┘     └─────────┘     └───────────┘   │        │
│        ▲                                          │        │
│        └──────────────────────────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: RED - Write Failing Test

**Purpose:** Define the expected behavior before implementation.

**Rules:**
1. Write exactly ONE test for ONE behavior
2. Test must FAIL before writing any implementation
3. Test must fail for the RIGHT reason (not syntax/import error)
4. Test name describes the expected behavior

**Commit convention:** `test: add test for <behavior>`

### Phase 2: GREEN - Minimal Implementation

**Purpose:** Make the test pass with minimal code.

**Rules:**
1. Write ONLY enough code to make the failing test pass
2. Don't anticipate future requirements
3. Don't refactor yet — ugly code is OK
4. Stop when the test passes

**Commit convention:** `feat: implement <behavior>`

### Phase 3: REFACTOR - Improve with Safety

**Purpose:** Clean up code while tests protect you.

**Rules:**
1. Tests must pass after EVERY change
2. If tests fail, undo immediately
3. Apply design patterns, extract methods, improve names
4. Remove duplication

**Commit convention:** `refactor: improve <aspect>`

---

## Language-Specific Patterns

### Go

**Test file:** `*_test.go` (same directory, same package)

**Test command:** `go test ./...`

```go
// user_test.go
package user

import "testing"

func TestCreateUser_WithValidEmail_ReturnsUser(t *testing.T) {
    // Arrange
    email := "test@example.com"

    // Act
    user, err := CreateUser(email)

    // Assert
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.Email != email {
        t.Errorf("got email %q, want %q", user.Email, email)
    }
}

// Table-driven test (preferred for multiple cases)
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "user@example.com", false},
        {"empty email", "", true},
        {"no at sign", "invalid", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail(%q) error = %v, wantErr %v",
                    tt.email, err, tt.wantErr)
            }
        })
    }
}
```

**TDD Cycle Example (Go):**

```bash
# RED: Write failing test
echo 'func TestAdd(t *testing.T) { if Add(2, 3) != 5 { t.Fail() } }' >> math_test.go
go test ./...  # FAIL: undefined: Add

# GREEN: Minimal implementation
echo 'func Add(a, b int) int { return a + b }' >> math.go
go test ./...  # PASS

# REFACTOR: Improve (if needed)
# No refactoring needed for simple function
```

---

### TypeScript

**Test file:** `*.test.ts` or `*.spec.ts`

**Test command:** `npm test` or `pnpm vitest run`

```typescript
// user.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { createUser, validateEmail } from './user';

describe('createUser', () => {
  it('should create user with valid email', () => {
    // Arrange
    const email = 'test@example.com';

    // Act
    const user = createUser(email);

    // Assert
    expect(user.email).toBe(email);
    expect(user.id).toBeDefined();
  });

  it('should throw for invalid email', () => {
    expect(() => createUser('')).toThrow('Invalid email');
  });
});

describe('validateEmail', () => {
  it.each([
    ['user@example.com', true],
    ['', false],
    ['invalid', false],
  ])('validateEmail(%s) should return %s', (email, expected) => {
    expect(validateEmail(email)).toBe(expected);
  });
});
```

**TDD Cycle Example (TypeScript):**

```bash
# RED: Write failing test
cat >> src/math.test.ts << 'EOF'
import { add } from './math';
it('adds two numbers', () => expect(add(2, 3)).toBe(5));
EOF
npm test  # FAIL: Cannot find module './math'

# GREEN: Minimal implementation
cat >> src/math.ts << 'EOF'
export const add = (a: number, b: number): number => a + b;
EOF
npm test  # PASS

# REFACTOR: Add types, documentation if needed
```

---

### Python

**Test file:** `test_*.py` or `*_test.py`

**Test command:** `pytest` or `python -m pytest`

```python
# test_user.py
import pytest
from user import create_user, validate_email

class TestCreateUser:
    def test_creates_user_with_valid_email(self):
        # Arrange
        email = "test@example.com"

        # Act
        user = create_user(email)

        # Assert
        assert user.email == email
        assert user.id is not None

    def test_raises_for_invalid_email(self):
        with pytest.raises(ValueError, match="Invalid email"):
            create_user("")

@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("", False),
    ("invalid", False),
])
def test_validate_email(email, expected):
    assert validate_email(email) == expected
```

**TDD Cycle Example (Python):**

```bash
# RED: Write failing test
cat >> test_math.py << 'EOF'
from math_utils import add
def test_add(): assert add(2, 3) == 5
EOF
pytest  # FAIL: ModuleNotFoundError

# GREEN: Minimal implementation
cat >> math_utils.py << 'EOF'
def add(a: int, b: int) -> int:
    return a + b
EOF
pytest  # PASS

# REFACTOR: Add docstrings, type hints if missing
```

---

### Rust

**Test file:** Same file with `#[cfg(test)]` module or `tests/*.rs`

**Test command:** `cargo test`

```rust
// user.rs
pub fn create_user(email: &str) -> Result<User, UserError> {
    if !validate_email(email) {
        return Err(UserError::InvalidEmail);
    }
    Ok(User { email: email.to_string(), id: generate_id() })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_user_with_valid_email() {
        // Arrange
        let email = "test@example.com";

        // Act
        let result = create_user(email);

        // Assert
        assert!(result.is_ok());
        assert_eq!(result.unwrap().email, email);
    }

    #[test]
    fn test_create_user_with_invalid_email_returns_error() {
        let result = create_user("");

        assert!(result.is_err());
        assert!(matches!(result, Err(UserError::InvalidEmail)));
    }

    #[test]
    #[should_panic(expected = "empty email")]
    fn test_panics_on_empty_email() {
        create_user_or_panic("");
    }
}
```

**TDD Cycle Example (Rust):**

```bash
# RED: Write failing test
cat >> src/lib.rs << 'EOF'
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_add() { assert_eq!(add(2, 3), 5); }
}
EOF
cargo test  # FAIL: cannot find function `add`

# GREEN: Minimal implementation
cat >> src/lib.rs << 'EOF'
pub fn add(a: i32, b: i32) -> i32 { a + b }
EOF
cargo test  # PASS

# REFACTOR: Generics, better error handling if needed
```

---

## Test Naming Conventions

Good test names describe:
1. **What** is being tested (function/method)
2. **Conditions** (inputs, state)
3. **Expected outcome**

| Language | Convention | Example |
|----------|-----------|---------|
| Go | `Test<Function>_<Condition>_<Outcome>` | `TestCreateUser_WithInvalidEmail_ReturnsError` |
| TypeScript | `should <outcome> when <condition>` | `'should throw error when email is invalid'` |
| Python | `test_<function>_<condition>_<outcome>` | `test_create_user_with_invalid_email_raises` |
| Rust | `test_<function>_<condition>_<outcome>` | `test_create_user_invalid_email_returns_error` |

---

## Edge Cases to Always Test

### 1. Empty/Null/Zero Values
```
- Empty strings: ""
- Null/None values
- Zero numbers: 0, 0.0
- Empty collections: [], {}, ()
```

### 2. Boundary Conditions
```
- First/last elements
- Min/max values: i32::MIN, i32::MAX
- Off-by-one: n-1, n, n+1
- Length boundaries
```

### 3. Error Cases
```
- Invalid input
- Missing required fields
- Permission denied
- Network failures (for integration tests)
```

### 4. Concurrency (if applicable)
```
- Race conditions
- Deadlocks
- Thread safety
```

---

## TDD Anti-Patterns to Avoid

### 1. Writing Tests After Code
- **Problem:** Tests just verify existing implementation
- **Fix:** Write test first, watch it fail, then implement

### 2. Testing Implementation Details
- **Problem:** Tests break when refactoring
- **Fix:** Test behavior, not implementation

### 3. Large Tests
- **Problem:** One test covers multiple behaviors
- **Fix:** One test = one behavior

### 4. Shared Mutable State
- **Problem:** Tests affect each other
- **Fix:** Isolate tests, use fresh fixtures

### 5. Skipping Refactor Phase
- **Problem:** Technical debt accumulates
- **Fix:** Always refactor after green

---

## Integration with CI/CD

### Pre-commit Hook
```bash
#!/bin/bash
# Run tests before allowing commit
go test ./... || exit 1
npm test || exit 1
pytest || exit 1
cargo test || exit 1
```

### GitHub Actions Example
```yaml
name: TDD Verification
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          go test ./...
          npm test
          pytest
          cargo test
```

---

## TDD Workflow Commands

| Command | Purpose |
|---------|---------|
| `/tdd <feature>` | Start TDD workflow for a feature |
| `/tdd-status` | Check TDD compliance status |

---

## Configuration

Configure TDD enforcer in `.claude/tdd-enforcer.local.md`:

```yaml
---
strictMode: false    # true = block, false = warn
testCommand: null    # auto-detect or override
---

## Custom Rules

Add project-specific TDD notes here.
```
