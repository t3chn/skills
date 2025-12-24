# Node.js Development Plugin

Modern Node.js/TypeScript development toolkit with NestJS patterns, Drizzle ORM, Vitest testing, and ESLint 9 flat config.

## Skills

| Skill | Description |
|-------|-------------|
| [node-conventions](./skills/node-conventions/SKILL.md) | Code review context — ES modules, async patterns |
| [nestjs-patterns](./skills/nestjs-patterns/SKILL.md) | NestJS application architecture, modules, DI, guards |
| [drizzle-orm](./skills/drizzle-orm/SKILL.md) | Type-safe SQL with Drizzle ORM |
| [testing-vitest](./skills/testing-vitest/SKILL.md) | Modern testing with Vitest |

## Agents

> **Code Review:** Use official `feature-dev:code-reviewer` with `node-conventions` skill for context.

## Commands

| Command | Description |
|---------|-------------|
| `/node-test` | Run Vitest with coverage |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| eslint-check | PreToolUse | Reminds to run ESLint after TypeScript changes |

## Quick Start

### New Project

```bash
pnpm init
pnpm add typescript @types/node tsx -D
pnpm add @nestjs/common @nestjs/core @nestjs/platform-express
pnpm add drizzle-orm postgres
pnpm add -D vitest @vitest/coverage-v8 drizzle-kit
```

### Run Tests

```bash
pnpm vitest run --coverage
```

### Lint

```bash
pnpm eslint . --fix
pnpm tsc --noEmit
```

## Stack

- **Node.js 20+** - LTS with modern features
- **TypeScript 5+** - Strict mode
- **NestJS** - Enterprise framework
- **Drizzle ORM** - Type-safe SQL
- **Vitest** - Fast testing (NOT Jest)
- **ESLint 9** - Flat config
- **pnpm** - Fast package manager

## Related

- [backend-core](../backend-core/SKILL.md) - Language-agnostic API patterns
- [secrets-guardian](../secrets-guardian/SKILL.md) - Pre-commit security
