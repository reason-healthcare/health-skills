## Purpose

Defines the `health-product-discovery` curated skill as a jurisdiction-aware healthcare discovery workflow that keeps a neutral base flow and applies explicit market overlays when repository or user context indicates US, EU, or concurrent applicability.

## Requirements

### Requirement: Skill supports explicit explore and document modes
The `health-product-discovery` skill SHALL support an exploratory mode for stress-testing ideas and a document mode for producing a structured planning artifact.

#### Scenario: Explore mode challenges assumptions before solutioning
- **WHEN** the user is early in problem framing or market validation
- **THEN** the skill uses an exploratory workflow that surfaces incentive conflicts, adoption barriers, workflow burden, and evidence gaps before converging on a solution

#### Scenario: Document mode produces a reusable planning artifact
- **WHEN** the user asks for a structured discovery output or planning document
- **THEN** the skill produces a document-shaped artifact rather than only conversational guidance
- **THEN** the document records the active market assumptions, key risks, and open validation questions

### Requirement: Skill supports jurisdiction-aware healthcare product discovery
The `health-product-discovery` skill SHALL keep its core discovery workflow jurisdiction-neutral and SHALL apply regional market overlays when repository or user context indicates `us`, `eu`, or `us+eu` applicability.

#### Scenario: Discovery defaults to neutral base flow
- **WHEN** the skill is invoked without evidence favoring a specific market overlay
- **THEN** the skill uses its base discovery workflow for problem framing, stakeholder mapping, workflow analysis, adoption readiness, and solution shaping
- **THEN** the skill does not silently assume US reimbursement, procurement, or buyer dynamics as the default market model

#### Scenario: Shared project context seeds overlay selection
- **WHEN** `.health-context.yaml` exists and contains a jurisdiction value
- **THEN** the skill uses that value as the default overlay starting point
- **THEN** the skill still allows user override or refinement when task-specific evidence conflicts with the stored context

#### Scenario: Multi-market discovery applies concurrent overlays
- **WHEN** repository evidence or confirmed context indicates `us+eu`
- **THEN** the skill applies both US and EU discovery overlays
- **THEN** the output distinguishes shared findings from market-specific findings instead of flattening both markets into one generic recommendation

### Requirement: Skill defines explicit US and EU market overlays in references
The `health-product-discovery` skill SHALL externalize market-specific discovery heuristics into reference files rather than embedding them as unnamed assumptions in the top-level prompt.

#### Scenario: US overlay is separated from base discovery flow
- **WHEN** a contributor inspects the skill references
- **THEN** a US market overlay reference exists for buyer structure, reimbursement incentives, procurement expectations, and adoption dynamics that are specific to a US healthcare context
- **THEN** those assumptions are no longer only implied by the base `SKILL.md`

#### Scenario: EU overlay is available for product and market discovery
- **WHEN** a contributor inspects the skill references
- **THEN** an EU market overlay reference exists alongside the US overlay reference
- **THEN** the EU overlay is framed as product-discovery and market-access guidance, not just as a regulatory appendix

### Requirement: EU discovery overlay covers product and market-access factors
The EU overlay for `health-product-discovery` SHALL guide product discovery through healthcare market realities that materially differ from a US-default frame.

#### Scenario: EU overlay covers fragmented market structure
- **WHEN** the EU overlay is applied
- **THEN** the skill prompts for member-state or regional fragmentation in buyers, deployment pathways, and evidence expectations
- **THEN** the skill identifies country-specific unknowns instead of treating the EU as a single uniform market

#### Scenario: EU overlay covers procurement and reimbursement variation
- **WHEN** the EU overlay is applied
- **THEN** the skill evaluates public procurement pathways, tender-driven buying, HTA considerations, and reimbursement variation across target countries or regions
- **THEN** the skill reflects those factors in viability, adoption, and timeline analysis

#### Scenario: EU overlay covers localisation and cross-border interoperability
- **WHEN** the EU overlay is applied
- **THEN** the skill evaluates multilingual and localisation requirements as product-level concerns
- **THEN** the skill evaluates cross-border interoperability expectations where relevant, including patient-summary or ePrescription-style exchange assumptions

#### Scenario: EU overlay covers public-system incentives and regulatory feasibility
- **WHEN** the EU overlay is applied
- **THEN** the skill considers public-system incentives such as continuity of care, service efficiency, and policy alignment in addition to local budget incentives
- **THEN** the skill flags when GDPR, EHDS, MDR/IVDR, AI Act, or NIS2 feasibility constraints materially affect product shape or rollout sequencing

### Requirement: Document mode preserves overlay-aware output structure
The `health-product-discovery` skill SHALL preserve a single document-mode artifact structure while incorporating any applicable market overlays into the planning output.

#### Scenario: Document output records market-specific assumptions
- **WHEN** document mode is used with a US, EU, or `us+eu` overlay
- **THEN** the output records the active market assumptions in sections such as stakeholder incentives, payment and business viability, adoption strategy, risks, and open questions
- **THEN** the output identifies which assumptions require country-specific or buyer-specific validation before execution

### Requirement: Skill remains analysis-only
The `health-product-discovery` skill SHALL produce analysis or document content only and SHALL not modify repository files, code, or configuration.

#### Scenario: User invokes discovery against an existing repository
- **WHEN** the skill is used in a repo-backed workflow
- **THEN** it may read repository context and prior artifacts as inputs
- **THEN** it does not edit code or operational files as part of discovery
