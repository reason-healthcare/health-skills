# EHR Design Review — Example Report

**Skill**: `health-human-factors`
**Date**: 2026-03-22
**Reviewer**: AI-assisted design review
**Target**: CareView EHR — Patient Summary and Lab Results screens (React, v3.1)

> This report is an engineering design review, not a formal certification or regulatory determination.

---

## Executive Summary

The CareView Patient Summary and Lab Results screens were reviewed against the Healthcare Software Design Style Guide covering 20 design categories. The review identified **16 findings**: **2 critical** (ambiguous date formatting creating potential for medication timing errors, and no persistent patient identity header on the lab results screen), **4 major** (color-only abnormal indicators, missing units on vitals, no keyboard navigation for data tables, and dangerous medication abbreviations), and **10 minor or informational** items.

The application demonstrates solid layout hierarchy and workflow efficiency on the Patient Summary screen but has significant gaps in accessibility, date safety, and clinical data display conventions on the Lab Results screen.

---

## Scope

**Artifacts reviewed**:
- `src/components/PatientSummary/PatientSummary.tsx`
- `src/components/PatientSummary/PatientHeader.tsx`
- `src/components/LabResults/LabResultsTable.tsx`
- `src/components/LabResults/LabResultsPage.tsx`
- `src/components/MedicationList/MedicationList.tsx`
- `src/styles/tokens.css` (design tokens)
- `src/utils/formatDate.ts`
- `src/utils/formatNumber.ts`

**Categories assessed**: 16 of 20

**Categories not assessable**: Audit Logging (no logging code in frontend scope), Security and Privacy (backend concern), Interoperability and Data Exchange (API layer not in scope), Internationalization (no i18n artifacts found)

---

## Findings

