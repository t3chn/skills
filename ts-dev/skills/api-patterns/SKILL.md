---
name: TypeScript API Patterns
description: This skill should be used when the user asks about "Hono", "tRPC", "Zod", "type-safe API", "TypeScript backend", "API validation", "edge functions", "serverless TypeScript", or needs guidance on building type-safe APIs.
version: 1.0.0
---

# TypeScript API Patterns

Type-safe APIs with Hono, tRPC, and Zod (2025).

## Hono — Edge-First Web Framework

### Setup

```bash
pnpm add hono
pnpm add -D @types/node
```

### Basic App

```typescript
import { Hono } from 'hono';
import { serve } from '@hono/node-server';

const app = new Hono();

app.get('/', (c) => c.text('Hello Hono!'));

app.get('/json', (c) => c.json({ message: 'Hello' }));

serve({ fetch: app.fetch, port: 3000 });
console.log('Server running on http://localhost:3000');
```

### Route Groups

```typescript
import { Hono } from 'hono';

// Create typed route group
const users = new Hono()
  .get('/', async (c) => {
    const users = await db.select().from(usersTable);
    return c.json(users);
  })
  .get('/:id', async (c) => {
    const id = c.req.param('id');
    const user = await db.select().from(usersTable).where(eq(usersTable.id, Number(id)));
    if (!user[0]) return c.notFound();
    return c.json(user[0]);
  })
  .post('/', async (c) => {
    const body = await c.req.json();
    const user = await db.insert(usersTable).values(body).returning();
    return c.json(user[0], 201);
  });

// Mount routes
const app = new Hono()
  .route('/users', users)
  .route('/posts', posts);

export type AppType = typeof app;
```

### Middleware

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { secureHeaders } from 'hono/secure-headers';

const app = new Hono();

// Built-in middleware
app.use('*', logger());
app.use('*', cors());
app.use('*', secureHeaders());

// Custom middleware
app.use('*', async (c, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  c.header('X-Response-Time', `${ms}ms`);
});

// Auth middleware
const authMiddleware = async (c: Context, next: Next) => {
  const token = c.req.header('Authorization')?.replace('Bearer ', '');
  if (!token) return c.json({ error: 'Unauthorized' }, 401);

  try {
    const user = await verifyToken(token);
    c.set('user', user);
    await next();
  } catch {
    return c.json({ error: 'Invalid token' }, 401);
  }
};

// Apply to routes
app.use('/api/*', authMiddleware);
```

### Zod Validation with Hono

```typescript
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

const app = new Hono()
  .post(
    '/users',
    zValidator('json', createUserSchema),
    async (c) => {
      // body is fully typed!
      const body = c.req.valid('json');
      const user = await createUser(body);
      return c.json(user, 201);
    }
  );
```

## tRPC — End-to-End Type Safety

### Setup

```bash
pnpm add @trpc/server @trpc/client zod
```

### Server Setup

```typescript
// server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { z } from 'zod';

const t = initTRPC.context<Context>().create();

export const router = t.router;
export const publicProcedure = t.procedure;

// Protected procedure
export const protectedProcedure = t.procedure.use(async ({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({ ctx: { user: ctx.user } });
});
```

### Router Definition

```typescript
// server/routers/users.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';

export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.number() }))
    .query(async ({ input }) => {
      const user = await db.query.users.findFirst({
        where: eq(users.id, input.id),
      });
      if (!user) throw new TRPCError({ code: 'NOT_FOUND' });
      return user;
    }),

  list: publicProcedure
    .input(z.object({
      limit: z.number().min(1).max(100).default(10),
      cursor: z.number().optional(),
    }))
    .query(async ({ input }) => {
      const items = await db.query.users.findMany({
        limit: input.limit + 1,
        where: input.cursor ? gt(users.id, input.cursor) : undefined,
      });

      let nextCursor: number | undefined;
      if (items.length > input.limit) {
        const nextItem = items.pop();
        nextCursor = nextItem?.id;
      }

      return { items, nextCursor };
    }),

  create: protectedProcedure
    .input(z.object({
      name: z.string().min(1),
      email: z.string().email(),
    }))
    .mutation(async ({ input, ctx }) => {
      const user = await db.insert(users).values({
        ...input,
        createdBy: ctx.user.id,
      }).returning();
      return user[0];
    }),
});
```

### App Router

```typescript
// server/routers/_app.ts
import { router } from '../trpc';
import { userRouter } from './users';
import { postRouter } from './posts';

export const appRouter = router({
  users: userRouter,
  posts: postRouter,
});

export type AppRouter = typeof appRouter;
```

### Client Usage

```typescript
// client/trpc.ts
import { createTRPCClient, httpBatchLink } from '@trpc/client';
import type { AppRouter } from '../server/routers/_app';

