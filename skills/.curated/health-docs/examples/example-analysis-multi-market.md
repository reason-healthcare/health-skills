# Example: Analyze Mode Output — Multi-Market

This example shows `health-docs` analyze mode when both US and EU overlays apply. The fictional product is **EuroTrack**, a care coordination platform deployed to US outpatient clinics and EU hospital networks in Germany and the Netherlands.

---

## Pass 1: Signal Detection

**Reading `.health-context.yaml`...**
File not found. Asking user:
> "Should I focus on US regulations (HIPAA/ONC/FDA), EU regulations (GDPR/MDR/AI Act/NIS2), or both? I'll detect signals automatically — this helps me prioritize what to look for."

User responds: `us+eu`

**Scanning repository for regulatory signals...**

Found US signals (high confidence):
- `Patient` model with `mrn`, `dob` fields (`app/models/patient.rb:8-14`)
- SMART on FHIR scopes in `config/oauth.yml` (`patient/Patient.read`, `patient/Observation.read`)
- HIPAA references in `docs/security.md:12, 45`
- `fhir_models` gem in `Gemfile:24`

Found EU signals (high confidence):
- `DataSubjectRequest` model with `erasure_request`, `portability_request` fields (`app/models/data_subject_request.rb:3-18`)
- `lawful_basis` field in `app/models/consent_record.rb:9`
- `data_controller`, `dpa_url` in `config/gdpr.yml`
- GDPR Art. 28 references in `docs/privacy.md:1, 34`
- MDR classification note in `docs/device-scope.md:5`
- `eu-west-1` region config in `config/infrastructure.yml:3`

Found EU signals (medium confidence):
- EHDS / cross-border patient summary references in `docs/interoperability.md:22`

**Proposed overlays: `us+eu`**

**Subagent dispatch:**
- `$health-regulatory-review` (scoped) — healthcare regulatory and EU signals detected ✓
- `$health-fhir-api-design` (scoped) — FHIR signals detected ✓
- `$health-human-factors` — UI files detected in `app/views/` ✓

---

## Coverage Matrix

| Dimension | Status | Source | Regulatory | Notes |
|---|---|---|---|---|
| orient/README | covered | `README.md:1-45` | — | Adequate overview |
| orient/domain-model | partial | `docs/domain.md` | — | Clinical entities listed; PHI classification absent |
| understand/architecture | partial | `README.md:46-80` | — | High-level only; no C4 diagram |
| understand/data-flows | absent-required | — | HIPAA §164.308(a)(1)(ii)(A) | **No PHI flow documentation found** |
| understand/integrations | partial | `README.md:82-91` | HIPAA §164.308(b)(1), GDPR Art. 28 | Epic integration listed; no BAA or DPA context |
| build/CONTRIBUTING | covered | `CONTRIBUTING.md` | — | ✓ |
| build/testing | partial | `spec/README.md` | HIPAA §164.308(a)(1)(ii)(A), AI Act Art. 9(7) | No PHI-safe test data policy |
| operate/deployment | covered | `docs/deployment.md` | — | ✓ |
| operate/runbooks/breach-notification | absent-required | — | HIPAA §164.408; GDPR Art. 33; NIS2 Art. 23 | **Required — 60-day (US), 72-hour (GDPR), 24-hour (NIS2) obligations; must have jurisdiction-specific sections** |
| operate/runbooks/dr-recovery | absent-required | — | HIPAA §164.308(a)(7) | **Required — contingency plan** |
| secure/auth-model | partial | `README.md:78-85`, `AGENTS.md:23` | HIPAA §164.312(a)(1), GDPR Art. 25 | ⚠ CONFLICT — session timeout: 30min (README) vs. 60min (AGENTS.md) |
| secure/audit-logs | partial | `README.md:45-60` | HIPAA §164.312(b), GDPR Art. 32 | Mentions audit logging; no schema or retention policy |
| secure/encryption | absent | — | HIPAA §164.312(e)(2)(ii), GDPR Art. 32(1)(a) | No at-rest or in-transit encryption docs |
| comply/hipaa/risk-analysis | absent-required | — | HIPAA §164.308(a)(1)(ii)(A) | **Required** |
| comply/hipaa/risk-management | absent-required | — | HIPAA §164.308(a)(1)(ii)(B) | **Required** |
| comply/hipaa/baa-inventory | absent-required | — | HIPAA §164.308(b)(1) | **Required — Epic integration detected** |
| comply/onc/api-access | absent | — | ONC 45 CFR §170.315(g)(10) | SMART on FHIR detected |
| comply/eu/gdpr/data-roles-and-lawful-basis | absent-required | — | GDPR Art. 6, 9, 26, 28 | **Required — controller identity and lawful basis not documented** |
| comply/eu/gdpr/data-subject-rights | absent-required | — | GDPR Art. 13–17, 20, 21 | **Required — DataSubjectRequest model detected but no process documented** |
| comply/eu/gdpr/vendor-and-transfer-boundaries | absent-required | — | GDPR Art. 28, 46 | **Required — eu-west-1 hosting + US integrations indicate cross-border transfers** |
| comply/eu/mdr-ivdr/classification-and-intended-use | absent-required | — | MDR Art. 10, Annex II/III | **Required — MDR classification note found in device-scope.md but no formal documentation** |
| comply/eu/ai-act/risk-and-human-oversight | absent | — | EU AI Act Art. 9, 14 | No AI/ML clinical inference detected; include if scope expands |
| comply/eu/nis2/incident-coordination-and-cyber-risk | absent-required | — | NIS2 Art. 21, 23 | **Required — healthcare provider in EU member states is in scope** |
| comply/eu/ehds/primary-use-data-exchange | absent | — | EHDS Art. 3–20 | Medium confidence; confirm with user |
| agent-context/AGENTS.md | partial | `AGENTS.md` | — | Exists; conflicts with README on auth |
| agent-context/phi-rules | absent | — | — | No explicit PHI rules for agents |

