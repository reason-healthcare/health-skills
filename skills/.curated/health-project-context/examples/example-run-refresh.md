# Example Run: Existing Artifact Refresh

## Existing Artifact Found

The repository already contains `.health-context.yaml`:

```yaml
version: 1
generated_at: "2026-01-15T10:00:00Z"

jurisdiction:
  value: us
  confidence: high
  evidence:
    - "HIPAA references in docs/security.md"

primary_audience:
  value: provider
  confidence: medium
  evidence:
    - "Clinician workflow language in app/views/"

project_stage:
  value: existing
  confidence: high
  evidence:
    - "Repository contains source code and CI"

confirmed_by_user: true
```

## New Evidence

The latest repository scan finds:

- GDPR and DPA workflow material added under `docs/privacy/`
- patient portal routes under `portal/src/`
- existing implementation evidence still supports `project_stage: existing`

## Refresh Review

The stored artifact no longer fully matches the repository evidence:

- `jurisdiction` was `us`, but the repo now contains meaningful EU signals alongside the existing US signals
- `primary_audience` was `provider`, but the repo now contains a patient-facing portal in addition to clinician workflows
- `project_stage` still matches the evidence and does not need to change

I will keep `project_stage` as-is and propose these updates:

```yaml
jurisdiction:
  value: us+eu
  confidence: high

primary_audience:
  value: mixed
  confidence: medium
```

Please confirm or correct these changed fields before I update the file.

## Result After Confirmation

The user accepts the jurisdiction change but asks to keep `primary_audience: provider` because the patient portal is still pilot-only.

The refreshed artifact updates only the changed fields:

```yaml
jurisdiction:
  value: us+eu
  confidence: high
  evidence:
    - "HIPAA references in docs/security.md"
    - "GDPR and DPA workflow material in docs/privacy/"

primary_audience:
  value: provider
  confidence: medium
  evidence:
    - "Clinician workflow language in app/views/"
    - "Patient portal exists in portal/src/ but is pilot-only per user confirmation"
```

`generated_at` is refreshed and `confirmed_by_user` remains `true`.
