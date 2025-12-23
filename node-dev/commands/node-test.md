---
name: node-test
description: Run Vitest with coverage for the current project
arguments:
  - name: path
    description: Specific test path or pattern (optional)
    required: false
  - name: watch
    description: Enable watch mode (true/false)
    required: false
---

# Run Node.js Tests

Execute Vitest with coverage reporting.

```bash
#!/bin/bash
set -e

# Build vitest command
CMD="pnpm vitest"

# Add watch or run mode
if [ "$watch" = "true" ]; then
    CMD="$CMD --watch"
else
    CMD="$CMD run"
fi

# Add coverage
CMD="$CMD --coverage"

# Add path if specified
if [ -n "$path" ]; then
    CMD="$CMD $path"
fi

echo "Running: $CMD"
eval $CMD
```

## Usage Examples

```
/node-test                           # Run all tests once
/node-test watch=true                # Watch mode
/node-test path=tests/unit           # Run unit tests only
/node-test path=user.service.test.ts # Run specific file
```
