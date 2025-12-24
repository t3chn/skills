---
name: tdd-status
description: Check TDD compliance status for the current session
---

# TDD Compliance Check

Analyze the current session for TDD compliance.

## Analysis Tasks

### 1. Check Code Modifications

Search for recent file modifications:
- Source code files (`.go`, `.ts`, `.py`, `.rs`)
- Test files (`*_test.go`, `*.test.ts`, `test_*.py`, `*_test.rs`)

### 2. Check Test Execution

Look for test commands that were run:
- `go test ./...`
- `npm test` / `pnpm vitest`
- `pytest`
- `cargo test`

### 3. Determine Compliance Status

**Compliant** if:
- No code modifications, OR
- Tests were executed after modifications

**Warning** if:
- Code was modified without running tests
- Test files were not modified (tests may exist but weren't written first)

**Non-compliant** if:
- Multiple code files modified without any test execution
- Test failures were ignored

## Report Format

Provide a status report:

```
## TDD Status Report

**Status:** [Compliant | Warning | Non-Compliant]

### Code Modifications
- [list of modified source files]

### Test Files Modified
- [list of modified test files]

### Tests Executed
- [list of test commands run]

### Recommendations
- [specific actions to improve compliance]
```

## Next Steps

If non-compliant, recommend:
1. Run the appropriate test command
2. Use `/tdd <feature>` for new features
3. Use the **test-analyzer** agent to find coverage gaps
