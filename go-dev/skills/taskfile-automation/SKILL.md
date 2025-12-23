---
name: Taskfile Automation
description: This skill should be used when the user asks about "Taskfile", "go-task", "task runner for Go", "alternative to Makefile", "Taskfile.yml", "task automation", "Go build automation", "task --watch", "task variables", "task dependencies", "cross-platform build Go", or needs guidance on setting up modern Go build automation with Taskfile.
version: 1.0.0
---

# Taskfile Automation for Go Projects

## Why Taskfile over Makefile?

- **Cross-platform**: Works on Windows, Linux, macOS without shell differences
- **YAML syntax**: More readable than Makefile syntax
- **Checksum-based**: Detects changes by content, not timestamps
- **Single binary**: No dependencies beyond the `task` binary
- **Better UX**: Colored output, task descriptions, tab completion

## Installation

```bash
# macOS
brew install go-task

# Linux
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin

# Windows (Chocolatey)
choco install go-task

# Go install
go install github.com/go-task/task/v3/cmd/task@latest
```

## Complete Taskfile.yml for Go Projects

```yaml
version: '3'

vars:
  BINARY_NAME: myapp
  MAIN_PACKAGE: ./cmd/myapp
  BUILD_DIR: ./bin
  COVERAGE_DIR: ./coverage

env:
  CGO_ENABLED: 0

tasks:
  default:
    desc: Show available tasks
    cmds:
      - task --list

  # ============ Build Tasks ============

  build:
    desc: Build the application
    vars:
      GIT_COMMIT:
        sh: git rev-parse --short HEAD 2>/dev/null || echo "unknown"
      GIT_BRANCH:
        sh: git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
      BUILD_TIME:
        sh: date -u +"%Y-%m-%dT%H:%M:%SZ"
    cmds:
      - go build -ldflags "-X main.Version={{.GIT_COMMIT}} -X main.Branch={{.GIT_BRANCH}} -X main.BuildTime={{.BUILD_TIME}}" -o {{.BUILD_DIR}}/{{.BINARY_NAME}} {{.MAIN_PACKAGE}}
    sources:
      - "**/*.go"
      - go.mod
      - go.sum
    generates:
      - "{{.BUILD_DIR}}/{{.BINARY_NAME}}"

  build:all:
    desc: Build for all platforms
    cmds:
      - task: build:linux
      - task: build:darwin
      - task: build:windows

  build:linux:
    desc: Build for Linux
    env:
      GOOS: linux
      GOARCH: amd64
    cmds:
      - go build -o {{.BUILD_DIR}}/{{.BINARY_NAME}}-linux-amd64 {{.MAIN_PACKAGE}}

  build:darwin:
    desc: Build for macOS
    env:
      GOOS: darwin
      GOARCH: arm64
    cmds:
      - go build -o {{.BUILD_DIR}}/{{.BINARY_NAME}}-darwin-arm64 {{.MAIN_PACKAGE}}

  build:windows:
    desc: Build for Windows
    env:
      GOOS: windows
      GOARCH: amd64
    cmds:
      - go build -o {{.BUILD_DIR}}/{{.BINARY_NAME}}-windows-amd64.exe {{.MAIN_PACKAGE}}

  # ============ Test Tasks ============

  test:
    desc: Run all tests
    cmds:
      - go test -race -short ./...

  test:verbose:
    desc: Run tests with verbose output
    cmds:
      - go test -race -v ./...

  test:coverage:
    desc: Run tests with coverage report
    cmds:
      - mkdir -p {{.COVERAGE_DIR}}
      - go test -race -coverprofile={{.COVERAGE_DIR}}/coverage.out ./...
      - go tool cover -html={{.COVERAGE_DIR}}/coverage.out -o {{.COVERAGE_DIR}}/coverage.html
      - go tool cover -func={{.COVERAGE_DIR}}/coverage.out

  test:integration:
    desc: Run integration tests
    cmds:
      - go test -race -tags=integration ./...

  bench:
    desc: Run benchmarks
    cmds:
      - go test -bench=. -benchmem -run=^$ ./...

  # ============ Lint & Format ============

  lint:
    desc: Run golangci-lint
    cmds:
      - golangci-lint run ./...

  lint:fix:
    desc: Run golangci-lint with auto-fix
    cmds:
      - golangci-lint run --fix ./...

  fmt:
    desc: Format code with gofmt and goimports
    cmds:
      - gofmt -s -w .
      - goimports -w .

  fmt:check:
    desc: Check code formatting
    cmds:
      - test -z "$(gofmt -l .)"
      - test -z "$(goimports -l .)"

  # ============ Development ============

  dev:
    desc: Run in development mode with hot reload
    cmds:
      - go run {{.MAIN_PACKAGE}} {{.CLI_ARGS}}

  watch:
    desc: Watch for changes and rebuild
    cmds:
      - task --watch build

  generate:
    desc: Run go generate
    cmds:
      - go generate ./...

  mod:tidy:
    desc: Tidy go modules
    cmds:
      - go mod tidy

  mod:update:
    desc: Update all dependencies
    cmds:
      - go get -u ./...
      - go mod tidy

  # ============ Quality Gates ============

  check:
    desc: Run all checks (lint + test)
    deps:
      - lint
      - test

  ci:
    desc: Run CI pipeline
    cmds:
      - task: fmt:check
      - task: lint
      - task: test:coverage
      - task: build

  # ============ Clean & Install ============

  clean:
    desc: Remove build artifacts
    cmds:
      - rm -rf {{.BUILD_DIR}}
      - rm -rf {{.COVERAGE_DIR}}

  install:
    desc: Install to GOPATH/bin
    vars:
      GIT_COMMIT:
        sh: git rev-parse --short HEAD 2>/dev/null || echo "unknown"
    cmds:
      - go install -ldflags "-X main.Version={{.GIT_COMMIT}}" {{.MAIN_PACKAGE}}

  # ============ Docker ============

  docker:build:
    desc: Build Docker image
    vars:
      IMAGE_TAG:
        sh: git rev-parse --short HEAD 2>/dev/null || echo "latest"
    cmds:
      - docker build -t {{.BINARY_NAME}}:{{.IMAGE_TAG}} .

  docker:run:
    desc: Run in Docker
    deps:
      - docker:build
    cmds:
      - docker run --rm {{.BINARY_NAME}}:latest
```

