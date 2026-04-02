## 1. Shared Jurisdiction Foundations

- [x] 1.1 Audit the affected curated skills for current US-default assumptions and note the concrete prompts, references, and examples that need to move into explicit overlays
- [x] 1.2 Define a shared jurisdiction detection and routing pattern using `us`, `eu`, `us+eu`, and `unclear`, including reuse of `.health-context.yaml` when present
- [x] 1.3 Add or update shared examples and documentation conventions so contributors can see how per-skill overlay references are organized and consumed

## 2. health-product-discovery Overlays

- [x] 2.1 Refactor `skills/.curated/health-product-discovery/SKILL.md` so the base workflow is jurisdiction-neutral and points to regional overlays instead of silently assuming US market conditions
- [x] 2.2 Extract current US-specific payment, reimbursement, buyer, procurement, and adoption assumptions into a dedicated US overlay reference under `skills/.curated/health-product-discovery/references/`
- [x] 2.3 Create an EU overlay reference under `skills/.curated/health-product-discovery/references/` covering member-state fragmentation, public procurement, HTA and reimbursement variation, localisation, cross-border interoperability, and public-system incentives
- [x] 2.4 Update document-mode guidance and examples so output records active US, EU, or `us+eu` market assumptions and distinguishes shared findings from market-specific findings

## 3. health-compliance-review Overlays

- [x] 3.1 Update `skills/.curated/health-compliance-review/SKILL.md` to select jurisdiction overlays from evidence and confirmed context before running the review
- [x] 3.2 Add explicit US and EU regulatory overlay references under `skills/.curated/health-compliance-review/references/`
- [x] 3.3 Ensure the EU overlay covers GDPR, EHDS, MDR/IVDR, AI Act, and NIS2 applicability signals while preserving report-only behavior and scoped invocation mode
- [x] 3.4 Add or update examples showing standalone and scoped review output for `us`, `eu`, and `us+eu` paths

## 4. health-docs Routing

- [x] 4.1 Update `skills/.curated/health-docs/SKILL.md` so analyze mode detects jurisdiction evidence, reuses `.health-context.yaml`, and proposes overlays before regulatory composition
- [x] 4.2 Add or update `health-docs` reference material for jurisdiction-specific documentation expectations where US and EU compliance documentation differ
- [x] 4.3 Update analyze and document examples to show evidence-backed overlay selection, concurrent `us+eu` handling, and human-review marking for EU-oriented compliance outputs

## 5. health-refactor Routing

- [x] 5.1 Update `skills/.curated/health-refactor/SKILL.md` so it detects jurisdiction context before invoking regulatory analysis
- [x] 5.2 Add any required `health-refactor` reference material for routing heuristics or output conventions tied to jurisdiction-aware analysis
- [x] 5.3 Update example plans so they show proposed overlay evidence and jurisdiction-aware composition of `health-compliance-review`

## 6. Library and Verification

- [x] 6.1 Update library-level docs and specs references so the curated healthcare skill library documents per-skill reference overlays rather than standalone `-eu` skills
- [x] 6.2 Validate the updated skill library with `python3 scripts/validate_skill_library.py`
- [x] 6.3 Verify shell compatibility with `python3 scripts/verify_skills_sh_compat.py`
- [x] 6.4 Audit skill security guidance with `python3 scripts/audit_skill_security.py`