---

## Priority Gaps

**P0 — US HIPAA required, absent:**
- `understand/data-flows.md` — HIPAA §164.308(a)(1)(ii)(A)
- `comply/hipaa/risk-analysis.md` — HIPAA §164.308(a)(1)(ii)(A)
- `comply/hipaa/risk-management.md` — HIPAA §164.308(a)(1)(ii)(B)
- `comply/hipaa/baa-inventory.md` — HIPAA §164.308(b)(1)
- `operate/runbooks/dr-recovery.md` — HIPAA §164.308(a)(7)

**P0 — EU GDPR required, absent:**
- `comply/eu/gdpr/data-roles-and-lawful-basis.md` — GDPR Art. 6, 9, 26, 28
- `comply/eu/gdpr/data-subject-rights.md` — GDPR Art. 13–17
- `comply/eu/gdpr/vendor-and-transfer-boundaries.md` — GDPR Art. 28, 46

**P0 — Shared (both HIPAA §164.408 and GDPR Art. 33 and NIS2 Art. 23):**
- `operate/runbooks/breach-notification.md` ⚠ Must include US (60-day) and EU (72-hour / 24-hour) sections; do not merge timelines into a single narrative

**P0 — EU MDR / NIS2 required, absent:**
- `comply/eu/mdr-ivdr/classification-and-intended-use.md` — MDR Art. 10
- `comply/eu/nis2/incident-coordination-and-cyber-risk.md` — NIS2 Art. 21, 23

**Cross-jurisdiction conflicts detected:**
- `secure/auth-model` — session timeout conflict (README 30min vs. AGENTS.md 60min); cannot be resolved by this skill; flag for human resolution
- HIPAA 6-year retention vs. GDPR Art. 17 erasure obligation — will be flagged in `comply/eu/gdpr/data-subject-rights.md` and `comply/hipaa/risk-analysis.md`; no automatic resolution; requires legal review

---

## Handoff Artifact (`analysis.md` frontmatter)

