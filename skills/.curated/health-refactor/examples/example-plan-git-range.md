# Example: Refactor Plan — Git Range Context

> Context: `origin/main..feature/medication-dashboard`

---

## Scope

- **Context mode**: git range
- **Input**: `origin/main..feature/medication-dashboard`
- **Proposed jurisdiction overlays**: `us`
- **Overlay evidence**:
  - patient medication and PCP workflow language
  - HIPAA-style PHI exposure concern in browser console
- **Resolved files** (6):
  - `src/components/MedList.tsx`
  - `src/components/MedDetail.tsx`
  - `src/services/medicationService.ts`
  - `src/utils/fhirTransforms.ts`
  - `src/hooks/useMedicationData.ts`
  - `tests/medicationService.test.ts`

---

## Findings

### Refactoring Findings

### [R-1] God component in MedList
- Source: refactor (standard, adjusted by healthcare override)
- Severity: major
- Category: Long method / god class
- File: src/components/MedList.tsx:1
- Detail: MedList.tsx is 480 lines with inline data fetching, FHIR bundle unpacking, sorting, filtering, and rendering in one component. Note: the FHIR unpacking and rendering mix patient-facing logic with data transformation — this is not a cohesive clinical workflow, so the standard "god class" finding stands. Healthcare override: when splitting, ensure audit trail continuity is preserved for any data-fetching paths.
- Guideline: Standard refactoring (extract method / single responsibility) + Healthcare override — preserve audit trail when splitting classes.

### [R-2] Duplicated FHIR MedicationRequest mapping
- Source: refactor (healthcare-specific, Part 1)
- Severity: minor
- Category: FHIR resource handling
- File: src/services/medicationService.ts:87
- Detail: MedicationRequest → display model mapping is duplicated between medicationService.ts (line 87) and fhirTransforms.ts (line 22). Changes to one are not reflected in the other.
- Guideline: Healthcare pattern 2 — centralize FHIR-to-domain mapping in one module.

### [R-3] Clinical date formatting scattered
- Source: refactor (healthcare-specific, Part 1)
- Severity: minor
- Category: Clinical data formatting
- File: src/components/MedDetail.tsx:41
- Detail: Date formatting for prescriptionDate and lastDispensed uses inline `toLocaleDateString()` with inconsistent locale arguments across MedDetail and MedList. Ambiguous date formats are a patient-safety concern in clinical UIs.
- Guideline: Healthcare pattern 3 — centralize clinical date/time formatting with explicit locale and timezone handling; use UCUM-standard units.

### Human-Factors Findings

### [HF-1] No loading state for medication list
- Source: human-factors
- Severity: major
- Category: Feedback & Status Visibility
- File: src/components/MedList.tsx:120
- Detail: When medication data is loading, the component renders an empty container with no loading indicator. Users may perceive the system as unresponsive.
- Guideline: NISTIR 7804 §4.2 — provide feedback within 1 second; display progress for operations over 1 second.

### [HF-2] Error message exposes FHIR operation outcome
- Source: human-factors
- Severity: minor
- Category: Error Recovery
- File: src/components/MedList.tsx:135
- Detail: When the FHIR server returns an error, the raw OperationOutcome JSON is rendered. This is not actionable for clinical users.
- Guideline: NISTIR 7804 §4.9 — error messages must be expressed in plain language with guidance on corrective action.

### Regulatory Findings

### [H-1] Patient name logged in development console
- Source: regulatory
- Severity: critical
- Category: PHI Exposure
- File: src/hooks/useMedicationData.ts:28
- Detail: `console.log("Fetching meds for:", patient.name)` writes the patient's name to the browser console. This persists in dev tools and may be captured in log aggregation.
- Guideline: US overlay — HIPAA minimum necessary handling

---

## Refactor Checklist

| # | Action | Refs | Status |
|---|--------|------|--------|
| 1 | Remove `console.log` that writes patient name in useMedicationData hook | H-1 | [ ] |
| 2 | Extract data-fetching and FHIR unpacking from MedList into useMedicationData hook | R-1 | [ ] |
| 3 | Add loading spinner and skeleton state to MedList while data is fetching | HF-1 | [ ] |
| 4 | Consolidate MedicationRequest mapping into fhirTransforms.ts and remove duplicate in medicationService.ts | R-2 | [ ] |
| 5 | Replace raw OperationOutcome display with user-friendly error component | HF-2 | [ ] |
| 6 | Create shared clinical date formatter with explicit locale/timezone and replace inline calls | R-3 | [ ] |

---

## Risks & Notes

- **Item 2 depends on item 4**: if the FHIR mapping is consolidated first (item 4), the MedList extraction (item 2) will be cleaner since it can import from one source.
- **Item 1 is safety-critical**: the PHI console log should be removed immediately, independent of other changes.
- **Test coverage gap**: `tests/medicationService.test.ts` has no tests for the mapping logic that will be consolidated in item 4. Add tests before refactoring.
- **Out-of-scope observation**: `src/services/medicationService.ts` imports a `patientSearch` utility not in the diff. If that utility also logs patient data, it warrants a separate review.
