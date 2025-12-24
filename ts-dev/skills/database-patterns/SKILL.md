---
name: TypeScript Database Patterns
description: This skill should be used when the user asks about "Drizzle", "TypeScript ORM", "database types", "SQL TypeScript", "migrations", "database schema", or needs guidance on type-safe database access with Drizzle ORM.
version: 1.0.0
---

# TypeScript Database Patterns

Type-safe database access with Drizzle ORM (2025).

## Why Drizzle (NOT Prisma)

| Aspect | Drizzle | Prisma |
|--------|---------|--------|
| Bundle size | ~100KB | 5MB+ |
| Cold start | Fast | Slow |
| Approach | SQL-first | Schema-first |
| Learning curve | Know SQL | Learn PSL |
| Performance | 2-3x faster | More overhead |

**Use Drizzle for**: Serverless, edge, new projects, SQL-familiar teams.

## Setup

```bash
pnpm add drizzle-orm postgres
pnpm add -D drizzle-kit
```

## Schema Definition

### Basic Tables

```typescript
// src/db/schema.ts
import {
  pgTable,
  serial,
  varchar,
  text,
  timestamp,
  integer,
  boolean,
  pgEnum,
} from 'drizzle-orm/pg-core';

// Enum
export const roleEnum = pgEnum('role', ['admin', 'user', 'guest']);

// Users table
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }).notNull(),
  role: roleEnum('role').default('user').notNull(),
  isActive: boolean('is_active').default(true).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// Posts table
export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: varchar('title', { length: 255 }).notNull(),
  content: text('content'),
  authorId: integer('author_id')
    .references(() => users.id, { onDelete: 'cascade' })
    .notNull(),
  published: boolean('published').default(false).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// Comments table
export const comments = pgTable('comments', {
  id: serial('id').primaryKey(),
  content: text('content').notNull(),
  postId: integer('post_id')
    .references(() => posts.id, { onDelete: 'cascade' })
    .notNull(),
  authorId: integer('author_id')
    .references(() => users.id, { onDelete: 'cascade' })
    .notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});
```

### Relations

```typescript
// src/db/relations.ts
import { relations } from 'drizzle-orm';
import { users, posts, comments } from './schema';

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
  comments: many(comments),
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
  comments: many(comments),
}));

export const commentsRelations = relations(comments, ({ one }) => ({
  post: one(posts, {
    fields: [comments.postId],
    references: [posts.id],
  }),
  author: one(users, {
    fields: [comments.authorId],
    references: [users.id],
  }),
}));
```

## Database Connection

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';
import * as relations from './relations';

const connectionString = process.env.DATABASE_URL!;

const client = postgres(connectionString, {
  max: 10,
  idle_timeout: 20,
  connect_timeout: 10,
});

export const db = drizzle(client, {
  schema: { ...schema, ...relations },
});

export type Database = typeof db;
```

## Type Inference

```typescript
import { InferSelectModel, InferInsertModel } from 'drizzle-orm';
import { users, posts } from './schema';

// Infer types from schema
export type User = InferSelectModel<typeof users>;
export type NewUser = InferInsertModel<typeof users>;

export type Post = InferSelectModel<typeof posts>;
export type NewPost = InferInsertModel<typeof posts>;

// Custom types
export type UserWithPosts = User & {
  posts: Post[];
};
```

## Queries

### Select

```typescript
import { eq, and, or, like, gt, desc, asc, isNull } from 'drizzle-orm';
import { db } from './db';
import { users, posts } from './schema';

// Simple select
const allUsers = await db.select().from(users);

// Select specific columns
const emails = await db
  .select({ id: users.id, email: users.email })
  .from(users);

// Where conditions
const activeUsers = await db
  .select()
  .from(users)
  .where(eq(users.isActive, true));

// Multiple conditions
const filteredUsers = await db
  .select()
  .from(users)
  .where(
    and(
      eq(users.role, 'admin'),
      gt(users.createdAt, new Date('2024-01-01'))
    )
  );

// Pattern matching
const searchResults = await db
  .select()
  .from(users)
  .where(like(users.name, '%john%'));

// Ordering
const sortedUsers = await db
  .select()
  .from(users)
  .orderBy(desc(users.createdAt));

// Pagination
const page = 1;
const pageSize = 10;
const paginatedUsers = await db
  .select()
  .from(users)
  .limit(pageSize)
  .offset((page - 1) * pageSize);
```

### Insert

```typescript
// Single insert
const [newUser] = await db
  .insert(users)
  .values({
    email: 'john@example.com',
    name: 'John Doe',
  })
  .returning();

