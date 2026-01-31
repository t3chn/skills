#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_REPO_URL = "git@github.com:t3chn/codex-skills.git"
DEFAULT_BRANCH = "main"

SUBMODULE_REL = Path(".codex/skills")
CONFIG_REL = Path(".codex/skills.config.json")
MANIFEST_REL = Path(".codex/skills.manifest")

CATALOG_REL = Path("catalog/skills.json")

ID_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"\b(\d+\.\d+\.\d+)\b")


class SkillsCtlError(RuntimeError):
    pass


def _eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _dump_toon(value: Any) -> str:
    """
    Token-optimized machine output.

    NOTE: This is JSON, but minified and stable for easy parsing and low token cost.
    """
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _extract_semver(text: str) -> str | None:
    m = SEMVER_RE.search(text)
    return m.group(1) if m else None


def _run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
        )
    except FileNotFoundError as e:
        raise SkillsCtlError(f"[ERROR] Command not found: {cmd[0]}") from e


def _git(
    args: list[str],
    *,
    cwd: Path,
    allow_file_protocol: bool = False,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    cmd = ["git"]
    if allow_file_protocol:
        cmd += ["-c", "protocol.file.allow=always"]
    cmd += args
    return _run(cmd, cwd=cwd, check=check, input_text=input_text)


def _git_stdout(
    args: list[str],
    *,
    cwd: Path,
    allow_file_protocol: bool = False,
) -> str:
    res = _git(args, cwd=cwd, allow_file_protocol=allow_file_protocol, check=True)
    return res.stdout.strip()


def _repo_root() -> Path:
    res = _run(["git", "rev-parse", "--show-toplevel"], check=False)
    if res.returncode != 0:
        raise SkillsCtlError("[ERROR] Not inside a git repository (needed for .codex/ bootstrap).")
    return Path(res.stdout.strip()).resolve()


def _detect_root() -> tuple[Path, bool]:
    """
    Return (root, is_git_repo). If not in a git repo, root is the current working directory.
    """
    res = _run(["git", "rev-parse", "--show-toplevel"], check=False)
    if res.returncode == 0 and res.stdout.strip():
        return Path(res.stdout.strip()).resolve(), True
    return Path.cwd().resolve(), False


def _looks_like_local_repo_url(repo_url: str) -> bool:
    if repo_url.startswith("file://"):
        return True
    expanded = Path(repo_url).expanduser()
    return expanded.exists()


def _ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _read_json_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise SkillsCtlError(f"[ERROR] Invalid JSON: {path} ({e})") from e
    if not isinstance(data, dict):
        raise SkillsCtlError(f"[ERROR] Invalid JSON (expected object): {path}")
    return data


def _write_json_file(path: Path, data: dict[str, Any]) -> None:
    _ensure_parent_dir(path)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_config(root: Path) -> dict[str, str]:
    data = _read_json_file(root / CONFIG_REL)
    repo_url = data.get("repo_url")
    branch = data.get("branch")
    out: dict[str, str] = {}
    if isinstance(repo_url, str) and repo_url.strip():
        out["repo_url"] = repo_url.strip()
    if isinstance(branch, str) and branch.strip():
        out["branch"] = branch.strip()
    return out


def _write_config(root: Path, *, repo_url: str, branch: str) -> None:
    _write_json_file(root / CONFIG_REL, {"repo_url": repo_url, "branch": branch})


def _find_submodule_name_by_path(root: Path, submodule_path: str) -> str | None:
    gitmodules = root / ".gitmodules"
    if not gitmodules.exists():
        return None
    res = _git(["config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$"], cwd=root, check=False)
    if res.returncode != 0:
        return None
    for line in res.stdout.splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) != 2:
            continue
        key, value = parts
        if value.strip() != submodule_path:
            continue
        # key: submodule.<name>.path
        if not key.startswith("submodule.") or not key.endswith(".path"):
            continue
        return key[len("submodule.") : -len(".path")]
    return None


def _read_gitmodules_url_branch(root: Path) -> tuple[str | None, str | None]:
    name = _find_submodule_name_by_path(root, str(SUBMODULE_REL))
    if name is None:
        return None, None
    url = _git_stdout(["config", "-f", ".gitmodules", "--get", f"submodule.{name}.url"], cwd=root)
    branch_res = _git(["config", "-f", ".gitmodules", "--get", f"submodule.{name}.branch"], cwd=root, check=False)
    branch = branch_res.stdout.strip() if branch_res.returncode == 0 else ""
    return (url.strip() or None, branch.strip() or None)


