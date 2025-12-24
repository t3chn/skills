#!/usr/bin/env python3
"""TDD Enforcement Stop Hook.

Analyzes session transcript to check if code was modified without running tests.
By default, issues a warning (advisory mode). Can be configured to block.
"""

import os
import sys
import json

# Add plugin root to path for imports
PLUGIN_ROOT = os.environ.get('CLAUDE_PLUGIN_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PLUGIN_ROOT not in sys.path:
    sys.path.insert(0, PLUGIN_ROOT)

from core.transcript_analyzer import analyze_transcript, read_transcript


def load_config() -> dict:
    """Load TDD enforcer configuration from .claude/tdd-enforcer.local.md"""
    config = {
        'strictMode': False,
        'testCommand': None,
    }

    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
    config_path = os.path.join(project_dir, '.claude', 'tdd-enforcer.local.md')

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                content = f.read()
                # Simple YAML frontmatter parsing
                if 'strictMode: true' in content:
                    config['strictMode'] = True
        except IOError:
            pass

    return config


def main():
    """Main entry point for Stop hook."""
    try:
        # Read input from stdin (Claude Code hook protocol)
        try:
            input_data = json.load(sys.stdin)
        except json.JSONDecodeError:
            input_data = {}

        # Get transcript path
        transcript_path = os.environ.get('TRANSCRIPT_PATH')
        if not transcript_path:
            # No transcript available, allow stop
            print(json.dumps({}))
            sys.exit(0)

        # Read and analyze transcript
        transcript_content = read_transcript(transcript_path)
        if not transcript_content:
            # Can't read transcript, allow stop
            print(json.dumps({}))
            sys.exit(0)

        # Analyze TDD compliance
        result = analyze_transcript(transcript_content)

        # Load config
        config = load_config()
        strict_mode = config['strictMode']

        # Determine response
        if result.is_compliant:
            # All good, allow stop
            if result.tests_executed:
                output = {
                    "systemMessage": f"TDD Check: {result.message}"
                }
            else:
                output = {}
        else:
            # TDD violation detected
            modified_list = '\n'.join(f"  - {f}" for f in result.modified_files[:5])
            if len(result.modified_files) > 5:
                modified_list += f"\n  ... and {len(result.modified_files) - 5} more"

            warning_msg = f"""**TDD Enforcement Warning**

Code was modified but tests were not executed.

**Modified files:**
{modified_list}

**Recommended action:**
Run your test suite to verify changes before completing this session.

Example commands:
- Go: `go test ./...`
- TypeScript: `npm test` or `pnpm vitest run`
- Python: `pytest`
- Rust: `cargo test`

**TDD Reminder:** Following Red-Green-Refactor:
1. **Red**: Write failing test first
2. **Green**: Minimal implementation to pass
3. **Refactor**: Improve with tests as safety net
"""

            if strict_mode:
                output = {
                    "decision": "block",
                    "reason": "Tests must be run after code modifications (TDD strict mode)",
                    "systemMessage": warning_msg
                }
            else:
                # Warning mode - allow but advise
                output = {
                    "systemMessage": warning_msg
                }

        print(json.dumps(output))

    except Exception as e:
        # On any error, allow the operation with a warning
        error_output = {
            "systemMessage": f"TDD Enforcer error: {str(e)}"
        }
        print(json.dumps(error_output))

    finally:
        # Always exit 0 (hook protocol)
        sys.exit(0)


if __name__ == '__main__':
    main()