## Key Features Used

### Variables & Dynamic Values

```yaml
vars:
  BINARY_NAME: myapp          # Static variable

tasks:
  build:
    vars:
      GIT_COMMIT:
        sh: git rev-parse --short HEAD  # Dynamic from shell
```

### Source Tracking (Skip if unchanged)

```yaml
tasks:
  build:
    sources:
      - "**/*.go"
      - go.mod
    generates:
      - ./bin/myapp
    cmds:
      - go build -o ./bin/myapp .
```

### Dependencies (Parallel by default)

```yaml
tasks:
  ci:
    deps:
      - lint      # These run in parallel
      - test
    cmds:
      - echo "All checks passed"
```

### Sequential Execution

```yaml
tasks:
  release:
    cmds:
      - task: test      # Run first
      - task: build     # Then build
      - task: publish   # Finally publish
```

### Environment Variables

```yaml
env:
  CGO_ENABLED: 0   # Global

tasks:
  build:linux:
    env:
      GOOS: linux  # Task-specific
      GOARCH: amd64
    cmds:
      - go build -o bin/app-linux .
```

### Platforms

```yaml
tasks:
  open:
    platforms: [darwin]
    cmds:
      - open ./docs/index.html

  open:
    platforms: [linux]
    cmds:
      - xdg-open ./docs/index.html
```

## Running Tasks

```bash
# List all tasks
task --list

# Run specific task
task build

# Run with variables
task dev -- --verbose --config=dev.yaml

# Watch mode
task --watch build

# Run multiple tasks
task lint test

# Dry run
task --dry build
```

## golangci-lint Configuration (.golangci.yml)

```yaml
version: "2"

run:
  timeout: 5m
  tests: false

linters:
  default: standard
  enable:
    - errcheck
    - gosec
    - misspell
    - unconvert
    - unparam
    - goconst
    - gocognit

  settings:
    errcheck:
      exclude-functions:
        - (*database/sql.DB).Close
        - (*database/sql.Rows).Close
        - (*os.File).Close
    gocognit:
      min-complexity: 15

issues:
  exclude-dirs:
    - vendor
  uniq-by-line: true
```

## Migration from Makefile

| Makefile | Taskfile |
|----------|----------|
| `.PHONY: build` | Not needed |
| `$(shell ...)` | `sh: ...` in vars |
| `$@`, `$<` | Named variables |
| Tab indentation | YAML (spaces) |
| `make build` | `task build` |

## Related Skills

- **Project Structure** — Where to put Taskfile.yml
- **Testing Patterns** — Test tasks configuration

## References

- [Taskfile.dev](https://taskfile.dev/) — Official documentation
- [go-task/task](https://github.com/go-task/task) — GitHub repository
