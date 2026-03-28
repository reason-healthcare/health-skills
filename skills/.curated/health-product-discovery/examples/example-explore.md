# Healthcare Product Discovery — Example Output

**Skill**: `health-product-discovery` (mode: explore)
**Date**: 2026-03-18

---

## Prompt

> We want to build a tool that helps primary care physicians identify patients at risk of chronic kidney disease progression who should be referred to nephrology. Many referrals happen too late — patients show up at stage 4 or 5 when earlier intervention could have slowed progression. We're thinking about an alert or dashboard in the EHR.

---

## Problem Summary

Chronic kidney disease (CKD) affects approximately 37 million US adults. Progression from stage 3 to stages 4–5 is often preventable or delayable with timely nephrology co-management, medication optimization (SGLT2 inhibitors, ACE/ARB titration), and dietary intervention. However, primary care physicians (PCPs) frequently miss the window for referral because:

- eGFR decline trends are not surfaced proactively in EHR workflows
- lab results are reviewed one at a time, not as a trajectory
- proteinuria (uACR) is under-ordered in primary care despite guideline recommendations
- PCPs manage large panels and CKD progression is a slow, silent process that competes with acute concerns

**Care setting**: primary care clinics (family medicine, internal medicine)
**Population**: adults with CKD stage 2–3b, particularly those with diabetes or hypertension as comorbidities
**Current state**: PCPs review labs reactively during annual visits or when results arrive. No systematic surveillance for eGFR trajectory or referral timing.

---

## Stakeholder-Incentive Map

| Stakeholder | Role | Incentive | Tension |
| --- | --- | --- | --- |
| **PCP** | User | Wants to provide good care but is time-constrained; doesn't want another alert to dismiss | Bears the workflow burden; must act on the recommendation |
| **Nephrologist** | Beneficiary / User | Wants appropriately timed referrals; currently receives late-stage patients who require urgent dialysis planning | Benefits from earlier referrals but has no role in purchasing the tool |
| **Patient** | Beneficiary | Wants to avoid dialysis and preserve kidney function; largely unaware of CKD progression risk | Benefits most but has no purchasing power and limited awareness |
| **Practice Manager / CMO** | Buyer | Cares about quality scores (HEDIS, MIPS), malpractice risk reduction, and payer contract performance | Makes the buy decision; motivated by measurable outcomes and regulatory incentives |
| **Payer (Medicare Advantage, ACO)** | Funder | Wants to reduce downstream costs (dialysis: ~$90K/year per patient); improving CKD management is a top value-based care priority | Captures the financial upside but funds it through quality incentive programs, not direct product purchase |
| **IT / EHR Admin** | Gatekeeper | Needs low integration burden; must approve anything that touches the EHR | Has veto power; will block anything that requires custom EHR builds or creates support burden |

### Key alignment

The strongest alignment is between the **practice manager/CMO** (quality scores, risk reduction) and the **payer** (cost avoidance). The PCP is the user but does not directly benefit from purchasing the tool — their incentive is better care, but their constraint is time.

### Key conflict

The PCP absorbs all the workflow burden. If the tool adds clicks, alerts, or cognitive load without saving time elsewhere, adoption will fail regardless of clinical merit.

---

## Workflow Integration Assessment

### Current workflow

1. Patient visits PCP for annual wellness or chronic disease follow-up
2. PCP orders a metabolic panel (includes creatinine, eGFR calculated)
3. Lab results return to EHR inbox; PCP reviews and signs off
4. If eGFR is notably low, PCP may consider referral — but "notably low" is subjective and there is no trend view
5. uACR is often not ordered unless PCP specifically remembers the guideline
6. Referral decision is made (or not) based on a single point-in-time value

### Where the tool fits

- **Best insertion point**: when lab results arrive in the EHR inbox or during pre-visit chart prep
- **EHR gravity**: the tool must live inside the EHR or surface within existing EHR workflows (inbox, chart review). A separate dashboard that PCPs must remember to check will fail.
- **Integration surface**: read eGFR history, uACR values, comorbidities (diabetes, hypertension), current medications. Write: CDS alert or inbox notification with referral recommendation.

### Workflow burden assessment

- A **passive dashboard** (PCP must navigate to it) has near-zero adoption risk but also near-zero adoption.
- A **CDS alert** at lab result review is the highest-value point but adds to alert fatigue.
- A **pre-visit summary flag** during chart prep by an MA or nurse could surface the recommendation without adding to the PCP's real-time cognitive load.

**Recommendation**: combine a population health registry view (for proactive panel management) with a point-of-care flag at lab review (for reactive catch). Avoid modal interrupting alerts.

---

## Payment Model Fit

