# Regulatory Mapping

This reference maps each documentation dimension and target file to the regulatory requirement it satisfies. Use it in analyze mode to assign regulatory class to coverage gaps, and in document mode to prioritize drafting order and apply `⚠ REQUIRES HUMAN REVIEW` to compliance-class documents.

For jurisdiction-specific work, use this file together with:

- `references/us-docs-overlay.md`
- `references/eu-docs-overlay.md`

**Classification key:**
- **Required** — explicitly mandated; absence is a compliance gap
- **Addressable** — must implement or document a reasonable alternative
- **Recommended** — not mandated but expected by auditors and regulators
- **Engineering evidence** — no direct mandate, but substantiates required policy claims

---

## HIPAA Security Rule Mapping

Source: HHS HIPAA Security Rule, 45 CFR Part 164, Subpart C

| Document | HIPAA Section | Classification | Requirement Summary |
|---|---|---|---|
| `understand/data-flows.md` | §164.308(a)(1)(ii)(A) | Engineering evidence | Supports required risk analysis — must identify where ePHI flows |
| `understand/integrations.md` | §164.308(b)(1) | Engineering evidence | Supports BAA inventory — identifies which vendors handle PHI |
| `build/testing.md` (PHI data policy) | §164.308(a)(1)(ii)(A) | Addressable | PHI-safe test data is a risk management measure |
| `operate/runbooks/breach-notification.md` | §164.408, §164.410 | Required | Covered entities must notify HHS and affected individuals within 60 days |
| `operate/runbooks/access-provisioning.md` | §164.312(a)(1) | Required | Unique user identification and access management procedures |
| `operate/runbooks/dr-recovery.md` | §164.308(a)(7) | Required | Contingency plan: data backup, DR, emergency operations, criticality analysis |
| `secure/auth-model.md` | §164.312(a)(1), §164.312(d) | Required | Unique user ID (required); person authentication (required) |
| `secure/audit-logs.md` | §164.312(b) | Required | Audit controls — record and examine activity in systems containing ePHI |
| `secure/encryption.md` | §164.312(a)(2)(iv), §164.312(e)(2)(ii) | Addressable | Encryption at rest and in transit — or document alternative safeguard |
| `secure/threat-model.md` | §164.308(a)(1)(ii)(A) | Engineering evidence | Supports risk analysis |
| `secure/secrets-management.md` | §164.312(a)(2)(iv) | Addressable | Key management is part of encryption addressable specification |
| `comply/hipaa/risk-analysis.md` | §164.308(a)(1)(ii)(A) | Required | Accurate and thorough assessment of potential risks to ePHI |
| `comply/hipaa/risk-management.md` | §164.308(a)(1)(ii)(B) | Required | Security measures sufficient to reduce risks to a reasonable level |
| `comply/hipaa/baa-inventory.md` | §164.308(b)(1) | Required | Written contracts with all business associates who handle PHI |
| `comply/hipaa/safeguard-mapping.md` | §164.308(a)(1)(ii)(B) | Recommended | Maps policy claims to engineering implementation — bridges policy and code |
| `agent-context/phi-rules.md` | §164.308(a)(5) | Addressable | Security awareness — ensures agents handling code enforce PHI rules |

### HIPAA Required Document Checklist

Documents that must exist. Absence is a reportable compliance gap:

- [ ] `operate/runbooks/breach-notification.md`
- [ ] `operate/runbooks/dr-recovery.md`
- [ ] `secure/auth-model.md` (or equivalent)
- [ ] `secure/audit-logs.md` (or equivalent)
- [ ] `comply/hipaa/risk-analysis.md`
- [ ] `comply/hipaa/risk-management.md`
- [ ] `comply/hipaa/baa-inventory.md`

---

## ONC / 21st Century Cures Act Mapping

Source: CMS Interoperability and Patient Access Final Rule (CMS-9115-F), ONC Cures Act Final Rule

Applies when the system exposes or consumes FHIR APIs for patient data access, or participates in health information exchange.

