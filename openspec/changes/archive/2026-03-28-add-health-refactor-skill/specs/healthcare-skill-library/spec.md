## MODIFIED Requirements

### Requirement: Curated skills cover initial healthcare categories
- **WHEN** the curated library is inspected
- **THEN** skills exist for FHIR API design, HIPAA code review, human factors design review, product discovery, and healthcare codebase refactoring
- **THEN** each skill includes `SKILL.md`, `agents/openai.yaml`, and supporting `references/` or `examples/` as appropriate

## ADDED Requirements

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

### Requirement: health-hipaa-review supports scoped invocation mode
The `health-hipaa-review` skill SHALL include a scoped invocation mode section in its SKILL.md.

#### Scenario: Scoped invocation is documented in SKILL.md
- **WHEN** a consumer or orchestrating skill reads the `health-hipaa-review` SKILL.md
- **THEN** an Invocation Modes section describes both standalone and scoped modes
- **THEN** the scoped mode specifies input (file list), behavior (skip scope confirmation), and output (findings with `H-` prefix)
