## Purpose

Defines the `health-refactor` curated skill: a plan-only orchestrator that resolves a bounded file scope, dispatches three analysis sub-agents (refactoring, human factors, HIPAA), and produces a prioritized refactor plan with findings and a checklist. The skill never modifies code.

## Requirements

### Requirement: Skill accepts a context mode that resolves to a bounded file set
The skill SHALL require exactly one context mode as input. Each mode resolves to a list of files that defines the analysis boundary.

#### Scenario: Git range context resolves changed files
- **WHEN** the user provides a git range context (e.g., `HEAD~5..HEAD`, `origin/main..HEAD`)
- **THEN** the skill resolves the file set by running `git diff --name-only <range>`
- **THEN** only files that currently exist in the working tree are included
- **THEN** the resolved file list is reported in the plan output under a Scope section

#### Scenario: File area context resolves directory contents
- **WHEN** the user provides a file area context (e.g., `app/dashboard`, `src/services/patient`)
- **THEN** the skill resolves the file set to all files under that path, respecting `.gitignore`
- **THEN** the resolved file list is reported in the plan output under a Scope section

#### Scenario: Symbol/dependency context resolves direct imports and importers
- **WHEN** the user provides a symbol or file name context (e.g., `PatientService`, `MedList.tsx`)
- **THEN** the skill locates the file containing that symbol
- **THEN** the skill resolves direct imports (files the root file imports) and direct importers (files that import the root file)
- **THEN** transitive dependencies beyond direct imports are NOT resolved
- **THEN** the resolved file list and dependency graph are reported in the plan output under a Scope section

#### Scenario: No context mode provided
- **WHEN** the user invokes the skill without specifying a context mode
- **THEN** the skill asks the user to provide one of the three supported context modes before proceeding

#### Scenario: Resolved file set is too large
- **WHEN** the resolved file set exceeds a practical threshold
- **THEN** the skill warns the user and suggests narrowing the scope before proceeding

### Requirement: Skill orchestrates three analysis sub-agents
The skill SHALL dispatch three analysis passes over the resolved file set: a refactoring analysis, a human-factors analysis, and a HIPAA analysis.

#### Scenario: Refactoring analysis composes baseline skill with healthcare reference
- **WHEN** the file set is resolved
- **THEN** the skill first delegates to a general-purpose refactoring skill (e.g., `$refactor`) if available, or applies standard refactoring heuristics directly, producing findings with IDs prefixed `R-`
- **THEN** the skill loads `references/refactor-patterns.md` Part 1 (healthcare-specific patterns) and produces additional `R-` findings
- **THEN** the skill applies Part 2 (healthcare overrides) to adjust standard findings — suppressing false positives where clinical context justifies the structure and escalating findings with clinical safety implications

#### Scenario: Human-factors analysis composes health-human-factors skill
- **WHEN** the file set is resolved
- **THEN** the skill invokes `health-human-factors` in scoped invocation mode, passing the file list
- **THEN** the human-factors analysis produces findings with IDs prefixed `HF-`

#### Scenario: HIPAA analysis composes health-hipaa-review skill
- **WHEN** the file set is resolved
- **THEN** the skill invokes `health-hipaa-review` in scoped invocation mode, passing the file list
- **THEN** the HIPAA analysis produces findings with IDs prefixed `H-`

#### Scenario: Analyses run in defined order
- **WHEN** the three analyses are dispatched
- **THEN** the refactoring analysis runs first, followed by human-factors, followed by HIPAA

### Requirement: Skill produces a plan-only output with findings and checklist
The skill SHALL produce a text-based refactor plan and SHALL NOT modify any code, configuration, or documentation.

#### Scenario: Plan output contains a scope section
- **WHEN** the plan is generated
- **THEN** the output includes a Scope section listing the context mode used, the resolved file set, and (for symbol mode) the dependency graph