// Bulk insert
await db.insert(users).values([
  { email: 'user1@example.com', name: 'User 1' },
  { email: 'user2@example.com', name: 'User 2' },
]);

// Upsert (on conflict)
await db
  .insert(users)
  .values({ email: 'john@example.com', name: 'John' })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'John Updated' },
  });
```

### Update

```typescript
// Update by condition
await db
  .update(users)
  .set({ isActive: false })
  .where(eq(users.id, 1));

// Update with returning
const [updated] = await db
  .update(users)
  .set({ name: 'New Name', updatedAt: new Date() })
  .where(eq(users.id, 1))
  .returning();
```

### Delete

```typescript
// Delete by condition
await db.delete(users).where(eq(users.id, 1));

// Delete with returning
const [deleted] = await db
  .delete(users)
  .where(eq(users.id, 1))
  .returning();
```

### Joins

```typescript
// Inner join
const postsWithAuthors = await db
  .select({
    post: posts,
    author: users,
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id));

// Left join
const usersWithPosts = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId));
```

### Relations Query (Recommended)

```typescript
// With relations (cleaner API)
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
});

// Nested relations
const postsWithDetails = await db.query.posts.findMany({
  with: {
    author: true,
    comments: {
      with: {
        author: true,
      },
    },
  },
  where: eq(posts.published, true),
  orderBy: desc(posts.createdAt),
  limit: 10,
});

// Single record
const user = await db.query.users.findFirst({
  where: eq(users.id, 1),
  with: {
    posts: {
      where: eq(posts.published, true),
      limit: 5,
    },
  },
});
```

## Transactions

```typescript
// Basic transaction
await db.transaction(async (tx) => {
  const [user] = await tx
    .insert(users)
    .values({ email: 'john@example.com', name: 'John' })
    .returning();

  await tx.insert(posts).values({
    title: 'First Post',
    authorId: user.id,
  });
});

// With rollback handling
try {
  await db.transaction(async (tx) => {
    await tx.insert(users).values({ /* ... */ });

    // This will rollback the transaction
    if (someCondition) {
      throw new Error('Rollback');
    }

    await tx.insert(posts).values({ /* ... */ });
  });
} catch (error) {
  console.error('Transaction failed:', error);
}
```

## Migrations

### drizzle.config.ts

```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  verbose: true,
  strict: true,
});
```

### Commands

```bash
# Generate migration
pnpm drizzle-kit generate

# Apply migrations
pnpm drizzle-kit migrate

# Push schema (dev only, no migration files)
pnpm drizzle-kit push

# Introspect existing database
pnpm drizzle-kit introspect

# Open Drizzle Studio
pnpm drizzle-kit studio
```

### package.json Scripts

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
```

## Repository Pattern

```typescript
// src/repositories/user.repository.ts
import { eq, like } from 'drizzle-orm';
import { db } from '../db';
import { users, type NewUser, type User } from '../db/schema';

export class UserRepository {
  async findById(id: number): Promise<User | undefined> {
    return db.query.users.findFirst({
      where: eq(users.id, id),
    });
  }

  async findByEmail(email: string): Promise<User | undefined> {
    return db.query.users.findFirst({
      where: eq(users.email, email),
    });
  }

  async findAll(params?: {
    search?: string;
    limit?: number;
    offset?: number;
  }): Promise<User[]> {
    return db.query.users.findMany({
      where: params?.search
        ? like(users.name, `%${params.search}%`)
        : undefined,
      limit: params?.limit ?? 10,
      offset: params?.offset ?? 0,
    });
  }

  async create(data: NewUser): Promise<User> {
    const [user] = await db.insert(users).values(data).returning();
    return user;
  }

  async update(id: number, data: Partial<NewUser>): Promise<User> {
    const [user] = await db
      .update(users)
      .set({ ...data, updatedAt: new Date() })
      .where(eq(users.id, id))
      .returning();
    return user;
  }

  async delete(id: number): Promise<void> {
    await db.delete(users).where(eq(users.id, id));
  }
}

export const userRepository = new UserRepository();
```

## Best Practices

### DO:
- Use relations query API for nested data
- Define types with `InferSelectModel`/`InferInsertModel`
- Use transactions for multi-step operations
- Index frequently queried columns
- Use migrations in production

### DON'T:
- Use `push` in production (use migrations)
- Store connection strings in code
- Ignore query performance
- Skip type inference

## Related Skills

- **type-patterns** — TypeScript type utilities
- **api-patterns** — Integrating with Hono/tRPC
- **testing-patterns** — Testing database queries
