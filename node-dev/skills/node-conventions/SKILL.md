---
name: node-conventions
description: Node.js/JavaScript conventions and best practices for code review context. Use with official feature-dev:code-reviewer agent.
globs: ["**/*.js", "**/*.mjs", "**/*.cjs", "**/package.json"]
---

# Node.js Conventions

Context for code review of Node.js/JavaScript projects. These conventions inform the official `feature-dev:code-reviewer` agent.

## Modern JavaScript

### Use ES Modules
```javascript
// CORRECT - ES modules
import { readFile } from 'node:fs/promises';
import express from 'express';

export function createApp() { ... }

// WRONG - CommonJS (unless required)
const fs = require('fs');
module.exports = { ... };
```

### Use Node Protocol for Builtins
```javascript
// CORRECT
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

// WRONG
import { readFile } from 'fs/promises';
```

### Prefer `const` and `let`
```javascript
// CORRECT
const config = loadConfig();
let retryCount = 0;

// WRONG
var config = loadConfig();  // No var!
```

## Error Handling

### Custom Error Classes
```javascript
export class AppError extends Error {
  constructor(message, code = 'UNKNOWN', statusCode = 500) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.statusCode = statusCode;
  }
}

export class NotFoundError extends AppError {
  constructor(resource) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
  }
}

export class ValidationError extends AppError {
  constructor(errors) {
    super('Validation failed', 'VALIDATION', 400);
    this.errors = errors;
  }
}
```

### Async Error Handling
```javascript
// WRONG - unhandled rejection
app.get('/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);  // Can throw!
  res.json(user);
});

// CORRECT - with wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await getUser(req.params.id);
  res.json(user);
}));
```

### Never Swallow Errors
```javascript
// WRONG
try {
  await riskyOperation();
} catch {
  // Silent failure
}

// CORRECT
try {
  await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error: error.message });
  throw error;  // Or handle appropriately
}
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | camelCase | `getUserById`, `parseConfig` |
| Classes | PascalCase | `UserService`, `HttpClient` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES`, `API_URL` |
| Files | kebab-case | `user-service.js`, `http-client.js` |
| Private | `#` prefix | `#internalMethod` (class fields) |

## Project Structure

```
src/
├── index.js              # Entry point
├── app.js                # Express app
├── config/               # Configuration
│   └── index.js
├── controllers/          # HTTP handlers
│   └── users.js
├── services/             # Business logic
│   └── user-service.js
├── repositories/         # Data access
│   └── user-repository.js
├── middleware/           # Express middleware
│   ├── auth.js
│   └── error-handler.js
└── utils/                # Helpers
    └── validation.js
tests/
├── setup.js
├── controllers/
└── services/
```

## Async Patterns

### Use async/await (Not Callbacks)
```javascript
// WRONG - callback hell
fs.readFile('config.json', (err, data) => {
  if (err) return handleError(err);
  JSON.parse(data, (err, config) => {
    // ...
  });
});

// CORRECT
const data = await fs.readFile('config.json', 'utf8');
const config = JSON.parse(data);
```

### Parallel Execution
```javascript
// Sequential (slow)
const user = await getUser(id);
const orders = await getOrders(id);

// Parallel (fast)
const [user, orders] = await Promise.all([
  getUser(id),
  getOrders(id),
]);
```

### Handle All Promise Rejections
```javascript
// In entry point
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection', { reason });
  process.exit(1);
});
```

## Testing with Jest/Vitest

```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from '../services/user-service.js';

describe('UserService', () => {
  let service;
  let mockRepo;

  beforeEach(() => {
    mockRepo = {
      findById: vi.fn(),
      save: vi.fn(),
    };
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

    it('throws NotFoundError when missing', async () => {
      mockRepo.findById.mockResolvedValue(null);

      await expect(service.getUser('1'))
        .rejects
        .toThrow(NotFoundError);
    });
  });
});
```

## Environment Configuration

```javascript
// config/index.js
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
});

export const config = envSchema.parse(process.env);
```

## Logging

```javascript
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined,
});

// Usage
logger.info({ userId, action: 'login' }, 'User logged in');
logger.error({ err, requestId }, 'Request failed');
```

## Security

- Never log sensitive data
- Validate all input (use Zod)
- Use `helmet` middleware for HTTP headers
- Rate limit API endpoints
- Use parameterized queries
- Store secrets in environment variables
- Keep dependencies updated (`npm audit`)

## Performance

### Avoid Blocking Event Loop
```javascript
// WRONG - blocks event loop
const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512');

// CORRECT - async
const hash = await new Promise((resolve, reject) => {
  crypto.pbkdf2(password, salt, 100000, 64, 'sha512', (err, key) => {
    if (err) reject(err);
    else resolve(key);
  });
});
```

### Use Streams for Large Data
```javascript
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

await pipeline(
  createReadStream('input.txt'),
  createGzip(),
  createWriteStream('output.txt.gz'),
);
```

## Code Review Checklist

- [ ] ES modules used (not CommonJS)
- [ ] Async errors handled (no unhandled rejections)
- [ ] No callback-style code
- [ ] Environment validated at startup
- [ ] Sensitive data not logged
- [ ] Tests mock external dependencies
- [ ] No blocking operations in async code
- [ ] Proper error classes with codes
