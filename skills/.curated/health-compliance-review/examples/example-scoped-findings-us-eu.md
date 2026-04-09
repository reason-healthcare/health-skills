# Scoped Regulatory Findings — Multi-Market Example

Used by orchestrating skills when `health-compliance-review` is invoked in scoped mode with `us+eu` overlays.

```md
### [H-1] Full patient export sent to analytics processor
- Severity: critical
- Category: minimum necessary / GDPR data minimization
- File: src/jobs/exportPatients.ts:41
- Detail: The export job sends full patient demographics, payer identifiers, and encounter text to an analytics sink even though the downstream report uses only aggregate cohort metrics.
- Guideline: US overlay — minimum necessary handling; EU overlay — data minimization and purpose limitation

### [H-2] Clinical triage recommendation lacks documented intended-use boundary
- Severity: high
- Category: FDA / MDR-AI applicability
- File: src/triage/recommendationEngine.ts:88
- Detail: The engine classifies urgency and recommends escalation paths without an explicit intended-use boundary or human-oversight note in nearby code or docs.
- Guideline: US overlay — device-style clinical recommendation review; EU overlay — MDR / AI Act intended-use and oversight review
```