| Model | Fit | Notes |
| --- | --- | --- |
| **Fee-for-service** | Weak | FFS does not reward prevention or early referral. The nephrologist generates more revenue from late-stage patients. No direct financial incentive for the PCP practice. |
| **Value-based care / ACO** | Strong | CKD progression to dialysis is a top cost driver. Shared savings models directly reward earlier intervention. MSSP and Medicare Advantage plans track CKD-related quality measures. |
| **MIPS / Quality reporting** | Medium | CKD screening and management measures exist (NQF 0062, NQF 0059). A tool that improves measure performance has tangible reporting value. |
| **Capitated / Medicare Advantage** | Strong | Plans bear the full cost of dialysis. Preventing or delaying one patient's progression saves ~$90K/year. Strong ROI case. |

**Payment model dependency**: this product is most viable in value-based care environments. In pure FFS settings, the business case is weak unless tied to quality incentive bonuses or malpractice risk reduction.

---

## Evidence and Adoption Readiness

### Evidence requirements

| Audience | Evidence needed | Current availability |
| --- | --- | --- |
| Clinical champion (PCP or CMO) | Evidence that earlier referral improves outcomes; evidence that the tool identifies the right patients | Strong published evidence for early nephrology referral benefit (Kidney Disease: Improving Global Outcomes guidelines). Algorithm validation would need a retrospective study. |
| IT governance | Low integration risk; FHIR-based data access; no custom EHR development | Depends on implementation approach |
| Payer partner | Cost avoidance modeling; projected dialysis delay per 1,000 patients | Actuarial models exist; would need to be applied to specific populations |

### Adoption readiness signals

- **Champion availability**: nephrologists and CMOs at value-based care organizations are likely champions. They have budget authority and outcome motivation.
- **Committee path**: health system quality committees and population health teams are the approval path. Typical timeline: 3–6 months for pilot approval.
- **Change management**: low for a non-interrupting flag; moderate for a CDS alert; high if it requires new ordering workflows.
- **Competing priorities**: CKD competes with diabetes management, behavioral health integration, and annual wellness visit optimization for quality improvement bandwidth.

---

## Key Constraints and Risks

### Clinical safety

- **False negatives**: if the tool misses a patient who should be referred, it could create a false sense of comprehensive coverage and delay referral further than the status quo.
- **False positives**: over-alerting on patients with stable CKD wastes nephrology capacity and erodes PCP trust.
- **Algorithm transparency**: PCPs need to understand why a patient was flagged. Black-box risk scores will be dismissed.

### Regulatory

- **FDA/SaMD**: a tool that recommends clinical action (referral) based on algorithmic analysis of patient data may meet the FDA definition of Software as a Medical Device. This needs legal review. If it only surfaces data trends without a recommendation, the regulatory burden is lower.
- **Information blocking**: if the tool is part of EHR-integrated CDS, it must not block data access (21st Century Cures Act / ONC rules).

### Technical

- **EHR variability**: eGFR calculation methods vary (CKD-EPI 2021 vs older equations). Creatinine-based vs cystatin-C formulas differ. The tool must handle multiple calculation methods or normalize.
- **Data quality**: uACR is under-ordered; many patients will lack proteinuria data. The tool must work with incomplete data and flag when uACR should be ordered.
- **FHIR availability**: lab history via FHIR R4 Observation resources is widely available on major EHRs. Condition and MedicationRequest access varies.

### Financial

- **Long payback period**: CKD progression is slow (years). ROI from delayed dialysis takes 2–5 years to materialize. This mismatches with annual budget cycles.
- **Small per-practice numbers**: a typical PCP panel of 2,000 patients may have 50–100 with CKD stage 2–3b, of which 5–10 are actively progressing. The per-practice impact is real but modest — the business case is stronger at the health system or payer level.

---

## Recommendation: Proceed with Scoping

**Proceed** — with the following conditions:

1. **Target value-based care organizations first.** The incentive alignment is clear and the buyer (CMO/quality leader) has budget authority and outcome motivation. Do not pursue FFS practices initially.

2. **Validate the FDA/SaMD question immediately.** The answer determines whether this is a 3-month or 18-month path to market. Consider a "data surfacing" approach (show eGFR trends and flag missing uACR) rather than an explicit "refer this patient" recommendation to reduce regulatory burden.

3. **Design for the PCP's time constraint, not the nephrologist's preference.** The PCP is the bottleneck. If the tool adds any net workflow burden, it will not be used. Pre-visit flags and population health views are lower-risk than real-time CDS alerts.

4. **Scope a retrospective validation study.** Partner with one health system to run the algorithm against 3 years of historical data. Measure: would it have identified the patients who progressed to stage 4–5 earlier than they were actually referred? This is the minimum evidence a clinical champion needs.

5. **Start with read-only EHR integration.** FHIR R4 Observation (labs), Condition (CKD diagnosis), and MedicationRequest (current meds) are sufficient for an MVP. Avoid write-back (order entry, referral creation) in the first version — it multiplies the integration and safety burden.

### Who needs to be in the room

- Clinician advisor (PCP with CKD panel experience)
- Nephrologist advisor (referral receiving perspective)
- Regulatory counsel (SaMD determination)
- EHR integration lead (FHIR access feasibility)
- Health economics / actuarial support (cost avoidance modeling for payer conversations)
