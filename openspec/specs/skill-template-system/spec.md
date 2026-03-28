## Purpose

Defines the standard skill template for initializing new skills with progressive disclosure and portable metadata conventions.

## Requirements

### Requirement: Repository provides a standard skill template
The repository SHALL provide a reusable template for initializing new skills.

#### Scenario: Contributor initializes a new skill
- **WHEN** a contributor scaffolds a new skill
- **THEN** the generated structure includes a `SKILL.md` file
- **THEN** the generated structure includes `agents/openai.yaml`
- **THEN** the generated structure supports optional `scripts/`, `references/`, and `assets/` directories

### Requirement: Template supports progressive disclosure
The standard skill template SHALL support concise core instructions with optional deeper resources loaded only when needed.

#### Scenario: Contributor adds detailed domain guidance
- **WHEN** the skill requires lengthy healthcare-specific references or documentation
- **THEN** the contributor can place that material in `references/` rather than overloading `SKILL.md`
- **THEN** the core `SKILL.md` remains focused on triggering context and workflow guidance

### Requirement: Template enforces portable metadata conventions
The standard skill template SHALL enforce metadata conventions that are portable across supported agents.

#### Scenario: Contributor validates a scaffolded skill
- **WHEN** validation runs against a templated skill
- **THEN** the skill name is checked for valid kebab-case naming
- **THEN** required frontmatter fields such as `name` and `description` are present
