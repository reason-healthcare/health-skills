#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates" / "skill"
MAX_NAME_LENGTH = 64
OPTIONAL_DIRS = ("scripts", "references", "assets")


def normalize_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def validate_name(value: str) -> None:
    if not value:
        raise ValueError("skill name cannot be empty")
    if len(value) > MAX_NAME_LENGTH:
        raise ValueError(f"skill name is too long: {len(value)} > {MAX_NAME_LENGTH}")
    if not re.fullmatch(r"[a-z0-9-]+", value):
        raise ValueError("skill name must use lowercase kebab-case")


def build_skill_md(name: str, title: str, description: str) -> str:
    template = (TEMPLATE_DIR / "SKILL.md").read_text()
    template = template.replace("your-skill-name", name)
    template = template.replace("Your Skill Name", title)
    template = template.replace("<replace-this>", description)
    return template


def build_openai_yaml(name: str, title: str) -> str:
    template = (TEMPLATE_DIR / "agents" / "openai.yaml").read_text()
    template = template.replace("Your Skill Name", title)
    template = template.replace("your-skill-name", name)
    template = template.replace("Healthcare skill starter", f"{title[:28]}".strip())
    return template


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a healthcare skill from the local template.")
    parser.add_argument("name", help="Skill name in kebab-case")
    parser.add_argument("--group", default=".experimental", choices=[".curated", ".experimental"])
    parser.add_argument("--description", default="this healthcare task")
    parser.add_argument(
        "--include",
        nargs="*",
        default=[],
        choices=OPTIONAL_DIRS,
        help="Optional resource directories to create",
    )
    args = parser.parse_args()

    name = normalize_name(args.name)
    validate_name(name)
    title = " ".join(part.capitalize() for part in name.split("-"))
    skill_dir = ROOT / "skills" / args.group / name
    if skill_dir.exists():
        print(f"[error] skill already exists: {skill_dir}", file=sys.stderr)
        return 1

    (skill_dir / "agents").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(build_skill_md(name, title, args.description))
    (skill_dir / "agents" / "openai.yaml").write_text(build_openai_yaml(name, title))
    for dirname in args.include:
        (skill_dir / dirname).mkdir()

    print(f"[ok] created {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
