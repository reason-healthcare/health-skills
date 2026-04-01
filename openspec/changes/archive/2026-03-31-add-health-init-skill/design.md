## Context

The skill library currently has healthcare skills that infer important top-level project context on demand, but there is no shared bootstrap artifact that persists those answers for reuse. The active jurisdiction work also shows a broader need: jurisdiction alone is not enough. Downstream skills often need to know who the product primarily serves and whether the target repository is an existing system or a greenfield effort before they can choose the right framing, questions, and regulatory overlays.

This change introduces a small but cross-cutting pattern: a reusable project-context artifact written into the target repository root and intended to be consumed by future healthcare skills. The design needs to keep the artifact lightweight, evidence-backed, and durable without turning it into a full project manifest or generic repo initializer.

Relevant existing patterns:
- `health-docs` already uses a durable skill artifact model in the target repository (`.health-docs/analysis.md`)
- `add-jurisdiction-aware-health-skills` establishes that jurisdiction detection must be evidence-backed and support `US`, `EU`, and concurrent `US+EU` applicability
- Existing curated skills use progressive disclosure, keeping core instructions small and detailed heuristics in `references/`

## Goals / Non-Goals

**Goals:**
- Infer three reusable project-context fields from repository evidence: jurisdiction, primary audience, and project stage
- Persist that context in a root-level artifact that future healthcare skills can discover and read cheaply
- Record confidence and evidence for every inferred field so downstream skills can decide whether to trust the artifact or ask for confirmation
- Treat project stage as primarily repository-detected rather than user-supplied
- Keep the first version narrow and healthcare-oriented rather than designing a generic project metadata schema

**Non-Goals:**
- Scaffolding application code, infrastructure, or repository layout
- Providing legal or regulatory certification
- Capturing every possible product attribute such as care setting, specialty, reimbursement model, or device class
- Replacing downstream skill-specific discovery when a skill needs deeper context than the artifact provides
- Defining a general-purpose metadata standard for non-healthcare repositories

## Decisions

### Decision 1: Use a hidden root-level YAML file named `.health-context.yaml`

**Decision**: The skill writes a single root-level file named `.health-context.yaml` in the target repository.

Example shape:

```yaml
version: 1
generated_at: "2026-03-31T12:00:00Z"

jurisdiction:
  value: us
  confidence: high
  evidence:
    - "HIPAA references in docs/security.md"

primary_audience:
  value: provider
  confidence: medium
  evidence:
    - "Clinician-facing scheduling workflow in app/views/appointments/"

project_stage:
  value: existing
  confidence: high
  evidence:
    - "Repository contains application source, CI config, and migrations"

confirmed_by_user: false
```

**Rationale**: The file lives in the repo root, as requested, but remains hidden to avoid clutter. YAML is easy for both humans and future skills to read and patch. A single file is sufficient for the narrow v1 context contract and keeps discovery simple.

**Alternatives considered**:
- Visible root file such as `project-context.md` or `health-context.md`. Rejected because it adds root noise and mixes machine-readable state with prose.
- Dedicated directory such as `.health-context/analysis.md`. Rejected because v1 does not need multiple files or run history.
- JSON instead of YAML. Rejected because YAML is easier to scan and annotate for skill-authored artifacts in this repository.

### Decision 2: Model each field independently with value, confidence, and evidence

**Decision**: The artifact stores each inferred field as a structured object with `value`, `confidence`, and `evidence` rather than collapsing everything into a flat summary.

Field set for v1:
- `jurisdiction`: `us`, `eu`, `us+eu`, or `unclear`
- `primary_audience`: `provider`, `patient`, `payer`, `administrative`, `other`, or `mixed`
- `project_stage`: `greenfield`, `existing`, or `unclear`

Top-level metadata:
- `version`
- `generated_at`
- `confirmed_by_user`

**Rationale**: These fields have different evidence sources and different levels of certainty. Treating them independently lets downstream skills trust one field while re-questioning another. It also avoids inventing a fake single-confidence score for the whole repository.

**Alternatives considered**:
- Single free-text narrative block. Rejected because future skills need deterministic reads.
- Flat key-value pairs without evidence. Rejected because opaque answers are hard to trust and hard to refresh.

### Decision 3: Use evidence-first inference with selective confirmation

**Decision**: The skill scans the repository first, proposes values with evidence, and writes the artifact after a lightweight confirmation step when needed. If evidence is high-confidence and non-conflicting, the skill may present the result as a proposed write; if evidence is mixed or confidence is low, it explicitly asks for correction or confirmation before persisting.