| Document | Requirement | Classification | Requirement Summary |
|---|---|---|---|
| `comply/onc/api-access.md` | 45 CFR §170.315(g)(10) | Required (if certified EHR) | Standardized patient list API documentation |
| `understand/integrations.md` | Information Blocking Rule | Recommended | Documents access capabilities and any restrictions with justification |
| `understand/data-flows.md` | Information Blocking Rule | Recommended | Demonstrates data is accessible without interference |

### ONC Note

ONC requirements apply primarily to certified health IT modules under the ONC Health IT Certification Program. Systems that exchange patient data but are not seeking certification are subject to information blocking provisions but not the full certification requirements. Confirm certification status during the evidence-informed interview.

---

## FDA Software as a Medical Device (SaMD) Mapping

Source: FDA Guidance — "Software as a Medical Device (SaMD): Clinical Evaluation" (2017); IEC 62304:2006; ISO 14971:2019

Applies when the software is intended to diagnose, prevent, monitor, treat, or alleviate disease and meets FDA's definition of a medical device.

| Document | Standard / Guidance | Classification | Requirement Summary |
|---|---|---|---|
| `comply/fda/srs.md` | IEC 62304 §5.2 | Required | Software Requirements Specification |
| `comply/fda/sdd.md` | IEC 62304 §5.3 | Required | Software Design Description |
| `comply/fda/risk-management.md` | ISO 14971 §4–7, IEC 62304 §7 | Required | Risk management file covering hazard analysis and residual risk |
| `understand/architecture.md` | IEC 62304 §5.3 | Engineering evidence | Architectural documentation supports design description |
| `build/testing.md` | IEC 62304 §5.5, §5.6 | Required | Software unit testing and integration testing documentation |

### FDA SaMD Note

FDA SaMD classification (Class I, II, III) affects the depth of documentation required. The skill detects SaMD signals but cannot determine device class — that requires clinical and regulatory review. Documents generated in `comply/fda/` are drafts that require clinical and regulatory expert review before submission.

---

## General Engineering Documentation (No Direct Mandate)

These documents have no direct regulatory requirement but are expected by technical reviewers and are needed for effective human and agent collaboration.

| Document | Audience | Notes |
|---|---|---|
| `orient/README.md` | All | Entry point; absence creates orientation gaps |
| `orient/domain-model.md` | Developers, agents | Clinical entity definitions reduce reasoning errors |
| `understand/architecture.md` | Developers, security reviewers | Supports multiple regulatory reviews indirectly |
| `understand/adr/` | Developers, future maintainers | Captures rationale; reduces re-litigation of decisions |
| `build/CONTRIBUTING.md` | Developers | Establishes contributing conventions |
| `build/onboarding.md` | Developers | Reduces onboarding time |
| `build/glossary.md` | Developers, agents | Critical for agents reasoning about clinical behavior |
| `operate/deployment.md` | DevOps | Deployment clarity reduces production incidents |
| `operate/monitoring.md` | DevOps, on-call | Observable systems; supports HIPAA audit controls indirectly |
| `agent-context/AGENTS.md` | AI agents | Primary agent entry point; synthesizes from other dimensions |
| `agent-context/constraints.md` | AI agents | Prevents agents from taking prohibited actions in the system |

---

## Overlay Note

- Use the base mappings above for shared engineering documentation and current US-oriented compliance dimensions.
- When `eu` or `us+eu` overlays are active, add the EU-oriented compliance targets from `references/eu-docs-overlay.md` to the coverage matrix and draft plan.
- When `us` or `us+eu` overlays are active, keep the current HIPAA / ONC / FDA mappings and supplement them with `references/us-docs-overlay.md` where needed.

---

## Prioritization Matrix

When document mode must decide what to draft first, use this order:

| Priority | Condition | Action |
|---|---|---|
| P0 | HIPAA required, absent | Draft immediately, mark for human review |
| P0 | GDPR required, absent (when `eu` or `us+eu`) | Draft immediately, mark for human review |
| P1 | HIPAA-required supporting evidence, absent | Draft, note HIPAA connection |
| P1 | MDR / AI Act / NIS2 required, absent (when regime confirmed) | Draft, mark for human review |
| P2 | ONC/FDA required, absent | Draft if regime confirmed, mark for human review |
| P2 | EHDS required, absent (when regime confirmed) | Draft, mark for human review |
| P3 | Agent-context missing | Draft — no human review required |
| P4 | General engineering docs, absent | Draft as time/scope allows |
| Skip | Required: false in profile | Do not create |

