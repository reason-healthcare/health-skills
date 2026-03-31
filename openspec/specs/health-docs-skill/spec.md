## Purpose

Defines the `health-docs` skill — a two-mode healthcare documentation orchestration skill that audits documentation coverage against a canonical seven-dimension hierarchy, detects applicable regulatory regimes from codebase signals, and consolidates existing documentation into a structured, maintainable form.

## Requirements

### Requirement: Skill supports analyze mode for coverage auditing
The skill SHALL scan a target repository, produce a structured coverage audit across seven documentation dimensions, and write `.health-docs/analysis.md`. No other repository files are written.

#### Scenario: Analyze mode runs broad scan first
- **WHEN** user invokes analyze mode
- **THEN** the skill inventories all markdown files, README files at every level, AGENTS.md and other agent instruction files, and CI/CD configs in the repository
- **THEN** the skill scans for PHI, ONC, and FDA SaMD regime signals in code and configuration
- **THEN** no files are written to the target repository during this pass (`.health-docs/analysis.md` is written after Pass 3, not during Pass 1)

#### Scenario: Analyze mode delegates to available subagents in parallel
- **WHEN** regime signals are detected and relevant subagents are installed
- **THEN** `$health-regulatory-review` is invoked in scoped mode if PHI signals are found
- **THEN** `$health-fhir-api-design` is invoked in scoped mode if FHIR resource types, SMART on FHIR auth patterns, EHR vendor SDK imports, or USCDI field references are found
- **THEN** `$health-human-factors` is invoked in scoped mode if UI source files are found (`.html`, `.tsx`, `.jsx`, `.vue`, `.erb`, or directories matching `app/views/`, `src/components/`, `templates/`)
- **THEN** subagent invocations that do not depend on each other are dispatched in parallel

#### Scenario: Analyze mode degrades gracefully without subagents
- **WHEN** a relevant subagent is not installed
- **THEN** the skill performs direct analysis for that dimension
- **THEN** the coverage artifact notes reduced confidence for that dimension

#### Scenario: Analyze mode writes structured handoff artifact
- **WHEN** analysis is complete
- **THEN** the skill writes `.health-docs/analysis.md` to the target repository
- **THEN** the artifact contains a structured coverage matrix with status, source locations, and regulatory class per dimension
- **THEN** the artifact contains a human-readable narrative with findings and source citations
- **THEN** `required` fields in the coverage matrix are left null, to be populated by document mode

### Requirement: Coverage matrix enumerates all dimensions
The skill SHALL include every dimension from the canonical hierarchy in the coverage matrix — including covered dimensions — so document mode can present a complete inclusion/skip list to the user.

#### Scenario: Coverage status uses five states
- **WHEN** assessing a documentation dimension
- **THEN** the skill assigns one of: covered (exists, current, complete), partial (exists but stale or incomplete), conflict (multiple sources describe the same topic with contradictory content), absent (no evidence found), or absent-required (absent and mandated by regulation)
- **THEN** partial findings include what was found and what is missing
- **THEN** conflict findings include all source locations and a description of what contradicts

#### Scenario: External links are flagged as unverifiable
- **WHEN** a documentation source is an external link (Confluence, Notion, GDrive)
- **THEN** the skill records the link as "unverifiable — content not assessed"
- **THEN** coverage for that dimension is marked partial, not covered

### Requirement: Regulatory regime is detected from codebase signals
The skill SHALL identify applicable regulatory regimes (HIPAA, ONC, FDA SaMD) from code and configuration evidence before asking the user any questions.

#### Scenario: PHI signals trigger HIPAA regime proposal
- **WHEN** the skill finds PHI field names (ssn, dob, mrn, npi, patient_id), PHI-bearing model names, FHIR resource types, HL7 references, or HIPAA-related comments in code
- **THEN** the skill proposes HIPAA as an applicable regime with high confidence
- **THEN** the skill lists the specific evidence found

#### Scenario: FHIR and EHR signals trigger ONC regime proposal
- **WHEN** the skill finds SMART on FHIR auth patterns, USCDI field references, EHR vendor SDKs, or FHIR bulk export operations
- **THEN** the skill proposes ONC as an applicable regime with medium confidence

#### Scenario: AI/ML clinical signals trigger FDA SaMD regime proposal
- **WHEN** the skill finds ML model loading, clinical scoring functions, diagnostic language in docs, or clinical terminology code lookups driving recommendations
- **THEN** the skill proposes FDA SaMD as an applicable regime and notes it for user confirmation

### Requirement: Skill supports document mode for consolidation and gap-filling
The skill SHALL consolidate existing documentation into the target hierarchy and draft new content for required gaps, after confirming a requirements profile with the user.

#### Scenario: Document mode reads handoff artifact before any interaction
- **WHEN** user invokes document mode
- **THEN** the skill reads `.health-docs/analysis.md` if it exists
- **THEN** the skill presents evidence-backed regime findings before asking any questions

#### Scenario: Document mode conducts evidence-informed interview
- **WHEN** document mode presents findings to the user
- **THEN** the interview requires at most three confirmation steps: regime confirmation, dimension inclusion review, and target directory confirmation
- **THEN** each confirmation presents evidence found and proposed action, not open-ended questions
- **THEN** the user can override any proposed inclusion or exclusion

#### Scenario: Document mode writes requirements profile back to artifact
- **WHEN** interview is complete
- **THEN** the skill writes the confirmed requirements profile (required: true/false per dimension) into `.health-docs/analysis.md`
- **THEN** subsequent document mode runs read the stored profile and skip the interview unless overridden

#### Scenario: Document mode presents pre-flight plan before writing
- **WHEN** requirements profile is confirmed
- **THEN** the skill shows a pre-flight plan listing: files to consolidate (with source locations), merges to perform (with conflicts flagged), new files to draft, and files to skip
- **THEN** no files are written until the user confirms the pre-flight plan

#### Scenario: Document mode consolidates before drafting
- **WHEN** executing the confirmed plan
- **THEN** existing content is copied to target locations (originals are flagged in place, not deleted) before any new content is drafted
- **THEN** when multiple sources cover the same topic, content is merged and conflicts are flagged in the output file for human resolution
- **THEN** any `comply/` target file produced by consolidation or merging carries the same `⚠ REQUIRES HUMAN REVIEW` header as drafted comply/ files
- **THEN** new content is drafted only for required dimensions with no existing source

#### Scenario: Regulatory-class documents are marked for human review
- **WHEN** document mode writes any content — consolidated, merged, or drafted — for comply/hipaa, comply/onc, or comply/fda dimensions
- **THEN** each target file carries a visible warning that it requires human review before serving as compliance evidence
- **THEN** the `.health-docs/analysis.md` requirements profile records all files requiring human review

### Requirement: Handoff artifact persists across mode invocations
The skill SHALL maintain `.health-docs/analysis.md` as a durable artifact that records coverage state, requirements profile, and run history.

#### Scenario: Run record is appended on each document mode execution
- **WHEN** document mode completes
- **THEN** a dated run record is written to `.health-docs/runs/YYYY-MM-DD.md` describing what was consolidated, merged, drafted, and skipped

#### Scenario: Stale artifact is detected and flagged
- **WHEN** document mode reads an existing artifact that is more than 90 days old
- **THEN** the skill notifies the user that the analysis may be stale and recommends re-running analyze mode before proceeding
