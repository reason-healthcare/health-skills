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
- **THEN** skills exist for project context bootstrap, FHIR API design, FHIR modeling, healthcare documentation, compliance review, human factors design review, product discovery, and healthcare codebase refactoring
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

### Requirement: health-compliance-review supports scoped invocation mode
The `health-compliance-review` skill SHALL include a scoped invocation mode section in its SKILL.md.

#### Scenario: Scoped invocation is documented in SKILL.md
- **WHEN** a consumer or orchestrating skill reads the `health-compliance-review` SKILL.md
- **THEN** an Invocation Modes section describes both standalone and scoped modes
- **THEN** the scoped mode specifies input (file list), behavior (skip scope confirmation), and output (findings with `H-` prefix)

### Requirement: Project context bootstrap skill is available in the curated library
The repository SHALL include a `health-init` skill in `skills/.curated/` for deriving reusable healthcare project context from repository evidence.

#### Scenario: Project context skill is discoverable
- **WHEN** a contributor inspects the skill library
- **THEN** a skill named `health-init` exists in `skills/.curated/`
- **THEN** the skill is listed in README.md and DEVELOPER.md under curated skills

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

### Requirement: FHIR modeling skill is available in the curated library
The repository SHALL include a `health-fhir-modeling` skill in `skills/.curated/` for software developers who need to map domain concepts to FHIR R4 resources and understand profile compliance requirements.

#### Scenario: FHIR modeling skill is discoverable
- **WHEN** a developer inspects the skill library
- **THEN** a skill named `health-fhir-modeling` exists in `skills/.curated/`
- **THEN** the skill is listed in README.md and DEVELOPER.md under curated skills

### Requirement: Curated healthcare skills have main OpenSpec capability specs
The repository SHALL maintain a corresponding main OpenSpec capability spec for each curated healthcare skill.

#### Scenario: Curated capability spec is present
- **WHEN** a maintainer inspects `skills/.curated/`
- **THEN** each curated healthcare skill has a corresponding spec in `openspec/specs/`
- **THEN** the main spec documents the skill's purpose, key modes or workflows, and contract-level outputs

### Requirement: Jurisdiction-aware healthcare overlays are implemented within top-level skills
The healthcare skill library SHALL keep `health-docs`, `health-refactor`, and `health-compliance-review` as the canonical top-level curated skills while implementing jurisdiction-specific behavior through per-skill reference overlays.

#### Scenario: Top-level skills remain canonical
- **WHEN** a contributor inspects the curated healthcare skills affected by jurisdiction work
- **THEN** `health-docs`, `health-refactor`, and `health-compliance-review` remain the top-level skill directories
- **THEN** the library does not introduce standalone `-eu` variants of those skills for this change

#### Scenario: Reference overlays are discoverable
- **WHEN** a contributor inspects the affected skill directories
- **THEN** jurisdiction-specific reference material is available within each skill's `references/` directory where behavior diverges by market
- **THEN** the overlay material is documented as part of the skill's resources or examples

### Requirement: Healthcare skills share one jurisdiction overlay vocabulary
Curated healthcare skills that participate in jurisdiction-aware composition SHALL use a common overlay vocabulary of `us`, `eu`, `us+eu`, and `unclear`.

#### Scenario: Shared overlay vocabulary is used across skills
- **WHEN** `health-product-discovery`, `health-compliance-review`, `health-docs`, and `health-refactor` describe or persist jurisdiction context
- **THEN** they use the same overlay labels
- **THEN** orchestrating skills can pass the selected overlays to downstream skills without translating between incompatible terms

#### Scenario: Shared context artifact is reused
- **WHEN** `.health-context.yaml` is present in a target repository
- **THEN** participating healthcare skills may use the artifact as the default jurisdiction context source
- **THEN** each skill still allows override when task-specific evidence conflicts with the stored value
