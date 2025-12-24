---
name: TypeScript Modern Tooling
description: This skill should be used when the user asks about "pnpm", "Bun", "tsup", "Vite", "Biome", "TypeScript config", "build tools", "bundler", "linting TypeScript", or needs guidance on modern TypeScript tooling (2025 best practices).
version: 1.0.0
---

# TypeScript Modern Tooling

Modern TypeScript development with pnpm, Biome, tsup, and Vite (2025).

## Package Managers

### pnpm (Recommended Default)

```bash
# Install pnpm
npm install -g pnpm

# Create project
pnpm init

# Add dependencies
pnpm add zod drizzle-orm
pnpm add -D typescript @types/node vitest

# Install from lockfile
pnpm install

# Run scripts
pnpm dev
pnpm build
```

**Why pnpm:**
- 70% less disk space (content-addressable storage)
- Strict dependency resolution (no phantom deps)
- Built-in monorepo support
- 2-3x faster than npm

### Bun (For Speed)

```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Create project
bun init

# Add dependencies (25x faster than npm)
bun add zod drizzle-orm
bun add -D typescript @types/bun vitest

# Run TypeScript directly
bun run src/index.ts

# Run scripts
bun dev
```

**Use Bun when:**
- Startup time matters (serverless, CLI)
- Maximum install speed needed
- Using Bun runtime features

## Build Tools

### tsup (Libraries)

Best for: TypeScript packages, CLI tools, simple builds.

```bash
pnpm add -D tsup
```

```typescript
// tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],      // Dual ESM/CJS
  dts: true,                    // Generate .d.ts
  splitting: true,              // Code splitting
  sourcemap: true,
  clean: true,                  // Clean dist/
  minify: true,                 // For production
  target: 'es2022',
  outDir: 'dist',
});
```

```json
// package.json
{
  "scripts": {
    "build": "tsup",
    "dev": "tsup --watch"
  }
}
```

### Vite (Applications)

Best for: Web apps, dev servers, HMR.

```bash
pnpm create vite my-app --template react-ts
# or
pnpm create vite my-app --template vanilla-ts
```

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  build: {
    target: 'es2022',
    sourcemap: true,
  },
  server: {
    port: 3000,
  },
});
```

### When to Use Which

| Tool | Use Case |
|------|----------|
| **tsup** | Libraries, CLI tools, simple packages |
| **Vite** | Web apps, dev server with HMR |
| **esbuild** | Direct bundling, maximum speed |
| **Rollup** | Custom plugins, complex output |

## Linting & Formatting: Biome

### Why Biome (NOT ESLint + Prettier)

- **10-25x faster** than ESLint
- **Single tool** for lint + format
- **Zero config** option
- **No plugin hell**

### Setup

```bash
pnpm add -D @biomejs/biome
pnpm biome init
```

### biome.json

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExcessiveCognitiveComplexity": "warn"
      },
      "correctness": {
        "noUnusedImports": "error",
        "noUnusedVariables": "error",
        "useExhaustiveDependencies": "warn"
      },
      "style": {
        "noNonNullAssertion": "warn",
        "useConst": "error"
      },
      "suspicious": {
        "noExplicitAny": "warn",
        "noConfusingVoidType": "error"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "always",
      "trailingCommas": "all"
    }
  }
}
```

### Usage

```bash
# Check (lint + format)
pnpm biome check .

# Fix automatically
pnpm biome check --write .

# Format only
pnpm biome format --write .

# Lint only
pnpm biome lint .

# CI mode (no writes)
pnpm biome ci .
```

### VS Code Integration

```json
// .vscode/settings.json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  }
}
```

## TypeScript Configuration

### Strict Mode (Required)

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true
  }
}
```

### What `strict: true` Enables

| Flag | Effect |
|------|--------|
| `noImplicitAny` | Error on implicit `any` |
| `strictNullChecks` | `null`/`undefined` not assignable to other types |
| `strictFunctionTypes` | Contravariant function parameter checking |
| `strictBindCallApply` | Type-safe `bind`, `call`, `apply` |
| `strictPropertyInitialization` | Class properties must be initialized |
| `noImplicitThis` | Error on `this` with implicit `any` |
| `alwaysStrict` | Emit `"use strict"` |
| `useUnknownInCatchVariables` | Catch variables are `unknown` |

### Module Resolution (2025)

```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "verbatimModuleSyntax": true,
    "isolatedModules": true
  }
}
```

## package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "typecheck": "tsc --noEmit",
    "ci": "biome ci . && pnpm typecheck && pnpm test:coverage"
  }
}
```

## Anti-patterns

| Wrong | Right |
|-------|-------|
| `npm install` | `pnpm add` |
| ESLint + Prettier + 50 plugins | Biome |
| `tsc` for bundling | tsup or Vite |
| `strict: false` | `strict: true` |
| `any` everywhere | Proper types |
| CommonJS (`require`) | ESM (`import`) |

## Quick Start Template

```bash
# Create project
mkdir my-project && cd my-project
pnpm init

# Install dependencies
pnpm add -D typescript @types/node tsup vitest @biomejs/biome

# Initialize configs
pnpm tsc --init
pnpm biome init

# Create structure
mkdir src tests
echo 'export const hello = "world";' > src/index.ts
```

## Related Skills

- **project-structure** — Directory organization
- **type-patterns** — TypeScript strict mode patterns
- **testing-patterns** — Vitest configuration
