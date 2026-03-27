#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from compose_skills import ROOT
from validate_skill_library import iter_skill_dirs, validate_skill_dir

DEFAULT_TARGETS = [ROOT / "skills"]


def verify_root(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.exists():
        return [f"{root}: missing root"]

    if root.name == "skills" and root.parent == ROOT:
        for skill_dir in iter_skill_dirs(root):
            errors.extend(validate_skill_dir(skill_dir))
        return errors

    for skill_dir in sorted(root.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            errors.extend(validate_skill_dir(skill_dir))
    return errors


def verify_distribution_root(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.exists():
        return [f"{root}: missing root"]

    readme = root / "README.md"
    if not readme.exists():
        errors.append(f"{root}: missing README.md")

    skills_root = root / "skills"
    if not skills_root.exists():
        errors.append(f"{root}: missing skills directory")
        return errors

    errors.extend(verify_root(skills_root))
    return errors


def verify_targets(targets: list[Path]) -> list[str]:
    errors: list[str] = []
    for target in targets:
        errors.extend(verify_root(target))
    return errors


def verify_dist_branch(branch: str) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="skills-dist-verify-") as tmpdir:
        worktree_path = Path(tmpdir)
        subprocess.run(["git", "worktree", "add", "--detach", str(worktree_path), branch], cwd=ROOT, check=True)
        try:
            return verify_distribution_root(worktree_path)
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(worktree_path)], cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify canonical and composed skills remain skills.sh compatible.")
    parser.add_argument("--target", action="append", help="Override target roots")
    parser.add_argument("--dist-root", help="Verify a clean dist tree rooted at this directory")
    parser.add_argument("--dist-branch", help="Verify a published dist branch by checking out a temporary worktree")
    args = parser.parse_args()

    if args.target and (args.dist_root or args.dist_branch):
        print("[error] use either --target, --dist-root, or --dist-branch", flush=True)
        return 1

    try:
        if args.dist_branch:
            errors = verify_dist_branch(args.dist_branch)
        else:
            if args.dist_root:
                errors = verify_distribution_root(Path(args.dist_root))
            else:
                targets = [Path(value) for value in args.target] if args.target else DEFAULT_TARGETS
                errors = verify_targets(targets)
    except subprocess.CalledProcessError as exc:
        print(f"[error] git command failed: {exc}", flush=True)
        return 1

    if errors:
        for error in errors:
            print(f"[error] {error}")
        return 1

    print("[ok] skill layout looks compatible with standard skills.sh discovery")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
