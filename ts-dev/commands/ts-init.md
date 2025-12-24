---
description: Initialize a new TypeScript project with modern structure
allowed-tools: Bash(pnpm:*), Bash(bun:*), Bash(npm:*), Bash(mkdir:*), Bash(ls:*), Bash(node:*), Write, Edit, Read
argument-hint: <project-name> [library|api|fullstack|monorepo]
---

# Initialize TypeScript Project

## Context

- Current directory: !`pwd`
- Node version: !`node --version 2>/dev/null || echo "Node not installed"`
- pnpm version: !`pnpm --version 2>/dev/null || echo "pnpm not installed"`
- Directory contents: !`ls -la 2>/dev/null | head -10`
- Existing package.json: !`test -f package.json && cat package.json | head -5 || echo "none"`

## Task

Create a new TypeScript project with the following parameters:
- **Project name:** $1
- **Project type:** $2 (default: library)

### Project Types
- `library` — Publishable npm package with tsup, ESM + CJS
- `api` — Hono backend with Drizzle ORM, Zod validation
- `fullstack` — Vite frontend + Hono backend in monorepo
- `monorepo` — Turborepo + pnpm workspaces setup

## Requirements

1. **Validate environment**
   - Verify Node.js is installed (v20+)
   - Check pnpm is available (install if needed)
   - Confirm current directory is suitable

2. **Create structure** based on project type:
   ```
   # Library
   src/index.ts
   tests/index.test.ts

   # API
   src/index.ts
   src/routes/health.ts
   src/db/schema.ts
   tests/routes/health.test.ts

   # Fullstack
   apps/web/src/main.tsx
   apps/api/src/index.ts
   packages/shared/src/index.ts

   # Monorepo
   apps/
   packages/
   turbo.json
   pnpm-workspace.yaml
   ```

3. **Generate config files:**
   - `tsconfig.json` — Strict TypeScript config
   - `biome.json` — Linter/formatter config
   - `vitest.config.ts` — Test configuration
   - `tsup.config.ts` — Build config (library)
   - `package.json` — Dependencies and scripts
   - `.gitignore` — Ignore patterns

4. **Initialize and verify:**
   ```bash
   pnpm install
   pnpm typecheck
   pnpm lint
   pnpm test:run
   ```

## Output

After creation, display:
- Directory tree
- Available npm scripts
- Next steps for development

Use the `ts-project-init` agent if complex scaffolding is needed.
