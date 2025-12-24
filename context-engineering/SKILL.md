---
name: Context Engineering
description: This skill should be used when the user asks about "context engineering", "context management", "prompt engineering", "context budget", "context overflow", "token limits", "AI context", "structured prompts", or needs guidance on optimizing AI agent context for better task completion.
version: 1.0.0
---

# Context Engineering — Maximizing AI Agent Effectiveness

## The Problem

AI agents have finite context windows. Poor context management leads to:
- Hallucinations from missing information
- Task failures from context overflow
- Inefficient token usage
- Lost important details during long sessions

## The Discipline

Context Engineering is the practice of structuring, loading, and managing context to maximize AI agent effectiveness.

```
┌─────────────────────────────────────────────┐
│           CONTEXT HIERARCHY                  │
├─────────────────────────────────────────────┤
│  1. System Instructions (fixed)             │
│  2. Project CLAUDE.md (loaded at start)     │
│  3. Convention Skills (auto-activated)      │
│  4. Serena Memories (on-demand)             │
│  5. Beads Task Context (injected)           │
│  6. Tool Outputs (dynamic)                  │
│  7. Conversation History (accumulated)      │
└─────────────────────────────────────────────┘
```

## Context Budget Management

### Ideal Distribution

| Category | Budget | Purpose |
|----------|--------|---------|
| System + Instructions | ~15% | Fixed overhead |
| Project Context | ~20% | CLAUDE.md, conventions |
| Working Memory | ~35% | Current task state |
| Tool Outputs | ~20% | Search results, file contents |
| Reserve | ~10% | Safety margin |

### Warning Signs

- Responses getting shorter/vaguer
- Forgetting earlier decisions
- Repeating already-done work
- Tool output truncation warnings

## Structured Context Loading

### 1. Session Start (Automatic)

```
SessionStart Hook:
├── Load CLAUDE.md
├── Inject bd prime (beads context)
├── Activate relevant convention skills
└── Load task-specific memories
```

### 2. Task Initialization

```
Before starting work:
1. Read project CLAUDE.md (if not loaded)
2. Check for relevant Serena memories
3. Review TodoWrite state
4. Load specific files only as needed
```

### 3. Progressive Loading

```
DON'T: Read entire codebase upfront
DO:    Load context progressively

Step 1: Get symbols overview
Step 2: Find specific symbols needed
Step 3: Read only relevant bodies
Step 4: Load references as needed
```

## Context Compression Techniques

### Summarize Verbose Outputs

When tool outputs are large:
```
Instead of keeping full file:
"The UserService class (300 lines) has methods:
- authenticate(email, password) → User
- register(data) → User
- resetPassword(email) → void
Key: Uses bcrypt for passwords, JWT for tokens"
```

### Use TodoWrite as State Machine

```
TodoWrite([
  {content: "Research auth patterns", status: "completed"},
  {content: "Implement UserService", status: "in_progress"},
  ...
])
```
→ Maintains state without repeating details

### Checkpoint to Memory

```
Before context gets full:
write_memory("task-progress.md", summary_of_work)
```

### Reference, Don't Repeat

```
Instead of: "As I mentioned, the auth uses JWT..."
Use: "Per auth-patterns memory, JWT is used for..."
```

## Serena Memory Patterns

### When to Write Memories

| Situation | Memory Type |
|-----------|-------------|
| Discovered architecture pattern | `patterns/*.md` |
| Found non-obvious dependency | `dependencies.md` |
| Made design decision | `decisions/*.md` |
| Completed research | `research/*.md` |
| Session checkpoint | `checkpoint-*.md` |

### Memory Structure

```markdown
# [Topic] — [One-line Summary]

## Key Points
- Point 1
- Point 2

## Details
[Only what's needed for future sessions]

## References
- file:line — description
```

## Anti-Patterns

| Anti-Pattern | Impact | Better Approach |
|--------------|--------|-----------------|
| Reading entire files | Wastes tokens | Use `get_symbols_overview` first |
| Keeping all tool output | Overflow | Summarize and discard |
| No memory usage | Context loss | Write discoveries to memory |
| Loading everything upfront | Early overflow | Progressive loading |
| Repeating explanations | Token waste | Reference previous work |

## Optimal Tool Usage

### For Code Exploration

```
1. get_symbols_overview(file) — Understand structure
2. find_symbol(name) — Locate specific symbols
3. find_referencing_symbols() — Understand usage
4. read_file(chunk) — Only when editing
```

### For Search

```
1. search_for_pattern() — Find candidates
2. find_symbol() — Confirm exact locations
3. Read only confirmed matches
```

### For Editing

```
1. find_symbol(include_body=True) — Get current state
2. replace_symbol_body() — Make change
3. Don't re-read to verify (tool is reliable)
```

## Context Recovery

When context seems full:

### Option 1: Checkpoint and Continue
```
/checkpoint
→ Saves state to memory
→ Continue in same session with fresh start point
```

### Option 2: Handoff Protocol
```
1. Sync beads: bd sync
2. Create comprehensive checkpoint
3. Commit pending changes
4. Report recovery instructions
```

### Option 3: Compression
```
1. Summarize completed work
2. Clear unnecessary tool outputs
3. Focus on remaining tasks only
```

## Integration with Tools

### Hooks
- `session-context.sh` — Automatic context injection
- `session-persist.sh` — Context preservation

### Skills (Auto-Activated)
- Convention skills provide language context
- This skill provides meta-context patterns

### Agents
- `session-checkpoint` — Saves context to memory
- `task-tracker` — Maintains task state

## Example: Full Context-Aware Flow

```
User: "Add rate limiting to the API"

1. Initial Context Load:
   - CLAUDE.md ✓ (automatic)
   - Convention skill ✓ (auto-activated for Go)
   - Check memories: list_memories()

2. Research (minimal loading):
   - get_symbols_overview("internal/api/middleware")
   - find_symbol("RateLimiter", substring_matching=True)
   - Only 2 files loaded, not entire codebase

3. Save Discovery:
   - write_memory("rate-limiting-research.md", findings)

4. Implement (focused):
   - TodoWrite for progress tracking
   - Edit only necessary files
   - Summarize changes, don't keep full diffs

5. Checkpoint (if long task):
   - /checkpoint before context gets full
```

## Related Skills

- **reliable-execution** — Full persistence patterns
- **serena-navigation** — Memory and exploration tools
- **beads-workflow** — Task state management