```yaml
---
generated_at: "2026-03-31T12:00:00Z"
schema_version: "1"

regime_detected:
  hipaa:
    proposed: true
    confidence: high
    evidence:
      - "Patient model with mrn, dob fields (app/models/patient.rb:8-14)"
      - "SMART on FHIR scopes in config/oauth.yml"
      - "HIPAA references in docs/security.md:12, 45"
      - "fhir_models gem in Gemfile:24"
  onc:
    proposed: true
    confidence: medium
    evidence:
      - "SMART on FHIR scopes: patient/Patient.read, patient/Observation.read"
  fda_samd:
    proposed: false
    confidence: low
    evidence: []
  gdpr:
    proposed: true
    confidence: high
    evidence:
      - "DataSubjectRequest model with erasure_request, portability_request (app/models/data_subject_request.rb:3-18)"
      - "lawful_basis field in app/models/consent_record.rb:9"
      - "data_controller, dpa_url in config/gdpr.yml"
      - "GDPR Art. 28 in docs/privacy.md:1, 34"
  mdr_ivdr:
    proposed: true
    confidence: medium
    evidence:
      - "MDR classification note in docs/device-scope.md:5"
  ai_act:
    proposed: false
    confidence: low
    evidence: []
  nis2:
    proposed: true
    confidence: high
    evidence:
      - "Healthcare provider in EU member states — in-scope entity class under NIS2"
      - "eu-west-1 region config in config/infrastructure.yml:3"
  ehds:
    proposed: false
    confidence: medium
    evidence:
      - "Cross-border patient summary reference in docs/interoperability.md:22"
    note: "Confirm with user — medium confidence only"

jurisdiction_detected:
  value: "us+eu"
  confidence: high
  evidence:
    us:
      - "HIPAA references in docs/security.md"
      - "SMART on FHIR scopes in config/oauth.yml"
    eu:
      - "DataSubjectRequest model with GDPR fields"
      - "data_controller config in config/gdpr.yml"
      - "eu-west-1 hosting in config/infrastructure.yml"
      - "MDR note in docs/device-scope.md"

doc_root_detected: "docs/"

coverage:
  - dimension: "understand/data-flows"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(a)(1)(ii)(A)"
    required: null
    confidence: high

  - dimension: "operate/runbooks/breach-notification"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.408; GDPR Art. 33; NIS2 Art. 23"
    required: null
    confidence: high

  - dimension: "comply/hipaa/risk-analysis"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(a)(1)(ii)(A)"
    required: null
    confidence: high

  - dimension: "comply/eu/gdpr/data-roles-and-lawful-basis"
    status: "absent-required"
    sources: []
    regulatory: "GDPR Art. 6, 9, 26, 28"
    required: null
    confidence: high

  - dimension: "comply/eu/gdpr/data-subject-rights"
    status: "absent-required"
    sources: []
    regulatory: "GDPR Art. 13–17, 20, 21"
    required: null
    confidence: high

  - dimension: "comply/eu/gdpr/vendor-and-transfer-boundaries"
    status: "absent-required"
    sources: []
    regulatory: "GDPR Art. 28, 46"
    required: null
    confidence: high

  - dimension: "comply/eu/mdr-ivdr/classification-and-intended-use"
    status: "absent-required"
    sources:
      - path: "docs/device-scope.md"
        lines: "5"
        note: "Classification note only — not formal MDR documentation"
    regulatory: "MDR Art. 10, Annex II/III"
    required: null
    confidence: medium

  - dimension: "comply/eu/nis2/incident-coordination-and-cyber-risk"
    status: "absent-required"
    sources: []
    regulatory: "NIS2 Art. 21, 23"
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
    regulatory: "HIPAA §164.312(a)(1); GDPR Art. 25"
    required: null
    confidence: high

requirements:
  interview_completed_at: null
  regime: []
  dimensions: {}
  human_review_required: []
---
```

## Summary

The repository behaves as a multi-market healthcare platform with clear US (HIPAA/SMART on FHIR) and EU (GDPR/MDR) signals. Documentation gaps must be split into: shared engineering docs (data flows, architecture), US compliance docs (`comply/hipaa/`), and EU compliance docs (`comply/eu/`). The breach notification runbook is dual-obligation and must include separate jurisdiction-specific timeline sections. The HIPAA retention / GDPR erasure conflict requires legal review before either document is finalized.

