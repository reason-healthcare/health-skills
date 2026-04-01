# Example: Refactor Plan — File Area Context

> Context: `src/dashboard`

---

## Scope

- **Context mode**: file area
- **Input**: `src/dashboard`
- **Proposed jurisdiction overlays**: `us+eu`
- **Overlay evidence**:
  - PHI storage concerns and audit language in dashboard service
  - cross-border care summary references in dashboard copy and integration types
- **Resolved files** (7):
  - `src/dashboard/DashboardPage.tsx`
  - `src/dashboard/PatientSummaryCard.tsx`
  - `src/dashboard/AlertBanner.tsx`
  - `src/dashboard/VitalsPanel.tsx`
  - `src/dashboard/dashboardService.ts`
  - `src/dashboard/types.ts`
  - `src/dashboard/index.ts`

---

## Findings

### Refactoring Findings

### [R-1] dashboardService.ts mixes FHIR fetching with UI state logic
- Source: refactor
- Severity: major
- Category: Long method / god class
- File: src/dashboard/dashboardService.ts:1
- Detail: dashboardService.ts (310 lines) handles FHIR Bundle fetching, Patient resource extraction, alert threshold evaluation, and dashboard layout preferences. These are four distinct responsibilities.
- Guideline: Standard refactoring (single responsibility / extract class) + Part 2 override — when splitting, ensure audit trail continuity for any data paths that access patient data.

### [R-2] Clinical terminology strings hardcoded in AlertBanner
- Source: refactor
- Severity: minor
- Category: Clinical terminology duplication
- File: src/dashboard/AlertBanner.tsx:18
- Detail: Alert severity labels ("STAT", "Urgent", "Routine") and clinical category strings ("Lab Critical", "Vital Sign Alert") are hardcoded. The same strings appear in dashboardService.ts with slightly different casing.
- Guideline: Healthcare pattern 1 — Clinical Terminology Duplication: extract clinical codes and terminology strings into a shared vocabulary module to prevent drift and silent inconsistencies.

### [R-3] Dead feature flag for legacy vitals view
- Source: refactor
- Severity: minor
- Category: Dead code and clinical feature flags
- File: src/dashboard/VitalsPanel.tsx:5
- Detail: `ENABLE_LEGACY_VITALS_VIEW` flag is checked on line 5 but the flag has been set to `false` in all environments since the v2.4 release. The guarded block (lines 8–45) is unreachable.
- Guideline: Part 2 override (Dead code and feature flags) — verify the flag is not a clinical safety gate and is fully retired across all environments before removing the guarded branch.

### Human-Factors Findings

### [HF-1] PatientSummaryCard truncates allergy list without indication
- Source: human-factors
- Severity: major
- Category: Information Density
- File: src/dashboard/PatientSummaryCard.tsx:62
- Detail: When a patient has more than 3 allergies, the list is silently truncated with no "show more" affordance or count indicator. Clinicians may miss critical allergy information.
- Guideline: NISTIR 7804 §4.7 — display critical clinical data completely or provide an explicit truncation indicator with access to the full list.

### [HF-2] VitalsPanel color-only encoding for abnormal values
- Source: human-factors
- Severity: major
- Category: Accessibility
- File: src/dashboard/VitalsPanel.tsx:78
- Detail: Abnormal vital signs are indicated solely by red text color. Users with color vision deficiency cannot distinguish abnormal from normal values.
- Guideline: WCAG 2.1 §1.4.1 — do not use color as the only visual means of conveying information. Add an icon or text label.

### Regulatory Findings

### [H-1] Patient summary cached in localStorage
- Source: regulatory
- Severity: critical
- Category: PHI Storage
- File: src/dashboard/dashboardService.ts:198
- Detail: `localStorage.setItem("lastPatientSummary", JSON.stringify(summary))` persists patient name, MRN, and active problem list in unencrypted browser storage. This data survives session close.
- Guideline: Shared US/EU privacy handling — avoid persistent client-side storage of patient data

### [H-2] Alert banner includes patient name in document title
- Source: regulatory
- Severity: major
- Category: PHI Exposure
- File: src/dashboard/AlertBanner.tsx:34
- Detail: `document.title = \`Alert: ${patient.name} - ${alert.category}\`` sets the browser tab title to include the patient's name. This is visible in screenshots, task switchers, and browser history.
- Guideline: Shared US/EU privacy handling — minimize patient identifiers in UI surface areas visible outside the app

---

## Refactor Checklist

| # | Action | Refs | Status |
|---|--------|------|--------|
| 1 | Remove PHI from localStorage — delete the `lastPatientSummary` cache or replace with a session-scoped, encrypted store | H-1 | [ ] |
| 2 | Remove patient name from `document.title` in AlertBanner; use a non-identifying label | H-2 | [ ] |
| 3 | Add truncation indicator and "show all" affordance to PatientSummaryCard allergy list | HF-1 | [ ] |
| 4 | Add icon or text badge alongside color for abnormal vitals in VitalsPanel | HF-2 | [ ] |
| 5 | Split dashboardService.ts into fhirClient, alertRules, and layoutPreferences modules | R-1 | [ ] |
| 6 | Extract clinical terminology strings into a shared vocabulary module | R-2 | [ ] |
| 7 | Remove dead `ENABLE_LEGACY_VITALS_VIEW` flag and guarded code block after confirming flag retirement | R-3 | [ ] |

---

## Risks & Notes

- **Item 1 is safety-critical**: PHI in localStorage is a compliance violation that should be addressed before any structural refactoring.
- **Item 5 before items 6 and 7**: splitting dashboardService.ts first makes the terminology extraction (item 6) and dead code removal (item 7) easier to isolate.
- **Item 7 requires verification**: confirm with the team that `ENABLE_LEGACY_VITALS_VIEW` is not scheduled for re-enablement. Check feature flag management system before removing.
- **Out-of-scope observation**: `src/dashboard/index.ts` re-exports all components. If dashboardService.ts is split (item 5), the barrel file will need updating — but that is an implementation detail, not a plan concern.
- **No test files found in scope**: the `src/dashboard` directory contains no test files. Consider adding tests before refactoring dashboardService.ts (item 5) to protect against regressions.
