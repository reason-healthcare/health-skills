#!/usr/bin/env python3
"""Security audit for skill files, approximating the checks run by skills.sh.

Checks modeled after observed scanner findings:

  Gen Agent Trust Hub
    COMMAND_EXECUTION  — user-controlled input passed to shell commands without
                         explicit sanitization / validation guard in the same
                         skill file.
    PROMPT_INJECTION   — skill reads untrusted external content (codebase files,
                         user documents) without a boundary rule that distinguishes
                         data from instructions.

  Snyk W007
    CREDENTIAL_HANDLING — skill instructs the agent to copy / reproduce content
                          verbatim (e.g. "preserve substance", "copy content")
                          without a redaction rule for secrets/credentials.

Each check emits findings at WARN or FAIL level. Any FAIL causes a non-zero exit.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
AUTHORED_GROUPS = {".curated", ".experimental"}

# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    skill: str
    level: str          # FAIL | WARN
    code: str
    message: str
    hint: str = ""


# Patterns that suggest the skill runs a shell command using user-provided input
SHELL_COMMAND_PATTERNS = [
    re.compile(r"run\s+`[^`]*<[^>]+>`", re.IGNORECASE),
    re.compile(r"execute\s+`[^`]*<[^>]+>`", re.IGNORECASE),
    re.compile(r"`git\s+\S+[^`]*<[^`]*>`", re.IGNORECASE),
    re.compile(r"git diff[^`\n]*<range>", re.IGNORECASE),
]

# Patterns that indicate sanitization / validation is already addressed
SANITIZATION_PATTERNS = [
    re.compile(r"(sanitiz|validat|reject|only.*valid|must.*contain|allowed.*character)", re.IGNORECASE),
]

# Patterns suggesting the skill reads untrusted external content
EXTERNAL_READ_PATTERNS = [
    re.compile(r"read\s+(each|all|every)\s+file", re.IGNORECASE),
    re.compile(r"ingest(ing)?\s+(content|file|codebase)", re.IGNORECASE),
    re.compile(r"(scan|process|analyze)\s+(the\s+)?(codebase|repository|source files)", re.IGNORECASE),
    re.compile(r"content\s+from\s+(the\s+)?(codebase|repository|source|target)", re.IGNORECASE),
]

# Patterns confirming a prompt-injection boundary rule exists
INJECTION_BOUNDARY_PATTERNS = [
    re.compile(r"(codebase|analyzed|source).{0,60}(data|not instructions|not directives)", re.IGNORECASE),
    re.compile(r"(prompt.injection|injection.boundary|treat.{0,30}as data)", re.IGNORECASE),
    re.compile(r"content.{0,60}(is data|not.*instruct)", re.IGNORECASE),
]

# Patterns suggesting verbatim content reproduction without redaction
VERBATIM_COPY_PATTERNS = [
    re.compile(r"preserve substance", re.IGNORECASE),
    re.compile(r"copy content from source", re.IGNORECASE),
    re.compile(r"(reproduce|replicate|verbatim).{0,40}content", re.IGNORECASE),
    re.compile(r"do not rewrite.{0,40}preserve substance", re.IGNORECASE),
]

# Patterns confirming credential redaction is addressed
REDACTION_PATTERNS = [
    re.compile(r"(redact|credential|secret|api.key|token).{0,60}(before|prior|scan|check)", re.IGNORECASE),
    re.compile(r"(scan for|detect|strip).{0,40}(secret|credential|key|token|password)", re.IGNORECASE),
    re.compile(r"\[REDACTED", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def check_command_execution(skill_name: str, content: str) -> list[Finding]:
    """FAIL if skill issues shell commands with user-controlled input and no
    explicit validation/sanitization guard in the same file."""
    findings: list[Finding] = []

    has_shell_command = any(p.search(content) for p in SHELL_COMMAND_PATTERNS)
    if not has_shell_command:
        return findings

    has_sanitization = any(p.search(content) for p in SANITIZATION_PATTERNS)
    if not has_sanitization:
        findings.append(Finding(
            skill=skill_name,
            level="FAIL",
            code="COMMAND_EXECUTION",
            message="Skill runs a shell command with user-provided input but no input validation rule was found.",
            hint="Add an Operating Rule that validates/rejects the input before use (e.g. 'reject shell special characters').",
        ))
    return findings


def check_prompt_injection(skill_name: str, content: str) -> list[Finding]:
    """FAIL if skill reads untrusted external content without a boundary rule."""
    findings: list[Finding] = []

    has_external_read = any(p.search(content) for p in EXTERNAL_READ_PATTERNS)
    if not has_external_read:
        return findings

    has_boundary = any(p.search(content) for p in INJECTION_BOUNDARY_PATTERNS)
    if not has_boundary:
        findings.append(Finding(
            skill=skill_name,
            level="FAIL",
            code="PROMPT_INJECTION",
            message="Skill reads untrusted external content (codebase/files) with no prompt-injection boundary rule.",
            hint="Add an Operating Rule stating that all codebase content is data to be analyzed, not instructions to follow.",
        ))
    return findings


def check_credential_handling(skill_name: str, content: str) -> list[Finding]:
    """FAIL if skill instructs verbatim content copy without a redaction rule."""
    findings: list[Finding] = []

    has_verbatim_copy = any(p.search(content) for p in VERBATIM_COPY_PATTERNS)
    if not has_verbatim_copy:
        return findings

    has_redaction = any(p.search(content) for p in REDACTION_PATTERNS)
    if not has_redaction:
        findings.append(Finding(
            skill=skill_name,
            level="FAIL",
            code="CREDENTIAL_HANDLING",
            message="Skill copies content verbatim without a credential/secret redaction rule.",
            hint="Add an Operating Rule to scan for and redact secrets/keys/tokens before reproducing content.",
        ))
    return findings


CHECKS = [
    check_command_execution,
    check_prompt_injection,
    check_credential_handling,
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def iter_skill_dirs(skills_dir: Path) -> list[Path]:
    skill_dirs: list[Path] = []
    for group_dir in sorted(skills_dir.iterdir()):
        if not group_dir.is_dir() or group_dir.name not in AUTHORED_GROUPS:
            continue
        for skill_dir in sorted(group_dir.iterdir()):
            if (skill_dir / "SKILL.md").exists():
                skill_dirs.append(skill_dir)
    return skill_dirs


def audit_skill(skill_dir: Path) -> list[Finding]:
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text()
    skill_name = skill_dir.name
    findings: list[Finding] = []
    for check in CHECKS:
        findings.extend(check(skill_name, content))
    return findings


def run_audit(skills_dir: Path) -> list[Finding]:
    all_findings: list[Finding] = []
    for skill_dir in iter_skill_dirs(skills_dir):
        all_findings.extend(audit_skill(skill_dir))
    return all_findings


def print_report(findings: list[Finding]) -> None:
    if not findings:
        print("[ok] no security findings")
        return

    by_skill: dict[str, list[Finding]] = {}
    for f in findings:
        by_skill.setdefault(f.skill, []).append(f)

    for skill, skill_findings in sorted(by_skill.items()):
        for f in skill_findings:
            print(f"[{f.level}] {skill}: {f.code}")
            print(f"       {f.message}")
            if f.hint:
                print(f"       hint: {f.hint}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Security audit for skill SKILL.md files")
    parser.add_argument(
        "skills_dir",
        nargs="?",
        type=Path,
        default=SKILLS_DIR,
        help="Path to the skills directory (default: repo skills/)",
    )
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="Downgrade FAIL findings to WARN (exit 0 regardless of findings)",
    )
    args = parser.parse_args()

    findings = run_audit(args.skills_dir)

    if args.warn_only:
        for f in findings:
            f.level = "WARN"

    print_report(findings)

    fail_count = sum(1 for f in findings if f.level == "FAIL")
    return 1 if fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
