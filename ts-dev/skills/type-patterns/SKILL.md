---
name: TypeScript Type Patterns
description: This skill should be used when the user asks about "TypeScript types", "generics", "utility types", "type guards", "strict mode", "type inference", "conditional types", "template literals", or needs guidance on advanced TypeScript type patterns.
version: 1.0.0
---

# TypeScript Type Patterns

Advanced TypeScript type patterns for type-safe applications (2025).

## Strict Mode Essentials

### Enable Everything

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### Handle `unknown` in Catch

```typescript
// With useUnknownInCatchVariables: true
try {
  riskyOperation();
} catch (error) {
  // error is unknown, not any
  if (error instanceof Error) {
    console.error(error.message);
  } else {
    console.error('Unknown error:', error);
  }
}
```

### Safe Array Access

```typescript
// With noUncheckedIndexedAccess: true
const arr = [1, 2, 3];
const first = arr[0]; // number | undefined

// Must check before use
if (first !== undefined) {
  console.log(first.toFixed(2));
}

// Or use assertion after validation
const validated = arr[0]!; // Only if you've validated
```

## Utility Types

### Built-in Types

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

// Partial - all properties optional
type PartialUser = Partial<User>;
// { id?: number; name?: string; ... }

// Required - all properties required
type RequiredUser = Required<PartialUser>;

// Pick - select properties
type UserCredentials = Pick<User, 'email' | 'name'>;
// { email: string; name: string }

// Omit - exclude properties
type PublicUser = Omit<User, 'email'>;
// { id: number; name: string; role: ... }

// Record - object type
type UserRoles = Record<string, User>;
// { [key: string]: User }

// Readonly - immutable
type ImmutableUser = Readonly<User>;

// Extract / Exclude for unions
type AdminRole = Extract<User['role'], 'admin'>; // 'admin'
type NonAdminRole = Exclude<User['role'], 'admin'>; // 'user'
```

### Custom Utility Types

```typescript
// Make specific properties optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

type CreateUserInput = PartialBy<User, 'id'>; // id is optional

// Make specific properties required
type RequiredBy<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Deep partial
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Nullable
type Nullable<T> = T | null;

// NonNullableFields
type NonNullableFields<T> = {
  [P in keyof T]: NonNullable<T[P]>;
};
```

## Generics

### Basic Constraints

```typescript
// Extend constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

// Default type
function createArray<T = string>(length: number, value: T): T[] {
  return Array(length).fill(value);
}
```

### Generic Interfaces

```typescript
// Repository pattern
interface Repository<T, ID = number> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, 'id'>): Promise<T>;
  update(id: ID, data: Partial<T>): Promise<T>;
  delete(id: ID): Promise<void>;
}

// Implementation
class UserRepository implements Repository<User> {
  async findById(id: number): Promise<User | null> {
    // ...
  }
  // ...
}
```

### Conditional Types

```typescript
// Basic conditional
type IsString<T> = T extends string ? true : false;

// Infer keyword
type ReturnTypeOf<T> = T extends (...args: any[]) => infer R ? R : never;

type ArrayElement<T> = T extends (infer E)[] ? E : never;

// Distributive conditional types
type ToArray<T> = T extends any ? T[] : never;
type Result = ToArray<string | number>; // string[] | number[]

// Extract promise value
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;
```

## Type Guards

### Type Predicates (`is`)

```typescript
interface Dog {
  bark(): void;
}

interface Cat {
  meow(): void;
}

type Animal = Dog | Cat;

// Type predicate
function isDog(animal: Animal): animal is Dog {
  return 'bark' in animal;
}

// Usage
function makeSound(animal: Animal) {
  if (isDog(animal)) {
    animal.bark(); // TypeScript knows it's Dog
  } else {
    animal.meow(); // TypeScript knows it's Cat
  }
}
```

### Assertion Functions (`asserts`)

```typescript
function assertIsDefined<T>(value: T): asserts value is NonNullable<T> {
  if (value === null || value === undefined) {
    throw new Error('Value is not defined');
  }
}

