## Context

Healthcare engineering teams operate under regulatory documentation requirements (HIPAA Security Rule, ONC 21st Century Cures Act, FDA SaMD guidance) but almost universally lack adequate engineering-layer documentation. What exists is typically scattered across README files, AGENTS.md, inline comments, external wikis, and oral tradition. No current AI skill addresses the full documentation lifecycle: auditing what exists, understanding what's required given the system's regulatory context, and consolidating existing content into a structured, maintainable form.

The skills library already covers specific healthcare engineering lenses (`health-hipaa-review`, `health-fhir-api-design`, `health-human-factors`). `health-docs` composes these skills and adds the orchestration layer that connects documentation coverage to regulatory requirements and produces actionable, structured output.

The skill is scaffolded using `scripts/init_skill.py` during implementation, following established library conventions.

## Goals / Non-Goals

**Goals:**
- Audit documentation coverage across seven dimensions: orient, understand, build, operate, secure, comply, agent-context
- Detect regulatory regime from codebase signals (HIPAA, ONC, FDA SaMD) before asking any questions
- Produce a structured handoff artifact (`.health-docs/analysis.md`) that document mode consumes
- Conduct evidence-informed interview in document mode — confirm findings, not interrogate
- Consolidate existing docs into the target hierarchy before filling gaps
- Delegate deep-dimension analysis to available subagents in parallel
- Flag regulatory-required gaps with the specific rule they satisfy
- Mark all `comply/` documents (consolidated, merged, or drafted) for human review
- Enumerate all dimensions in the coverage matrix, not just gaps

**Non-Goals:**
- Certifying HIPAA compliance or providing legal advice
- Creating policy documents (Class 1 evidence docs) without human review and sign-off
- Analyzing content behind external links (Confluence, Notion, GDrive)
- Modifying code, tests, or configurations
- Covering state-specific privacy laws (CCPA, NY SHIELD) in v1

## Decisions

### Decision 1: Skill file layout

Use `scripts/init_skill.py` to scaffold `skills/.experimental/health-docs/` with the standard template structure:

```
skills/.experimental/health-docs/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── doc-hierarchy.md        ← canonical documentation tree
│   ├── regime-signals.md       ← PHI/ONC/SaMD detection patterns
│   └── regulatory-mapping.md   ← dimension → regulatory requirement
└── examples/
    ├── example-analysis.md     ← sample coverage report
    └── example-analysis-artifact.md  ← sample .health-docs/analysis.md
```

Alternatives considered: embedding reference content inline in SKILL.md. Rejected — keeps SKILL.md focused and allows references to evolve without restructuring the workflow.

### Decision 2: Handoff artifact location — `.health-docs/`

The analysis artifact lives in `.health-docs/analysis.md` in the target repo, not at the root or in `docs/`. This is a skill work directory — always findable, cleanly separated from the documentation it's helping produce.

```
.health-docs/
├── analysis.md         ← structured coverage + narrative + requirements profile
└── runs/               ← dated run records for audit trail
    └── YYYY-MM-DD.md
```

Alternatives considered: `docs-analysis.md` at repo root (clutters root), inside `docs/` (docs/ may not exist yet). `.health-docs/` parallels `.github/` — a tooling directory that's distinct from content.

### Decision 3: Respect existing documentation directory; suggest `docs/` only when absent

During Pass 1, the skill detects the existing documentation root using a fixed precedence order: `docs/` > `documentation/` > `wiki/` > `doc/`. The first match by precedence is selected. If a root is found, document mode uses it without a blocking confirmation — the user is informed and can override. Other detected directories are noted in the artifact narrative.

Only when no documentation directory is detected does the skill require a response: it proposes `docs/` as a new default and waits for the user to confirm or specify a different path before any files are written.

The skill SHALL NOT suggest migrating content from an existing directory to `docs/` if the user's repo uses a different convention.

Alternatives considered: always defaulting to `docs/` regardless of existing structure. Rejected — overriding a team's established convention creates unnecessary churn and diff noise without adding value. Also considered: always confirming even when a directory is detected. Rejected — adding a blocking prompt for a case the skill can resolve deterministically from evidence is unnecessary friction.

