---
name: ts-essential-libs
description: Essential TypeScript libraries for production applications. Use these battle-tested packages instead of reinventing the wheel or using wrong primitives.
globs: ["**/*.ts", "**/*.tsx", "**/package.json", "**/tsconfig.json"]
---

# TypeScript Essential Libraries

> **Golden Rule**: Use the right tool for the job. These libraries represent thousands of hours of community effort and real-world battle-testing.

## 💰 Decimal & Money (NEVER use number!)

### dinero.js — Currency-Aware (Recommended)
```typescript
import { dinero, add, multiply, toDecimal } from 'dinero.js';
import { USD, EUR } from '@dinero.js/currencies';

// WRONG: number for money
const price = 19.99;
const total = price * 3;  // 59.97000000000001 — BROKEN!

// CORRECT: dinero.js
const price = dinero({ amount: 1999, currency: USD });
const total = multiply(price, 3);  // $59.97 — exact

// Addition
const subtotal = add(price1, price2);

// Display
const formatted = toDecimal(total);  // "59.97"

// Currency safety (same currency required)
const usd = dinero({ amount: 1000, currency: USD });
const eur = dinero({ amount: 1000, currency: EUR });
// add(usd, eur) — TypeScript error!
```

### decimal.js — Arbitrary Precision
```typescript
import Decimal from 'decimal.js';

// For calculations requiring high precision
const price = new Decimal('19.99');
const total = price.times(3);  // Decimal('59.97')

// Comparison
if (price.greaterThan('10')) { /* ... */ }

// Rounding
const rounded = price.toDecimalPlaces(2);

// Convert to number when needed
const num = total.toNumber();
```

### currency.js — Lightweight (1.14 KB)
```typescript
import currency from 'currency.js';

const price = currency(19.99);
const total = price.multiply(3);  // currency(59.97)

// Formatting
total.format();  // "$59.97"
total.format({ symbol: '€', separator: '.', decimal: ',' });  // "€59,97"

// Addition/subtraction
const result = currency(10).add(5.5).subtract(2);
```

**When to use**:
- `dinero.js`: Multi-currency, type-safe, immutable (recommended)
- `decimal.js`: Arbitrary precision math, scientific calculations
- `currency.js`: Simple money formatting, tiny bundle

---

## ✅ Validation

### Zod — TypeScript-First (Recommended)
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(18).max(120),
  role: z.enum(['admin', 'user']).default('user'),
  metadata: z.record(z.string()).optional(),
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;

// Validation
const result = UserSchema.safeParse(data);
if (result.success) {
  const user: User = result.data;
} else {
  console.error(result.error.issues);
}

// Transform
const CreateUserSchema = UserSchema.omit({ metadata: true });
const UpdateUserSchema = UserSchema.partial();

// Async validation
const AsyncSchema = z.string().refine(
  async (val) => await checkUnique(val),
  { message: 'Must be unique' }
);
```

### Valibot — Smaller Bundle (90% smaller than Zod)
```typescript
import * as v from 'valibot';

const UserSchema = v.object({
  name: v.pipe(v.string(), v.minLength(1), v.maxLength(100)),
  email: v.pipe(v.string(), v.email()),
  age: v.pipe(v.number(), v.integer(), v.minValue(18), v.maxValue(120)),
});

type User = v.InferOutput<typeof UserSchema>;

// Validation
const result = v.safeParse(UserSchema, data);
if (result.success) {
  const user: User = result.output;
}
```

### TypeBox — JSON Schema Compatible
```typescript
import { Type, Static } from '@sinclair/typebox';
import { Value } from '@sinclair/typebox/value';

