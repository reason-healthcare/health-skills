# Jurisdiction Signals

Use this reference when deciding whether a repository is primarily US, primarily EU, clearly both, or still unclear.

## Output Values

- `us`
- `eu`
- `us+eu`
- `unclear`

## Strong US Signals

Treat the following as strong US-oriented evidence when they appear in code, docs, config, examples, or product language:

- HIPAA, PHI, BAA, breach notification under HIPAA
- CMS, Medicare, Medicaid, MIPS, ACO, HEDIS references in a US context
- ONC, 21st Century Cures Act, information blocking
- USCDI, US Core, QI Core, SMART on FHIR for certified EHR API contexts
- NPI, taxonomy codes, payer contract language specific to US plans
- Epic/Cerner/athenahealth integration language framed around US compliance

## Strong EU Signals

Treat the following as strong EU-oriented evidence:

- GDPR, DPA, DPO, lawful basis, data subject rights
- EHDS references
- MDR, IVDR, CE marking, notified body language
- NIS2 or EU AI Act references
- EEA residency or EU member-state deployment language
- European reimbursement, trust framework, or procurement references

## Mixed-Market Signals

Use `us+eu` when the repo contains meaningful evidence for both regions rather than a stray mention of one side.

Examples:

- HIPAA plus GDPR operational requirements in docs
- US Core plus MDR or EHDS product requirements
- Separate deployment, privacy, or compliance paths for US and EU customers
- Integration material that targets both US EHR regulation and EU device/privacy obligations

Do not collapse to `us` just because US evidence is more common in healthcare software. If both regions matter, preserve that.

## Weak Or Ambiguous Evidence

Evidence is weak when it is generic, aspirational, or mentioned only in passing. Examples:

- "privacy-compliant"
- "international expansion later"
- a single acronym with no surrounding product or compliance context

When evidence is weak or contradictory, use `unclear` and state why.

## Evidence Quality Rules

- Prefer concrete source-backed evidence over assumptions.
- Prefer repeated signals across docs, code, integrations, and policies over a single mention.
- Keep evidence short and specific, ideally naming the file or feature area that triggered the inference.
