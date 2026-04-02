#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PROFILES_DIR = ROOT / "profiles"
README_FILE = ROOT / "README.md"
AUTHORED_GROUPS = {".curated", ".experimental"}
DIST_GROUPS = {".curated"}
TARGET_LAYOUT = {
    "agents": Path(".agents") / "skills",
    "claude": Path(".claude") / "skills",
}
LEGACY_AGENT_ROOTS = [Path(".codex"), Path(".gemini")]
EMPTY_SKILL_ROOTS = [Path(".github") / "skills"]


def iter_skill_dirs(groups: set[str] | None = None) -> list[Path]:
    included_groups = groups or AUTHORED_GROUPS
    skill_dirs: list[Path] = []
    for group_dir in sorted(SKILLS_DIR.iterdir()):
        if not group_dir.is_dir() or group_dir.name not in included_groups:
            continue
        for skill_dir in sorted(group_dir.iterdir()):
            if (skill_dir / "SKILL.md").exists():
                skill_dirs.append(skill_dir)
    return skill_dirs


def target_root_for(base_root: Path, agent: str) -> Path:
    return base_root / TARGET_LAYOUT[agent]


def ensure_empty_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        if child.name == ".gitkeep":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def cleanup_legacy_outputs(base_root: Path) -> None:
    for legacy_root in LEGACY_AGENT_ROOTS:
        target = base_root / legacy_root
        if target.exists():
            shutil.rmtree(target)

    for empty_root in EMPTY_SKILL_ROOTS:
        ensure_empty_dir(base_root / empty_root)


def compose_agent(agent: str, skill_dirs: list[Path], base_root: Path = ROOT) -> None:
    target_root = target_root_for(base_root, agent)
    target_root.mkdir(parents=True, exist_ok=True)
    for skill_dir in skill_dirs:
        target_skill_dir = target_root / skill_dir.name
        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)
        shutil.copytree(skill_dir, target_skill_dir)

        overlay_dir = PROFILES_DIR / agent / skill_dir.name
        if not overlay_dir.exists():
            continue

        appended = overlay_dir / "SKILL.append.md"
        if appended.exists():
            with (target_skill_dir / "SKILL.md").open("a") as handle:
                handle.write("\n\n")
                handle.write(appended.read_text().rstrip())
                handle.write("\n")

        overlay_yaml = overlay_dir / "agents" / "openai.yaml"
        if overlay_yaml.exists():
            (target_skill_dir / "agents").mkdir(exist_ok=True)
            shutil.copy2(overlay_yaml, target_skill_dir / "agents" / "openai.yaml")


def compose_all(base_root: Path = ROOT, agents: list[str] | None = None) -> int:
    selected_agents = agents or sorted(TARGET_LAYOUT)
    skill_dirs = iter_skill_dirs()
    cleanup_legacy_outputs(base_root)
    for agent in selected_agents:
        compose_agent(agent, skill_dirs, base_root=base_root)
        print(f"[ok] composed {len(skill_dirs)} skills for {agent}")
    if base_root != ROOT and README_FILE.exists():
        shutil.copy2(README_FILE, base_root / "README.md")
        print("[ok] copied README.md to composed root")
    return 0


def export_dist_tree(output_root: Path) -> int:
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)

    dist_skills_root = output_root / "skills"
    dist_skills_root.mkdir(parents=True, exist_ok=True)

    for group_dir in sorted(SKILLS_DIR.iterdir()):
        if not group_dir.is_dir() or group_dir.name not in DIST_GROUPS:
            continue
        target_group_dir = dist_skills_root / group_dir.name
        target_group_dir.mkdir(parents=True, exist_ok=True)
        for skill_dir in iter_skill_dirs({group_dir.name}):
            shutil.copytree(skill_dir, target_group_dir / skill_dir.name)
        print(f"[ok] exported {len(iter_skill_dirs({group_dir.name}))} skills in {group_dir.name}")

    if README_FILE.exists():
        shutil.copy2(README_FILE, output_root / "README.md")
        print("[ok] copied README.md to dist root")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose canonical skills into agent install trees.")
    parser.add_argument("--agent", action="append", choices=sorted(TARGET_LAYOUT), help="Compose only one agent")
    parser.add_argument("--root", default=str(ROOT), help="Base directory where agent install trees should be written")
    parser.add_argument("--dist-root", help="Build a clean distribution tree rooted at this directory")
    args = parser.parse_args()

    if args.dist_root:
        if args.root != str(ROOT) or args.agent:
            parser.error("--dist-root cannot be combined with --root or --agent")
        return export_dist_tree(Path(args.dist_root))

    return compose_all(base_root=Path(args.root), agents=args.agent)


if __name__ == "__main__":
    raise SystemExit(main())
