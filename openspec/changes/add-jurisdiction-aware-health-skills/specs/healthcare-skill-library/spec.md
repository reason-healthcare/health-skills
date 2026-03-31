## ADDED Requirements

### Requirement: Jurisdiction-aware healthcare overlays are implemented within top-level skills
The healthcare skill library SHALL keep `health-docs`, `health-refactor`, and `health-regulatory-review` as the canonical top-level curated skills while implementing jurisdiction-specific behavior through per-skill reference overlays.

#### Scenario: Top-level skills remain canonical
- **WHEN** a contributor inspects the curated healthcare skills affected by jurisdiction work
- **THEN** `health-docs`, `health-refactor`, and `health-regulatory-review` remain the top-level skill directories
- **THEN** the library does not introduce standalone `-eu` variants of those skills for this change

#### Scenario: Reference overlays are discoverable
- **WHEN** a contributor inspects the affected skill directories
- **THEN** jurisdiction-specific reference material is available within each skill's `references/` directory where behavior diverges by market
- **THEN** the overlay material is documented as part of the skill's resources or examples

### Requirement: Healthcare skills share one jurisdiction overlay vocabulary
Curated healthcare skills that participate in jurisdiction-aware composition SHALL use a common overlay vocabulary of `us`, `eu`, `us+eu`, and `unclear`.

#### Scenario: Shared overlay vocabulary is used across skills
- **WHEN** `health-product-discovery`, `health-regulatory-review`, `health-docs`, and `health-refactor` describe or persist jurisdiction context
- **THEN** they use the same overlay labels
- **THEN** orchestrating skills can pass the selected overlays to downstream skills without translating between incompatible terms

#### Scenario: Shared context artifact is reused
- **WHEN** `.health-context.yaml` is present in a target repository
- **THEN** participating healthcare skills may use the artifact as the default jurisdiction context source
- **THEN** each skill still allows override when task-specific evidence conflicts with the stored value
