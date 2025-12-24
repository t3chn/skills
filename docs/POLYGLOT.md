# Polyglot Repository Behavior

How convention skills work in multi-language repositories.

## Overview

Convention skills auto-activate based on file globs. In polyglot repos, multiple skills may be active simultaneously.

## Glob Patterns

| Skill | Globs | Triggers On |
|-------|-------|-------------|
| go-conventions | `**/*.go`, `**/go.mod` | Go source files |
| ts-conventions | `**/*.ts`, `**/*.tsx`, `**/tsconfig.json` | TypeScript files |
| rust-conventions | `**/*.rs`, `**/Cargo.toml` | Rust files |
| python-conventions | `**/*.py`, `**/pyproject.toml` | Python files |
| node-conventions | `**/*.js`, `**/*.mjs`, `**/package.json` | JavaScript/Node files |

## Polyglot Scenarios

### Scenario 1: Full-Stack TypeScript + Go

```
myproject/
├── api/           # Go backend
│   ├── main.go
│   └── go.mod
├── web/           # TypeScript frontend
│   ├── src/
│   │   └── App.tsx
│   └── tsconfig.json
└── package.json   # Monorepo root
```

**Active skills:**
- Editing `api/*.go` → `go-conventions` active
- Editing `web/*.tsx` → `ts-conventions` active
- Editing `package.json` → `node-conventions` active

**Code review behavior:**
- `feature-dev:code-reviewer` gets language-specific context automatically
- When reviewing `api/`, Go conventions apply
- When reviewing `web/`, TypeScript conventions apply

### Scenario 2: Python + Rust Hybrid

```
myproject/
├── src/           # Rust core
│   └── lib.rs
├── python/        # Python bindings
│   └── wrapper.py
├── Cargo.toml
└── pyproject.toml
```

**Active skills:**
- Editing `src/*.rs` → `rust-conventions` active
- Editing `python/*.py` → `python-conventions` active

### Scenario 3: JavaScript + TypeScript Mixed

```
myproject/
├── src/
│   ├── index.ts   # TypeScript
│   └── config.js  # JavaScript config
├── tsconfig.json
└── package.json
```

**Active skills:**
- Editing `*.ts` → `ts-conventions` active
- Editing `*.js` → `node-conventions` active
- No overlap due to distinct globs

## Best Practices for Polyglot Repos

### 1. Use Directory-Based Organization

```
# Good - clear separation
api/          # One language
web/          # Another language
scripts/      # Third language

# Avoid - mixed files
src/
├── handler.go
├── utils.ts
└── config.py
```

### 2. Separate Review Commands

```bash
# Review Go parts only
/go-review api/

# Review TypeScript parts only
/ts-review web/
```

### 3. Project-Specific CLAUDE.md

Add language-specific rules in your project's `CLAUDE.md`:

```markdown
# Project Conventions

## Go (api/)
- Use sqlc for database queries
- Context timeout: 30s for external calls

## TypeScript (web/)
- Use Zod for all API responses
- No `any` types
```

## No Conflicts

Convention skills provide **additive context**, not conflicting rules:

- Each skill only activates for its file types
- `code-reviewer` receives all relevant context
- No priority conflicts between skills

## Testing Polyglot Setup

Run the integration test to verify skills are properly configured:

```bash
./scripts/test-skills.sh
```

All 36 checks should pass, including:
- No overlapping globs between ts/node
- All skills have required frontmatter
- Marketplace references all skills