### Decision 4: Two-pass analysis with parallel subagents

Analyze mode runs two passes:

**Pass 1 (direct, broad scan):** inventory all doc files, scan for regime signals, map agent instruction files. No subagents.

**Pass 2 (delegated, parallel where possible):** invoke available subagents for deep-dimension coverage. Each subagent runs in scoped mode against the Pass 1 file inventory.

```
Pass 2 subagent dispatch:
  ├── $health-hipaa-review    (if PHI signals found)                     → secure/ + comply/hipaa
  ├── $health-fhir-api-design (if FHIR/ONC signals found)                → understand/ + comply/onc
  └── $health-human-factors   (if UI source files found)                 → build/testing
```

FHIR/ONC signals: FHIR resource types, SMART on FHIR auth, EHR vendor SDK imports, USCDI references.  
UI source files: `.html`, `.tsx`, `.jsx`, `.vue`, `.erb`, or directories `app/views/`, `src/components/`, `templates/`.

If a subagent is unavailable, the skill falls back to direct analysis with reduced confidence noted in the artifact.

Alternatives considered: single-pass direct analysis only. Rejected — misses the domain depth already encoded in existing skills, duplicates logic.

### Decision 5: Evidence-informed interview before document mode writes

Document mode reads `.health-docs/analysis.md` and presents evidence-backed findings before asking anything. The interview is three confirmations, not a questionnaire:

1. Confirm regime (with evidence: "Found Patient model with MRN, DOB fields — treating as HIPAA")
2. Confirm dimension inclusion per required/skip profile (fast scan with override option)
3. Confirm target directory

This keeps human interaction minimal and grounded in what the skill already knows.

### Decision 6: Consolidate before draft

Document mode processes in strict order:
1. **Consolidate** — copy existing content to target locations (no rewrites); flag originals in place for human-reviewed cleanup
2. **Merge** — combine multiple sources; flag conflicts for human resolution
3. **Draft new** — only for required dimensions with no existing source
4. **Flag originals** — annotate source locations to indicate content was copied to the new path; do not delete

Drafting before consolidation would produce content that overlaps or conflicts with scattered existing docs. Consolidate-first ensures drafted content fills genuine gaps.

### Decision 7: Regulatory-required docs marked for human review

Any document in `comply/hipaa/`, `comply/onc/`, or `comply/fda/` written by the skill — whether consolidated, merged, or drafted — carries a visible `⚠ REQUIRES HUMAN REVIEW` header. The skill cannot certify these documents; human sign-off is required before they function as compliance evidence. This applies equally whether content is moved wholesale from an existing file or generated fresh.

## Risks / Trade-offs

- **Incomplete codebase scan** → External documentation (Confluence, Notion, GDrive) is invisible to the skill. Mitigation: explicitly flag external links as "unverifiable — content not assessed" in the coverage matrix.

- **False regime detection** → PHI field names could appear in non-healthcare systems (e.g., a general CRM with "patient" as a customer segment). Mitigation: evidence-informed interview confirms regime before any document mode writes.

- **Conflict resolution ambiguity** → Two sources describe the same topic differently. Mitigation: document mode never silently resolves conflicts — flags them in the pre-flight plan and the merged document, requiring human resolution.

- **Drafted compliance docs treated as complete** → Future developers may not notice `⚠ REQUIRES HUMAN REVIEW` markers. Mitigation: header is prominent; also noted in `.health-docs/analysis.md` run record.

- **Subagent availability variance** → The skill's coverage quality depends on which skills are installed. Mitigation: skill notes confidence level per dimension; degrades gracefully with direct analysis fallback.

## Open Questions

- Should document mode support a `--re-interview` flag to redo the requirements profile, or just prompt interactively when the profile is stale?
- Should `.health-docs/runs/` carry enough detail to reconstruct what was moved where, enabling a future "undo" operation?
- In v1, is FDA SaMD detection worth implementing given complexity, or should it be a stub that tells the user to run the skill again with `--regime samd`?
