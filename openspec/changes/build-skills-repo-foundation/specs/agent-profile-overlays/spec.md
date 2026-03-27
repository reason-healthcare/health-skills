## ADDED Requirements

### Requirement: Repository supports optional agent-specific overlays
The repository SHALL support optional overlays that customize a base skill for a specific agent without duplicating the full skill.

#### Scenario: Maintainer needs agent-specific customization
- **WHEN** a maintainer needs to adjust metadata or instructions for one agent
- **THEN** the maintainer can add an overlay under `profiles/<agent>/<skill>/`
- **THEN** the base skill remains unchanged for other agents

### Requirement: Overlay application is deterministic
The repository SHALL define deterministic composition rules for applying overlays to base skills.

#### Scenario: Build process composes a profiled skill
- **WHEN** the composition workflow runs for a base skill with an overlay
- **THEN** the resulting agent-specific skill is produced from the same base skill and overlay inputs every time
- **THEN** the workflow applies only supported overlay file types and locations

### Requirement: Overlay validation prevents unsupported drift
The repository SHALL validate overlays against their corresponding base skill before distribution.

#### Scenario: Overlay references a missing base skill
- **WHEN** validation runs on an overlay
- **THEN** validation fails if the referenced base skill does not exist
- **THEN** validation fails if the overlay uses unsupported files or paths