---

## EU Regulatory Mapping

Source: GDPR (Regulation (EU) 2016/679), Directive (EU) 2022/2555 (NIS2), MDR (Regulation (EU) 2017/745), IVDR (Regulation (EU) 2017/746), AI Act (Regulation (EU) 2024/1689), EHDS (Regulation (EU) 2025/327).

All documents in `comply/eu/` require `⚠ REQUIRES HUMAN REVIEW` — regulatory interpretation is member-state-specific and the skill cannot certify compliance.

### GDPR Mapping

| Document | GDPR Article | Classification | Requirement Summary |
|---|---|---|---|
| `comply/eu/gdpr/data-roles-and-lawful-basis.md` | Art. 6, 9, 26, 28 | Required | Documents legal basis for processing, controller identity, and any joint-controller or controller-processor relationships |
| `comply/eu/gdpr/data-subject-rights.md` | Art. 13–17, 20, 21 | Required | Documents how rights requests (erasure, portability, rectification, objection) are handled |
| `comply/eu/gdpr/vendor-and-transfer-boundaries.md` | Art. 28, 46, 49 | Required | Inventory of processors and sub-processors; SCCs, adequacy decisions, or transfer impact assessments for cross-border flows |
| `understand/data-flows.md` | Art. 30 | Engineering evidence | Supports Records of Processing Activities (RoPA) — ePHI flows map closely to personal data flows |
| `understand/integrations.md` | Art. 28 | Engineering evidence | Identifies processors and sub-processors that require DPAs |
| `secure/auth-model.md` | Art. 25, 32 | Engineering evidence | Privacy by design and security of processing |
| `secure/audit-logs.md` | Art. 32, 33 | Engineering evidence | Security measures; supports breach detection and 72-hour notification obligation |
| `secure/encryption.md` | Art. 32(1)(a) | Addressable | Encryption is a listed security measure under Art. 32 |
| `operate/runbooks/breach-notification.md` | Art. 33, 34 | Required | Controller must notify supervisory authority within 72 hours; may need to notify data subjects |

### GDPR Required Document Checklist

Documents that must exist when GDPR applies. Absence is a reportable gap:

- [ ] `comply/eu/gdpr/data-roles-and-lawful-basis.md`
- [ ] `comply/eu/gdpr/data-subject-rights.md`
- [ ] `comply/eu/gdpr/vendor-and-transfer-boundaries.md`
- [ ] `operate/runbooks/breach-notification.md` (also HIPAA-required — shared document, jurisdiction-specific sections)

---

### MDR / IVDR Mapping

Applies when SaMD or device-style signals suggest the product may qualify as a medical device under EU law.

| Document | Standard / Regulation | Classification | Requirement Summary |
|---|---|---|---|
| `comply/eu/mdr-ivdr/classification-and-intended-use.md` | MDR Art. 10, Annex II/III | Required | Documents intended purpose, device classification rationale, and technical documentation summary |
| `understand/architecture.md` | MDR Annex II §3 | Engineering evidence | Software architecture is part of the technical documentation file |
| `build/testing.md` | IEC 62304 §5.5, §5.6 | Required | Software unit and integration testing |
| `comply/fda/risk-management.md` | ISO 14971 | Required | Shared with FDA path — risk management file applies under both MDR and ISO 14971 |

### MDR Required Document Checklist

- [ ] `comply/eu/mdr-ivdr/classification-and-intended-use.md`

---

### EU AI Act Mapping

Applies when the product includes AI or ML components that may qualify as high-risk AI under Annex III, Category 5 (healthcare).