function processUser(user: User | null) {
  assertIsDefined(user);
  // TypeScript now knows user is User, not null
  console.log(user.name);
}
```

### Discriminated Unions

```typescript
// Tag each variant
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>) {
  if (result.success) {
    // TypeScript knows result.data exists
    console.log(result.data);
  } else {
    // TypeScript knows result.error exists
    console.error(result.error);
  }
}

// API response pattern
type ApiResponse<T> =
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };
```

## Template Literal Types

### Basic Patterns

```typescript
// String manipulation
type Uppercase<S extends string> = intrinsic;
type EventName = `on${Capitalize<string>}`;

// Dynamic keys
type CSSProperty = 'margin' | 'padding';
type CSSDirection = 'top' | 'right' | 'bottom' | 'left';
type CSSRule = `${CSSProperty}-${CSSDirection}`;
// 'margin-top' | 'margin-right' | ... | 'padding-left'
```

### Route Types

```typescript
type Route = '/users' | '/users/:id' | '/posts' | '/posts/:id';

// Extract params
type ExtractParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<Rest>
    : T extends `${infer _Start}:${infer Param}`
    ? Param
    : never;

type UserRouteParams = ExtractParams<'/users/:id'>; // 'id'
```

### Event Emitter Types

```typescript
type EventMap = {
  click: { x: number; y: number };
  focus: { target: HTMLElement };
  submit: { data: FormData };
};

type EventHandler<T extends keyof EventMap> = (event: EventMap[T]) => void;

class TypedEmitter {
  on<T extends keyof EventMap>(event: T, handler: EventHandler<T>): void {
    // ...
  }

  emit<T extends keyof EventMap>(event: T, data: EventMap[T]): void {
    // ...
  }
}
```

## Branded Types

### Prevent Type Confusion

```typescript
// Brand symbol
declare const __brand: unique symbol;

type Brand<T, B> = T & { [__brand]: B };

// Branded IDs
type UserId = Brand<number, 'UserId'>;
type PostId = Brand<number, 'PostId'>;

// Constructor functions
const UserId = (id: number): UserId => id as UserId;
const PostId = (id: number): PostId => id as PostId;

// Usage - can't mix up IDs
function getUser(id: UserId): User { /* ... */ }
function getPost(id: PostId): Post { /* ... */ }

const userId = UserId(1);
const postId = PostId(1);

getUser(userId); // OK
getUser(postId); // Error: PostId not assignable to UserId
```

## Inference Patterns

### Infer from Functions

```typescript
// Get return type
type MyReturnType<T extends (...args: any) => any> =
  T extends (...args: any) => infer R ? R : never;

// Get parameter types
type MyParameters<T extends (...args: any) => any> =
  T extends (...args: infer P) => any ? P : never;

// Usage
function createUser(name: string, age: number): User {
  return { id: 1, name, age };
}

type CreateUserReturn = MyReturnType<typeof createUser>; // User
type CreateUserParams = MyParameters<typeof createUser>; // [string, number]
```

### Const Assertions

```typescript
// Without as const
const routes1 = ['/', '/users', '/posts']; // string[]

// With as const - preserves literal types
const routes2 = ['/', '/users', '/posts'] as const;
// readonly ['/', '/users', '/posts']

type Route = (typeof routes2)[number]; // '/' | '/users' | '/posts'

// Object literal
const config = {
  env: 'production',
  port: 3000,
} as const;
// { readonly env: 'production'; readonly port: 3000 }
```

## Anti-patterns

| Wrong | Right |
|-------|-------|
| `any` | `unknown` with type guards |
| `as Type` everywhere | Proper type inference |
| `!` non-null assertion | Null checks or `??` |
| `// @ts-ignore` | Fix the type error |
| Loose function types | Strict generic constraints |

## Related Skills

- **modern-tooling** — TypeScript configuration
- **api-patterns** — Type-safe API design with Zod
- **testing-patterns** — Type testing patterns