const UserSchema = Type.Object({
  name: Type.String({ minLength: 1, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
  age: Type.Integer({ minimum: 18, maximum: 120 }),
});

type User = Static<typeof UserSchema>;

// Validation (very fast)
const isValid = Value.Check(UserSchema, data);
const errors = [...Value.Errors(UserSchema, data)];

// JSON Schema output (for OpenAPI)
const jsonSchema = UserSchema;  // Already valid JSON Schema!
```

**When to use**:
- `zod`: Most projects, great DX, huge ecosystem (78+ integrations)
- `valibot`: Bundle size critical (1.37 KB vs 13.5 KB)
- `typebox`: JSON Schema needed, OpenAPI, maximum performance

---

## 🌐 HTTP Client

### ky — Modern Fetch Wrapper (Recommended)
```typescript
import ky from 'ky';

// Simple GET
const user = await ky.get('https://api.example.com/users/1').json<User>();

// POST with JSON
const newUser = await ky.post('https://api.example.com/users', {
  json: { name: 'John', email: 'john@example.com' },
}).json<User>();

// With configuration
const api = ky.create({
  prefixUrl: 'https://api.example.com',
  timeout: 10000,
  retry: 3,
  hooks: {
    beforeRequest: [
      (request) => {
        request.headers.set('Authorization', `Bearer ${token}`);
      },
    ],
  },
});

const users = await api.get('users').json<User[]>();
```

### ofetch — Universal Fetch (Nuxt/UnJS)
```typescript
import { ofetch } from 'ofetch';

// Auto JSON parsing
const user = await ofetch<User>('/api/users/1');

// With options
const data = await ofetch('/api/users', {
  method: 'POST',
  body: { name: 'John' },
  retry: 3,
  retryDelay: 500,
});

// Create instance
const api = ofetch.create({
  baseURL: 'https://api.example.com',
  headers: { Authorization: `Bearer ${token}` },
});
```

### got — Node.js Only (Full-Featured)
```typescript
import got from 'got';

// For Node.js backends only
const user = await got.get('https://api.example.com/users/1').json<User>();

// With retry, timeout, and more
const api = got.extend({
  prefixUrl: 'https://api.example.com',
  timeout: { request: 10000 },
  retry: { limit: 3 },
  hooks: {
    beforeRequest: [
      (options) => {
        options.headers.authorization = `Bearer ${token}`;
      },
    ],
  },
});
```

**When to use**:
- `ky`: Browser + Node, modern Fetch API, small (~3 KB)
- `ofetch`: Nuxt/UnJS ecosystem, universal
- `got`: Node.js only, advanced features, streaming

---

## ⚠️ Error Handling

### neverthrow — Result Type (Recommended)
```typescript
import { ok, err, Result, ResultAsync } from 'neverthrow';

type UserError = 'NOT_FOUND' | 'INVALID_EMAIL' | 'DB_ERROR';

function getUser(id: string): Result<User, UserError> {
  const user = db.find(id);
  if (!user) return err('NOT_FOUND');
  return ok(user);
}

// Usage with pattern matching
const result = getUser('123');

result.match(
  (user) => console.log(`Found: ${user.name}`),
  (error) => console.error(`Error: ${error}`),
);

// Chaining
const userName = getUser('123')
  .map((user) => user.name)
  .mapErr((e) => `Failed: ${e}`)
  .unwrapOr('Unknown');

// Async version
async function fetchUser(id: string): ResultAsync<User, UserError> {
  return ResultAsync.fromPromise(
    fetch(`/api/users/${id}`).then((r) => r.json()),
    () => 'DB_ERROR' as const,
  );
}
```

### ts-results — Rust-Inspired
```typescript
import { Ok, Err, Result } from 'ts-results';

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return Err('Division by zero');
  return Ok(a / b);
}

const result = divide(10, 2);
if (result.ok) {
  console.log(result.val);  // 5
}
```

### Effect — Full Ecosystem (Advanced)
```typescript
import { Effect, pipe } from 'effect';

const getUser = (id: string) =>
  Effect.tryPromise({
    try: () => fetch(`/api/users/${id}`).then((r) => r.json()),
    catch: () => new UserNotFoundError(id),
  });

// Composable, typed errors, dependency injection
const program = pipe(
  getUser('123'),
  Effect.map((user) => user.name),
  Effect.catchTag('UserNotFoundError', () => Effect.succeed('Unknown')),
);

await Effect.runPromise(program);
```

**When to use**:
- `neverthrow`: Simple Result type, gradual adoption
- `ts-results`: Rust-like API, lightweight
- `effect`: Full FP ecosystem, complex apps (steep learning curve)

---

## 🕐 Date & Time

### date-fns — Modular (Recommended)
```typescript
import { format, addDays, differenceInDays, parseISO } from 'date-fns';
import { formatInTimeZone } from 'date-fns-tz';

// Formatting
format(new Date(), 'yyyy-MM-dd HH:mm:ss');  // "2024-12-25 10:30:00"

// Manipulation
const tomorrow = addDays(new Date(), 1);
const daysUntil = differenceInDays(deadline, new Date());

// Parsing
const date = parseISO('2024-12-25T10:30:00Z');

// Timezone
formatInTimeZone(date, 'America/New_York', 'yyyy-MM-dd HH:mm zzz');
```

### Day.js — Lightweight (6 KB)
```typescript
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';

dayjs.extend(utc);
dayjs.extend(timezone);

// Similar to Moment.js API
const now = dayjs();
const formatted = now.format('YYYY-MM-DD');
const tomorrow = now.add(1, 'day');

// Timezone
dayjs().tz('America/New_York').format();
```

### Luxon — Timezone-First
```typescript
import { DateTime } from 'luxon';

// Built-in timezone support (via Intl API)
const now = DateTime.now().setZone('America/New_York');
const formatted = now.toFormat('yyyy-MM-dd HH:mm');

// Parsing with timezone
const dt = DateTime.fromISO('2024-12-25T10:30:00', { zone: 'UTC' });
const local = dt.setZone('local');

// Human-readable diffs
const diff = dt.toRelative();  // "in 3 days"
```

**When to use**:
- `date-fns`: Most projects, tree-shakable, fast
- `dayjs`: Moment.js replacement, tiny bundle
- `luxon`: Complex timezone handling

---

## 🆔 ID Generation

### nanoid — URL-Safe (Recommended)
```typescript
import { nanoid, customAlphabet } from 'nanoid';

// Default (21 chars, URL-safe)
const id = nanoid();  // "V1StGXR8_Z5jdHi6B-myT"

// Custom length
const shortId = nanoid(10);  // "IRFa-VaY2b"

// Custom alphabet
const nanoId = customAlphabet('0123456789abcdef', 12);
const hexId = nanoId();  // "4f90d13a42"
```

### cuid2 — Secure (Recommended for DBs)
```typescript
import { createId, isCuid } from '@paralleldrive/cuid2';

// Cryptographically secure, collision-resistant
const id = createId();  // "ckopqwooh000001me8ysxfl39"

// Validation
if (isCuid(id)) {
  // Valid CUID2
}
```

### ulid — Sortable
```typescript
import { ulid } from 'ulid';

// Time-ordered, sortable
const id = ulid();  // "01ARZ3NDEKTSV4RRFFQ69G5FAV"

// IDs generated close together sort chronologically
const ids = [ulid(), ulid(), ulid()];
ids.sort();  // Already in order!
```

### uuid — Standard
```typescript
import { v4 as uuidv4, v7 as uuidv7 } from 'uuid';

// Random UUID v4
const id = uuidv4();  // "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"

// Time-ordered UUID v7 (better for DBs)
const id7 = uuidv7();  // Sortable like ULID
```

**When to use**:
- `nanoid`: URLs, short IDs, client-side (21 chars)
- `cuid2`: Database PKs, high-security (most secure)
- `ulid`: When sorting by creation time matters
- `uuid`: Enterprise compatibility, v7 for DBs

---

## 📊 Logging

### pino — High Performance (Recommended)
```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',  // Dev only
    options: { colorize: true },
  },
});

