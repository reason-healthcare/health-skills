# Regulatory Mapping

This reference maps each documentation dimension and target file to the regulatory requirement it satisfies. Use it in analyze mode to assign regulatory class to coverage gaps, and in document mode to prioritize drafting order and apply `⚠ REQUIRES HUMAN REVIEW` to compliance-class documents.

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

## Prioritization Matrix

When document mode must decide what to draft first, use this order:

| Priority | Condition | Action |
|---|---|---|
| P0 | HIPAA required, absent | Draft immediately, mark for human review |
| P1 | HIPAA-required supporting evidence, absent | Draft, note HIPAA connection |
| P2 | ONC/FDA required, absent | Draft if regime confirmed, mark for human review |
| P3 | Agent-context missing | Draft — no human review required |
| P4 | General engineering docs, absent | Draft as time/scope allows |
| Skip | Required: false in profile | Do not create |
