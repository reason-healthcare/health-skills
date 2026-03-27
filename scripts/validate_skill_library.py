#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PROFILES_DIR = ROOT / "profiles"
MAX_NAME_LENGTH = 64
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
ALLOWED_OVERLAY_FILES = {"SKILL.append.md", "agents/openai.yaml"}
AUTHORED_GROUPS = {".curated", ".experimental"}


def iter_skill_dirs(skills_dir: Path) -> list[Path]:
    skill_dirs: list[Path] = []
    for group_dir in sorted(skills_dir.iterdir()):
        if not group_dir.is_dir() or group_dir.name not in AUTHORED_GROUPS:
            continue
        for skill_dir in sorted(group_dir.iterdir()):
            if (skill_dir / "SKILL.md").exists():
                skill_dirs.append(skill_dir)
    return skill_dirs


def read_frontmatter(path: Path) -> dict:
    content = path.read_text()
    if not content.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    _, rest = content.split("---\n", 1)
    frontmatter_text, _ = rest.split("\n---\n", 1)
    data: dict[str, object] = {}
    current_key: str | None = None
    for line in frontmatter_text.splitlines():
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")) and ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            data[current_key] = value if value else {}
        elif current_key and isinstance(data.get(current_key), dict):
            continue
    if not data:
        raise ValueError("frontmatter is not a mapping")
    return data


def strip_quotes(value: str) -> str:
    return value.strip().strip("'\"")


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    try:
        frontmatter = read_frontmatter(skill_md)
    except Exception as exc:  # noqa: BLE001
        return [f"{skill_dir}: invalid SKILL.md frontmatter ({exc})"]

    unexpected = sorted(set(frontmatter) - ALLOWED_FRONTMATTER)
    if unexpected:
        errors.append(f"{skill_dir}: unexpected frontmatter keys: {', '.join(unexpected)}")

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not isinstance(name, str) or not strip_quotes(name):
        errors.append(f"{skill_dir}: missing frontmatter name")
    else:
        normalized_name = strip_quotes(name)
        if len(normalized_name) > MAX_NAME_LENGTH or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-" for ch in normalized_name):
            errors.append(f"{skill_dir}: invalid kebab-case skill name '{normalized_name}'")

    if not isinstance(description, str) or not strip_quotes(description):
        errors.append(f"{skill_dir}: missing frontmatter description")

    agent_yaml = skill_dir / "agents" / "openai.yaml"
    if agent_yaml.exists():
        if "interface:" not in agent_yaml.read_text():
            errors.append(f"{skill_dir}: agents/openai.yaml missing interface block")

    return errors


def relative_overlay_files(overlay_dir: Path) -> list[str]:
    files: list[str] = []
    for path in overlay_dir.rglob("*"):
        if path.is_file():
            files.append(path.relative_to(overlay_dir).as_posix())
    return sorted(files)


def validate_profiles(profiles_dir: Path, skills_dir: Path) -> list[str]:
    errors: list[str] = []
    if not profiles_dir.exists():
        return errors

    known_skills = {skill_dir.name for skill_dir in iter_skill_dirs(skills_dir)}
    for agent_dir in sorted(profiles_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        for overlay_dir in sorted(agent_dir.iterdir()):
            if not overlay_dir.is_dir():
                continue
            if overlay_dir.name not in known_skills:
                errors.append(f"{overlay_dir}: overlay references missing base skill")
                continue
            files = relative_overlay_files(overlay_dir)
            for relpath in files:
                if relpath not in ALLOWED_OVERLAY_FILES:
                    errors.append(f"{overlay_dir}: unsupported overlay file '{relpath}'")
            openai_yaml = overlay_dir / "agents" / "openai.yaml"
            if openai_yaml.exists():
                if "interface:" not in openai_yaml.read_text():
                    errors.append(f"{overlay_dir}: overlay openai.yaml missing interface block")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical skills and overlays.")
    parser.add_argument("--skills-dir", default=str(SKILLS_DIR))
    parser.add_argument("--profiles-dir", default=str(PROFILES_DIR))
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    profiles_dir = Path(args.profiles_dir)
    errors: list[str] = []

    if not skills_dir.exists():
        print("[error] skills directory does not exist", file=sys.stderr)
        return 1

    for skill_dir in iter_skill_dirs(skills_dir):
        errors.extend(validate_skill_dir(skill_dir))
    errors.extend(validate_profiles(profiles_dir, skills_dir))

    if errors:
        for error in errors:
            print(f"[error] {error}")
        return 1

    print("[ok] skill library is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
