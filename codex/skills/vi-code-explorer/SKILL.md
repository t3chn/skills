---
name: vi-code-explorer
description: "Deeply analyze an existing codebase feature by tracing execution/data flow, mapping architecture layers, and listing the key files and entry points. Use when you need to understand how something works before changing or extending it."
---

# Code Explorer (Deep Codebase Tracing)

Provide a concrete, end-to-end understanding of how a feature works by tracing it from entry points through all layers to outputs/storage.

## Workflow

1. **Define the target**
   - Restate what you are exploring (feature/area) and what questions you must answer (behavior, boundaries, invariants).

2. **Find entry points**
   - Locate where the feature starts (UI routes/components, API endpoints, background jobs, CLI commands, event handlers).

3. **Trace execution and data flow**
   - Follow the call chain from entry to output.
   - Track key data structures, transformations, side effects, and error paths.

4. **Map architecture and boundaries**
   - Identify layers (presentation → domain/business → data).
   - Note key abstractions and interfaces and where cross-cutting concerns live (auth, logging, caching, retries).

5. **Identify dependencies**
   - List internal modules and external services/libraries involved.
   - Note configuration knobs and feature flags.

## Output checklist

Include:

- **Entry points** with file paths (and line numbers when available).
- **Step-by-step execution flow** with important data transformations.
- **Key components** and responsibilities (what owns what).
- **Architecture notes**: patterns, boundaries, conventions, and extension points.
- **Dependencies**: internal/external.
- **Risks / sharp edges**: tricky behavior, performance hotspots, error-handling gaps.
- **Essential reading list**: 5–15 files that are truly required to understand the area.