export const trpc = createTRPCClient<AppRouter>({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000/trpc',
    }),
  ],
});

// Usage - fully typed!
const user = await trpc.users.getById.query({ id: 1 });
//    ^? User

const newUser = await trpc.users.create.mutate({
  name: 'John',
  email: 'john@example.com',
});
```

## Zod — Schema Validation

### Basic Schemas

```typescript
import { z } from 'zod';

// Primitives
const nameSchema = z.string().min(1).max(100);
const ageSchema = z.number().int().positive();
const emailSchema = z.string().email();

// Objects
const userSchema = z.object({
  id: z.number(),
  name: nameSchema,
  email: emailSchema,
  age: ageSchema.optional(),
  role: z.enum(['admin', 'user']).default('user'),
  createdAt: z.date(),
});

// Infer TypeScript type
type User = z.infer<typeof userSchema>;
```

### Advanced Patterns

```typescript
import { z } from 'zod';

// Transforms
const dateSchema = z.string().transform((str) => new Date(str));

// Refinements
const passwordSchema = z.string()
  .min(8)
  .refine((val) => /[A-Z]/.test(val), 'Must contain uppercase')
  .refine((val) => /[0-9]/.test(val), 'Must contain number');

// Union types
const responseSchema = z.discriminatedUnion('status', [
  z.object({ status: z.literal('success'), data: userSchema }),
  z.object({ status: z.literal('error'), error: z.string() }),
]);

// Recursive types
interface Category {
  name: string;
  children: Category[];
}

const categorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    children: z.array(categorySchema),
  })
);

// Coercion
const querySchema = z.object({
  page: z.coerce.number().default(1),
  limit: z.coerce.number().default(10),
});
```

### Error Handling

```typescript
import { z, ZodError } from 'zod';

const schema = z.object({
  email: z.string().email(),
  age: z.number().min(18),
});

try {
  schema.parse({ email: 'invalid', age: 15 });
} catch (error) {
  if (error instanceof ZodError) {
    const formatted = error.flatten();
    // {
    //   fieldErrors: {
    //     email: ['Invalid email'],
    //     age: ['Number must be greater than or equal to 18']
    //   }
    // }
  }
}

// Safe parse (no throw)
const result = schema.safeParse(data);
if (result.success) {
  console.log(result.data);
} else {
  console.log(result.error.flatten());
}
```

## Error Handling Pattern

### Result Type

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Usage
async function getUser(id: number): Promise<Result<User>> {
  try {
    const user = await db.query.users.findFirst({
      where: eq(users.id, id),
    });

    if (!user) {
      return { success: false, error: new Error('User not found') };
    }

    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}

// Handling
const result = await getUser(1);
if (result.success) {
  console.log(result.data.name);
} else {
  console.error(result.error.message);
}
```

### HTTP Error Responses

```typescript
import { Hono } from 'hono';
import { HTTPException } from 'hono/http-exception';

const app = new Hono();

// Custom error class
class AppError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code?: string
  ) {
    super(message);
  }
}

// Error handler middleware
app.onError((err, c) => {
  if (err instanceof AppError) {
    return c.json({
      error: err.message,
      code: err.code,
    }, err.statusCode);
  }

  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  }

  console.error(err);
  return c.json({ error: 'Internal Server Error' }, 500);
});

// Usage
app.get('/users/:id', async (c) => {
  const user = await findUser(c.req.param('id'));
  if (!user) {
    throw new AppError(404, 'User not found', 'USER_NOT_FOUND');
  }
  return c.json(user);
});
```

## OpenAPI Generation

```typescript
import { Hono } from 'hono';
import { swaggerUI } from '@hono/swagger-ui';
import { OpenAPIHono, createRoute, z } from '@hono/zod-openapi';

const app = new OpenAPIHono();

const getUserRoute = createRoute({
  method: 'get',
  path: '/users/{id}',
  request: {
    params: z.object({
      id: z.string().openapi({ example: '1' }),
    }),
  },
  responses: {
    200: {
      content: {
        'application/json': {
          schema: userSchema,
        },
      },
      description: 'User found',
    },
    404: {
      description: 'User not found',
    },
  },
});

app.openapi(getUserRoute, async (c) => {
  const { id } = c.req.valid('param');
  const user = await getUser(Number(id));
  return c.json(user);
});

// Swagger UI
app.get('/docs', swaggerUI({ url: '/doc' }));
app.doc('/doc', {
  openapi: '3.0.0',
  info: { title: 'My API', version: '1.0.0' },
});
```

## Related Skills

- **type-patterns** — TypeScript type utilities
- **database-patterns** — Drizzle ORM integration
- **testing-patterns** — Testing APIs
