## 1. Repository Foundation

- [x] 1.1 Create the canonical repository structure for shared skills under `skills/` with initial `.curated` and `.experimental` groupings
- [x] 1.2 Create the `profiles/`, `templates/`, `docs/`, and `scripts/` directories required by the design
- [x] 1.3 Define which existing agent-specific directories will remain authored versus generated during migration

## 2. Skill Template System

- [x] 2.1 Add a standard skill template containing `SKILL.md` and `agents/openai.yaml`
- [x] 2.2 Add optional template support for `scripts/`, `references/`, and `assets/`
- [x] 2.3 Ensure the template structure supports progressive disclosure for healthcare-oriented skills

## 3. Authoring Guide

- [x] 3.1 Write a healthcare-focused skill creation guide covering repository conventions and domain-fit expectations
- [x] 3.2 Document how contributors should use `SKILL.md`, `references/`, `scripts/`, and `assets/`
- [x] 3.3 Define curated versus experimental distribution-readiness criteria in the guide

## 4. Validation And Composition

- [x] 4.1 Implement validation for skill frontmatter, naming, and required files
- [x] 4.2 Implement validation for agent profile overlays against referenced base skills
- [x] 4.3 Implement composition logic to build agent-specific outputs from canonical skills plus optional overlays
- [x] 4.4 Verify the composed output remains compatible with `skills.sh` conventions

## 5. Healthcare Skill Library Setup

- [x] 5.1 Define the initial curated healthcare skill categories the repository will support
- [x] 5.2 Add initial placeholder or starter skills that demonstrate the canonical structure for healthcare product-development workflows
- [x] 5.3 Ensure curated skills are clearly separated from experimental or system-only skills

## 6. Migration And Verification

- [x] 6.1 Migrate existing reusable skills into the canonical source layout without destructive removal of current agent-specific folders
- [x] 6.2 Generate or map agent-specific install outputs from the canonical source and overlay model
- [x] 6.3 Verify repository documentation and generated outputs are internally consistent with the proposal, design, and specs
