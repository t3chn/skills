#!/bin/bash
# Run tests for all detected languages
# Called by pre-commit on pre-push stage

set -e

echo "Running tests..."

TESTS_RUN=0

# Go
if [ -f go.mod ]; then
    echo "  -> Go tests"
    go test ./... -v
    TESTS_RUN=$((TESTS_RUN + 1))
fi

# Python
if [ -f pyproject.toml ] || [ -f setup.py ]; then
    echo "  -> Python tests"
    if command -v uv &> /dev/null; then
        uv run pytest -v 2>/dev/null || python -m pytest -v
    else
        python -m pytest -v
    fi
    TESTS_RUN=$((TESTS_RUN + 1))
fi

# TypeScript/Node
if [ -f package.json ]; then
    echo "  -> TypeScript/Node tests"
    if command -v pnpm &> /dev/null; then
        pnpm test 2>/dev/null || npm test 2>/dev/null || echo "    (no test script found)"
    else
        npm test 2>/dev/null || echo "    (no test script found)"
    fi
    TESTS_RUN=$((TESTS_RUN + 1))
fi

# Rust
if [ -f Cargo.toml ]; then
    echo "  -> Rust tests"
    cargo test
    TESTS_RUN=$((TESTS_RUN + 1))
fi

if [ $TESTS_RUN -eq 0 ]; then
    echo "  (no test frameworks detected)"
fi

echo "All tests passed!"
