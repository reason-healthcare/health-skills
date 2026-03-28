# Example: `.health-docs/analysis.md` Handoff Artifact

This file shows the full structure of `.health-docs/analysis.md` — first as written by analyze mode (with `required: null` fields), then after document mode has completed the interview and populated the requirements profile.

---

## State 1: After Analyze Mode (before document mode interview)

`required` is `null` for all dimensions — populated by document mode.

```markdown
---
generated_at: "2026-03-28T14:23:00Z"
schema_version: "1"

regime_detected:
  hipaa:
    proposed: true
    confidence: high
    evidence:
      - "Patient model with mrn, dob, ssn fields (app/models/patient.rb:8-14)"
      - "Encounter model with diagnosis_codes, provider_npi (app/models/encounter.rb:5-22)"
      - "FHIR R4 Observation, MedicationRequest resources (app/fhir/resources/)"
      - "'phi' in 18 variable names and 6 comments"
      - "fhir_models gem in Gemfile:24"
  onc:
    proposed: true
    confidence: medium
    evidence:
      - "SMART on FHIR scopes in config/oauth.yml:12"
      - "Epic FHIR sandbox URL in config/integrations.yml:8"
  fda_samd:
    proposed: false
    confidence: low
    evidence: []

doc_root_detected: "docs/"

coverage:
  - dimension: "orient/domain-model"
    status: "absent"
    sources: []
    regulatory: null
    required: null
    confidence: high

  - dimension: "understand/data-flows"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(a)(1)(ii)(A)"
    required: null
    confidence: high

  - dimension: "understand/integrations"
    status: "partial"
    sources:
      - path: "README.md"
        lines: "82-91"
        note: "Lists Epic integration but no BAA context"
    regulatory: "HIPAA §164.308(b)(1)"
    required: null
    confidence: high

  - dimension: "secure/auth-model"
    status: "conflict"
    sources:
      - path: "README.md"
        lines: "78-85"
        note: "Session timeout: 30 minutes"
      - path: "AGENTS.md"
        lines: "23-31"
        note: "Session timeout: 60 minutes"
    regulatory: "HIPAA §164.312(a)(1)"
    required: null
    confidence: high

  - dimension: "secure/audit-logs"
    status: "partial"
    sources:
      - path: "README.md"
        lines: "45-60"
        note: "Mentions audit logging exists but no schema or retention policy"
    regulatory: "HIPAA §164.312(b)"
    required: null
    confidence: high

  - dimension: "operate/runbooks/breach-notification"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.408"
    required: null
    confidence: high

  - dimension: "comply/hipaa/risk-analysis"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(a)(1)(ii)(A)"
    required: null
    confidence: high

  - dimension: "comply/hipaa/baa-inventory"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(b)(1)"
    required: null
    confidence: high

  - dimension: "comply/onc/api-access"
    status: "absent"
    sources: []
    regulatory: "ONC 45 CFR §170.315(g)(10)"
    required: null
    confidence: medium

  - dimension: "agent-context/phi-rules"
    status: "absent"
    sources: []
    regulatory: null
    required: null
    confidence: high

requirements:
  interview_completed_at: null
  regime: []
  dimensions: {}
  human_review_required: []

---

[Human narrative body follows — see example-analysis.md for full content]
```

---

## State 2: After Document Mode Interview (requirements profile populated)

After the 3-confirmation interview, document mode writes `required: true/false` for each dimension and adds the `requirements` profile block.

```markdown
---
generated_at: "2026-03-28T14:23:00Z"
schema_version: "1"

regime_detected:
  hipaa:
    proposed: true
    confidence: high
    evidence:
      - "Patient model with mrn, dob, ssn fields (app/models/patient.rb:8-14)"
  onc:
    proposed: true
    confidence: medium
    evidence:
      - "SMART on FHIR scopes in config/oauth.yml:12"
  fda_samd:
    proposed: false
    confidence: low
    evidence: []

doc_root_detected: "docs/"

coverage:
  - dimension: "understand/data-flows"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(a)(1)(ii)(A)"
    required: true           # ← populated by document mode
    confidence: high

  - dimension: "comply/hipaa/risk-analysis"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(a)(1)(ii)(A)"
    required: true
    confidence: high

  - dimension: "comply/onc/api-access"
    status: "absent"
    sources: []
    regulatory: "ONC 45 CFR §170.315(g)(10)"
    required: true           # ← user confirmed ONC applies
    confidence: medium

  - dimension: "comply/fda/srs"
    status: "absent"
    sources: []
    regulatory: "IEC 62304 §5.2"
    required: false          # ← user confirmed SaMD does not apply
    confidence: low

requirements:
  interview_completed_at: "2026-03-28T14:45:00Z"
  regime:
    - hipaa
    - onc
  dimensions:
    "orient/domain-model":               true
    "understand/architecture":           true
    "understand/data-flows":             true
    "understand/integrations":           true
    "build/CONTRIBUTING":                true
    "build/testing":                     true
    "build/glossary":                    true
    "operate/deployment":                true
    "operate/runbooks/breach-notification": true
    "operate/runbooks/access-provisioning": true
    "operate/runbooks/dr-recovery":      true
    "secure/auth-model":                 true
    "secure/audit-logs":                 true
    "secure/encryption":                 true
    "comply/hipaa/risk-analysis":        true
    "comply/hipaa/risk-management":      true
    "comply/hipaa/baa-inventory":        true
    "comply/onc/api-access":             true
    "comply/fda/srs":                    false
    "comply/fda/sdd":                    false
    "comply/fda/risk-management":        false
    "agent-context/AGENTS.md":           true
    "agent-context/phi-rules":           true
    "agent-context/domain-context":      true
    "agent-context/constraints":         true

human_review_required:
  - "docs/operate/runbooks/breach-notification.md"
  - "docs/operate/runbooks/dr-recovery.md"
  - "docs/comply/hipaa/risk-analysis.md"
  - "docs/comply/hipaa/risk-management.md"
  - "docs/comply/hipaa/baa-inventory.md"
  - "docs/comply/onc/api-access.md"

---

[Human narrative body — unchanged from analyze mode output]
```
