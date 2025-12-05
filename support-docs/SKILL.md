---
name: support-docs
description: |
  Generate SUPPORT.md for AI support bot from project sources (README, CLAUDE.md, code).
  Creates standardized support documentation with auto-generated FAQ.
  Use when: setting up support bot for a project, need consistent support docs format, want AI-generated FAQ from codebase.
  Triggers: "support docs", "generate support", "SUPPORT.md", "support bot documentation"
---

# Support Docs Generator

Generate standardized SUPPORT.md files for AI support bots from project sources.

## Quick Start

```bash
/support:generate [project-path]
```

If no path provided, uses current directory.

## Procedure: generate

### Step 1: Analyze Project

Read project sources in order:
1. `README.md` — product description, features, usage
2. `CLAUDE.md` — technical details, architecture (if exists)
3. `package.json` / `Cargo.toml` / `pyproject.toml` — dependencies, scripts
4. Key source files (main entry points)

### Step 2: Extract Information

From sources, identify:
- **Product name** and one-line description
- **Quick start** steps (installation, first run)
- **Key features** with brief descriptions
- **Common issues** and solutions
- **Contact/support** channels

### Step 3: Generate FAQ

Analyze the product and generate 5-10 typical user questions:

**Question types to include:**
- Getting started ("How do I install/configure X?")
- Core features ("How do I do X?")
- Troubleshooting ("Why is X not working?")
- Limitations ("Can I do X?" where X is not supported)
- Integration ("Does X work with Y?")

**FAQ quality guidelines:**
- Questions should be natural, as users would ask them
- Answers should be concise but complete
- Reference specific features/commands from docs
- Acknowledge limitations honestly

### Step 4: Write SUPPORT.md

Create file with this structure:

```markdown
# [Product Name] Support Guide

> [One-line description]

## Quick Start

1. [Step 1]
2. [Step 2]
3. [Step 3]

## FAQ

### Q: [Question 1]
[Answer]

### Q: [Question 2]
[Answer]

[... 5-10 questions ...]

## Features

- **[Feature 1]**: [Brief description]
- **[Feature 2]**: [Brief description]

## Troubleshooting

### [Problem 1]
**Symptoms:** [What user sees]
**Solution:** [How to fix]

### [Problem 2]
**Symptoms:** [What user sees]
**Solution:** [How to fix]

## Getting Help

If this guide doesn't answer your question:
- [Support channel 1]
- [Support channel 2]

---
*Auto-generated support documentation. Last updated: [date]*
```

### Step 5: Validate

After writing, verify:
- [ ] All sections filled with real content
- [ ] No placeholder text remaining
- [ ] FAQ answers match actual product capabilities
- [ ] Quick start steps are accurate
- [ ] Contact channels are correct

## Output

- Creates/updates `SUPPORT.md` in project root
- Reports summary of generated content
- Lists any warnings (missing info, potential issues)

## Example

**Input:** Project with README.md describing a CLI todo app

**Output SUPPORT.md:**
```markdown
# AI TodoList Support Guide

> AI-powered todo list with natural language task management

## Quick Start

1. Install: `npm install -g ai-todolist`
2. Configure: `ai-todo config --api-key YOUR_KEY`
3. Add task: `ai-todo add "Buy groceries tomorrow"`

## FAQ

### Q: How do I add a task with a due date?
Use natural language: `ai-todo add "Submit report by Friday 5pm"`

### Q: Can I use it offline?
No, AI TodoList requires internet connection for AI features.

...
```

## Notes

- Keep SUPPORT.md under 5K tokens for efficient bot context
- Regenerate when README or features change significantly
- FAQ should evolve based on actual user questions
