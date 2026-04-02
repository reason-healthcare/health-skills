## ADDED Requirements

### Requirement: Skill detects jurisdiction context before regulatory composition
The `health-refactor` skill SHALL determine the applicable healthcare jurisdiction overlays before composing regulatory analysis.

#### Scenario: Shared project context seeds routing
- **WHEN** `.health-context.yaml` exists and contains a jurisdiction value
- **THEN** the skill uses that value as the initial routing proposal
- **THEN** the skill checks the bounded file scope for confirming or conflicting evidence before dispatching downstream analysis

#### Scenario: Proposed overlays are surfaced before routing
- **WHEN** the skill has enough evidence to choose `us`, `eu`, `us+eu`, or `unclear`
- **THEN** it reports the proposed overlay set with brief evidence in the plan output
- **THEN** it allows user correction when the evidence is mixed or low-confidence

## MODIFIED Requirements

### Requirement: Skill orchestrates three analysis sub-agents
The skill SHALL dispatch three analysis passes over the resolved file set: a refactoring analysis, a human-factors analysis, and a healthcare regulatory analysis selected from evidence-backed jurisdiction overlays.

#### Scenario: Refactoring analysis composes baseline skill with healthcare reference
- **WHEN** the file set is resolved
- **THEN** the skill first delegates to a general-purpose refactoring skill (e.g., `$refactor`) if available, or applies standard refactoring heuristics directly, producing findings with IDs prefixed `R-`
- **THEN** the skill loads `references/refactor-patterns.md` Part 1 (healthcare-specific patterns) and produces additional `R-` findings
- **THEN** the skill applies Part 2 (healthcare overrides) to adjust standard findings — suppressing false positives where clinical context justifies the structure and escalating findings with clinical safety implications

#### Scenario: Human-factors analysis composes health-human-factors skill
- **WHEN** the file set is resolved
- **THEN** the skill invokes `health-human-factors` in scoped invocation mode, passing the file list
- **THEN** the human-factors analysis produces findings with IDs prefixed `HF-`

#### Scenario: Regulatory analysis composes health-compliance-review skill
- **WHEN** the file set is resolved and jurisdiction overlays have been selected
- **THEN** the skill invokes `health-compliance-review` in scoped invocation mode, passing the file list and the active `us`, `eu`, or `us+eu` overlays
- **THEN** the regulatory analysis produces findings with IDs prefixed `H-`

#### Scenario: Analyses run in defined order
- **WHEN** the three analyses are dispatched
- **THEN** the refactoring analysis runs first, followed by human-factors, followed by healthcare regulatory analysis
