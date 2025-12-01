# Debugging Tools by Language

## Node.js / TypeScript

### Chrome DevTools (Built-in)

```bash
# Run with inspect flag
node --inspect-brk app.js

# Open chrome://inspect in Chrome
# Set breakpoints, step through code
```

### VS Code Debugger

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Server",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "npm: build",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"]
    }
  ]
}
```

### Debug Module

```typescript
import debug from "debug";

const log = debug("app:server");
const error = debug("app:error");

log("Starting server on port %d", 3000);
error("Failed to connect to database");

// Run with: DEBUG=app:* node app.js
```

### CPU Profiling (0x)

```bash
# Install
npm install -g 0x

# Profile application
0x node app.js

# Open flamegraph in browser
```

### Clinic.js

```bash
npm install -g clinic

# CPU profiling
clinic doctor -- node app.js

# Heap profiling
clinic heapprofiler -- node app.js

# Event loop analysis
clinic bubbleprof -- node app.js
```

### Heap Snapshots

```typescript
import { writeHeapSnapshot } from "v8";

app.get("/debug/heap", (req, res) => {
  const filename = writeHeapSnapshot();
  res.send(`Heap snapshot written to ${filename}`);
});

// Analyze in Chrome DevTools
```

## Python

### PDB (Built-in Debugger)

```python
import pdb

def problematic_function(data):
    pdb.set_trace()  # Breakpoint

    # Debugger commands:
    # l - list code
    # n - next line
    # s - step into
    # c - continue
    # p variable - print variable
    # q - quit
    result = process(data)
    return result
```

### IPython Debugger

```python
from IPython import embed

def problematic_function(data):
    embed()  # Drop into IPython shell
    result = process(data)
    return result
```

### VS Code Debugger

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

### CPU Profiling (cProfile)

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code
result = expensive_operation()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(10)  # Top 10 functions
```

### Memory Profiling

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    large_list = [i for i in range(1000000)]
    return sum(large_list)

# Run with: python -m memory_profiler script.py
```

## Go

### Delve (Standard Debugger)

```bash
# Install
go install github.com/go-delve/delve/cmd/dlv@latest

# Debug
dlv debug main.go

# Commands:
# b main.main - set breakpoint
# c - continue
# n - next line
# s - step into
# p variable - print variable
# q - quit
```

### VS Code Debugger

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Package",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}"
    }
  ]
}
```

### pprof (Profiling)

```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    // Enable profiling endpoint
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()

    startServer()
}

// Profile CPU:
// go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

// Profile heap:
// go tool pprof http://localhost:6060/debug/pprof/heap
```

## Rust

### LLDB/GDB (Native Debuggers)

```bash
# Build with debug info
cargo build

# Debug with LLDB
rust-lldb ./target/debug/myapp

# Debug with GDB
rust-gdb ./target/debug/myapp
```

### VS Code Debugger (CodeLLDB)

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug",
      "program": "${workspaceFolder}/target/debug/myapp",
      "args": [],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

## API Debugging

### cURL

```bash
# Verbose output with headers
curl -v https://api.example.com/users

# Include response headers
curl -i https://api.example.com/users

# POST with JSON
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John"}' \
  -v
```

### HTTPie (User-Friendly)

```bash
# Simple GET
http GET https://api.example.com/users

# POST with JSON
http POST https://api.example.com/users name=John email=john@example.com

# Custom headers
http GET https://api.example.com/users Authorization:"Bearer token123"
```
