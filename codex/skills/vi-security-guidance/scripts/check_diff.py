#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    scope: str
    file_path: str
    rule_name: str
    line_preview: str | None


def _run_git_diff(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return ""
    except subprocess.CalledProcessError:
        return ""
    return completed.stdout


def _iter_added_lines_with_file(diff_text: str) -> Iterable[tuple[str | None, str]]:
    current_file: str | None = None
    for raw_line in diff_text.splitlines():
        match = re.match(r"^diff --git a/(.+?) b/(.+)$", raw_line)
        if match:
            current_file = match.group(2)
            continue

        if raw_line.startswith("+++ ") or raw_line.startswith("--- "):
            continue

        if raw_line.startswith("+"):
            yield current_file, raw_line[1:]


def _touched_files(diff_text: str) -> set[str]:
    files: set[str] = set()
    for raw_line in diff_text.splitlines():
        match = re.match(r"^diff --git a/(.+?) b/(.+)$", raw_line)
        if match:
            files.add(match.group(2))
    return files


def _is_workflow_file(path: str) -> bool:
    normalized = path.lstrip("/")
    return normalized.startswith(".github/workflows/") and normalized.endswith((".yml", ".yaml"))


def _matches_ext(path: str | None, exts: tuple[str, ...]) -> bool:
    if not path:
        return False
    return Path(path).suffix.lower() in exts


def _scan_diff(scope: str, diff_text: str) -> list[Finding]:
    findings: list[Finding] = []

    for file_path in sorted(_touched_files(diff_text)):
        if _is_workflow_file(file_path):
            findings.append(
                Finding(
                    scope=scope,
                    file_path=file_path,
                    rule_name="github_actions_workflow",
                    line_preview=None,
                )
            )

    for file_path, added_line in _iter_added_lines_with_file(diff_text):
        if not added_line.strip():
            continue

        if _matches_ext(file_path, (".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx")):
            if "child_process.exec" in added_line or "execSync(" in added_line or "exec(" in added_line:
                findings.append(Finding(scope, file_path or "<unknown>", "child_process_exec", added_line.strip()))
            if "new Function" in added_line:
                findings.append(Finding(scope, file_path or "<unknown>", "new_function_injection", added_line.strip()))
            if "eval(" in added_line:
                findings.append(Finding(scope, file_path or "<unknown>", "eval_injection", added_line.strip()))
            if "dangerouslySetInnerHTML" in added_line:
                findings.append(
                    Finding(scope, file_path or "<unknown>", "react_dangerously_set_html", added_line.strip())
                )
            if "document.write" in added_line:
                findings.append(Finding(scope, file_path or "<unknown>", "document_write_xss", added_line.strip()))
            if ".innerHTML" in added_line:
                findings.append(Finding(scope, file_path or "<unknown>", "innerHTML_xss", added_line.strip()))

        if _matches_ext(file_path, (".html", ".htm")):
            if ".innerHTML" in added_line:
                findings.append(Finding(scope, file_path or "<unknown>", "innerHTML_xss", added_line.strip()))

        if _matches_ext(file_path, (".py",)):
            if "pickle" in added_line:
                findings.append(Finding(scope, file_path or "<unknown>", "pickle_deserialization", added_line.strip()))
            if "os.system" in added_line or "from os import system" in added_line:
                findings.append(Finding(scope, file_path or "<unknown>", "os_system_injection", added_line.strip()))

    # Dedupe noisy repeats
    deduped: dict[tuple[str, str, str, str | None], Finding] = {}
    for finding in findings:
        key = (finding.scope, finding.file_path, finding.rule_name, finding.line_preview)
        deduped[key] = finding
    return list(deduped.values())


def _print_findings(findings: list[Finding]) -> None:
    findings.sort(key=lambda f: (f.scope, f.file_path, f.rule_name, f.line_preview or ""))

    print("Potential security footguns found:\n")
    for finding in findings:
        print(f"- [{finding.scope}] {finding.file_path}: {finding.rule_name}")
        if finding.line_preview:
            print(f"  + {finding.line_preview}")

    print(
        "\nReminders:\n"
        "- GitHub Actions: treat event fields as untrusted; avoid interpolating into `run:`; prefer `env:` + quoting.\n"
        "- Node: prefer `execFile`/`spawn` with args; avoid `exec`/`execSync` with dynamic strings.\n"
        "- XSS sinks: avoid `.innerHTML`/`document.write`/`dangerouslySetInnerHTML` unless content is trusted/sanitized.\n"
        "- Avoid `eval`/`new Function` and unsafe deserialization (`pickle`) on untrusted data.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan git diffs for common security footguns.")
    parser.add_argument("--staged", action="store_true", help="Scan staged diff (git diff --staged).")
    parser.add_argument("--all", action="store_true", help="Scan both staged and working tree diffs.")
    parsed = parser.parse_args()

    if parsed.all:
        scopes = [("working-tree", ["diff", "--no-color"]), ("staged", ["diff", "--no-color", "--staged"])]
    else:
        scopes = [("staged", ["diff", "--no-color", "--staged"])] if parsed.staged else [("working-tree", ["diff", "--no-color"])]

    all_findings: list[Finding] = []
    for scope_name, cmd_args in scopes:
        diff_text = _run_git_diff(cmd_args)
        if not diff_text.strip():
            continue
        all_findings.extend(_scan_diff(scope_name, diff_text))

    if not all_findings:
        print("No security footguns detected in the selected diff(s).")
        return 0

    _print_findings(all_findings)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
