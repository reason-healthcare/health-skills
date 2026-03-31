## Context

The curated healthcare skills in this repository currently lean US-first even when the skill name sounds general. That bias shows up in different ways across the library:

- `health-product-discovery` bakes US-style reimbursement, buyer, and procurement assumptions directly into the core discovery flow
- `health-regulatory-review` has been renamed away from `health-hipaa-review`, but its current emphasis is still primarily HIPAA and adjacent US privacy/security review
- `health-docs` and `health-refactor` compose regulatory analysis without a shared jurisdiction-selection model

This change is cross-cutting because it affects multiple curated skills, their reference materials, and the composition rules between them. It also needs to coexist with the new shared `.health-context.yaml` pattern introduced by `health-project-context`, so jurisdiction can be reused when a prior skill has already inferred and persisted it.

The product-discovery portion of the change needs more than a generic “add EU support” statement. EU healthcare product discovery is shaped by market structure and operating constraints that differ materially from a US-default frame:

- healthcare delivery and procurement are fragmented across member states rather than behaving like one uniform market
- public procurement and framework purchasing are more central to the buying path
- HTA and reimbursement pathways vary by country or region and affect what “commercially viable” means
- multilingual and localisation requirements are product-level concerns, not just go-to-market packaging
- cross-border interoperability expectations are influenced by EU digital health programs such as EHDS and MyHealth@EU
- public-system incentives often prioritize continuity of care, system efficiency, and policy alignment alongside local budget realities

The design therefore needs to separate jurisdiction-neutral discovery guidance from regional overlays, while keeping the top-level skills compact and composable.

## Goals / Non-Goals

**Goals:**
- Make jurisdiction selection explicit, evidence-backed, and reusable across healthcare skills
- Refactor `health-product-discovery` so its base workflow stays jurisdiction-neutral and region-specific market assumptions move into references
- Define a concrete EU product-discovery overlay that covers product and market-access concerns, not just regulation names
- Extend `health-regulatory-review`, `health-docs`, and `health-refactor` so they can select `US`, `EU`, `US+EU`, or `unclear` overlays from evidence
- Reuse `.health-context.yaml` when present so repeated runs do not re-derive the same jurisdiction context without cause
- Preserve current skill ergonomics by avoiding a fork into separate top-level `health-product-discovery-us` and `health-product-discovery-eu` skills

**Non-Goals:**
- Building a full country-by-country EU market-access knowledge base in this change
- Replacing downstream human judgment for legal, reimbursement, or regulatory decisions
- Introducing new persistent artifacts beyond those already used by the skills involved
- Turning each jurisdiction overlay into a separate standalone curated skill in this change
- Expanding `health-project-context` schema in this change

## Decisions

### Decision 1: Use one shared jurisdiction model across all affected skills

**Decision**: The affected skills use the same overlay vocabulary: `us`, `eu`, `us+eu`, and `unclear`. They should all select overlays from repository evidence first, then allow user override. When `.health-context.yaml` exists, skills should treat its jurisdiction field as the default starting point and only re-question it if evidence conflicts or the user asks to override.

**Rationale**: The main problem is inconsistent, implicit jurisdiction selection. A shared model keeps composition predictable and avoids each skill inventing its own labels or heuristics.

**Alternatives considered**:
- Let each skill define its own jurisdiction choices. Rejected because orchestration between skills would drift quickly.
- Treat jurisdiction as user-input only. Rejected because the change exists specifically to improve evidence-backed routing.

### Decision 2: Keep `health-product-discovery` core prompts jurisdiction-neutral and move market assumptions into overlays

**Decision**: The main `health-product-discovery` workflow remains the base skill. Region-specific product and market assumptions move into reference files that the skill can apply selectively.

Recommended structure:
- `references/us-market-overlay.md`
- `references/eu-market-overlay.md`

The base skill continues to own generic discovery stages such as problem framing, stakeholder mapping, workflow analysis, adoption readiness, and solution shaping. Overlay references contribute additional prompts, cautions, and market-structure heuristics.

**Rationale**: The current problem is not that US discovery logic exists; it is that it is treated as the invisible default. Pulling it into a named US overlay makes assumptions inspectable and makes room for an EU overlay without duplicating the whole skill.

**Alternatives considered**:
- Fork the skill into `health-product-discovery-us` and `health-product-discovery-eu`. Rejected because most of the workflow is shared and the divergence is primarily in market context.
- Keep a single blended discovery flow with occasional EU notes. Rejected because it would continue to hide the default assumptions and be harder to maintain.

### Decision 3: Define the EU product-discovery overlay around product and market-access factors, not just regulatory labels

**Decision**: The EU overlay for `health-product-discovery` explicitly covers:

- member-state fragmentation in buyers, deployment patterns, and evidence expectations
- public procurement and tender-driven buying paths
- HTA and reimbursement variation across countries or regions
- multilingual and localisation requirements for workflows, patient-facing content, and procurement materials
- cross-border interoperability expectations tied to EU digital health exchange initiatives
- public-system incentive structures, including policy alignment and service-efficiency goals
- regulatory feasibility checkpoints where MDR/IVDR, GDPR, EHDS, AI Act, or NIS2 materially constrain product shape or rollout

**Rationale**: The user asked for product and market detail, not merely an EU compliance appendix. Discovery quality depends on whether the team understands how the product gets bought, adopted, localized, validated, and integrated into real delivery systems.

**Alternatives considered**:
- Put only regulatory references in the EU overlay. Rejected because that would leave product viability analysis US-shaped.
- Attempt full country-specific logic in v1. Rejected because it is too broad for a single cross-cutting change.

