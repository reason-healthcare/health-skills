## Purpose

Defines the canonical repository structure, source-of-truth model, and derived-artifact relationship between authored skills on `main` and generated outputs (local agent trees and `dist` branch).

## Requirements

### Requirement: Repository defines canonical authored source
The repository SHALL use a canonical authored source layout that is independent from agent-specific installation directories.

#### Scenario: Maintainer authors a shared skill
- **WHEN** a maintainer creates or edits a base skill
- **THEN** the maintainer uses the canonical source tree (`skills/` on `main`) rather than authoring directly inside an agent-specific install directory

#### Scenario: Source of truth is unambiguous
- **WHEN** a contributor inspects the repository
- **THEN** `skills/` on the `main` branch is the single source of truth
- **THEN** local agent trees (`.agents/skills/`, `.claude/skills/`) and the `dist` branch are clearly identified as generated outputs

### Requirement: Repository remains compatible with skills.sh discovery
The repository SHALL structure base skills so they can be consumed by `skills.sh` without inventing a custom skill format.

#### Scenario: Consumer prepares skills for distribution
- **WHEN** a consumer packages or installs a skill from the repository
- **THEN** the skill content conforms to standard Agent Skills file expectations such as `SKILL.md`
- **THEN** the packaging flow does not require a proprietary runtime-specific skill schema

### Requirement: Agent-specific installs are derived artifacts
The repository SHALL treat agent-specific skill directories as generated or composed outputs derived from base skills and optional overlays.

#### Scenario: Maintainer updates a canonical skill
- **WHEN** the base skill changes
- **THEN** agent-specific outputs are updated from the canonical source plus overlay rules
- **THEN** agent-specific directories are not treated as co-equal sources of truth
