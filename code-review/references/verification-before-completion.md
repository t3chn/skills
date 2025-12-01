# Verification Before Completion

> **Iron Law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

## Contents
- [The Gate Function](#the-gate-function)
- [Common Failures](#common-failures)
- [Red Flags](#red-flags)
- [Key Patterns](#key-patterns)
- [Stack-Specific Commands](#stack-specific-commands)

## The Gate Function

```
BEFORE claiming any status:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Original symptom: passes | Code changed |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |

## Key Patterns

**Tests:**
```
✅ [Run test] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**TDD Red-Green:**
```
✅ Write → Run (pass) → Revert fix → Run (FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter ≠ compiler)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## Stack-Specific Commands

**Node.js/TypeScript:**
```bash
npm run lint          # or: npx eslint .
npm run typecheck     # or: npx tsc --noEmit
npm test              # or: npx vitest run
npm run build         # verify production build
```

**Python:**
```bash
ruff check .          # linting
ruff format --check . # formatting
mypy .                # type checking
pytest                # tests
python -m build       # verify package builds
```

**Go:**
```bash
go fmt ./...          # formatting
go vet ./...          # static analysis
golangci-lint run     # comprehensive linting
go test ./...         # tests
go build ./...        # verify build
```

**Rust:**
```bash
cargo fmt -- --check  # formatting
cargo clippy          # linting
cargo test            # tests
cargo build --release # verify release build
```

## When To Apply

**ALWAYS before:**
- ANY success/completion claims
- ANY expression of satisfaction
- Committing, PR creation, task completion
- Moving to next task

**No shortcuts. Run the command. Read the output. THEN claim the result.**
