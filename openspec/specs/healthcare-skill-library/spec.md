## Purpose

Defines the healthcare skill library structure, curated skill catalog, example output expectations, and distribution model via the `dist` branch.

## Requirements

### Requirement: Repository organizes a healthcare skill library
The repository SHALL provide a canonical skill library structure for shared skills used to build healthcare technology software and digital health products.

#### Scenario: Canonical skill categories exist
- **WHEN** a maintainer inspects the repository structure
- **THEN** the repository exposes a dedicated `skills/` hierarchy for authored skills
- **THEN** the structure distinguishes between curated (`skills/.curated/`) and experimental (`skills/.experimental/`) skill groupings

#### Scenario: Curated skills cover initial healthcare categories
- **WHEN** the curated library is inspected
- **THEN** skills exist for FHIR API design, HIPAA code review, human factors design review, product discovery, and healthcare codebase refactoring
- **THEN** each skill includes `SKILL.md`, `agents/openai.yaml`, and supporting `references/` or `examples/` as appropriate

### Requirement: Healthcare system documentation skill is available
The repository SHALL provide a curated skill for healthcare system documentation coverage auditing and consolidation.

#### Scenario: Healthcare system documentation skill is available
- **WHEN** the curated skill library is inspected
- **THEN** a skill named `health-docs` exists in `skills/.curated/`
- **THEN** the skill includes `SKILL.md`, `agents/openai.yaml`, `references/` (doc-hierarchy, regime-signals, regulatory-mapping), and `examples/`

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

### Requirement: Curated skills support scoped invocation for composition
Curated skills that produce report-only output SHALL support a scoped invocation mode so that orchestrating skills can compose them with a pre-determined file scope and receive findings-only output.

#### Scenario: Skill is invoked in scoped mode
- **WHEN** an orchestrating skill invokes a report-only skill with the phrase "scoped review" and a pre-determined list of file paths
- **THEN** the invoked skill skips interactive scope confirmation
- **THEN** the invoked skill reviews only the provided files
- **THEN** the invoked skill returns a findings-only list without executive summary, coverage matrix, or open questions sections

#### Scenario: Scoped mode finding format is consistent
- **WHEN** a skill produces findings in scoped mode
- **THEN** each finding includes: ID (with skill-specific prefix), severity, category, file location with line reference, detail, and guideline reference
- **THEN** the format is consistent across all skills that support scoped invocation

#### Scenario: Standalone mode remains the default
- **WHEN** a skill is invoked without the "scoped review" phrase
- **THEN** the skill operates in standalone mode with interactive scope confirmation and full report output
- **THEN** existing standalone behavior is not changed

### Requirement: health-human-factors supports scoped invocation mode
The `health-human-factors` skill SHALL include a scoped invocation mode section in its SKILL.md.

#### Scenario: Scoped invocation is documented in SKILL.md
- **WHEN** a consumer or orchestrating skill reads the `health-human-factors` SKILL.md
- **THEN** an Invocation Modes section describes both standalone and scoped modes
- **THEN** the scoped mode specifies input (file list), behavior (skip scope confirmation), and output (findings with `HF-` prefix)

### Requirement: health-regulatory-review supports scoped invocation mode
The `health-regulatory-review` skill SHALL include a scoped invocation mode section in its SKILL.md.

#### Scenario: Scoped invocation is documented in SKILL.md
- **WHEN** a consumer or orchestrating skill reads the `health-regulatory-review` SKILL.md
- **THEN** an Invocation Modes section describes both standalone and scoped modes
- **THEN** the scoped mode specifies input (file list), behavior (skip scope confirmation), and output (findings with `H-` prefix)

### Requirement: Project context bootstrap skill is available in the experimental library
The repository SHALL include a `health-project-context` skill in `skills/.experimental/` for deriving reusable healthcare project context from repository evidence.

#### Scenario: Project context skill is discoverable
- **WHEN** a contributor inspects the skill library
- **THEN** a skill named `health-project-context` exists in `skills/.experimental/`
- **THEN** the skill is listed in README.md and DEVELOPER.md under experimental skills when implemented

### Requirement: Shared healthcare project context artifact is standardized
The healthcare skill library SHALL standardize `.health-context.yaml` as the reusable root-level artifact for shared project context.

#### Scenario: Artifact contract is discoverable
- **WHEN** a contributor inspects the project-context skill and related library documentation
- **THEN** `.health-context.yaml` is identified as the root-level context artifact
- **THEN** the documented shared fields are `jurisdiction`, `primary_audience`, and `project_stage`

#### Scenario: Downstream skills treat project context as reusable input
- **WHEN** a healthcare skill needs jurisdiction, audience, or project-stage context and `.health-context.yaml` is present
- **THEN** the skill may use the artifact as its default context source
- **THEN** the skill still allows override when task-specific evidence or user input conflicts with the stored values