#### Scenario: Plan output contains findings from all three sub-agents
- **WHEN** findings exist from any sub-agent
- **THEN** each finding includes: ID (prefixed by source), severity (critical / major / minor), category, file location with line reference, detail describing what was observed, and the guideline or pattern that applies

#### Scenario: Plan output contains a prioritized refactor checklist
- **WHEN** findings have been collected
- **THEN** the plan includes a Refactor Checklist table with columns: number, action, finding references, and status checkbox
- **THEN** checklist items are ordered by priority: safety-critical (P1) first, then structural (P2), then improvement (P3)
- **THEN** each checklist item references one or more finding IDs

#### Scenario: Plan output contains risks and notes
- **WHEN** the plan is generated
- **THEN** the plan includes a Risks and Notes section with caveats, execution dependencies between checklist items, and potential side effects of the suggested refactoring actions

#### Scenario: No findings from a sub-agent
- **WHEN** a sub-agent produces zero findings for the file set
- **THEN** the plan notes that sub-agent found no issues and does not include an empty findings section for it

### Requirement: Embedded refactoring reference covers healthcare-aware patterns
The skill SHALL include a `references/refactor-patterns.md` file organized in two parts: healthcare-specific patterns and healthcare overrides to standard refactoring.

#### Scenario: Reference Part 1 covers healthcare-specific refactoring patterns
- **WHEN** the reference is loaded during refactoring analysis
- **THEN** Part 1 provides full pattern entries for concerns unique to healthcare software: clinical terminology duplication, FHIR resource handling, clinical data formatting centralization, audit trail integrity during refactoring, tenant isolation risks, clinical domain naming, and error handling in clinical paths

#### Scenario: Reference Part 2 provides healthcare overrides to standard refactoring
- **WHEN** standard refactoring heuristics identify a code smell
- **THEN** Part 2 provides clinical nuances that modify how to apply them: long method / god class (do not flag cohesive clinical workflows), dead code and feature flags (verify clinical flags are not safety gates), test coverage (clinical logic requires tests as a prerequisite), code modularity (dependency direction enables safe FHIR/EHR evolution), and inline documentation (document clinical rationale and source authority for magic numbers)

#### Scenario: Reference does not duplicate generic refactoring guidance
- **WHEN** the reference content is evaluated
- **THEN** standard refactoring patterns (extract method, rename variable, reduce complexity) are NOT included — they are handled by the baseline refactoring skill or the agent's innate knowledge
- **THEN** the reference covers only what is unique to healthcare or where clinical context overrides standard heuristics

### Requirement: Skill includes example plan output for each context mode
The skill SHALL include three example plan files demonstrating the output contract for each context mode.

#### Scenario: Git range example plan exists
- **WHEN** a consumer reviews the skill's examples directory
- **THEN** `examples/example-plan-git-range.md` demonstrates a plan produced from a git range context including scope, findings from all three sub-agents, a prioritized checklist, and risks

#### Scenario: File area example plan exists
- **WHEN** a consumer reviews the skill's examples directory
- **THEN** `examples/example-plan-file-area.md` demonstrates a plan produced from a file area context including scope, findings from all three sub-agents, a prioritized checklist, and risks

#### Scenario: Symbol/dependency example plan exists
- **WHEN** a consumer reviews the skill's examples directory
- **THEN** `examples/example-plan-symbol.md` demonstrates a plan produced from a symbol/dependency context including scope with dependency graph, findings from all three sub-agents, a prioritized checklist, and risks

### Requirement: Skill is scaffolded via init_skill.py
The skill directory SHALL be initialized using `scripts/init_skill.py` before customization.

#### Scenario: Scaffold produces base structure
- **WHEN** the scaffold command is run with `--group .curated --include references examples`
- **THEN** the skill directory is created at `skills/.curated/health-refactor/` with `SKILL.md`, `agents/openai.yaml`, `references/`, and `examples/`
- **THEN** the generated `SKILL.md` and `agents/openai.yaml` are starting points that are replaced with full skill content during implementation