| ID | Severity | Category | Location | Finding | Guideline | Risk | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HF-01 | Critical | 8. Date and Time | `formatDate.ts:12` | Dates are formatted as `MM/DD/YYYY` (e.g., `03/04/2026`). This format is ambiguous internationally and violates the unambiguous display standard. | Display dates as `DD Mon YYYY` (e.g., `04 Mar 2026`). ISO-8601 for storage, unambiguous format for display. Source: ISO 8601, ONC SAFER. | A date like `03/04/2026` could be read as March 4 or April 3, leading to medication timing or appointment errors for internationally trained staff. | Confirmed |
| HF-02 | Critical | 1. Patient Context | `LabResultsPage.tsx` | The lab results screen does not render `PatientHeader`. Patient name, DOB, and MRN are absent. The only patient identifier is a tab title (`"Labs — Smith"`). | Every patient view must display full name, DOB, MRN, age, and sex in a persistent header. Source: NIST Health IT Usability, ONC SAFER. | Clinicians could view or act on lab results for the wrong patient without realizing it, particularly when multiple patient tabs are open. | Confirmed |
| HF-03 | Major | 3. Color Standards | `LabResultsTable.tsx:87` | Abnormal lab values are indicated solely by red text color. No icon, symbol, or text label accompanies the color change. | Color must never be the sole indicator. Pair with icons (▲/▼), text labels, or patterns. Source: WCAG 2.1 (1.4.1), FDA Human Factors. | Color-blind users (approximately 8% of male clinicians) will not see the abnormal indication. Critical values could be missed. | Confirmed |
| HF-04 | Major | 7. Units of Measure | `PatientSummary.tsx:134` | Vitals section displays values without units: `BP: 120/80`, `Temp: 98.6`, `HR: 72`. | All measurements must display units. Never display numbers without units. Source: IEC 62366, NIST. | `Temp: 98.6` is ambiguous — Fahrenheit vs Celsius. A temperature misread could mask a fever or trigger unnecessary intervention. | Confirmed |
| HF-05 | Major | 12. Accessibility | `LabResultsTable.tsx` | Data table is built with `<div>` elements styled as a grid. No `<table>`, `<th>`, `<td>`, ARIA roles, or `aria-sort` attributes. Tab key does not move focus between cells. | Use semantic HTML tables or equivalent ARIA roles. Support keyboard navigation and screen reader announcement. Source: WCAG 2.1 (1.3.1, 2.1.1). | Screen reader users cannot navigate or interpret the lab results table. Keyboard-only users cannot interact with sort or filter controls. | Confirmed |
| HF-06 | Major | 10. Medication Safety | `MedicationList.tsx:45` | Medication display uses abbreviations: `Heparin 5000 U SC qd`. | Avoid dangerous abbreviations. Use `units` not `U`, `daily` not `qd`. Source: ISMP, FDA. | `U` can be misread as `0`, `4`, or `cc`. `5000 U` could be misread as `50,000`. ISMP lists these as error-prone abbreviations. | Confirmed |
| HF-07 | Minor | 5. Data Tables | `LabResultsTable.tsx` | Lab value column is left-aligned. Reference range column is absent. | Align numeric values to the right. Always show reference ranges for lab results. Source: ISO 9241, clinical informatics best practice. | Left-aligned numbers are harder to compare across rows. Without reference ranges, clinicians must recall normal values from memory. | Confirmed |
| HF-08 | Minor | 4. Typography | `tokens.css:18` | Body text size is set to `13px`. Table text is `11px`. | Body text minimum 16px, table text 14–16px. Source: ISO 9241-303. | Small text increases misread risk for clinical values, especially in low-light clinical environments or for clinicians with uncorrected vision. | Confirmed |
| HF-09 | Minor | 6. Numeric Formatting | `formatNumber.ts:8` | Temperature values display as `98.60` (trailing zero). Lab values display with inconsistent decimal places (e.g., `1.3` alongside `7.200`). | Avoid trailing zeros unless meaningful. Limit decimals to clinically relevant precision. Source: ISMP, FDA. | `5.0 mg` could be misread as `50 mg`. Inconsistent precision reduces trust in displayed values. | Confirmed |
| HF-10 | Minor | 2. Layout and Hierarchy | `PatientSummary.tsx` | Allergies are listed below notes and historical data, requiring scrolling past 3 screens of content. | Standard order: identity → allergies → medications → problems → vitals → labs → orders → notes → history. Source: NIST, ONC SAFER. | Critical allergy information is buried. Clinicians may prescribe without checking allergies if they require excessive scrolling. | Confirmed |
| HF-11 | Minor | 11. Forms and Data Entry | `MedicationList.tsx:112` | The "Adjust Dose" input is a plain text field with no range guidance, validation, or autocomplete. | Display allowable ranges for numeric values. Validate inputs immediately. Source: IEC 62366, FDA Human Factors. | Clinician could enter a dose outside the safe range with no system feedback until after submission. | Confirmed |
| HF-12 | Minor | 9. Alerts and CDS | `PatientSummary.tsx:201` | Drug interaction alerts show only "Interaction detected" with no detail about the interacting drugs, risk, or severity. | Alerts must clearly explain reason, involved medications, and risk level. Source: ONC SAFER, FDA. | Vague alerts contribute to alert fatigue. Clinicians may dismiss the alert without understanding the clinical risk. | Likely |
| HF-13 | Minor | 15. Error Prevention | `LabResultsPage.tsx:67` | The "Mark as Reviewed" button has no confirmation step. Clicking it immediately marks all displayed labs as reviewed. | Prevent errors with confirmation for bulk actions. Source: ISO 14971, IEC 62366. | Accidental click marks unreviewed results as reviewed, creating a false audit trail. | Confirmed |
| HF-14 | Info | 13. Workflow Optimization | `PatientSummary.tsx` | Navigating from Patient Summary to Labs requires 3 clicks: Summary → Clinical → Diagnostics → Labs. | Reduce clicks for frequent workflows. Source: NIST Health IT Usability. | Lab review is a high-frequency action. Three navigation levels add friction to a core clinical workflow. | Confirmed |
| HF-15 | Info | 4. Typography | `tokens.css:22` | The application uses `Helvetica Neue` as primary font. | Prefer highly legible fonts: Inter, Source Sans, Roboto, Segoe UI. Source: ISO 9241. | Helvetica Neue is legible but has known issues distinguishing `l`, `I`, and `1` in clinical contexts. Lower risk but worth noting. | Likely |
| HF-16 | Info | 20. Documentation and Help | General | No contextual help tooltips or inline guidance found on either screen. | Clinical software must include contextual help and clear error explanations. Source: IEC 62366. | New users have no on-screen guidance for interpreting lab flags, alert actions, or navigation. | Confirmed |

