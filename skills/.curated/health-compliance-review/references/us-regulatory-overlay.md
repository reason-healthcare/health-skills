# US Regulatory Overlay

Use this overlay when repository evidence points to US healthcare delivery, US patient data exchange, or US regulatory programs.

## Primary Areas

- HIPAA Security Rule and Privacy Rule engineering implications
- PHI and ePHI handling, minimum necessary access, audit controls, and third-party boundaries
- ONC and interoperability signals when certified health IT, SMART on FHIR, USCDI, or information-blocking concerns are present
- FDA SaMD and device-style risk questions when software drives clinical recommendations or treatment decisions

## High-Signal Evidence

- HIPAA, PHI, ePHI, BAA, covered entity, business associate
- USCDI, ONC, SMART on FHIR, App Orchard, Epic, Cerner/Oracle Health, CMS
- NPI, Medicare, Medicaid, prior auth, MIPS, HEDIS
- FDA, SaMD, 510(k), De Novo, PMA

## Review Prompts

- Is PHI exposed through logs, analytics, exports, caches, support tooling, or third-party processors?
- Are minimum-necessary access boundaries visible in the implementation?
- Does the system show ONC or interoperability obligations through API or EHR behavior?
- Does the product make treatment, diagnosis, triage, or risk recommendations that trigger FDA-style questions?
