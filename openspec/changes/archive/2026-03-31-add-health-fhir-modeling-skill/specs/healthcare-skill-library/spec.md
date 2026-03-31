## ADDED Requirements

### Requirement: FHIR modeling skill is available in the experimental library
The repository SHALL include a `health-fhir-modeling` skill in `skills/.experimental/` for software developers who need to map domain concepts to FHIR R4 resources and understand profile compliance requirements.

#### Scenario: FHIR modeling skill is discoverable
- **WHEN** a developer inspects the skill library
- **THEN** a skill named `health-fhir-modeling` exists in `skills/.experimental/`
- **THEN** the skill is listed in README.md and DEVELOPER.md under experimental skills
