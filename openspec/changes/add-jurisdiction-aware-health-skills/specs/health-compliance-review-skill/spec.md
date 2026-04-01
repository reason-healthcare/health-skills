## ADDED Requirements

### Requirement: Skill performs evidence-backed jurisdiction-aware regulatory review
The `health-compliance-review` skill SHALL produce a report-only healthcare compliance review that selects `us`, `eu`, `us+eu`, or `unclear` overlays from repository evidence and confirmed context before evaluating control areas.

#### Scenario: Shared project context informs overlay selection
- **WHEN** `.health-context.yaml` exists and contains a jurisdiction value
- **THEN** the skill uses that value as the default overlay proposal
- **THEN** the skill re-checks repository evidence and allows override when the stored value appears stale, incomplete, or in conflict with the task context

#### Scenario: Overlay selection is surfaced with evidence
- **WHEN** the skill proposes a jurisdiction overlay set
- **THEN** it presents the proposed overlay or overlays with concrete code, configuration, or documentation evidence
- **THEN** it allows the user to correct the selection before continuing when confidence is low or evidence is mixed

#### Scenario: Multi-market repositories use concurrent overlays
- **WHEN** the system appears to operate in both US and EU contexts
- **THEN** the skill applies both US and EU overlays in the same review
- **THEN** the final report separates shared findings from US-specific and EU-specific findings

### Requirement: Skill defines explicit US and EU regulatory overlays in references
The `health-compliance-review` skill SHALL express jurisdiction-specific regulatory heuristics through reference overlays owned by the skill.

#### Scenario: US regulatory overlay remains available
- **WHEN** a contributor inspects the skill references
- **THEN** US-oriented healthcare privacy, security, and regulatory review guidance remains available as explicit reference material rather than only as implicit HIPAA-centric defaults

#### Scenario: EU regulatory overlay is available
- **WHEN** a contributor inspects the skill references
- **THEN** EU-oriented healthcare regulatory review guidance exists as explicit reference material
- **THEN** that overlay is available to both standalone invocations and orchestrating skills using scoped mode

### Requirement: EU overlay covers major healthcare regulatory applicability signals
The EU overlay for `health-compliance-review` SHALL identify the major EU-oriented regulatory and assurance regimes relevant to healthcare software systems.

#### Scenario: Privacy and health-data regimes are evaluated
- **WHEN** the EU overlay is applied
- **THEN** the skill evaluates GDPR and EHDS-oriented health-data handling signals where repository evidence suggests they are relevant
- **THEN** the skill distinguishes confirmed code or configuration evidence from policy or legal unknowns

#### Scenario: Device and AI regimes are evaluated
- **WHEN** the EU overlay is applied to software with device-like or AI-enabled clinical behavior
- **THEN** the skill evaluates MDR/IVDR and AI Act applicability signals where relevant
- **THEN** the skill notes when classification, intended use, or human oversight questions require human follow-up

#### Scenario: Cybersecurity regimes are evaluated
- **WHEN** the EU overlay is applied to operational healthcare systems or digital infrastructure
- **THEN** the skill evaluates NIS2-style cybersecurity applicability signals where relevant
- **THEN** the report identifies where technical evidence is insufficient to confirm organizational obligations

### Requirement: Scoped invocation remains available for orchestrating skills
The `health-compliance-review` skill SHALL continue to support scoped invocation mode for orchestrating skills while preserving overlay-aware review behavior.

#### Scenario: Scoped review respects pre-determined file list
- **WHEN** an orchestrating skill invokes `health-compliance-review` in scoped mode with a file list
- **THEN** the skill skips interactive scope confirmation
- **THEN** the skill evaluates only the provided files against the active jurisdiction overlays

#### Scenario: Scoped review output remains findings-only
- **WHEN** the skill operates in scoped mode
- **THEN** the output remains a findings-only list suitable for composition
- **THEN** each finding continues to include an ID, severity, category, file location, detail, and guideline reference
