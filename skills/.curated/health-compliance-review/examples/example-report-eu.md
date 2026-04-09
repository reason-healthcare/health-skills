# Healthcare Regulatory Review Report

**Skill**: `health-compliance-review`
**Date**: 2026-03-31
**Auditor**: AI-assisted engineering review
**Target**: CrossBorderCare Coordination Platform
**Selected overlays**: `eu`

> This report is an engineering review, not legal advice, certification, or a formal compliance determination.

## Overlay Selection

Evidence supporting `eu`:
- `docs/privacy.md` references GDPR, controller/processor roles, and special-category health data
- `docs/interoperability.md` references EHDS-aligned patient summary exchange
- `docs/device-scope.md` references MDR classification review and CE-mark planning
- `ops/security.md` references NIS2 incident reporting preparation

## Executive Summary

CrossBorderCare is a care-coordination platform used by provider networks in two EU member states. The review identified engineering gaps in GDPR-oriented health-data handling, unclear controller/processor boundaries for analytics vendors, and missing documentation for MDR-classification rationale around a symptom-triage module.

## Findings

| ID | Severity | Category | Affected Area | Evidence | Risk | Remediation Direction | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H-01 | Critical | GDPR data minimization | `services/exportJob.ts` | Full patient summaries are exported to analytics storage when only aggregated outcome counts are required. | Excess health-data processing beyond the apparent stated purpose. | Reduce export payloads to the minimum data needed and document the purpose boundary. | Confirmed |
| H-02 | High | Controller / processor boundary | `docs/vendors.md` | External analytics and messaging vendors are listed, but roles and transfer boundaries are not defined. | Unclear accountability for health-data handling and cross-border transfers. | Document controller/processor roles and vendor transfer boundaries. | Likely |
| H-03 | High | MDR / IVDR intended use | `services/triageRules.ts` | Symptom-triage logic ranks urgency and recommended follow-up actions, but no intended-use rationale is documented. | Device-software classification may be understated. | Create an intended-use and classification rationale for human review. | Likely |
| H-04 | Medium | NIS2 incident coordination | `ops/runbooks/security.md` | General incident response exists, but there is no healthcare-specific escalation path or evidence of NIS2-style coordination planning. | Operational response obligations may be underdefined. | Add incident coordination documentation and decision ownership. | Likely |

## Open Questions

- Which legal entity is the controller for member-state-specific deployments?
- Does the symptom-triage module stay advisory, or does it influence clinical action strongly enough to raise classification risk?
- Are vendor transfers limited to the EEA, or do any processors move data elsewhere?