// Structured logging
logger.info({ userId: 123, action: 'login' }, 'User logged in');

// Child loggers with context
const requestLogger = logger.child({ requestId: 'abc-123' });
requestLogger.info('Processing request');

// Error logging
logger.error({ err, userId }, 'Failed to process user');
```

### winston — Flexible (Multi-Transport)
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json(),
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

logger.info('User logged in', { userId: 123 });
```

### consola — Universal (Browser + Node)
```typescript
import { consola } from 'consola';

consola.info('Info message');
consola.success('Success!');
consola.error('Error occurred');
consola.box('Boxed message');  // Pretty output

// Scoped logger
const log = consola.withTag('api');
log.info('Request received');
```

**When to use**:
- `pino`: Production APIs, 5x faster than winston
- `winston`: Multiple transports, complex routing
- `consola`: CLI tools, development, universal

---

## 🧪 Testing

### Vitest — Modern Testing (Recommended)
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('UserService', () => {
  let service: UserService;
  let mockRepo: MockedObject<UserRepository>;

  beforeEach(() => {
    mockRepo = {
      find: vi.fn(),
      save: vi.fn(),
    };
    service = new UserService(mockRepo);
  });

  it('should find user by id', async () => {
    mockRepo.find.mockResolvedValue({ id: '1', name: 'John' });

    const user = await service.getUser('1');

    expect(user.name).toBe('John');
    expect(mockRepo.find).toHaveBeenCalledWith('1');
  });

  it.each([
    { age: 17, expected: false },
    { age: 18, expected: true },
    { age: 65, expected: true },
  ])('isAdult($age) should be $expected', ({ age, expected }) => {
    expect(isAdult(age)).toBe(expected);
  });
});
```

### Mocking Patterns
```typescript
import { vi, type MockedFunction } from 'vitest';

