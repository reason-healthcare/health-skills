# Example Run

## Proposed Context

- `jurisdiction`: `us`
  Evidence:
  - HIPAA and PHI language in `docs/security.md`
  - US Core references in `docs/interoperability.md`
  Confidence: `high`

- `primary_audience`: `provider`
  Evidence:
  - Clinician-facing chart review and order entry language in `app/views/`
  - Role names include physician, nurse, and care coordinator
  Confidence: `medium`

- `project_stage`: `existing`
  Evidence:
  - Repository contains source code, tests, CI workflows, and migrations
  Confidence: `high`

## Pre-Write Review

I found strong US regulatory signals and no meaningful EU signals, so I am proposing `jurisdiction: us`.

The product appears primarily provider-facing because the workflow language centers on clinicians and care-team operations. That is less certain than jurisdiction, so I am marking it `medium` confidence.

The repository is clearly an existing system rather than greenfield because it includes real implementation code, tests, CI, and migrations.

I am ready to write `.health-context.yaml` with these values. If any field is wrong, correct it now before I persist the file.

## Result After Confirmation

The user accepts `jurisdiction` and `project_stage`, but changes `primary_audience` to `mixed` because the repository also contains a patient-facing portal.

The persisted artifact updates:

```yaml
primary_audience:
  value: mixed
  confidence: medium
  evidence:
    - "Clinician-facing workflows in app/views/"
    - "Patient portal routes in portal/src/"
```

`confirmed_by_user` is set to `true`.
