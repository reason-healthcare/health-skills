# Jurisdiction-Aware Overlay Conventions

Use this guide when a curated healthcare skill needs regional behavior without forking into separate top-level skills.

## Core Pattern

- Keep one canonical top-level skill directory.
- Put regional variance in `references/`.
- Use the shared overlay vocabulary: `us`, `eu`, `us+eu`, `unclear`.
- Reuse `.health-context.yaml` when it exists, but verify with task-specific evidence before trusting it blindly.
- Show the proposed overlay selection with concrete evidence when confidence is low or mixed.

## Audit Baseline

This repository had four main US-default assumption clusters that now need explicit overlays instead of silent defaults.

| Skill | US-default assumptions to externalize | Target overlay files | Example updates |
|---|---|---|---|
| `health-product-discovery` | fee-for-service, value-based care, payer incentives, hospital committee buying, US EHR procurement gravity | `references/us-market-overlay.md`, `references/eu-market-overlay.md` | show `us` and `us+eu` discovery outputs |
| `health-regulatory-review` | HIPAA-first privacy/security framing presented as the whole regulatory surface | `references/us-regulatory-overlay.md`, `references/eu-regulatory-overlay.md` | show `us`, `eu`, and `us+eu` review outputs |
| `health-docs` | HIPAA/ONC/FDA-only detection and compliance drafting assumptions | `references/us-docs-overlay.md`, `references/eu-docs-overlay.md` | show jurisdiction detection and EU compliance docs in analyze/document examples |
| `health-refactor` | automatic HIPAA composition without prior jurisdiction routing | `references/jurisdiction-routing.md` | show overlay evidence in plan examples |

## Detection Contract

When a skill needs jurisdiction context:

1. Read `.health-context.yaml` if present.
2. Scan the task scope for confirming or conflicting evidence.
3. Propose one of `us`, `eu`, `us+eu`, or `unclear`.
4. Show the evidence when confidence is not high.
5. Apply only the overlay references relevant to the selected jurisdiction set.

## Overlay Organization

Recommended naming:

- `references/us-*.md` for US-specific behavior
- `references/eu-*.md` for EU-specific behavior
- `references/jurisdiction-*.md` for shared routing heuristics

Keep the top-level `SKILL.md` focused on:

- when overlays are selected
- where the overlay references live
- how output should separate shared findings from market-specific findings

Do not duplicate the full overlay detail inline in `SKILL.md`.

## Output Conventions

- If both markets apply, separate shared findings from market-specific findings.
- If the overlay is `unclear`, say so and surface the missing evidence rather than guessing.
- Compliance-class output for either market still requires human review.
