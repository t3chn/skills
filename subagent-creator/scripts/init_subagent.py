#!/usr/bin/env python3
"""Initialize a new subagent with proper structure."""

import argparse
import sys
from pathlib import Path

TEMPLATE = '''---
name: {name}
description: TODO: Describe when to use this agent. Be specific about triggers and required inputs.
tools: Read, Glob, Grep
model: sonnet
---

# {title}

TODO: One-line role description.

## Input Required

- **TODO** - What the agent expects to receive

## Process

1. TODO: First step
2. TODO: Second step
3. TODO: Third step

## Output Format

```
TODO: Define exact output format
```

## Rules

- TODO: Add constraints and boundaries
- TODO: Define what NOT to do
'''


def create_subagent(name: str, output_path: Path) -> Path:
    """Create a new subagent file."""
    # Validate name
    if not name.replace("-", "").isalnum():
        print(f"Error: Name must contain only lowercase letters, numbers, and hyphens")
        sys.exit(1)

    if name != name.lower():
        print(f"Error: Name must be lowercase")
        sys.exit(1)

    # Create output directory if needed
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate file
    file_path = output_path / f"{name}.md"

    if file_path.exists():
        print(f"Error: {file_path} already exists")
        sys.exit(1)

    # Format template
    title = name.replace("-", " ").title()
    content = TEMPLATE.format(name=name, title=title)

    file_path.write_text(content)
    print(f"Created: {file_path}")

    return file_path


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new subagent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s code-reviewer
  %(prog)s test-runner --path ./agents
  %(prog)s doc-generator --path ~/.claude/agents
        """
    )
    parser.add_argument("name", help="Subagent name (lowercase, hyphens only)")
    parser.add_argument(
        "--path", "-p",
        type=Path,
        default=Path("./agents"),
        help="Output directory (default: ./agents)"
    )

    args = parser.parse_args()

    create_subagent(args.name, args.path)

    print(f"\nNext steps:")
    print(f"1. Edit the TODO placeholders in {args.path / args.name}.md")
    print(f"2. Test by dispatching via Task tool")


if __name__ == "__main__":
    main()
