#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from compose_skills import ROOT, export_dist_tree
from verify_skills_sh_compat import verify_distribution_root


def ensure_git_repo() -> None:
    subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=ROOT, check=True, capture_output=True, text=True)


def build_dist_tree(output_root: Path) -> None:
    export_dist_tree(output_root)


def verify_dist_tree(output_root: Path) -> None:
    errors = verify_distribution_root(output_root)
    if errors:
        raise RuntimeError("\n".join(errors))


def git_output(args: list[str], cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def publish_dist_branch(branch: str, staging_root: Path, push: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="skills-dist-publish-") as tmpdir:
        worktree_path = Path(tmpdir)
        subprocess.run(["git", "worktree", "add", "--detach", str(worktree_path), "HEAD"], cwd=ROOT, check=True)
        temp_branch = f"__{branch}_build__"
        try:
            subprocess.run(["git", "checkout", "--orphan", temp_branch], cwd=worktree_path, check=True)
            for entry in worktree_path.iterdir():
                if entry.name == ".git":
                    continue
                if entry.is_dir():
                    shutil.rmtree(entry)
                else:
                    entry.unlink()

            for entry in staging_root.iterdir():
                destination = worktree_path / entry.name
                if entry.is_dir():
                    shutil.copytree(entry, destination)
                else:
                    shutil.copy2(entry, destination)

            subprocess.run(["git", "add", "-A"], cwd=worktree_path, check=True)
            subprocess.run(["git", "commit", "-m", f"Publish {branch} branch"], cwd=worktree_path, check=True)
            commit_sha = git_output(["rev-parse", "HEAD"], cwd=worktree_path)
            subprocess.run(["git", "checkout", "--detach", commit_sha], cwd=worktree_path, check=True)
            subprocess.run(["git", "update-ref", f"refs/heads/{branch}", commit_sha], cwd=ROOT, check=True)
            subprocess.run(["git", "update-ref", "-d", f"refs/heads/{temp_branch}"], cwd=ROOT, check=False)
            if push:
                subprocess.run(["git", "push", "origin", f"+{branch}:{branch}"], cwd=ROOT, check=True)
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(worktree_path)], cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a clean dist tree and force-update a dist branch.")
    parser.add_argument("--branch", default="dist", help="Branch to replace with the built dist output")
    parser.add_argument("--push", action="store_true", help="Force-push the updated dist branch to origin")
    parser.add_argument("--output-dir", help="Optional explicit staging directory for the built dist tree")
    parser.add_argument("--build-only", action="store_true", help="Only build the dist tree, do not publish the branch")
    args = parser.parse_args()

    staging_root = Path(args.output_dir) if args.output_dir else Path(tempfile.mkdtemp(prefix="skills-dist-tree-"))
    output_was_explicit = args.output_dir is not None

    try:
        build_dist_tree(staging_root)
        verify_dist_tree(staging_root)
        print(f"[ok] built dist tree at {staging_root}")
        if args.build_only:
            return 0

        ensure_git_repo()
        publish_dist_branch(args.branch, staging_root, push=args.push)
        print(f"[ok] updated branch '{args.branch}' to match the built dist tree")
        if args.push:
            print(f"[ok] force-pushed branch '{args.branch}' to origin")
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"[error] git command failed: {exc}")
        return 1
    except RuntimeError as exc:
        print(f"[error] dist verification failed:\n{exc}")
        return 1
    finally:
        if not output_was_explicit and staging_root.exists():
            shutil.rmtree(staging_root)


if __name__ == "__main__":
    raise SystemExit(main())
