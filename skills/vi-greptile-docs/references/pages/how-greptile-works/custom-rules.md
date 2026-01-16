# Custom Rules

URL: https://www.greptile.com/docs/how-greptile-works/custom-rules

Custom rules enable Greptile to enforce your organizations specific best practices across all pull requests, ensuring consistency and compliance with your teams established standards.

## Enforcing Organizational Standards

Custom rules ensure your teams best practices are consistently applied across all code reviews, catching deviations that human reviewers might miss.

## Common Custom Rule Examples

Architecture & Design Patterns

* Controllers should not directly import database models - use services instead
* Domain logic must not depend on external frameworks or libraries
* Use the repository pattern for all database access
* All API endpoints must follow RESTful naming conventions
* GraphQL resolvers should delegate business logic to service classes
* Use consistent error response formats across all API endpoints
* React components should use TypeScript interfaces for props
* Vue components must use composition API, not options API
* Angular components should implement OnDestroy for cleanup

Security & Compliance

* All user inputs must be validated before processing
* SQL queries must use parameterized statements to prevent injection
* File uploads require content type and size validation
* Protected API routes must include authentication middleware
* Admin functions require role-based access control checks
* Session tokens must have expiration times set
* Personal data access must be logged for audit purposes
* Sensitive data should be encrypted at rest
* No hardcoded secrets or API keys in source code

Code Quality & Performance

* Async functions must include proper error handling with try-catch blocks
* Database connections must be properly closed after use
* All API requests should be logged with request ID for tracing
* Public methods must have corresponding unit tests
* Functions should have a maximum complexity limit
* Avoid nested callbacks, use async/await instead
* Memory-intensive operations should include cleanup
* Cache frequently accessed data appropriately

JavaScript/TypeScript Best Practices

* Use const/let instead of var for variable declarations
* Prefer async/await over Promise chains for readability
* Use strict equality (===) instead of loose equality (==)
* Always define return types for functions
* Use meaningful variable and function names
* Avoid any type, use specific types instead
* Handle promise rejections explicitly

Python Best Practices

* Follow PEP 8 style guidelines for naming conventions
* Use list comprehensions instead of loops where appropriate
* Include type hints for all function parameters and return values
* Use context managers for resource management
* Prefer f-strings over string concatenation
* Handle exceptions with specific exception types
* Use dataclasses for simple data containers

Go Best Practices

* Follow idiomatic Go patterns and conventions
* Handle errors explicitly, dont ignore them
* Use meaningful variable names, avoid single-letter variables
* Use interfaces for abstraction
* Prefer composition over embedding
* Use context for cancellation and timeouts
* Initialize struct fields explicitly

Java Best Practices

* Use Optional instead of returning null for optional values
* Prefer composition over inheritance for code reuse
* Close resources properly using try-with-resources
* Use StringBuilder for string concatenation in loops
* Make fields private and use getters/setters
* Use final keyword for immutable variables
* Handle checked exceptions appropriately
