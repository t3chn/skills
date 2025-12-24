---
description: Generate Vitest tests for TypeScript code
allowed-tools: Bash(pnpm:*), Bash(vitest:*), Bash(ls:*), Read, Write, Edit, Glob, Grep
argument-hint: <file-or-function> [unit|integration]
---

# Generate TypeScript Tests

## Context

- Current directory: !`pwd`
- Vitest config: !`test -f vitest.config.ts && echo "vitest.config.ts found" || echo "No vitest config"`
- Test files: !`find . -name "*.test.ts" -o -name "*.spec.ts" 2>/dev/null | head -10 || echo "No test files"`
- Source file: !`test -f "$1" && head -20 "$1" || echo "File not specified or not found"`

## Task

Generate Vitest tests for:
- **Target:** $1 (file path or function name)
- **Test type:** $2 (default: unit)

### Test Types
- `unit` — Isolated tests with mocking, co-located with source
- `integration` — Tests with real dependencies, in tests/ directory

## Requirements

1. **Analyze target code**
   - Read the source file
   - Identify functions/classes/methods
   - Understand types and dependencies
   - Find existing test patterns in codebase

2. **Plan test coverage**
   - Happy path scenarios
   - Error cases and exceptions
   - Edge cases (null, undefined, empty, boundary)
   - Async behavior
   - Type narrowing

3. **Generate tests with Vitest**
   ```typescript
   import { describe, it, expect, beforeEach, vi } from 'vitest';

   describe('ComponentName', () => {
     it('should do something when condition', () => {
       // Arrange, Act, Assert
     });
   });
   ```

4. **Include mocking**
   - Use `vi.fn()` for functions
   - Use `vi.mock()` for modules
   - Use `vi.spyOn()` for spying
   - Use `vi.useFakeTimers()` for timers

5. **Verify tests run**
   ```bash
   pnpm vitest run <test-file>
   ```

## Output

After generation:
- Test file path
- Number of tests created
- Coverage summary
- Command to run tests

## Best Practices

- Use `describe` for grouping
- Use `it('should X when Y')` naming
- One assertion concept per test
- Mock external dependencies
- Test error messages
- Cover edge cases

Use the `ts-test-generator` agent for complex test generation.
