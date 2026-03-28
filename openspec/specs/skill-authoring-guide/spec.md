## Purpose

Defines the skill authoring guide covering the OpenSpec-based creation workflow, experimental testing, promotion to curated, validation, and distribution readiness criteria.

## Requirements

### Requirement: Repository defines a healthcare-focused authoring guide
The repository SHALL include a skill authoring guide for contributors creating shared healthcare-tech skills.

#### Scenario: New contributor starts authoring a skill
- **WHEN** the contributor follows the repository guide
- **THEN** the guide explains how to structure skill instructions, references, scripts, and assets
- **THEN** the guide explains how the repository expects healthcare relevance to be expressed

### Requirement: Authoring guide defines an OpenSpec-based creation workflow
The authoring guide SHALL define a skill creation workflow that uses OpenSpec for design before implementation.

#### Scenario: Contributor creates a new skill
- **WHEN** the contributor begins a new skill
- **THEN** the workflow starts with an OpenSpec proposal describing purpose, healthcare context, and output shape
- **THEN** the contributor scaffolds the skill directory after the proposal is accepted
- **THEN** the contributor continues through OpenSpec design, specs, and tasks before implementation

### Requirement: Authoring guide defines experimental testing workflow
The authoring guide SHALL explain how to test experimental skills before promotion.

#### Scenario: Contributor tests an experimental skill
- **WHEN** the contributor finishes drafting a skill in `skills/.experimental/`
- **THEN** the guide instructs them to compose skills into local agent trees and invoke the skill directly
- **THEN** the guide specifies what to verify: trigger behavior, workflow coherence, reference loading, and output contract conformance

### Requirement: Authoring guide defines promotion to curated
The authoring guide SHALL define the process for promoting an experimental skill to curated.

#### Scenario: Maintainer promotes a skill
- **WHEN** an experimental skill meets curated standards
- **THEN** the guide instructs moving the skill from `skills/.experimental/` to `skills/.curated/`
- **THEN** the guide requires validation, README update, optional overlay creation, and dist branch publication

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