| Document | AI Act Article | Classification | Requirement Summary |
|---|---|---|---|
| `comply/eu/ai-act/risk-and-human-oversight.md` | Art. 9, 14, 17 | Required | Risk management system; human oversight measures; technical documentation |
| `understand/data-flows.md` | Art. 10 | Engineering evidence | Data governance for training / validation data |
| `build/testing.md` | Art. 9(7) | Required | Testing against defined metrics; test logs |
| `understand/architecture.md` | Art. 11, Annex IV | Engineering evidence | System architecture as part of technical documentation |

### AI Act Required Document Checklist

- [ ] `comply/eu/ai-act/risk-and-human-oversight.md`

---

### NIS2 Mapping

Applies when the organization is an essential or important entity under NIS2 (healthcare providers and health IT infrastructure in EU member states are in scope).

| Document | NIS2 Article | Classification | Requirement Summary |
|---|---|---|---|
| `comply/eu/nis2/incident-coordination-and-cyber-risk.md` | Art. 21, 23 | Required | Cybersecurity risk management measures and incident reporting procedures (24/72-hour obligation) |
| `operate/runbooks/breach-notification.md` | Art. 23 | Required | Incident notification runbook — covers both GDPR Art. 33 and NIS2 Art. 23 timelines |
| `secure/threat-model.md` | Art. 21(2)(a) | Engineering evidence | Risk analysis and information system security policies |
| `secure/secrets-management.md` | Art. 21(2)(h) | Engineering evidence | Supply chain security — includes key and credential management |

### NIS2 Required Document Checklist

- [ ] `comply/eu/nis2/incident-coordination-and-cyber-risk.md`
- [ ] `operate/runbooks/breach-notification.md` (shared with GDPR and HIPAA; must include NIS2 timeline section when applicable)

---

### EHDS Mapping

Applies when the product participates in European Health Data Space primary-use exchange (MyHealth@EU) or secondary-use data access.

| Document | EHDS Regulation | Classification | Requirement Summary |
|---|---|---|---|
| `comply/eu/ehds/primary-use-data-exchange.md` | EHDS Art. 3–20 | Required | Documents interoperability approach, EHR system obligations, and cross-border patient summary handling |
| `understand/integrations.md` | EHDS Art. 5 | Engineering evidence | Integration with national contact points or MyHealth@EU gateway |

---

## Cross-Jurisdiction Conflict Guide

When `us+eu` is active, the following known conflicts and alignments apply. Flag conflicts as `conflict` items in the coverage matrix and note that resolution requires legal review — do not attempt to resolve them in documentation.

| Topic | US (HIPAA) | EU (GDPR) | Disposition |
|---|---|---|---|
| Data retention | Required: 6 years for covered entities (§164.530(j)) | Required: erasure on request (Art. 17); no fixed retention floor | **Conflict** — document the tension explicitly; `comply/eu/gdpr/data-subject-rights.md` must note the HIPAA retention obligation as a lawful restriction on erasure |
| Minimum necessary vs. data minimization | Minimum necessary standard (§164.502(b)) | Data minimization principle (Art. 5(1)(c)) | **Aligned** — both limit processing to what is needed; cite both in `understand/data-flows.md` |
| De-identification | Safe Harbor or Expert Determination methods (§164.514) | Anonymization removes GDPR scope; pseudonymization reduces but does not eliminate obligations | **Partial alignment** — HIPAA de-id may not meet GDPR anonymization threshold; note in `comply/hipaa/risk-analysis.md` and `comply/eu/gdpr/data-roles-and-lawful-basis.md` |
| Breach notification timeline | 60 days to HHS + affected individuals (§164.408) | 72 hours to supervisory authority (GDPR Art. 33); 24 hours for NIS2 significant incidents | **Conflict** — `operate/runbooks/breach-notification.md` must include jurisdiction-specific timeline sections; do not merge into a single narrative |
| Cross-border data export | Business associate agreements govern vendor transfers | Standard Contractual Clauses or adequacy decisions required for transfers outside EEA | **Additive** — US BAA and EU SCCs are separate obligations; both must be reflected in `comply/eu/gdpr/vendor-and-transfer-boundaries.md` and `comply/hipaa/baa-inventory.md` |