def _choose_repo_url_branch(root: Path, *, cli_repo_url: str | None, cli_branch: str | None) -> tuple[str, str]:
    if cli_repo_url:
        repo_url = cli_repo_url.strip()
        branch = (cli_branch or "").strip() or DEFAULT_BRANCH
        return repo_url, branch

    config = _load_config(root)
    if config.get("repo_url"):
        repo_url = config["repo_url"]
        branch = config.get("branch") or DEFAULT_BRANCH
        return repo_url, branch

    gitmodules_url, gitmodules_branch = _read_gitmodules_url_branch(root)
    if gitmodules_url:
        return gitmodules_url, gitmodules_branch or DEFAULT_BRANCH

    env_url = os.environ.get("SKILLS_REPO_URL", "").strip()
    env_branch = os.environ.get("SKILLS_REPO_BRANCH", "").strip()
    if env_url:
        return env_url, env_branch or DEFAULT_BRANCH

    return DEFAULT_REPO_URL, DEFAULT_BRANCH


def _validate_ids(ids: list[str]) -> list[str]:
    cleaned: list[str] = []
    for raw in ids:
        s = raw.strip()
        if not s:
            continue
        if not ID_RE.match(s):
            raise SkillsCtlError(f"[ERROR] Invalid skill id: {s!r} (expected [a-z0-9-]+)")
        cleaned.append(s)
    if not cleaned:
        return []
    # Dedup while keeping stable sorted output later.
    return cleaned


def _load_manifest(root: Path) -> list[str]:
    path = root / MANIFEST_REL
    if not path.exists():
        return []
    ids: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if not ID_RE.match(line):
            raise SkillsCtlError(f"[ERROR] Invalid id in manifest {MANIFEST_REL}: {line!r}")
        ids.append(line)
    # Keep deterministic order in-memory too.
    return sorted(set(ids))


def _write_manifest(root: Path, ids: list[str]) -> None:
    _ensure_parent_dir(root / MANIFEST_REL)
    unique = sorted(set(_validate_ids(ids)))
    header = (
        "# .codex/skills.manifest\n"
        "# One skill id per line. Lines starting with # are comments.\n"
    )
    body = "\n".join(unique)
    text = header + (body + "\n" if body else "")
    (root / MANIFEST_REL).write_text(text, encoding="utf-8")


def _is_git_repo(path: Path) -> bool:
    res = _run(["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"], check=False)
    return res.returncode == 0 and res.stdout.strip() == "true"


def _ensure_submodule(root: Path, *, repo_url: str, branch: str) -> None:
    submodule_dir = root / SUBMODULE_REL
    allow_file = _looks_like_local_repo_url(repo_url)

    registered_name = _find_submodule_name_by_path(root, str(SUBMODULE_REL))
    if registered_name is not None:
        # Submodule is registered. Ensure it's checked out on disk.
        _git(
            ["submodule", "update", "--init", "--depth", "1", "--", str(SUBMODULE_REL)],
            cwd=root,
            allow_file_protocol=allow_file,
        )
        return

    if submodule_dir.exists():
        if _is_git_repo(submodule_dir):
            raise SkillsCtlError(
                f"[ERROR] {SUBMODULE_REL} exists but is not registered as a submodule in .gitmodules."
            )
        raise SkillsCtlError(f"[ERROR] {SUBMODULE_REL} exists but is not a git repo/submodule.")

    (root / SUBMODULE_REL.parent).mkdir(parents=True, exist_ok=True)
    _git(
        ["submodule", "add", "-b", branch, repo_url, str(SUBMODULE_REL)],
        cwd=root,
        allow_file_protocol=allow_file,
    )
    _git(
        ["submodule", "update", "--init", "--depth", "1", "--", str(SUBMODULE_REL)],
        cwd=root,
        allow_file_protocol=allow_file,
    )


def _ensure_sparse(skills_repo_dir: Path) -> None:
    res = _git(["sparse-checkout", "init", "--cone"], cwd=skills_repo_dir, check=False)
    if res.returncode != 0:
        raise SkillsCtlError(
            "[ERROR] git sparse-checkout is not available. "
            "Upgrade git to a version that supports `git sparse-checkout`."
        )


