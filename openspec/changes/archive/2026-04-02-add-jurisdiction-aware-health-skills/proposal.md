## Why

Healthcare skills in this repository currently assume a primarily US regulatory lens, which is too narrow for teams building products that may be US-only, EU-only, or span both markets. We need jurisdiction-aware orchestration so the skills can detect applicable regulatory overlays from repo evidence, apply US and EU guidance concurrently when needed, and still allow explicit user override when the evidence is mixed or incomplete.

## What Changes

- Add jurisdiction-aware healthcare skill routing based on evidence from the target repository, with explicit support for `US-only`, `EU-only`, and concurrent `US+EU` regulatory overlays plus a fallback `unclear` outcome when evidence is insufficient.

### Skill-by-skill breakdown

- Extend `health-product-discovery` so the base skill stays jurisdiction-neutral while market-specific discovery logic moves into explicit overlay references. Extract US-specific payment, reimbursement, buyer, and procurement assumptions into a dedicated US reference file, and add a new EU discovery overlay reference covering member-state market fragmentation, public procurement pathways, HTA and reimbursement variation, multilingual/localisation requirements, cross-border interoperability expectations, and public-system incentive structures.
- Extend `health-compliance-review` so it no longer behaves like a US/HIPAA-only review under a broader name. Keep it as a top-level skill, but add US and EU overlay references so the skill can select an EU-oriented regulatory path covering GDPR, EHDS, MDR/IVDR, AI Act, and NIS2 applicability signals alongside the existing US-oriented review path.
- Extend `health-refactor` so it remains a top-level orchestrating skill, performs lightweight jurisdiction detection before routing to `health-compliance-review` or other applicable regulatory analysis, and uses per-skill reference overlays to show evidence for the proposed overlay set and support user override instead of implicitly assuming a US-only path even when US-only is the most common case.
- Extend `health-docs` so it remains a top-level skill and routes to jurisdiction-specific regulatory analysis and documentation mappings using per-skill reference overlays, including an EU-oriented path covering GDPR, EHDS, MDR/IVDR, AI Act, and NIS2 when applicable, while also supporting simultaneous US overlays for multi-market products and EU-only products.
- Reuse confirmed jurisdiction context from shared skill artifacts where available, especially `.health-context.yaml`, so repeated runs do not re-ask unless the user overrides or the evidence materially changes.

## Capabilities

### Modified Capabilities
- `health-docs-skill`: add jurisdiction-aware routing, evidence-backed overlay detection, and override behavior for concurrent US and EU applicability plus unclear contexts
- `health-product-discovery-skill`: extract current US-shaped discovery assumptions into explicit US references and add an EU product-discovery overlay covering EU buyer, market-access, reimbursement, procurement, interoperability, and localisation factors
- `health-compliance-review-skill`: add jurisdiction-aware regulatory review selection and per-skill overlay references so the renamed regulatory-review skill supports both US- and EU-oriented regulatory analysis instead of behaving as a HIPAA-only skill under a broader name
- `health-refactor-skill`: add jurisdiction detection, routing behavior, and per-skill overlay references so regulatory analysis is selected from evidence and can combine multiple applicable overlays instead of assuming a fixed US-only path
- `healthcare-skill-library`: expand curated healthcare skill expectations to include jurisdiction-aware composition and EU-oriented regulatory support

## Impact

- Affects curated healthcare skills, especially `health-product-discovery`, `health-refactor`, `health-docs`, `health-compliance-review`, and supporting references/examples
- Introduces EU regulatory references and routing logic alongside existing US-oriented healthcare analysis
- Splits product-discovery market logic into explicit regional overlays so US-specific incentives are no longer silently treated as the default healthcare market model
- Clarifies that product discovery remains a general healthcare skill with composable regional overlays, not a forked US/EU skill pair
- Uses the repository's current regulatory-review skill name, `health-compliance-review`, when referring to downstream regulatory analysis composition
- No breaking API changes are intended, but skill prompts, examples, and output artifacts will gain jurisdiction-related fields and behavior for multiple simultaneous regulatory overlays
