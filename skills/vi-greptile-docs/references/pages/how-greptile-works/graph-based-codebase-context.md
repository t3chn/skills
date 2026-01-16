# Graph-based Codebase Context

URL: https://www.greptile.com/docs/how-greptile-works/graph-based-codebase-context

Greptile builds a complete graph of your codebase to understand how code changes affect other parts of your system, enabling context-aware code reviews that catch issues traditional tools miss.

## Why Codebase Context Matters

Most code review tools analyze files in isolation, missing critical relationships:
**Without Context:**

```
// Reviewing this function alone
function updateUserEmail(userId: string, email: string) {
return db.users.update(userId, { email });
}
// Misses: validation patterns, error handling, related functions
```

**With Context:**

```
// Greptile sees the bigger picture
function updateUserEmail(userId: string, email: string) {
return db.users.update(userId, { email });
// Notices: other update functions validate input
// Notices: similar functions handle errors
// Notices: email updates trigger notifications elsewhere
}
```

## Codebase Indexing

When you sign up, Greptile builds a complete graph of your repository containing every code element:

**Legend:** Files Functions External calls/variables

### Indexing Process

Repository Scanning

Parses every file to extract directories, files, functions, classes, variables

Relationship Mapping

Connects all elements: function calls, imports, dependencies, variable usage

Graph Storage

Stores the complete graph for instant querying during code reviews

## How Greptile Analyzes Functions

### 2. Function Usage

```
// Greptile finds everywhere foo() is called
function foo(x: string) {
return processData(x);
}

// Usage sites discovered:
// components/UserForm.tsx:45
// services/DataService.ts:12
// tests/integration.test.ts:78
// Impact analysis: changes will affect 3 files
```

### 3. Pattern Consistency

```
// When reviewing this SQL function:
function getUserById(id: string) {
return db.query('SELECT * FROM users WHERE id = $1', [id]);
}

// Greptile checks other SQL functions:
// getUserByEmail() - uses parameterized queries
// getOrderById() - uses string concatenation
// Suggests: "Use parameterized queries like other DB functions"
```

### Real-time Graph Queries

Every time a file is reviewed, Greptile queries the pre-built graph:

```
// When reviewing this change:
function updateUserProfile(userId: string, data: UserData) {
// New code being reviewed
}

// Greptile instantly knows:
// Import dependencies: UserData interface, validation utils
// Function calls: database.update(), validateUserData()
// Callers: ProfileController.update(), AdminPanel.updateUser()
// Similar patterns: updateUserEmail(), updateUserSettings()
```

## Complete Context

Reviews consider the entire codebase, not just changed files

## Pattern Recognition

Finds inconsistencies and suggests improvements based on existing code

## Impact Analysis

Identifies all code that could be affected by changes

The graph-based approach transforms code review from isolated file analysis into comprehensive system understanding, catching issues that would otherwise slip through traditional reviews.
