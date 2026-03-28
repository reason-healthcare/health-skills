## MODIFIED Requirements

### Requirement: Curated skills cover initial healthcare categories
The repository SHALL provide curated skills covering FHIR API design, HIPAA code review, human factors design review, product discovery, and healthcare codebase refactoring.

#### Scenario: Curated skills cover initial healthcare categories
- **WHEN** the curated skill library is inspected
- **THEN** skills exist for FHIR API design, HIPAA code review, human factors design review, product discovery, and healthcare codebase refactoring
- **THEN** each skill includes `SKILL.md`, `agents/openai.yaml`, and supporting `references/` or `examples/` as appropriate

### Requirement: Healthcare system documentation skill is available
The repository SHALL provide a skill for healthcare system documentation coverage auditing and consolidation.

#### Scenario: Healthcare system documentation skill is available
- **WHEN** the skill library is inspected
- **THEN** a skill named `health-docs` exists in `skills/.experimental/`
- **THEN** the skill includes `SKILL.md`, `agents/openai.yaml`, `references/` (doc-hierarchy, regime-signals, regulatory-mapping), and `examples/`
- **NOTE** The skill graduates to `skills/.curated/` once validated in production use; it is not distributed via the `dist` branch until promoted

#### Scenario: New skill scope is evaluated
- **WHEN** a contributor proposes a new curated skill
- **THEN** the skill is evaluated against healthcare software, digital health product, or healthcare delivery workflow relevance
- **THEN** purely generic skills without domain relevance are not treated as first-class curated healthcare skills
