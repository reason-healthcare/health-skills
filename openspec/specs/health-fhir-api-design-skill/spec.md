## Purpose

Defines the `health-fhir-api-design` curated skill for designing and reviewing FHIR R4 API interactions, including searches, operations, validation patterns, and workflow coordination.

## Requirements

### Requirement: Skill exists in the curated skill library
The repository SHALL include a `health-fhir-api-design` skill at `skills/.curated/health-fhir-api-design/`.

#### Scenario: Skill directory is present
- **WHEN** a maintainer inspects `skills/.curated/`
- **THEN** a `health-fhir-api-design/` directory exists containing `SKILL.md`, `agents/openai.yaml`, `references/fhir-patterns.md`, and at least one example output

### Requirement: Design mode produces concrete FHIR R4 interaction guidance
In design mode, the skill SHALL translate user requirements into specific FHIR R4 interaction patterns with concrete examples and trade-offs.

#### Scenario: User asks for a FHIR interaction design
- **WHEN** the user describes data access, write, or workflow-coordination requirements
- **THEN** the skill maps the request to R4 resources, search patterns, operations, validation behavior, or workflow interactions
- **THEN** the skill includes concrete HTTP examples rather than only abstract descriptions
- **THEN** the skill states trade-offs and server-support variability where relevant

### Requirement: Review and scoped review modes detect API design issues
The skill SHALL support both direct review and scoped review of existing FHIR API designs.

#### Scenario: User reviews an existing API design
- **WHEN** the user provides existing queries, operation usage, or API design snippets
- **THEN** the skill evaluates correctness and completeness
- **THEN** the output lists issues with severity and corrective guidance

#### Scenario: Scoped review is used by orchestrating skills
- **WHEN** the skill is invoked with the phrase `scoped review` and a pre-determined file list
- **THEN** the skill skips interactive clarification
- **THEN** the output is findings-only and each finding includes severity, category, file location, detail, guideline, and confidence

### Requirement: Skill remains within FHIR R4 design scope
The skill SHALL constrain its recommendations to FHIR R4 API design and SHALL not silently drift into profile authoring or non-R4 guidance.

#### Scenario: R5 or non-standard features are relevant
- **WHEN** a newer-version feature or non-standard server capability would improve the design
- **THEN** the skill explicitly labels that dependency or version difference
- **THEN** it still provides the closest FHIR R4-compatible primary recommendation