---

## Category Coverage Matrix

| # | Category | Status |
| --- | --- | --- |
| 1 | Patient Context and Identity | Non-Compliant |
| 2 | Layout and Information Hierarchy | Partial |
| 3 | Color Standards | Non-Compliant |
| 4 | Typography | Non-Compliant |
| 5 | Data Tables and Clinical Data Display | Non-Compliant |
| 6 | Numeric Formatting | Partial |
| 7 | Units of Measure | Non-Compliant |
| 8 | Date and Time Formatting | Non-Compliant |
| 9 | Alerts and Clinical Decision Support | Partial |
| 10 | Medication Safety | Non-Compliant |
| 11 | Forms and Data Entry | Partial |
| 12 | Accessibility | Non-Compliant |
| 13 | Workflow Optimization | Partial |
| 14 | Audit Logging | Not Assessable |
| 15 | Error Prevention | Partial |
| 16 | Clinical Terminology Standards | Compliant |
| 17 | Interoperability and Data Exchange | Not Assessable |
| 18 | Internationalization | Not Assessable |
| 19 | Security and Privacy | Not Assessable |
| 20 | Documentation and Help | Non-Compliant |

---

## Positive Observations

- **Patient Summary layout** uses a clear two-column structure with vitals and medications visible without scrolling (aside from allergy placement)
- **Clinical terminology**: medication codes use RxNorm, lab codes use LOINC — both are appropriate standard terminologies
- **Patient header on summary screen** includes all required identifiers (name, DOB, MRN, age, sex, photo) in a persistent banner — this is a strong implementation that should be reused on other screens
- **Medication list** groups by active/discontinued status with clear visual separation

---

## Open Questions

1. **Accessibility testing**: does the application pass automated WCAG scanning (axe, Lighthouse)? The `<div>`-based table suggests broader accessibility issues may exist.
2. **Color contrast**: the red abnormal text on white background needs measured contrast ratio. Visual inspection suggests it may be below 4.5:1, but tooling is needed to confirm.
3. **Alert fatigue metrics**: how many alerts does a typical clinician encounter per session? The vague alert text suggests CDS tuning may be needed.
4. **Multi-patient safety**: when multiple patient tabs are open, is there a visual differentiation (color coding, prominent banner) to reduce wrong-patient risk?
5. **Touch target sizing**: if used on tablets in clinical settings, do interactive elements meet the 44×44px minimum?

---

## Standards Basis

- NIST Health IT Usability Guides (NISTIR 7741, NISTIR 7742)
- FDA Guidance: Applying Human Factors and Usability Engineering to Medical Devices
- IEC 62366-1:2015 — Application of usability engineering to medical devices
- ISO 9241-110, ISO 9241-303 — Ergonomics of human-computer interaction
- ISO 14971:2019 — Application of risk management to medical devices
- WCAG 2.1 Level AA — Web Content Accessibility Guidelines
- ONC SAFER Guides — Safety Assurance Factors for EHR Resilience
- ISMP List of Error-Prone Abbreviations, Symbols, and Dose Designations
- HL7 FHIR R4 — resource alignment context
