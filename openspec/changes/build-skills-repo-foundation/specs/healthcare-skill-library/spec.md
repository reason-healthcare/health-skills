## ADDED Requirements

### Requirement: Repository organizes a healthcare skill library
The repository SHALL provide a canonical skill library structure for shared skills used to build healthcare technology software and digital health products.

#### Scenario: Canonical skill categories exist
- **WHEN** a maintainer inspects the repository structure
- **THEN** the repository exposes a dedicated `skills/` hierarchy for authored skills
- **THEN** the structure distinguishes between at least curated and experimental skill groupings

### Requirement: Healthcare-oriented skills remain domain-specific
The repository SHALL treat healthcare software and product-development use cases as the primary domain for authored shared skills.

#### Scenario: New skill scope is evaluated
- **WHEN** a contributor proposes a new curated skill
- **THEN** the skill is evaluated against healthcare software, digital health product, or healthcare delivery workflow relevance
- **THEN** purely generic skills without domain relevance are not treated as first-class curated healthcare skills
