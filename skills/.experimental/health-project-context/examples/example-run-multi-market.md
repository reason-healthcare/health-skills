# Example Run: Multi-Market Detection

## Proposed Context

- `jurisdiction`: `us+eu`
  Evidence:
  - HIPAA operational guidance in `docs/security.md`
  - US Core references in `docs/interoperability.md`
  - GDPR data subject rights workflow in `docs/privacy.md`
  - MDR classification notes in `docs/regulatory/device.md`
  Confidence: `high`

- `primary_audience`: `mixed`
  Evidence:
  - Clinician workflow components in `app/views/`
  - Patient portal routes in `portal/src/`
  Confidence: `medium`

- `project_stage`: `existing`
  Evidence:
  - Repository contains source code, CI workflows, tests, and deployment configuration
  Confidence: `high`

## Pre-Write Review

I found strong evidence for both US and EU regulatory contexts, so I am proposing `jurisdiction: us+eu` rather than collapsing to a single market.

The product appears to serve both providers and patients as first-class audiences. Because neither side clearly dominates, I am proposing `primary_audience: mixed`.

The repository has enough implementation evidence to classify it as `existing`.

I am ready to write `.health-context.yaml` with these values. If one of the audience or jurisdiction labels should be narrower, correct it now before I persist the file.

## Result After Confirmation

The user confirms all three values.

The persisted artifact includes:

```yaml
jurisdiction:
  value: us+eu
  confidence: high
  evidence:
    - "HIPAA operational guidance in docs/security.md"
    - "GDPR data subject rights workflow in docs/privacy.md"

primary_audience:
  value: mixed
  confidence: medium
  evidence:
    - "Clinician workflow components in app/views/"
    - "Patient portal routes in portal/src/"
```

`confirmed_by_user` is set to `true`.
