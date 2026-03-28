## Why

Healthcare engineering teams consistently lack the documentation their systems require — both for regulatory compliance (HIPAA, ONC, FDA SaMD) and for effective human and agent collaboration. Existing tools either generate generic templates or require manual effort to organize scattered content. A skill that can audit coverage and consolidate documentation from actual codebase evidence fills a gap no current tool addresses well.

## What Changes

- Add new `health-docs` skill to `skills/.experimental/`
- Skill supports two modes: **analyze** (coverage audit, no writes) and **document** (consolidate + fill gaps)
- Analyze mode produces a structured handoff artifact (`.health-docs/analysis.md`) consumed by document mode
- Document mode conducts evidence-informed interview before any writes, then confirms a pre-flight plan
- Skill composes existing skills (`$health-hipaa-review`, `$health-fhir-api-design`, `$health-human-factors`) as subagents for deep-dimension analysis
- Uses `scripts/init_skill.py` to scaffold the skill directory during implementation

## Capabilities

### New Capabilities

- `health-docs-skill`: The `health-docs` skill — analyze and document modes, subagent orchestration, handoff artifact contract, evidence-informed interview, documentation hierarchy, regulatory regime detection

### Modified Capabilities

- `healthcare-skill-library`: Add `health-docs` to the skill library registry and README

## Impact

- New skill in `skills/.experimental/health-docs/`
- New references: documentation hierarchy definition, regulatory dimension checklist, PHI signal detection patterns
- New example outputs: sample analysis report, sample `.health-docs/analysis.md` handoff artifact
- `README.md` updated to list new skill
- `DEVELOPER.md` updated to list new experimental skill
- `docs/skill-creation-guide.md` updated if subagent orchestration or two-mode design patterns warrant documentation
- No breaking changes to existing skills