If `.health-context.yaml` already exists, the skill reads it before inference. It should:
- preserve the file when the stored values still fit the evidence
- update fields when evidence materially changes or the user overrides them
- avoid repeatedly re-asking questions for already confirmed context unless confidence drops or new conflicting evidence appears

**Rationale**: The goal is to reduce repetitive questioning, not eliminate human control. This mirrors the durable-artifact pattern already used by `health-docs`, while keeping the interaction lighter because the artifact is much smaller.

**Alternatives considered**:
- Always ask the user first. Rejected because project stage in particular is often directly observable from repo structure.
- Fully automatic writes with no confirmation path. Rejected because audience and jurisdiction can be ambiguous in multi-sided healthcare products.

### Decision 4: Project stage is determined from repository maturity signals, not declared intent

**Decision**: `project_stage` is inferred from repository structure and contents using simple heuristics:

- `existing` when there is substantial implementation evidence such as application source trees, lockfiles, CI workflows, migrations, deployment configs, production-oriented documentation, or multi-directory operational structure
- `greenfield` when the repository is mostly empty, template-only, proposal/spec-only, or otherwise lacks meaningful implementation evidence
- `unclear` when evidence is too sparse or contradictory to classify confidently

The skill treats “I plan to build X” as weaker evidence than what is actually present on disk.

**Rationale**: This field was explicitly requested as agent-determined. The most useful answer for downstream skills is not aspirational state but the current repository reality they must operate against.

**Alternatives considered**:
- Ask the user whether the project is greenfield. Rejected because it makes the skill less useful as a bootstrap step and invites inaccurate self-classification.
- Infer stage from git history depth alone. Rejected because repository age is a poor proxy for implementation maturity.

### Decision 5: Detection heuristics live in references, not inlined into SKILL.md

**Decision**: The skill keeps `SKILL.md` focused on trigger conditions, workflow, artifact contract, and operating rules. Detailed heuristics live in `references/`, likely split into:
- `jurisdiction-signals.md`
- `audience-signals.md`
- `stage-signals.md`

**Rationale**: Jurisdiction and audience inference can grow quickly. Keeping those heuristics in references follows the repo’s progressive-disclosure pattern and makes future expansion easier without bloating the top-level skill instructions.

**Alternatives considered**:
- Put all detection rules directly in `SKILL.md`. Rejected because the skill would become harder to trigger, maintain, and review.

### Decision 6: Downstream skills consume the artifact as a hint with override semantics

**Decision**: The artifact is a reusable context source, not an immutable authority. Future healthcare skills should read `.health-context.yaml` first when present, use high-confidence or user-confirmed values as defaults, and still allow override when the task-specific context indicates the stored answer may be stale or too broad.

Expected downstream behavior:
- Trust `confirmed_by_user: true` unless the user explicitly overrides
- Trust high-confidence values by default
- Reconfirm low-confidence or `unclear` values only when needed for the skill’s task

**Rationale**: This creates a practical reuse contract without forcing every skill to blindly trust stale metadata.

**Alternatives considered**:
- Require all future skills to treat the artifact as authoritative. Rejected because healthcare products often span multiple audiences or jurisdictions and context may change over time.

## Risks / Trade-offs

- **Audience inference is inherently fuzzy** → Mitigation: allow `mixed` and `other`, preserve evidence, and use confirmation when signals conflict.
- **Jurisdiction detection may overfit to documentation language** → Mitigation: require concrete evidence examples and allow `unclear` instead of forcing a market label.
- **A single root file can become stale** → Mitigation: include `generated_at`, preserve evidence, and let downstream skills re-check when context appears inconsistent.
- **Root artifact may be seen as clutter by some teams** → Mitigation: use a hidden dotfile and keep the schema intentionally small.
- **Downstream skills may diverge in how they interpret the artifact** → Mitigation: define a narrow, explicit contract in specs and reference the file format from the healthcare skill library guidance.

## Migration Plan

No repository migration is required for existing skills in v1. The new skill can be introduced as an experimental bootstrap step, and downstream skills can adopt `.health-context.yaml` opportunistically over time. If a target repository already contains a similar local context file, the skill should not attempt to merge formats automatically in v1; it should either write the new artifact or ask the user how to proceed.

## Open Questions

- Should v1 record a `repo_type` or `product_type` field for platform or tooling repositories, or is `primary_audience: other` sufficient?
- Should the skill write a short markdown summary alongside `.health-context.yaml`, or is YAML-only enough for the first release?
- When the repository clearly serves both provider and patient workflows, should the skill default to `mixed` automatically or force the user to choose a primary audience?
