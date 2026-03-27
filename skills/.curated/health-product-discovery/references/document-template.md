# Document Mode Output Template

Use this template for document mode output. Replace bracketed placeholders with specifics. Remove sections marked optional if not applicable.

---

# [Product or Initiative Name]: Discovery Document

## Context

**Problem:** [One-paragraph description of the clinical, operational, or administrative problem.]

**Care Setting:** [Specialty, facility type, patient population]

**Current Workflow:**

1. [Step — who does what, in which system, triggered by what]
2. [Step]
3. [Step]

**Pain Points:**

- **Clinician burden:** [Time, cognitive load, documentation overhead]
- **Organizational pain:** [Cost, throughput, compliance gaps]
- **Patient impact:** [Safety events, delays, experience gaps]

---

## Stakeholder-Incentive Map

| Stakeholder | Role | Interest | Burden of Change | Alignment |
|---|---|---|---|---|
| [e.g., Primary care physician] | User | [What they need] | [What adoption costs them] | [Aligned / Conflicted / Neutral] |
| [e.g., Health system CIO] | Buyer | [What drives their decision] | [Procurement, integration cost] | |
| [e.g., Patient with chronic condition] | Beneficiary | [Outcome improvement] | [Behavior change required] | |
| [e.g., Medicare / commercial payer] | Funder | [Cost or quality impact] | [None / policy change needed] | |
| [e.g., Nursing leadership] | Veto holder | [Staffing, workflow concerns] | [Training, process change] | |

**Key conflicts:** [Where buyer incentives diverge from user or beneficiary interests]

---

## Goals

| Goal | Dimension | Success Metric |
|---|---|---|
| [e.g., Reduce time-to-referral for specialty care] | Operational efficiency | [e.g., Median referral completion time] |
| [e.g., Improve medication reconciliation accuracy] | Clinical outcomes | [e.g., Discrepancy rate at discharge] |
| [e.g., Reduce per-encounter documentation time] | Clinician burden | [e.g., Minutes per encounter in EHR] |
| [e.g., Increase patient follow-up completion] | Patient experience | [e.g., 30-day follow-up rate] |

---

## Non-Goals

- [What is explicitly out of scope and why]
- [What might be expected but is deferred — state the reason]

---

## Scope

### In Scope

- **Features:** [Core capabilities]
- **Workflows:** [Which workflows are affected]
- **Data:** [What data is used, created, or exchanged]
- **Integrations:** [EHR, lab, pharmacy, payer, HIE]
- **EHR surface:** [Embedded app, SMART on FHIR, CDS Hooks, sidebar, standalone]
- **Scale:** [Single site / health system / multi-organization]

### Out of Scope

- [Explicit exclusions]

---

## Payment Model and Business Viability

**Payment model:** [Fee-for-service / value-based / capitated / bundled / grant-funded / hybrid]

**Value capture alignment:** [Does the party who pays for the product also capture the financial benefit? If not, describe the gap.]

**Procurement path:** [Who approves, what committees are involved, expected timeline]

**Revenue or funding model:** [SaaS subscription / per-encounter / shared savings / grant / embedded in existing contract]

---

## Technical Approach

**Architecture:** [High-level description]

**EHR integration:** [Integration strategy and surface area]

**Data sources:** [Clinical, claims, operational, patient-reported — note ownership and quality]

**Decision logic:** [What is deterministic, what uses AI/ML, what requires human judgment]

**Interoperability:** [FHIR R4, HL7v2, custom API, bulk data — note which exchanges are critical path]

**Deployment:** [Cloud, on-prem, hybrid — who operates and monitors]

---

## Evidence and Validation Plan

**Evidence needed:** [What type — clinical, operational, financial — and for which audience]

**Validation approach:** [Retrospective analysis, prospective pilot, A/B comparison, quality improvement study]

**Pilot design (if applicable):**

- Site: [Target site or setting]
- Duration: [Expected pilot length]
- Population: [Inclusion criteria]
- Controls: [Comparison approach]

**Success metrics:** [Tied back to Goals table above]

---

## Adoption Strategy

**Champion profile:** [e.g., Medical director interested in quality improvement, department head with workflow pain]

**Entry point:** [Which department, unit, or use case to start with]

**Change management:** [Training needs, workflow redesign, communication plan]

**Rollout:** [Phased by site / by population / by feature]

---

## Acceptance Criteria

- [ ] [Clinical workflow criterion — e.g., "Clinician can complete referral without leaving EHR"]
- [ ] [Integration criterion — e.g., "Patient data syncs from EHR within 5 minutes"]
- [ ] [Data criterion — e.g., "Medication list reflects current prescribed and OTC medications"]
- [ ] [Performance criterion — e.g., "Decision support response in under 2 seconds"]
- [ ] [Safety criterion — e.g., "Alert escalation path for critical findings is tested and documented"]

---

## Risks and Open Questions

### Clinical Safety

- [Risk: description — Mitigation: approach — Status: open/mitigated]

### Adoption

- [Risk: description — Mitigation: approach — Status: open/mitigated]

### Regulatory and Compliance

- [Risk: description — Mitigation: approach — Status: open/mitigated]

### Technical and Integration

- [Risk: description — Mitigation: approach — Status: open/mitigated]

### Unresolved Dependencies

- [Dependency — Who can resolve it — Timeline]

---

## Notes

**Assumptions requiring validation:**

- [Assumption — How to validate — Who to ask]

**Constraints:**

- [Hard constraint and its source]

**References and prior art:**

- [Link or citation]

---

## Recommended Next Step

**Recommendation:** [Proceed / Validate / Spike / Defer]

**Rationale:** [Why this recommendation, given what was discovered]

**Near-term actions:**

1. [Action — Owner — Timeframe]
2. [Action — Owner — Timeframe]

**Who needs to be in the room:** [Roles or specific people required for next step]
