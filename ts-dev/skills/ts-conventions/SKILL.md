---
name: ts-conventions
description: TypeScript project conventions and best practices for code review context. Use with official feature-dev:code-reviewer agent.
globs: ["**/*.ts", "**/*.tsx", "**/tsconfig.json"]
---

# TypeScript Conventions

Context for code review of TypeScript projects. These conventions inform the official `feature-dev:code-reviewer` agent.

## Type Safety

### Prefer Strict Types Over `any`
```typescript
// WRONG
function process(data: any): any

// CORRECT
function process<T extends Record<string, unknown>>(data: T): ProcessedData<T>
```

### Use Type Guards
```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}
```

### Discriminated Unions
```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Usage
if (result.success) {
  console.log(result.data);  // TypeScript knows data exists
}
```

## Error Handling

### Custom Error Classes
```typescript
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
  }
}
```

### Result Pattern (No Exceptions for Flow Control)
```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const user = await db.users.findUnique({ where: { id } });
    if (!user) {
      return { ok: false, error: new NotFoundError('User') };
    }
    return { ok: true, value: user };
  } catch (e) {
    return { ok: false, error: e as Error };
  }
}
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Interfaces | PascalCase, no `I` prefix | `User`, `ApiResponse` |
| Types | PascalCase | `UserRole`, `RequestConfig` |
| Functions | camelCase | `getUserById`, `parseConfig` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `API_URL` |
| React Components | PascalCase | `UserProfile`, `DataTable` |
| Hooks | use* prefix | `useAuth`, `useLocalStorage` |

## Modern Patterns

### Zod for Runtime Validation
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(['admin', 'user']),
});

type User = z.infer<typeof UserSchema>;

// Validate at runtime
const user = UserSchema.parse(unknownData);
```

### Branded Types for Type Safety
```typescript
type UserId = string & { readonly brand: unique symbol };
type OrderId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId;
}

// Now getUserById(orderId) is a compile error!
```

### 2025 Tooling

**Runtimes:**
- **Bun** — Faster runtime, built-in bundler, native TypeScript
- **Node 22+** — Native TypeScript via `--experimental-strip-types`

**Validation alternatives:**
- **Valibot** — Lighter than Zod (~1KB vs ~12KB), same API
- **ArkType** — Type-safe at compile time, fast runtime

**Package managers:**
- **pnpm** — Fast, disk-efficient (recommended)
- **Bun** — Built-in package manager, fastest installs

## Testing Patterns

### Vitest Structure
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('UserService', () => {
  let service: UserService;
  let mockRepo: MockProxy<UserRepository>;

  beforeEach(() => {
    mockRepo = mock<UserRepository>();
    service = new UserService(mockRepo);
  });

  describe('getUser', () => {
    it('returns user when found', async () => {
      const expected = { id: '1', name: 'Test' };
      mockRepo.findById.mockResolvedValue(expected);

      const result = await service.getUser('1');

      expect(result).toEqual(expected);
      expect(mockRepo.findById).toHaveBeenCalledWith('1');
    });

    it('throws NotFoundError when user missing', async () => {
      mockRepo.findById.mockResolvedValue(null);

      await expect(service.getUser('1')).rejects.toThrow(NotFoundError);
    });
  });
});
```

### MSW for API Mocking
```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Test' });
  }),
];

const server = setupServer(...handlers);
```

## Project Structure

```
src/
├── components/          # React components
├── hooks/              # Custom hooks
├── lib/                # Core utilities
├── services/           # Business logic
├── types/              # Shared types
├── utils/              # Helper functions
└── index.ts            # Entry point
```

## Async Patterns

### Avoid Floating Promises
```typescript
// WRONG
button.onClick = () => {
  fetchData();  // Floating promise!
};

// CORRECT
button.onClick = () => {
  void fetchData();  // Explicit void
};

// Or handle errors
button.onClick = () => {
  fetchData().catch(handleError);
};
```

### Use Promise.all for Parallel
```typescript
// Sequential (slow)
const user = await getUser(id);
const orders = await getOrders(id);

// Parallel (fast)
const [user, orders] = await Promise.all([
  getUser(id),
  getOrders(id),
]);
```

## Security

- Validate all external input with Zod
- Use parameterized queries (never string SQL)
- Escape HTML output (React does this automatically)
- Never store secrets in client code
- Use HTTPS for all API calls
- Set Content-Security-Policy headers

## Code Review Checklist

- [ ] No `any` types (use `unknown` if needed)
- [ ] Errors handled with Result pattern or try/catch
- [ ] No floating promises
- [ ] Input validated at boundaries (Zod)
- [ ] Types exported from dedicated files
- [ ] Tests cover happy path and error cases
- [ ] No hardcoded secrets or URLs
- [ ] Discriminated unions for state