def _set_sparse(skills_repo_dir: Path, paths: list[str]) -> None:
    _ensure_sparse(skills_repo_dir)
    unique = sorted({p.strip().strip("/") for p in paths if p.strip()})
    if not unique:
        unique = ["catalog"]
    input_text = "\n".join(unique) + "\n"
    res = _git(
        ["sparse-checkout", "set", "--stdin"],
        cwd=skills_repo_dir,
        check=False,
        input_text=input_text,
    )
    if res.returncode != 0:
        raise SkillsCtlError(f"[ERROR] Failed to set sparse-checkout:\n{res.stderr.strip()}")


def _submodule_dirty(skills_repo_dir: Path) -> bool:
    res = _git(["status", "--porcelain"], cwd=skills_repo_dir, check=True)
    return bool(res.stdout.strip())


def _ensure_catalog_present(skills_repo_dir: Path) -> None:
    catalog_path = skills_repo_dir / CATALOG_REL
    if catalog_path.exists():
        return
    _set_sparse(skills_repo_dir, ["catalog"])
    if not catalog_path.exists():
        raise SkillsCtlError(f"[ERROR] Missing catalog after sparse checkout: {catalog_path}")


def _load_catalog(skills_repo_dir: Path) -> dict[str, Any]:
    catalog_path = skills_repo_dir / CATALOG_REL
    if not catalog_path.exists():
        raise SkillsCtlError(f"[ERROR] Missing catalog: {catalog_path} (run `skillsctl bootstrap`)")
    try:
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SkillsCtlError(f"[ERROR] Invalid catalog JSON: {catalog_path} ({e})") from e
    if not isinstance(data, dict):
        raise SkillsCtlError(f"[ERROR] Invalid catalog (expected object): {catalog_path}")
    if data.get("schema_version") != 1:
        raise SkillsCtlError(f"[ERROR] Unsupported catalog schema_version: {data.get('schema_version')!r}")
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise SkillsCtlError("[ERROR] Invalid catalog: skills must be a list")
    return data


