# EU Docs Overlay

Use this overlay when `health-docs` selects `eu` or `us+eu`.

## Additional Compliance Targets

Add these dimensions when the evidence supports EU deployment or EU-regulatory relevance:

- `comply/eu/gdpr/data-roles-and-lawful-basis`
- `comply/eu/gdpr/data-subject-rights`
- `comply/eu/gdpr/vendor-and-transfer-boundaries`
- `comply/eu/ehds/primary-use-data-exchange`
- `comply/eu/mdr-ivdr/classification-and-intended-use`
- `comply/eu/ai-act/risk-and-human-oversight`
- `comply/eu/nis2/incident-coordination-and-cyber-risk`

Target file shape under `docs/comply/eu/`:

```
docs/comply/eu/
├── gdpr/
│   ├── data-roles-and-lawful-basis.md
│   ├── data-subject-rights.md
│   └── vendor-and-transfer-boundaries.md
├── ehds/
│   └── primary-use-data-exchange.md
├── mdr-ivdr/
│   └── classification-and-intended-use.md
├── ai-act/
│   └── risk-and-human-oversight.md
└── nis2/
    └── incident-coordination-and-cyber-risk.md
```

## Focus Areas

- GDPR roles, lawful basis, vendor boundaries, and rights handling for health data
- EHDS or cross-border exchange assumptions where primary-use workflows exist
- MDR / IVDR intended use and classification rationale when the product behaves like device software
- AI Act risk, oversight, and documentation needs for AI-enabled clinical workflows
- NIS2 operational cybersecurity and incident coordination expectations

## Analyze / Document Notes

- All `docs/comply/eu/` outputs require human review.
- If the target member state is unclear, keep the documents explicit about country-specific unknowns rather than pretending one EU-wide answer exists.
