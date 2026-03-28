# Example: Analyze Mode Output

This example shows the human-readable narrative produced by `health-docs` analyze mode for a fictional FHIR-based healthcare application — CareTrack, a care coordination platform for outpatient clinics.

---

## health-docs analyze — CareTrack

### Regime Detection

**Scanning for regulatory signals...**

Found PHI indicators (high confidence):
- `Patient` model with `mrn`, `dob`, `ssn` fields (`app/models/patient.rb:8-14`)
- `Encounter` model with `diagnosis_codes`, `provider_npi` (`app/models/encounter.rb:5-22`)
- FHIR R4 `Observation`, `MedicationRequest` resources (`app/fhir/resources/`)
- `"phi"` appears in 18 variable names and 6 comments
- `fhir_models` gem in `Gemfile:24`

Found ONC indicators (medium confidence):
- SMART on FHIR scopes in `config/oauth.yml:12`: `patient/Patient.read`, `patient/Observation.read`
- Epic FHIR sandbox URL in `config/integrations.yml:8`

Found FDA SaMD indicators (none):
- No clinical decision support, scoring functions, or diagnostic language detected.

**Proposed regime: HIPAA + ONC**

---

### Subagent Dispatch

Dispatching to available subagents in parallel:
- `$health-hipaa-review` (scoped) — PHI signals detected ✓
- `$health-fhir-api-design` (scoped) — FHIR signals detected ✓
- `$health-human-factors` — no UI files detected, skipping

Merged subagent findings into coverage matrix below.

---

### Coverage Matrix

| Dimension | Status | Source | Regulatory | Notes |
|---|---|---|---|---|
| orient/README | covered | `README.md:1-45` | — | Adequate overview |
| orient/domain-model | absent | — | — | No clinical entity definitions found |
| orient/stakeholder-map | absent | — | — | |
| understand/architecture | partial | `README.md:46-80` | — | High-level only; no C4 diagram |
| understand/data-flows | absent-required | — | HIPAA §164.308(a)(1)(ii)(A) | **No PHI flow documentation found** |
| understand/integrations | partial | `README.md:82-91` | HIPAA §164.308(b)(1) | Lists Epic integration but no BAA context |
| understand/adr | absent | — | — | No decision records |
| build/CONTRIBUTING | covered | `CONTRIBUTING.md` | — | Adequate |
| build/onboarding | partial | `README.md:92-110` | — | Setup steps present but incomplete |
| build/testing | partial | `spec/README.md` | HIPAA §164.308(a)(1)(ii)(A) | No PHI-safe test data policy |
| build/glossary | absent | — | — | No clinical term definitions |
| operate/deployment | covered | `docs/deployment.md` | — | ✓ |
| operate/monitoring | partial | `docs/monitoring.md` | — | No PHI-specific alert guidance |
| operate/runbooks/breach-notification | absent-required | — | HIPAA §164.408 | **Required — 60-day notification clock** |
| operate/runbooks/access-provisioning | absent-required | — | HIPAA §164.312(a)(1) | **Required — access control procedures** |
| operate/runbooks/dr-recovery | absent-required | — | HIPAA §164.308(a)(7) | **Required — contingency plan** |
| secure/threat-model | absent | — | HIPAA §164.308(a)(1)(ii)(A) | Supports risk analysis |
| secure/auth-model | partial | `README.md:78-85`, `AGENTS.md:23` | HIPAA §164.312(a)(1) | ⚠ CONFLICT — session timeout described as 30min in README, 60min in AGENTS.md |
| secure/encryption | absent | — | HIPAA §164.312(e)(2)(ii) | No at-rest or in-transit encryption docs |
| secure/audit-logs | partial | `README.md:45-60` | HIPAA §164.312(b) | Mentions audit logging but no schema or retention policy |
| secure/secrets-management | absent | — | HIPAA §164.312(a)(2)(iv) | |
| comply/hipaa/risk-analysis | absent-required | — | HIPAA §164.308(a)(1)(ii)(A) | **Required** |
| comply/hipaa/risk-management | absent-required | — | HIPAA §164.308(a)(1)(ii)(B) | **Required** |
| comply/hipaa/baa-inventory | absent-required | — | HIPAA §164.308(b)(1) | **Required — Epic integration detected** |
| comply/hipaa/safeguard-mapping | absent | — | HIPAA §164.308(a)(1)(ii)(B) | Recommended |
| comply/onc/api-access | absent | — | ONC 45 CFR §170.315(g)(10) | SMART on FHIR detected |
| agent-context/AGENTS.md | partial | `AGENTS.md` | — | Exists but conflicts with README on auth |
| agent-context/phi-rules | absent | — | — | No explicit PHI rules for agents |
| agent-context/domain-context | absent | — | — | |
| agent-context/constraints | absent | — | — | |

---

### Priority Gaps

**P0 — HIPAA required, absent (act immediately):**
- `operate/runbooks/breach-notification.md` — HIPAA §164.408
- `operate/runbooks/access-provisioning.md` — HIPAA §164.312(a)(1)
- `operate/runbooks/dr-recovery.md` — HIPAA §164.308(a)(7)
- `understand/data-flows.md` — HIPAA §164.308(a)(1)(ii)(A)
- `comply/hipaa/risk-analysis.md` — HIPAA §164.308(a)(1)(ii)(A)
- `comply/hipaa/risk-management.md` — HIPAA §164.308(a)(1)(ii)(B)
- `comply/hipaa/baa-inventory.md` — HIPAA §164.308(b)(1)

**P1 — HIPAA supporting evidence, absent:**
- `secure/threat-model.md`
- `secure/encryption.md`
- `secure/secrets-management.md`
- `build/testing.md` (PHI test data policy section)

**P2 — ONC candidate:**
- `comply/onc/api-access.md` — SMART on FHIR detected (confirm ONC applies)

**P3 — Agent context missing:**
- `agent-context/phi-rules.md`
- `agent-context/domain-context.md`
- `agent-context/constraints.md`

**Conflict requiring human resolution:**
- `secure/auth-model.md` — session timeout: `README.md` says 30 min, `AGENTS.md` says 60 min

**External link — unverifiable:**
- `CONTRIBUTING.md:34` links to Confluence page "Engineering Standards" — content not assessed

---

### Existing Documentation Root

Detected: `docs/` (existing convention — document mode will use this path)

---

### Summary

CareTrack has a partial documentation foundation. Operational and development docs exist in `docs/` and are reasonably maintained. The critical gap is compliance-class documentation: 7 HIPAA-required documents are entirely absent, including breach notification procedures (§164.408), the contingency plan (§164.308(a)(7)), and the three foundational compliance documents (risk analysis, risk management, BAA inventory). A PHI data flow diagram, required as the basis for the risk analysis, also does not exist.

Recommend running `health-docs document` to consolidate existing content and draft missing required documents for human review.

---

*Handoff artifact written to `.health-docs/analysis.md`*
