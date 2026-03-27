## ADDED Requirements

### Requirement: Repository defines a healthcare-focused authoring guide
The repository SHALL include a skill authoring guide for contributors creating shared healthcare-tech skills.

#### Scenario: New contributor starts authoring a skill
- **WHEN** the contributor follows the repository guide
- **THEN** the guide explains how to structure skill instructions, references, scripts, and assets
- **THEN** the guide explains how the repository expects healthcare relevance to be expressed

### Requirement: Authoring guide defines validation workflow
The authoring guide SHALL define a standard validation workflow before a skill is treated as ready for distribution.

#### Scenario: Contributor prepares a skill for curated distribution
- **WHEN** the contributor finishes drafting a skill
- **THEN** the guide requires structural validation of required files and metadata
- **THEN** the guide requires checking compatibility with the repository's packaging and overlay rules

### Requirement: Authoring guide defines distribution readiness
The authoring guide SHALL define what makes a skill ready to be distributed as a shared skill.

#### Scenario: Maintainer reviews a proposed curated skill
- **WHEN** the maintainer evaluates the skill for inclusion
- **THEN** the guide provides explicit criteria for readiness such as domain fit, structural completeness, and validation status
- **THEN** the maintainer can distinguish draft or experimental skills from curated distributable skills

