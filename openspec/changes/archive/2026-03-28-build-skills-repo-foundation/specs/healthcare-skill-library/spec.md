## ADDED Requirements

### Requirement: Repository organizes a healthcare skill library
The repository SHALL provide a canonical skill library structure for shared skills used to build healthcare technology software and digital health products.

#### Scenario: Canonical skill categories exist
- **WHEN** a maintainer inspects the repository structure
- **THEN** the repository exposes a dedicated `skills/` hierarchy for authored skills
- **THEN** the structure distinguishes between curated (`skills/.curated/`) and experimental (`skills/.experimental/`) skill groupings

#### Scenario: Curated skills cover initial healthcare categories
- **WHEN** the curated library is inspected
- **THEN** skills exist for FHIR API design, HIPAA code review, human factors design review, and product discovery
- **THEN** each skill includes `SKILL.md`, `agents/openai.yaml`, and supporting `references/` or `examples/` as appropriate

### Requirement: Healthcare-oriented skills remain domain-specific
The repository SHALL treat healthcare software and product-development use cases as the primary domain for authored shared skills.

#### Scenario: New skill scope is evaluated
- **WHEN** a contributor proposes a new curated skill
- **THEN** the skill is evaluated against healthcare software, digital health product, or healthcare delivery workflow relevance
- **THEN** purely generic skills without domain relevance are not treated as first-class curated healthcare skills

### Requirement: Skills include example outputs
Curated skills SHOULD include example output artifacts that demonstrate the expected report or design shape.

#### Scenario: Consumer evaluates a skill
- **WHEN** a consumer reviews a curated skill before use
- **THEN** the `examples/` directory contains a representative sample output matching the output contract in `SKILL.md`

### Requirement: Skills are distributed via a dedicated branch
The repository SHALL publish curated skills to a `dist` branch for consumer installation.

#### Scenario: Consumer installs skills
- **WHEN** a consumer runs `npx skills add` against the repository
- **THEN** installation targets the `dist` branch containing only composed curated skills
- **THEN** the `dist` branch does not contain experimental skills, scripts, or development artifacts
