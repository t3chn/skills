---
name: Vitest Testing
description: This skill should be used when the user asks about "Vitest", "Node.js tests", "TypeScript tests", "testing NestJS", "mocking vi", "test coverage", or needs guidance on modern Node.js testing with Vitest.
version: 1.0.0
---

# Vitest Testing

Modern Node.js/TypeScript testing with Vitest (NOT Jest).

## Setup

```bash
pnpm add -D vitest @vitest/coverage-v8
```

## Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['**/*.{test,spec}.{ts,js}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'dist/', '**/*.d.ts'],
    },
    setupFiles: ['./tests/setup.ts'],
  },
});
```

## Basic Tests

```typescript
// tests/user.service.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { UserService } from '../src/users/users.service';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
    vi.clearAllMocks();
  });

  it('should create user', async () => {
    const user = await service.create({ email: 'test@example.com' });
    expect(user.id).toBeDefined();
  });

  it('should throw on duplicate email', async () => {
    await service.create({ email: 'test@example.com' });

    await expect(
      service.create({ email: 'test@example.com' })
    ).rejects.toThrow('Email already exists');
  });
});
```

## Mocking with vi

### Basic Mocking

```typescript
import { vi, describe, it, expect } from 'vitest';

// Mock a module
vi.mock('../src/email/email.service', () => ({
  EmailService: vi.fn(() => ({
    send: vi.fn().mockResolvedValue(true),
  })),
}));

// Mock a function
const mockFn = vi.fn();
mockFn.mockReturnValue('mocked');
mockFn.mockResolvedValue('async mocked');
mockFn.mockRejectedValue(new Error('error'));

// Mock implementation
mockFn.mockImplementation((x) => x * 2);
```

### Spy on Methods

```typescript
import { vi, describe, it, expect } from 'vitest';

describe('Spying', () => {
  it('should spy on method', () => {
    const obj = {
      method: (x: number) => x * 2,
    };

    const spy = vi.spyOn(obj, 'method');

    obj.method(5);

    expect(spy).toHaveBeenCalledWith(5);
    expect(spy).toHaveReturnedWith(10);
  });
});
```

### Mock Timers

```typescript
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('Timers', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should handle setTimeout', async () => {
    const callback = vi.fn();

    setTimeout(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalled();
  });
});
```

## E2E Testing with NestJS

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { Test } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import request from 'supertest';
import { AppModule } from '../src/app.module';

describe('Users (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleRef.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('/users (POST)', async () => {
    const response = await request(app.getHttpServer())
      .post('/users')
      .send({ email: 'test@example.com', name: 'Test', password: 'password123' })
      .expect(201);

    expect(response.body.id).toBeDefined();
  });

  it('/users/:id (GET)', async () => {
    const response = await request(app.getHttpServer())
      .get('/users/1')
      .expect(200);

    expect(response.body.email).toBe('test@example.com');
  });
});
```

## Testing with Database

```typescript
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import { db } from '../src/db';
import { users } from '../src/db/schema';
import { sql } from 'drizzle-orm';

describe('UserRepository', () => {
  beforeAll(async () => {
    // Run migrations or setup
  });

  beforeEach(async () => {
    // Clean database
    await db.execute(sql`TRUNCATE TABLE users CASCADE`);
  });

  afterAll(async () => {
    // Close connection
  });

  it('should insert user', async () => {
    const [user] = await db.insert(users).values({
      email: 'test@example.com',
      name: 'Test',
      hashedPassword: 'hash',
    }).returning();

    expect(user.id).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });
});
```

## HTTP Mocking with msw

```typescript
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { describe, it, expect, beforeAll, afterAll, afterEach } from 'vitest';

const server = setupServer(
  http.get('https://api.example.com/users/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'John' });
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('API Client', () => {
  it('should fetch user', async () => {
    const response = await fetch('https://api.example.com/users/1');
    const user = await response.json();

    expect(user.name).toBe('John');
  });
});
```

## Running Tests

```bash
# Run all tests
pnpm vitest

# Watch mode
pnpm vitest --watch

# Run specific file
pnpm vitest user.service.test.ts

# With coverage
pnpm vitest --coverage

# UI mode
pnpm vitest --ui

# Run once (CI)
pnpm vitest run
```

## package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:cov": "vitest run --coverage",
    "test:watch": "vitest --watch",
    "test:ui": "vitest --ui"
  }
}
```

## Best Practices

### DO:
- Use `describe` blocks to group related tests
- Use `beforeEach` to reset state
- Mock external services (APIs, databases in unit tests)
- Use meaningful test names: `should_doX_when_conditionY`
- Test edge cases and error paths
- Use `vi.clearAllMocks()` in `beforeEach`

### DON'T:
- Share state between tests
- Use `time.sleep()` - use fake timers
- Test implementation details
- Mock everything in integration tests
- Use `any` type in test code

## Related Skills

- **nestjs-patterns** - Testing NestJS applications
- **drizzle-orm** - Testing database queries
