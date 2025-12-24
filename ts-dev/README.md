# ts-dev

Modern TypeScript development toolkit for Claude Code (2025 best practices).

## Overview

This plugin provides skills, agents, and commands for TypeScript development with:
- **Biome** for linting/formatting (not ESLint)
- **Vitest** for testing (not Jest)
- **tsup/Vite** for building
- **pnpm** as package manager
- **Hono/tRPC** for APIs
- **Drizzle** for databases

## Skills

| Skill | Description |
|-------|-------------|
| `project-structure` | Monorepo patterns, tsconfig bases, barrel exports |
| `modern-tooling` | pnpm, Biome, tsup, Vite configuration |
| `type-patterns` | Strict mode, utility types, generics, type guards |
| `testing-patterns` | Vitest setup, mocking, async testing |
| `api-patterns` | Hono, tRPC, Zod validation, error handling |
| `database-patterns` | Drizzle ORM schema, queries, transactions |

## Agents

| Agent | Description | Color |
|-------|-------------|-------|
| `ts-code-reviewer` | Review code for type safety and patterns | Blue |
| `ts-project-init` | Scaffold new TypeScript projects | Green |
| `ts-test-generator` | Generate Vitest tests | Cyan |

## Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `/ts-init` | `/ts-init myproject api` | Initialize TypeScript project |
| `/ts-review` | `/ts-review src/ types` | Review code for issues |
| `/ts-test` | `/ts-test src/service.ts` | Generate tests for file |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `biome-check` | PostToolUse | Check formatting after edits |

## Templates

- `tsconfig.json` — Strict TypeScript configuration
- `biome.json` — Biome linter/formatter config
- `gitignore.txt` — Node/TypeScript ignores

## Installation

Add to your Claude Code plugins:

```json
{
  "plugins": ["ts-dev"]
}
```

## Relationship with node-dev

- **ts-dev** — Pure TypeScript patterns, type safety, modern tooling
- **node-dev** — NestJS backend framework patterns

They complement each other. Use ts-dev for TypeScript fundamentals, node-dev for NestJS-specific patterns.

## Stack Recommendations

| Category | Recommendation |
|----------|---------------|
| Package Manager | pnpm |
| Build (Library) | tsup |
| Build (App) | Vite |
| Linting | Biome |
| Testing | Vitest |
| API Framework | Hono |
| RPC | tRPC |
| Validation | Zod |
| Database | Drizzle ORM |
| Monorepo | Turborepo |

## License

MIT
