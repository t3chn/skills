---
name: backend-nodejs
description: |
  Node.js/TypeScript backend with NestJS, Drizzle/Prisma, modern tooling (Vitest, ESLint 9).
  For general patterns (API design, auth, security) see backend-core.
  Triggers: "nodejs backend", "nestjs", "express", "drizzle", "prisma", "vitest"
---

# Node.js/TypeScript Backend Development

Modern Node.js backend with TypeScript, NestJS, Vitest, ESLint 9.

**For general patterns** (API design, auth, security, architecture): use `backend-core`

## Modern Tooling (2025)

### Testing: Vitest (NOT Jest)

```bash
pnpm add -D vitest @vitest/coverage-v8
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

```typescript
// tests/user.service.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('UserService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should create user', async () => {
    const user = await service.create({ email: 'test@example.com' });
    expect(user.id).toBeDefined();
  });
});
```

### Linting: ESLint 9 Flat Config (NOT .eslintrc)

```javascript
// eslint.config.js
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': 'error',
    },
  },
  {
    ignores: ['dist/', 'node_modules/', 'coverage/'],
  }
);
```

### Package Manager: pnpm

```bash
# Init project
pnpm init
pnpm add typescript @types/node tsx -D

# TypeScript config
pnpm tsc --init
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

## NestJS Patterns

### Project Structure

```
src/
├── main.ts
├── app.module.ts
├── common/
│   ├── decorators/
│   ├── filters/
│   ├── guards/
│   └── interceptors/
├── users/
│   ├── users.module.ts
│   ├── users.controller.ts
│   ├── users.service.ts
│   ├── dto/
│   │   ├── create-user.dto.ts
│   │   └── update-user.dto.ts
│   └── entities/
│       └── user.entity.ts
tests/
├── users.e2e-spec.ts
```

### Module Pattern

```typescript
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

### Controller Pattern

```typescript
import { Controller, Get, Post, Body, Param, HttpCode, HttpStatus } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  async create(@Body() createUserDto: CreateUserDto): Promise<UserResponse> {
    return this.usersService.create(createUserDto);
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<UserResponse> {
    return this.usersService.findOne(+id);
  }
}
```

### DTO Validation

```typescript
import { IsEmail, IsString, MinLength, IsOptional } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(1)
  name: string;

  @IsString()
  @MinLength(8)
  password: string;
}
```

### Exception Filters

```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    const message = exception instanceof HttpException
      ? exception.getResponse()
      : 'Internal server error';

    response.status(status).json({
      statusCode: status,
      message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

## Drizzle ORM (Recommended)

### Setup

```bash
pnpm add drizzle-orm postgres
pnpm add -D drizzle-kit
```

### Schema Definition

```typescript
// src/db/schema.ts
import { pgTable, serial, varchar, timestamp, integer } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }).notNull(),
  hashedPassword: varchar('hashed_password', { length: 255 }).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: varchar('title', { length: 255 }).notNull(),
  authorId: integer('author_id').references(() => users.id),
});
```

### Queries

```typescript
import { eq } from 'drizzle-orm';
import { db } from './db';
import { users } from './schema';

// Select
const user = await db.select().from(users).where(eq(users.id, 1));

// Insert
const [newUser] = await db.insert(users).values({
  email: 'user@example.com',
  name: 'John',
  hashedPassword: hash,
}).returning();

// Update
await db.update(users)
  .set({ name: 'Updated' })
  .where(eq(users.id, 1));
```

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
});
```

## Prisma Alternative

### Setup

```bash
pnpm add @prisma/client
pnpm add -D prisma
npx prisma init
```

### Schema

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId Int
}
```

### Queries

```typescript
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

// Find
const user = await prisma.user.findUnique({ where: { id: 1 } });

// Create
const user = await prisma.user.create({
  data: { email: 'test@example.com', name: 'Test' },
});

// With relations
const userWithPosts = await prisma.user.findUnique({
  where: { id: 1 },
  include: { posts: true },
});
```

## Security

### Password Hashing (Argon2)

```typescript
import { hash, verify } from 'argon2';

async function hashPassword(password: string): Promise<string> {
  return hash(password);
}

async function verifyPassword(hash: string, password: string): Promise<boolean> {
  return verify(hash, password);
}
```

### JWT with jose

```typescript
import { SignJWT, jwtVerify } from 'jose';

const secret = new TextEncoder().encode(process.env.JWT_SECRET);

async function signToken(payload: Record<string, unknown>): Promise<string> {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('15m')
    .sign(secret);
}

async function verifyToken(token: string): Promise<Record<string, unknown>> {
  const { payload } = await jwtVerify(token, secret);
  return payload;
}
```

## Testing

### E2E Testing with Vitest

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
});
```

### Mocking with vi

```typescript
import { vi } from 'vitest';

const mockUserRepository = {
  findOne: vi.fn(),
  save: vi.fn(),
};

vi.mock('./user.repository', () => ({
  UserRepository: vi.fn(() => mockUserRepository),
}));
```

## Anti-patterns

- `Jest` -> `Vitest`
- `.eslintrc.*` -> `eslint.config.js` (flat config)
- `npm` -> `pnpm`
- `bcrypt` -> `argon2`
- `jsonwebtoken` -> `jose`
- Sync database calls -> async with connection pooling
- `require()` -> `import`
- `any` type -> proper typing with generics
