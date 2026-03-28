## Why

We need a shared repository for creating, validating, and distributing AI skills that help teams build healthcare technology software and digital health products with more consistency. The immediate opportunity is to define a portable skill system, templates, and authoring standards that make high-quality healthcare-focused skills reusable across agents and compatible with `skills.sh`.

## What Changes

- Introduce a canonical repository structure for authoring and distributing shared healthcare-tech skills under `skills/`.
- Define how healthcare-oriented skills are organized, versioned, validated, and prepared for `skills.sh` consumption.
- Standardize a reusable skill template including `SKILL.md`, `agents/openai.yaml`, and optional `scripts/`, `references/`, and `assets/` directories.
- Define a healthcare-focused skill creation guide that captures state-of-the-art authoring patterns, progressive disclosure, validation, and distribution practices.
- Define an optional profile overlay model under `profiles/<agent>/<skill>/` for agent-specific customizations without forking the base skill.

## Capabilities

### New Capabilities
- `healthcare-skill-library`: Establish repository conventions and packaging rules for a shared library of skills used to create healthcare software and products.
- `skills-repo-foundation`: Establish canonical directory contracts and compatibility rules for `skills.sh` discovery and multi-agent portability.
- `skill-template-system`: Provide a standard template and generation contract for new healthcare-oriented skills, including metadata and optional resource bundles.
- `agent-profile-overlays`: Enable optional per-agent overlay patches/config to customize behavior without duplicating base skills.
- `skill-authoring-guide`: Define a state-of-the-art authoring, validation, and distribution process for creating and maintaining high-quality skills.

### Modified Capabilities
- None.

## Impact

- Affected code and content: repository structure (`skills/`, `profiles/`, `templates/`, `docs/`, `scripts/`), OpenSpec specs and tasks, and initial healthcare-tech skill authoring assets.
- APIs/interfaces: skill packaging and distribution flow for `skills.sh`, including deterministic mapping from canonical source + optional overlays to target agent skill directories.
- Dependencies/systems: requires alignment with Agent Skills `SKILL.md` frontmatter conventions, `skills.sh` discovery behavior, and repository guidance for healthcare product development workflows.
