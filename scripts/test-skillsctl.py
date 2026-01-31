#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
import json
from pathlib import Path


def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def git(args: list[str], *, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git"] + args, cwd=cwd, check=check)


def git_commit_all(repo: Path, message: str) -> None:
    git(["add", "-A"], cwd=repo)
    git(
        [
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-m",
            message,
        ],
        cwd=repo,
    )


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Expected path to exist: {path}")


def assert_not_exists(path: Path) -> None:
    if path.exists():
        raise AssertionError(f"Expected path to not exist: {path}")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    skillsctl = repo_root / "skills" / "vi-project-bootstrap" / "scripts" / "skillsctl.py"
    assert_exists(skillsctl)

    with tempfile.TemporaryDirectory(prefix="skillsctl-test-") as td:
        tmp = Path(td)

        # Create a snapshot skills repo from the current working tree (including uncommitted changes).
        skills_src = tmp / "skills-src"
        shutil.copytree(
            repo_root,
            skills_src,
            ignore=shutil.ignore_patterns(".git", ".beads", "dist", "__pycache__", ".DS_Store"),
        )
        git(["init", "-b", "main"], cwd=skills_src)
        git_commit_all(skills_src, "snapshot")

        # Create a project repo.
        project = tmp / "project"
        project.mkdir(parents=True, exist_ok=True)
        git(["init", "-b", "main"], cwd=project)
        (project / "README.md").write_text("test\n", encoding="utf-8")
        git_commit_all(project, "init")

        report = json.loads(run(["python3", str(skillsctl), "doctor"], cwd=project, check=True).stdout)
        if report.get("git_repo") is not True:
            raise AssertionError(f"expected git_repo=true in doctor report, got: {report.get('git_repo')!r}")

        # Bootstrap.
        run(
            [
                "python3",
                str(skillsctl),
                "bootstrap",
                "--repo-url",
                str(skills_src),
                "--branch",
                "main",
                "--stage",
                "--yes",
            ],
            cwd=project,
            check=True,
        )
        staged = git(["diff", "--cached", "--name-only"], cwd=project).stdout.splitlines()
        expected = {".gitmodules", ".codex/skills", ".codex/skills.config.json", ".codex/skills.manifest"}
        if not expected.issubset(set(staged)):
            raise AssertionError(f"bootstrap staged unexpected set.\nexpected superset: {expected}\nactual: {set(staged)}")
        git_commit_all(project, "bootstrap")

        # Install.
        run(
            ["python3", str(skillsctl), "install", "vi-security-guidance", "--stage", "--yes"],
            cwd=project,
            check=True,
        )
        assert_exists(project / ".codex" / "skills" / "skills" / "vi-security-guidance" / "SKILL.md")
        git_commit_all(project, "install security-guidance")

        # Remove.
        run(["python3", str(skillsctl), "remove", "vi-security-guidance", "--stage", "--yes"], cwd=project, check=True)
        assert_not_exists(project / ".codex" / "skills" / "skills" / "vi-security-guidance" / "SKILL.md")
        git_commit_all(project, "remove security-guidance")

        # Idempotent bootstrap/sync.
        run(["python3", str(skillsctl), "bootstrap", "--yes"], cwd=project, check=True)
        run(["python3", str(skillsctl), "sync", "--yes"], cwd=project, check=True)

        # Recover after removing submodule working dir.
        shutil.rmtree(project / ".codex" / "skills")
        run(["python3", str(skillsctl), "sync", "--yes"], cwd=project, check=True)
        assert_exists(project / ".codex" / "skills" / "catalog" / "skills.json")

    print("[OK] skillsctl integration tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
