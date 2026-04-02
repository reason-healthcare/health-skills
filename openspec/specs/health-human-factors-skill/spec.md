## Purpose

Defines the `health-human-factors` curated skill as a report-only healthcare UI and workflow review grounded in patient-safety, usability, accessibility, and clinical data-display standards.

## Requirements

### Requirement: Skill exists in the curated skill library
The repository SHALL include a `health-human-factors` skill at `skills/.curated/health-human-factors/`.

#### Scenario: Skill directory is present
- **WHEN** a maintainer inspects `skills/.curated/`
- **THEN** a `health-human-factors/` directory exists containing `SKILL.md`, `agents/openai.yaml`, `references/style-guide.md`, and at least one example review report

### Requirement: Skill performs report-only healthcare design review
The `health-human-factors` skill SHALL inspect healthcare or EHR interfaces and produce findings without modifying code, designs, or documentation.

#### Scenario: Review covers healthcare-specific design categories
- **WHEN** the skill is invoked on screens, components, markup, or UI code
- **THEN** the review evaluates the provided artifacts against the healthcare design style guide categories
- **THEN** the skill prioritizes patient-safety and clinical usability risks over cosmetic improvements

#### Scenario: Non-assessable categories are not treated as passes
- **WHEN** the provided artifacts do not contain enough information to evaluate a review category
- **THEN** the skill marks that area as not assessable rather than compliant
- **THEN** the output distinguishes direct evidence from likely inferences and non-code dependencies

### Requirement: Skill supports standalone and scoped review modes
The `health-human-factors` skill SHALL support both standalone reviews and scoped reviews used by orchestrating skills.

#### Scenario: Standalone review produces the full report
- **WHEN** the skill is invoked directly without the phrase `scoped review`
- **THEN** the output includes an executive summary, scope, findings, category coverage matrix, positive observations, open questions, and standards basis

#### Scenario: Scoped review produces findings-only output
- **WHEN** the skill is invoked with the phrase `scoped review` and a pre-determined file list
- **THEN** the skill skips scope confirmation
- **THEN** the output is findings-only and each finding includes severity, category, file location, detail, guideline, and confidence
