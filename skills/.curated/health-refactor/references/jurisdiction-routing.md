# Jurisdiction Routing

Use this reference before composing `health-compliance-review`.

## Routing Order

1. Read `.health-context.yaml` if present.
2. Inspect only the bounded file set and nearby task context.
3. Propose `us`, `eu`, `us+eu`, or `unclear`.
4. Surface the evidence in the Scope section before regulatory findings.

## High-Signal US Evidence

- HIPAA, PHI, ePHI, BAA
- NPI, Medicare, Medicaid, USCDI, ONC, SMART on FHIR
- US payer, prior auth, MIPS, HEDIS, CMS

## High-Signal EU Evidence

- GDPR, DPA, DPO, special category data
- EHDS, MyHealth@EU, patient summary, ePrescription
- MDR, IVDR, CE mark, notified body
- AI Act, NIS2

## Output Convention

- `us`: US-specific regulatory concerns only
- `eu`: EU-specific regulatory concerns only
- `us+eu`: separate shared findings from market-specific findings
- `unclear`: explain what evidence is missing and avoid overclaiming regulatory scope