def _catalog_by_id(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in catalog.get("skills", []):
        if not isinstance(item, dict):
            continue
        skill_id = item.get("id")
        if isinstance(skill_id, str) and skill_id:
            out[skill_id] = item
    return out


def _resolve_paths(catalog: dict[str, Any], ids: list[str]) -> list[str]:
    by_id = _catalog_by_id(catalog)
    paths: set[str] = {"catalog"}
    for skill_id in ids:
        item = by_id.get(skill_id)
        if item is None:
            raise SkillsCtlError(f"[ERROR] Unknown skill id: {skill_id!r}")
        targets = item.get("targets") or {}
        codex = targets.get("codex") if isinstance(targets, dict) else None
        path = codex.get("path") if isinstance(codex, dict) else None
        if not isinstance(path, str) or not path.strip():
            raise SkillsCtlError(f"[ERROR] Skill {skill_id!r} is missing targets.codex.path in catalog")
        paths.add(path.strip().strip("/"))
    return sorted(paths)


def _stage_project_files(root: Path) -> None:
    candidates = [
        root / ".gitmodules",
        root / CONFIG_REL,
        root / MANIFEST_REL,
        root / SUBMODULE_REL,
    ]
    existing = [str(p.relative_to(root)) for p in candidates if p.exists()]
    if existing:
        _git(["add", "--"] + existing, cwd=root)


def _tokenize_query(query: str) -> list[str]:
    return [t for t in re.split(r"[^A-Za-z0-9]+", query.lower()) if t]


def _score_suggest(query: str, item: dict[str, Any]) -> int:
    q = query.strip().lower()
    if not q:
        return 0

    skill_id = str(item.get("id") or "").lower()
    score = 0
    if skill_id:
        if q == skill_id:
            score += 100
        elif skill_id.startswith(q):
            score += 40

    aliases = item.get("aliases") or []
    if isinstance(aliases, list):
        for alias in aliases:
            if not isinstance(alias, str):
                continue
            a = alias.lower()
            if q == a:
                score += 100
            elif a.startswith(q):
                score += 40

    tokens = _tokenize_query(query)
    tags = item.get("tags") or []
    title = str(item.get("title") or "").lower()
    desc = str(item.get("description") or "").lower()

    for tok in tokens:
        if isinstance(tags, list) and any(tok in str(tag).lower() for tag in tags):
            score += 20
        if tok and tok in title:
            score += 10
        if tok and tok in desc:
            score += 5

    return score


@dataclass(frozen=True)
class _Ctx:
    root: Path
    repo_url: str
    branch: str


def _ctx_from_args(*, cli_repo_url: str | None, cli_branch: str | None) -> _Ctx:
    root = _repo_root()
    repo_url, branch = _choose_repo_url_branch(root, cli_repo_url=cli_repo_url, cli_branch=cli_branch)
    return _Ctx(root=root, repo_url=repo_url, branch=branch)


def cmd_bootstrap(args: argparse.Namespace) -> int:
    ctx = _ctx_from_args(cli_repo_url=args.repo_url, cli_branch=args.branch)
    _ensure_submodule(ctx.root, repo_url=ctx.repo_url, branch=ctx.branch)

    # Ensure config exists (prefer .gitmodules values if present).
    if not (ctx.root / CONFIG_REL).exists():
        url, branch = _read_gitmodules_url_branch(ctx.root)
        _write_config(ctx.root, repo_url=url or ctx.repo_url, branch=branch or ctx.branch)

    skills_repo_dir = ctx.root / SUBMODULE_REL
    _set_sparse(skills_repo_dir, ["catalog"])

    if not (ctx.root / MANIFEST_REL).exists():
        _write_manifest(ctx.root, [])

    if args.stage:
        _stage_project_files(ctx.root)

    print("[OK] Bootstrapped .codex/skills (submodule + sparse-checkout catalog).")
    return 0


def cmd_catalog(args: argparse.Namespace) -> int:
    root = _repo_root()
    skills_repo_dir = root / SUBMODULE_REL
    if not skills_repo_dir.exists():
        raise SkillsCtlError("[ERROR] Missing .codex/skills. Run `skillsctl bootstrap` first.")
    _ensure_catalog_present(skills_repo_dir)
    catalog = _load_catalog(skills_repo_dir)
    if args.toon:
        print(_dump_toon(catalog.get("skills", [])))
        return 0

    for item in catalog.get("skills", []):
        if not isinstance(item, dict):
            continue
        skill_id = item.get("id")
        title = item.get("title")
        desc = item.get("description") or ""
        tags = item.get("tags") or []
        if not isinstance(skill_id, str):
            continue
        print(f"{skill_id} — {title}")
        if isinstance(tags, list) and tags:
            print(f"  tags: {', '.join(str(t) for t in tags)}")
        if isinstance(desc, str) and desc.strip():
            first_line = desc.strip().splitlines()[0]
            print(f"  {first_line}")
        print()
    return 0


def cmd_suggest(args: argparse.Namespace) -> int:
    root = _repo_root()
    skills_repo_dir = root / SUBMODULE_REL
    if not skills_repo_dir.exists():
        raise SkillsCtlError("[ERROR] Missing .codex/skills. Run `skillsctl bootstrap` first.")
    _ensure_catalog_present(skills_repo_dir)
    catalog = _load_catalog(skills_repo_dir)

    scored: list[tuple[int, str, dict[str, Any]]] = []
    for item in catalog.get("skills", []):
        if not isinstance(item, dict):
            continue
        skill_id = item.get("id")
        if not isinstance(skill_id, str):
            continue
        score = _score_suggest(args.query, item)
        if score <= 0:
            continue
        scored.append((score, skill_id, item))

    scored.sort(key=lambda t: (-t[0], t[1]))
    scored = scored[: args.limit]

    if args.toon:
        out = []
        for score, skill_id, item in scored:
            out.append(
                {
                    "id": skill_id,
                    "score": score,
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "tags": item.get("tags"),
                }
            )
        print(_dump_toon(out))
        return 0

    for score, skill_id, item in scored:
        title = item.get("title")
        desc = item.get("description") or ""
        print(f"{skill_id} — {title} (score: {score})")
        if isinstance(desc, str) and desc.strip():
            print(f"  {desc.strip().splitlines()[0]}")
    return 0


def _apply_selection(
    *,
    ctx: _Ctx,
    next_ids: list[str],
    stage: bool,
) -> None:
    _ensure_submodule(ctx.root, repo_url=ctx.repo_url, branch=ctx.branch)

    # Ensure config exists for reproducibility (prefer the actual .gitmodules URL/branch).
    if not (ctx.root / CONFIG_REL).exists():
        url, branch = _read_gitmodules_url_branch(ctx.root)
        _write_config(ctx.root, repo_url=url or ctx.repo_url, branch=branch or ctx.branch)

    skills_repo_dir = ctx.root / SUBMODULE_REL

    # If we'll change sparse selection, ensure there are no local edits inside the submodule.
    if skills_repo_dir.exists() and _submodule_dirty(skills_repo_dir):
        raise SkillsCtlError(
            "[ERROR] Refusing to change sparse-checkout selection because .codex/skills is dirty.\n"
            "Fix: commit/stash/reset changes inside .codex/skills, then retry."
        )

    _ensure_catalog_present(skills_repo_dir)
    catalog = _load_catalog(skills_repo_dir)
    by_id = _catalog_by_id(catalog)
    for skill_id in next_ids:
        if skill_id not in by_id:
            raise SkillsCtlError(f"[ERROR] Unknown skill id: {skill_id!r}")

    _write_manifest(ctx.root, next_ids)
    paths = _resolve_paths(catalog, next_ids)
    _set_sparse(skills_repo_dir, paths)

    if stage:
        _stage_project_files(ctx.root)


def cmd_install(args: argparse.Namespace) -> int:
    ctx = _ctx_from_args(cli_repo_url=args.repo_url, cli_branch=args.branch)
    current = _load_manifest(ctx.root)
    incoming = _validate_ids(args.ids)
    next_ids = sorted(set(current).union(incoming))
    _apply_selection(ctx=ctx, next_ids=next_ids, stage=args.stage)
    print(f"[OK] Installed {len(incoming)} skill(s). Selected total: {len(next_ids)}.")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    ctx = _ctx_from_args(cli_repo_url=args.repo_url, cli_branch=args.branch)
    current = _load_manifest(ctx.root)
    remove_ids = set(_validate_ids(args.ids))
    next_ids = [i for i in current if i not in remove_ids]
    _apply_selection(ctx=ctx, next_ids=next_ids, stage=args.stage)
    print(f"[OK] Removed {len(remove_ids)} skill(s). Selected total: {len(next_ids)}.")
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    ctx = _ctx_from_args(cli_repo_url=args.repo_url, cli_branch=args.branch)
    next_ids = sorted(set(_validate_ids(args.ids)))
    _apply_selection(ctx=ctx, next_ids=next_ids, stage=args.stage)
    print(f"[OK] Set selection to {len(next_ids)} skill(s).")
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    ctx = _ctx_from_args(cli_repo_url=args.repo_url, cli_branch=args.branch)
    if not (ctx.root / MANIFEST_REL).exists():
        _write_manifest(ctx.root, [])
    ids = _load_manifest(ctx.root)
    _apply_selection(ctx=ctx, next_ids=ids, stage=args.stage)
    print(f"[OK] Synced .codex/skills to manifest ({len(ids)} skill(s)).")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = _repo_root()
    config_present = (root / CONFIG_REL).exists()
    config = _load_config(root) if config_present else {}

    submodule_present = (root / SUBMODULE_REL).exists() and _is_git_repo(root / SUBMODULE_REL)
    submodule_dirty = _submodule_dirty(root / SUBMODULE_REL) if submodule_present else False

    manifest_present = (root / MANIFEST_REL).exists()
    manifest_ids = _load_manifest(root) if manifest_present else []

    sparse_paths: list[str] = []
    if submodule_present:
        res = _git(["sparse-checkout", "list"], cwd=root / SUBMODULE_REL, check=False)
        if res.returncode == 0:
            sparse_paths = [ln.strip() for ln in res.stdout.splitlines() if ln.strip()]

    git_version = _run(["git", "--version"], check=False).stdout.strip()

    out = {
        "repo_root": str(root),
        "config_present": config_present,
        "repo_url": config.get("repo_url"),
        "branch": config.get("branch"),
        "submodule_present": submodule_present,
        "submodule_dirty": submodule_dirty,
        "manifest_present": manifest_present,
        "manifest_ids": manifest_ids,
        "sparse_paths": sparse_paths,
        "git_version": git_version,
    }

    if args.toon:
        print(_dump_toon(out))
        return 0

    print(f"repo: {root}")
    print(f"config: {'present' if config_present else 'missing'}")
    if config_present:
        print(f"  repo_url: {config.get('repo_url')}")
        print(f"  branch: {config.get('branch') or DEFAULT_BRANCH}")
    print(f"submodule: {'present' if submodule_present else 'missing'}")
    if submodule_present:
        print(f"  dirty: {submodule_dirty}")
    print(f"manifest: {'present' if manifest_present else 'missing'} ({len(manifest_ids)} selected)")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    root, is_git_repo = _detect_root()

    git_version = _extract_semver(_run(["git", "--version"], check=False).stdout.strip() or "")

    bd_present = shutil.which("bd") is not None
    bd_version = None
    if bd_present:
        res = _run(["bd", "--version"], check=False)
        bd_version = _extract_semver(res.stdout.strip()) or None

    uvx_present = shutil.which("uvx") is not None
    uvx_version = None
    if uvx_present:
        res = _run(["uvx", "--version"], check=False)
        uvx_version = _extract_semver(res.stdout.strip()) or None

    beads_path = root / ".beads"
    beads_present = beads_path.exists()
    beads_config_present = (beads_path / "config.yaml").exists() if beads_path.is_dir() else False

    precommit_yaml = root / ".pre-commit-config.yaml"
    precommit_yml = root / ".pre-commit-config.yml"
    precommit_config_present = precommit_yaml.exists() or precommit_yml.exists()

    precommit_hook_present = False
    if is_git_repo:
        hook_rel = _run(["git", "rev-parse", "--git-path", "hooks/pre-commit"], check=False).stdout.strip()
        if hook_rel:
            precommit_hook_present = (root / hook_rel).exists()

    codex_dir_present = (root / ".codex").exists()
    codex_config_present = (root / CONFIG_REL).exists()
    codex_config = _load_config(root) if codex_config_present else {}
    effective_repo_url = None
    effective_branch = None
    if git_version is not None:
        try:
            effective_repo_url, effective_branch = _choose_repo_url_branch(
                root, cli_repo_url=None, cli_branch=None
            )
        except Exception:
            effective_repo_url, effective_branch = None, None

    submodule_dir = root / SUBMODULE_REL
    codex_skills_present = submodule_dir.exists() and _is_git_repo(submodule_dir)
    codex_skills_registered = _find_submodule_name_by_path(root, str(SUBMODULE_REL)) is not None if is_git_repo else False
    codex_skills_dirty = _submodule_dirty(submodule_dir) if codex_skills_present else None

    codex_sparse_paths: list[str] | None = None
    codex_catalog_present = None
    if codex_skills_present:
        res = _git(["sparse-checkout", "list"], cwd=submodule_dir, check=False)
        if res.returncode == 0:
            codex_sparse_paths = [ln.strip() for ln in res.stdout.splitlines() if ln.strip()]
        codex_catalog_present = (submodule_dir / CATALOG_REL).exists()

    manifest_present = (root / MANIFEST_REL).exists()
    manifest_ids = _load_manifest(root) if manifest_present else []

    # Recommended baseline: keep small and stable.
    baseline_skills = ["vi-security-guidance", "vi-prek", "vi-beads", "vi-feature-dev"]
    suggest_skills = [s for s in baseline_skills if s not in set(manifest_ids)]

    next_steps: list[str] = []
    if not is_git_repo:
        next_steps.append("git_init")
    if is_git_repo and not codex_skills_registered:
        next_steps.append("skills_bootstrap")
    if bd_present and not beads_present:
        next_steps.append("bd_init")
    if (not bd_present) and (not beads_present):
        next_steps.append("bd_install")
    if (not uvx_present) and (not precommit_config_present):
        next_steps.append("uv_install")
    if uvx_present and not precommit_config_present:
        next_steps.append("prek_init")
    if uvx_present and is_git_repo and precommit_config_present and not precommit_hook_present:
        next_steps.append("prek_install")
    if is_git_repo and suggest_skills:
        next_steps.append("skills_install")

    report = {
        "git_repo": is_git_repo,
        "repo_root": str(root),
        "git_version": git_version,
        "bd_present": bd_present,
        "bd_version": bd_version,
        "beads_present": beads_present,
        "beads_config_present": beads_config_present,
        "uvx_present": uvx_present,
        "uvx_version": uvx_version,
        "precommit_config_present": precommit_config_present,
        "precommit_hook_present": precommit_hook_present if is_git_repo else None,
        "codex_dir_present": codex_dir_present,
        "codex_config_present": codex_config_present,
        "codex_repo_url": codex_config.get("repo_url"),
        "codex_branch": codex_config.get("branch"),
        "effective_repo_url": effective_repo_url,
        "effective_branch": effective_branch,
        "codex_skills_present": codex_skills_present,
        "codex_skills_registered": codex_skills_registered,
        "codex_skills_dirty": codex_skills_dirty,
        "codex_sparse_paths": codex_sparse_paths,
        "codex_catalog_present": codex_catalog_present,
        "skills_manifest_present": manifest_present,
        "skills_manifest_ids": manifest_ids,
        "suggest_skills": suggest_skills,
        "next_steps": next_steps,
    }

    if args.human:
        print(f"repo_root: {root}")
        print(f"git_repo: {is_git_repo}")
        print(f"bd: {'present' if bd_present else 'missing'}")
        print(f"beads: {'present' if beads_present else 'missing'}")
        print(f"uvx: {'present' if uvx_present else 'missing'}")
        print(f"precommit config: {'present' if precommit_config_present else 'missing'}")
        print(f"codex skills: {'present' if codex_skills_registered else 'missing'}")
        if next_steps:
            print(f"next_steps: {', '.join(next_steps)}")
        return 0

    print(_dump_toon(report))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="skillsctl", description="Manage repo-scoped Codex skills via submodule+sparse.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_repo_flags(p: argparse.ArgumentParser) -> None:
        p.add_argument("--repo-url", help="Skills repo URL (defaults: config/env/hardcoded).")
        p.add_argument("--branch", help="Skills repo branch (default: main).")
        p.add_argument("--stage", action="store_true", help="Stage project file changes (git add).")
        p.add_argument("--yes", action="store_true", help="Non-interactive mode (reserved for future prompts).")

    p_bootstrap = sub.add_parser("bootstrap", help="Initialize .codex/skills submodule + sparse-checkout catalog.")
    add_repo_flags(p_bootstrap)
    p_bootstrap.set_defaults(func=cmd_bootstrap)

    p_catalog = sub.add_parser("catalog", help="List the catalog of available skills.")
    p_catalog.add_argument(
        "--toon",
        "--json",
        dest="toon",
        action="store_true",
        help="Token-optimized machine output (minified JSON).",
    )
    p_catalog.set_defaults(func=cmd_catalog)

    p_suggest = sub.add_parser("suggest", help="Suggest skills for a query using catalog scoring.")
    p_suggest.add_argument("query", help="Query string (e.g. 'pdf', 'security', 'rust cli').")
    p_suggest.add_argument("--limit", type=int, default=10, help="Max results (default: 10).")
    p_suggest.add_argument(
        "--toon",
        "--json",
        dest="toon",
        action="store_true",
        help="Token-optimized machine output (minified JSON).",
    )
    p_suggest.set_defaults(func=cmd_suggest)

    p_install = sub.add_parser("install", help="Add skill id(s) to the manifest and update sparse-checkout.")
    add_repo_flags(p_install)
    p_install.add_argument("ids", nargs="+", help="Skill id(s) to install.")
    p_install.set_defaults(func=cmd_install)

    p_remove = sub.add_parser("remove", help="Remove skill id(s) from the manifest and update sparse-checkout.")
    add_repo_flags(p_remove)
    p_remove.add_argument("ids", nargs="+", help="Skill id(s) to remove.")
    p_remove.set_defaults(func=cmd_remove)

    p_set = sub.add_parser("set", help="Replace the manifest selection with the given skill id(s).")
    add_repo_flags(p_set)
    p_set.add_argument("ids", nargs="*", help="Skill id(s) to set (empty clears selection).")
    p_set.set_defaults(func=cmd_set)

    p_sync = sub.add_parser("sync", help="Sync submodule+sparse-checkout to the committed manifest.")
    add_repo_flags(p_sync)
    p_sync.set_defaults(func=cmd_sync)

    p_status = sub.add_parser("status", help="Show current bootstrap/selection status.")
    p_status.add_argument(
        "--toon",
        "--json",
        dest="toon",
        action="store_true",
        help="Token-optimized machine output (minified JSON).",
    )
    p_status.set_defaults(func=cmd_status)

    p_doctor = sub.add_parser("doctor", help="Run environment and project checks.")
    p_doctor.add_argument("--human", action="store_true", help="Human-readable output (debug).")
    p_doctor.set_defaults(func=cmd_doctor)

    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except SkillsCtlError as e:
        _eprint(str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
