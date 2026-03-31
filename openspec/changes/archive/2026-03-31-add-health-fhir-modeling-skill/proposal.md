## Why

Software developers building healthcare apps know their domain — room transfers, prior authorizations, care gaps — but not how those concepts map to FHIR. The existing `health-fhir-api-design` skill covers exchange patterns and REST operations but assumes the developer already knows which resources and profiles to use. That upstream modeling knowledge gap has no skill covering it.

## What Changes

- New skill `health-fhir-modeling` targeting app developers who need to select the right FHIR base resources for domain concepts, understand profile constraints they will encounter (US Core, QI Core), model relationships between resources, use extensions correctly without inventing unnecessary ones, and apply terminology bindings in practical terms (LOINC for observations, SNOMED for clinical concepts, binding strength implications).
- Skill operates in two modes: **Model** (map a domain concept to FHIR resources) and **Review** (evaluate an existing FHIR model for correctness and US Core compliance).
- Scope is deliberately constrained to reading and applying existing FHIR models — not authoring new profiles or publishing StructureDefinitions.

## Capabilities

### New Capabilities

- `health-fhir-modeling-skill`: A skill for software developers that guides FHIR resource selection, relationship modeling, profile compliance checks, extension usage, and practical terminology application. Outputs annotated example instances and mapping rationale, not StructureDefinition artifacts.

### Modified Capabilities

- `healthcare-skill-library`: Register the new skill in the library inventory.

## Impact

- New skill directory added at `skills/.experimental/health-fhir-modeling/`
- README and DEVELOPER.md updated with new skill entry
- `openspec/specs/healthcare-skill-library/spec.md` updated to include new skill