### Decision 4: Keep existing top-level skills and attach overlays through each skill's references

**Decision**: `health-regulatory-review`, `health-docs`, and `health-refactor` remain the top-level skills. Jurisdiction-specific behavior lives in reference overlays owned by each skill rather than in new `-eu` skill directories. `health-regulatory-review` is still the shared downstream regulatory analysis skill used by `health-docs` and `health-refactor`, but its US and EU paths should be implemented as explicit per-skill overlays.

Suggested direction:
- `health-regulatory-review/references/us-*.md` and `health-regulatory-review/references/eu-*.md`
- `health-docs/references/us-*.md` and `health-docs/references/eu-*.md` where documentation expectations differ
- `health-refactor/references/` material only where the orchestrator needs routing-specific heuristics or output conventions

**Rationale**: This preserves the current top-level skill surface while still making jurisdiction behavior inspectable and maintainable. It also matches how the repository already prefers progressive disclosure through references instead of multiplying trigger skills.

**Alternatives considered**:
- Create a separate `health-docs-eu` or `health-regulatory-review-eu` skill directory. Rejected because the user wants the existing top-level skills to remain canonical and the variation is overlay behavior, not a fundamentally separate workflow.
- Inline all jurisdiction logic directly into each `SKILL.md`. Rejected because it would make the top-level prompts too large.

### Decision 5: `health-regulatory-review` becomes the shared regulatory overlay selector

**Decision**: `health-regulatory-review` remains the downstream regulatory analysis skill used by `health-docs` and `health-refactor`, and it gains an explicit EU-oriented review path. That path should cover GDPR, EHDS, MDR/IVDR, AI Act, and NIS2 applicability signals and present them as evidence-based overlays rather than as a monolithic “EU compliance” answer.

**Rationale**: The recent rename to `health-regulatory-review` only makes sense if the skill actually supports non-US regulatory analysis. Centralizing overlay logic there reduces duplication across orchestrating skills.

**Alternatives considered**:
- Teach each consumer skill its own EU regulatory heuristics. Rejected because that would duplicate compliance logic.

### Decision 6: `health-docs` and `health-refactor` should detect once, show evidence, and then route

**Decision**: Orchestrating skills should not silently assume a US-only path. They should:

1. read `.health-context.yaml` if present
2. scan the repo for confirming or conflicting jurisdiction signals
3. show the proposed overlay set with brief evidence
4. continue with routing, allowing override if needed

`health-docs` uses that selection to decide which regulatory analysis paths and documentation expectations apply. `health-refactor` uses it to decide which regulatory review to include in the bounded analysis pass.

**Rationale**: These skills are composition points. The user experience improves when the jurisdiction decision is surfaced once at the orchestration layer instead of buried in downstream outputs.

**Alternatives considered**:
- Let only `health-regulatory-review` perform selection. Rejected because consumers would still appear to behave unpredictably from the user’s perspective.

### Decision 7: Keep new detail in references and examples, not in oversized top-level prompts

**Decision**: Skill-specific detail should live in references and examples:

- `health-product-discovery`: US and EU market overlay references, plus examples showing US-only, EU-only, and `us+eu` discovery framing
- `health-regulatory-review`: reference material for EU applicability signals and example outputs
- `health-docs` and `health-refactor`: examples showing evidence-backed routing and override behavior

Top-level `SKILL.md` files should describe when overlays are selected and how composition works, but not inline every regional heuristic.

**Rationale**: The repo already uses progressive disclosure successfully. This change increases complexity; references keep that complexity reviewable without making trigger files unwieldy.

**Alternatives considered**:
- Inline all overlay heuristics into each `SKILL.md`. Rejected because it would bloat the skills and make updates harder.

## Risks / Trade-offs

- **EU overlay remains too abstract to guide real discovery work** → Mitigation: encode concrete product/market prompts in the reference file and back them with examples, not just a list of regimes.
- **Jurisdiction detection may oscillate across skills** → Mitigation: standardize on one overlay vocabulary and reuse `.health-context.yaml` where available.
- **`us+eu` mode could produce overly broad outputs** → Mitigation: require each skill to separate shared findings from market-specific findings rather than blending them into one undifferentiated checklist.
- **EU market guidance may still overgeneralize across member states** → Mitigation: make fragmentation an explicit overlay principle and instruct skills to name country-specific unknowns instead of flattening them.
- **More reference files increases maintenance burden** → Mitigation: keep the overlay split minimal and confine regional detail to the skills that actually need it.

## Migration Plan

1. Update `health-product-discovery` to move current US-shaped assumptions into a dedicated US overlay reference and add the EU overlay reference.
2. Update `health-regulatory-review` to support EU applicability signals and EU-oriented review output.
3. Update `health-docs` and `health-refactor` to perform evidence-backed overlay selection and route accordingly.
4. Add examples showing `us`, `eu`, and `us+eu` paths, plus reuse of `.health-context.yaml`.
5. Verify that current US-only behavior still works when evidence strongly indicates a US-only repository.

Rollback is low-risk because the change is prompt/reference oriented. If a specific overlay proves noisy, the corresponding routing logic or reference can be reverted without changing repository data formats.

## Open Questions

- Should the first EU overlay version explicitly call out common country-cluster differences, or is “member-state fragmentation” plus country-specific unknowns sufficient?
- Should `.health-context.yaml` eventually carry more discovery-relevant market fields, such as primary buyer type or deployment market, or should those remain skill-local?
