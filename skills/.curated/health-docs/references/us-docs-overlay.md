# US Docs Overlay

Use this overlay when `health-docs` selects `us` or `us+eu`.

## Expected Compliance Targets

The base hierarchy already includes the primary US-oriented compliance targets:

- `docs/comply/hipaa/risk-analysis.md`
- `docs/comply/hipaa/risk-management.md`
- `docs/comply/hipaa/baa-inventory.md`
- `docs/comply/onc/api-access.md`
- `docs/comply/fda/*.md` when SaMD or device-style signals apply

## Focus Areas

- PHI handling, access control, audit logs, and breach-response runbooks
- BAA-relevant integration documentation
- ONC / SMART on FHIR API documentation when interoperability or certified-health-IT signals appear
- FDA-oriented design, risk, and validation artifacts when clinical recommendation or device signals appear

## Analyze / Document Notes

- Treat HIPAA-required gaps as top-priority absent-required items.
- Keep US-only compliance outputs clearly marked for human review.