// Module mock
vi.mock('./userRepository', () => ({
  UserRepository: vi.fn().mockImplementation(() => ({
    find: vi.fn(),
  })),
}));

// Spy on method
const spy = vi.spyOn(service, 'processUser');
spy.mockResolvedValue({ success: true });

// Partial mock
vi.mock('./utils', async (importOriginal) => ({
  ...(await importOriginal<typeof import('./utils')>()),
  sendEmail: vi.fn(),
}));

// Timer mocks
vi.useFakeTimers();
vi.setSystemTime(new Date('2024-12-25'));
vi.advanceTimersByTime(1000);
```

### MSW — API Mocking
```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'John' });
  }),
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '123', ...body }, { status: 201 });
  }),
];

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---

## 🔐 Security

### jose — JWT/JWE/JWS
```typescript
import * as jose from 'jose';

// Create JWT
const secret = new TextEncoder().encode('your-secret-key');
const token = await new jose.SignJWT({ sub: userId })
  .setProtectedHeader({ alg: 'HS256' })
  .setIssuedAt()
  .setExpirationTime('24h')
  .sign(secret);

// Verify JWT
const { payload } = await jose.jwtVerify(token, secret);
console.log(payload.sub);  // userId
```

### bcrypt — Password Hashing
```typescript
import bcrypt from 'bcrypt';

// Hash
const hash = await bcrypt.hash(password, 10);

// Verify
const isValid = await bcrypt.compare(password, hash);
```

### argon2 — Modern Hashing (Recommended)
```typescript
import argon2 from 'argon2';

// Hash
const hash = await argon2.hash(password);

// Verify
const isValid = await argon2.verify(hash, password);
```

---

## ⚡ State Management

### Zustand — Simple (Recommended)
```typescript
import { create } from 'zustand';

interface UserStore {
  user: User | null;
  setUser: (user: User) => void;
  logout: () => void;
}

const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}));

// Usage
const user = useUserStore((state) => state.user);
const setUser = useUserStore((state) => state.setUser);
```

### Jotai — Atomic
```typescript
import { atom, useAtom } from 'jotai';

const userAtom = atom<User | null>(null);
const isLoggedInAtom = atom((get) => get(userAtom) !== null);

// Usage
const [user, setUser] = useAtom(userAtom);
```

---

## 📋 Quick Reference

| Category | Recommended | Alternative |
|----------|-------------|-------------|
| **Decimal/Money** | `dinero.js` | `decimal.js`, `currency.js` |
| **Validation** | `zod` | `valibot` (size), `typebox` (perf) |
| **HTTP Client** | `ky` | `ofetch`, `got` (Node) |
| **Error Handling** | `neverthrow` | `effect` (advanced) |
| **Date/Time** | `date-fns` | `dayjs` (size), `luxon` (tz) |
| **ID Generation** | `nanoid` / `cuid2` | `ulid` (sortable), `uuid` |
| **Logging** | `pino` | `winston` (transports) |
| **Testing** | `vitest` | MSW (API mocking) |
| **JWT** | `jose` | - |
| **Password** | `argon2` | `bcrypt` |
| **State** | `zustand` | `jotai` (atomic) |

## 📦 package.json Example

```json
{
  "dependencies": {
    "dinero.js": "^2.0.0",
    "zod": "^3.24.0",
    "ky": "^1.7.0",
    "neverthrow": "^8.1.0",
    "date-fns": "^4.1.0",
    "nanoid": "^5.0.0",
    "pino": "^9.5.0",
    "jose": "^5.9.0",
    "argon2": "^0.41.0"
  },
  "devDependencies": {
    "vitest": "^2.1.0",
    "msw": "^2.6.0",
    "pino-pretty": "^13.0.0"
  }
}
```
