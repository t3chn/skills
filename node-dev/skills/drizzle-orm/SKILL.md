---
name: Drizzle ORM
description: This skill should be used when the user asks about "Drizzle", "Drizzle ORM", "drizzle-kit", "TypeScript ORM", "Node.js database", "SQL schema", or needs guidance on Drizzle ORM patterns and migrations.
version: 1.0.0
---

# Drizzle ORM

Type-safe SQL with Drizzle ORM for Node.js/TypeScript.

## Setup

```bash
pnpm add drizzle-orm postgres
pnpm add -D drizzle-kit
```

## Schema Definition

```typescript
// src/db/schema.ts
import { pgTable, serial, varchar, timestamp, integer, boolean, text } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }).notNull(),
  hashedPassword: varchar('hashed_password', { length: 255 }).notNull(),
  isActive: boolean('is_active').default(true).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: varchar('title', { length: 255 }).notNull(),
  content: text('content'),
  authorId: integer('author_id').references(() => users.id).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
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

const connectionString = process.env.DATABASE_URL!;

const client = postgres(connectionString, {
  max: 10,
  idle_timeout: 20,
  connect_timeout: 10,
});

export const db = drizzle(client, { schema });
```

## Queries

### Select

```typescript
import { eq, and, or, like, gt, desc } from 'drizzle-orm';
import { db } from './db';
import { users, posts } from './schema';

// Simple select
const user = await db.select().from(users).where(eq(users.id, 1));

// Select specific columns
const emails = await db
  .select({ email: users.email, name: users.name })
  .from(users);

// With conditions
const activeUsers = await db
  .select()
  .from(users)
  .where(
    and(
      eq(users.isActive, true),
      gt(users.createdAt, new Date('2024-01-01'))
    )
  );

// With ordering and limit
const recentPosts = await db
  .select()
  .from(posts)
  .orderBy(desc(posts.createdAt))
  .limit(10);

// Pattern matching
const searchResults = await db
  .select()
  .from(users)
  .where(like(users.name, '%john%'));
```

### Insert

```typescript
// Single insert
const [newUser] = await db.insert(users).values({
  email: 'user@example.com',
  name: 'John',
  hashedPassword: hash,
}).returning();

// Bulk insert
await db.insert(users).values([
  { email: 'user1@example.com', name: 'User 1', hashedPassword: hash1 },
  { email: 'user2@example.com', name: 'User 2', hashedPassword: hash2 },
]);

// Insert with conflict handling
await db.insert(users)
  .values({ email: 'user@example.com', name: 'John', hashedPassword: hash })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'Updated John' },
  });
```

### Update

```typescript
// Update by condition
await db.update(users)
  .set({ name: 'Updated Name', updatedAt: new Date() })
  .where(eq(users.id, 1));

// Update with returning
const [updated] = await db.update(users)
  .set({ isActive: false })
  .where(eq(users.id, 1))
  .returning();
```

### Delete

```typescript
// Delete by condition
await db.delete(users).where(eq(users.id, 1));

// Delete with returning
const [deleted] = await db.delete(users)
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

### Relations Query

```typescript
// Using relations (query API)
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
});

const userById = await db.query.users.findFirst({
  where: eq(users.id, 1),
  with: {
    posts: {
      orderBy: desc(posts.createdAt),
      limit: 5,
    },
  },
});
```

## Transactions

```typescript
await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values({
    email: 'user@example.com',
    name: 'John',
    hashedPassword: hash,
  }).returning();

  await tx.insert(posts).values({
    title: 'First Post',
    authorId: user.id,
  });
});
```

## drizzle.config.ts

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

## Migrations

```bash
# Generate migration
pnpm drizzle-kit generate

# Apply migrations
pnpm drizzle-kit migrate

# Push schema (dev only)
pnpm drizzle-kit push

# Open Drizzle Studio
pnpm drizzle-kit studio
```

## Type Inference

```typescript
import { InferSelectModel, InferInsertModel } from 'drizzle-orm';
import { users } from './schema';

// Types inferred from schema
type User = InferSelectModel<typeof users>;
type NewUser = InferInsertModel<typeof users>;
```

## Related Skills

- **nestjs-patterns** - NestJS integration
- **testing-vitest** - Testing database queries
