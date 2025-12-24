---
name: TypeScript Project Structure
description: This skill should be used when the user asks about "TypeScript project", "tsconfig", "monorepo", "Turborepo", "pnpm workspaces", "project layout", "barrel exports", "path aliases", or needs guidance on TypeScript project organization.
version: 1.0.0
---

# TypeScript Project Structure

Modern TypeScript project organization with monorepo patterns (2025).

## Single Package Structure

```
mypackage/
├── src/
│   ├── index.ts              # Main entry point (barrel export)
│   ├── types.ts              # Shared type definitions
│   ├── utils/
│   │   ├── index.ts          # Barrel export
│   │   └── helpers.ts
│   └── features/
│       ├── users/
│       │   ├── index.ts      # Feature barrel
│       │   ├── types.ts
│       │   ├── service.ts
│       │   └── repository.ts
│       └── posts/
│           └── ...
├── tests/
│   ├── setup.ts
│   └── features/
│       └── users.test.ts
├── dist/                     # Built output (gitignored)
├── package.json
├── tsconfig.json
├── biome.json
└── vitest.config.ts
```

## Monorepo Structure (Turborepo + pnpm)

```
monorepo/
├── apps/
│   ├── web/                  # Next.js/SvelteKit app
│   │   ├── src/
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── api/                  # Hono/tRPC backend
│       ├── src/
│       ├── package.json
│       └── tsconfig.json
├── packages/
│   ├── shared/               # Shared types & utilities
│   │   ├── src/
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── ui/                   # Shared UI components
│   │   └── ...
│   └── config/               # Shared configs
│       ├── tsconfig/
│       │   ├── base.json
│       │   ├── node.json
│       │   └── react.json
│       └── biome/
│           └── biome.json
├── turbo.json
├── pnpm-workspace.yaml
├── package.json
└── biome.json
```

## tsconfig.json Patterns

### Base Configuration

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    // Language & Environment
    "target": "ES2022",
    "lib": ["ES2022"],

    // Modules
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "resolveJsonModule": true,

    // Strict Type Checking (ALL ON)
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,

    // Emit
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "dist",

    // Interop
    "esModuleInterop": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,

    // Performance
    "skipLibCheck": true,
    "incremental": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Library Configuration

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "composite": true,
    "outDir": "dist"
  },
  "include": ["src"],
  "exclude": ["**/*.test.ts"]
}
```

### React/Browser Configuration

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "noEmit": true
  }
}
```

## Barrel Exports

### Pattern

```typescript
// src/features/users/index.ts
export { UserService } from './service';
export { UserRepository } from './repository';
export type { User, CreateUserInput } from './types';

// Re-export everything
export * from './types';
export * from './service';
```

### Anti-pattern: Circular Dependencies

```typescript
// BAD: Creates circular import
// src/features/users/service.ts
import { PostService } from '../posts'; // posts imports users!

// GOOD: Extract shared types
// src/shared/types.ts
export interface User { ... }

// Both services import from shared
import type { User } from '@/shared/types';
```

## Path Aliases

### tsconfig.json

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/features/*": ["src/features/*"],
      "@/utils/*": ["src/utils/*"]
    }
  }
}
```

### Usage

```typescript
// Instead of relative paths
import { UserService } from '../../../features/users';

// Use aliases
import { UserService } from '@/features/users';
```

## Monorepo Setup (Turborepo + pnpm)

### pnpm-workspace.yaml

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### turbo.json

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {},
    "typecheck": {
      "dependsOn": ["^build"]
    }
  }
}
```

### Root package.json

```json
{
  "name": "monorepo",
  "private": true,
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "test": "turbo test",
    "lint": "turbo lint && biome check .",
    "typecheck": "turbo typecheck"
  },
  "devDependencies": {
    "@biomejs/biome": "^1.9.0",
    "turbo": "^2.3.0",
    "typescript": "^5.7.0"
  },
  "packageManager": "pnpm@9.15.0"
}
```

### Package References

```json
// apps/web/package.json
{
  "name": "@monorepo/web",
  "dependencies": {
    "@monorepo/shared": "workspace:*",
    "@monorepo/ui": "workspace:*"
  }
}
```

## Entry Points (package.json exports)

```json
{
  "name": "my-library",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./utils": {
      "types": "./dist/utils/index.d.ts",
      "import": "./dist/utils/index.js"
    }
  },
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "files": ["dist"]
}
```

## Best Practices

### DO:
- Use `src/` for source, `dist/` for output
- Group by feature, not by type (services/, repositories/)
- Use barrel exports (`index.ts`) for clean imports
- Keep shared types in `src/types.ts` or `src/shared/`
- Use path aliases for deep imports
- Use `workspace:*` for monorepo dependencies

### DON'T:
- Mix source and output in same directory
- Create circular dependencies between features
- Export everything from root (breaks tree-shaking)
- Use relative paths like `../../../`
- Commit `node_modules/` or `dist/`

## Related Skills

- **modern-tooling** — Build tools and package managers
- **type-patterns** — TypeScript type organization
