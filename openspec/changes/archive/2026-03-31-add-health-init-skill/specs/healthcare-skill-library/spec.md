## ADDED Requirements

### Requirement: Project context bootstrap skill is available in the experimental library
The repository SHALL include a `health-init` skill in `skills/.experimental/` for deriving reusable healthcare project context from repository evidence.

#### Scenario: Project context skill is discoverable
- **WHEN** a contributor inspects the skill library
- **THEN** a skill named `health-init` exists in `skills/.experimental/`
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
