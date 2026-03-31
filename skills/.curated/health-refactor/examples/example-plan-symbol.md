# Example: Refactor Plan — Symbol/Dependency Context

> Context: `PatientService`

---

## Scope

- **Context mode**: symbol/dependency
- **Input**: `PatientService`
- **Proposed jurisdiction overlays**: `eu`
- **Overlay evidence**:
  - GDPR-style export and access concerns in service and audit paths
  - member-state deployment note in worker configuration comments
- **Root file**: `src/services/PatientService.ts`

### Dependency Graph

```
Direct imports (PatientService imports these):
  ├── src/lib/fhirClient.ts
  ├── src/models/PatientDTO.ts
  └── src/utils/auditLogger.ts

Root:
  └── src/services/PatientService.ts

Direct importers (these import PatientService):
  ├── src/api/patientRouter.ts
  ├── src/components/PatientSearch.tsx
  └── src/workers/eligibilityWorker.ts
```

- **Resolved files** (7):
  - `src/services/PatientService.ts` (root)
  - `src/lib/fhirClient.ts`
  - `src/models/PatientDTO.ts`
  - `src/utils/auditLogger.ts`
  - `src/api/patientRouter.ts`
  - `src/components/PatientSearch.tsx`
  - `src/workers/eligibilityWorker.ts`

---

## Findings

### Refactoring Findings

### [R-1] PatientService handles FHIR operations, caching, and audit in one class
- Source: refactor
- Severity: major
- Category: Long method / god class
- File: src/services/PatientService.ts:1
- Detail: PatientService (390 lines) manages FHIR Patient reads/searches, an in-memory patient cache with TTL logic, and audit log writes. These are three distinct responsibilities sharing mutable state.
- Guideline: Refactor pattern 1 — extract caching into a dedicated cache layer and audit calls into middleware or decorator.

### [R-2] PatientDTO uses generic field names for clinical concepts
- Source: refactor
- Severity: minor
- Category: Clinical domain naming
- File: src/models/PatientDTO.ts:12
- Detail: Fields named `data1`, `data2`, `flag` carry clinical meaning (insurance group, coverage type, VIP indicator) but use non-descriptive names. Developers must read comments to understand the fields.
- Guideline: Refactor pattern 8 — use domain-specific names that map to clinical terminology (e.g., `coverageGroup`, `coverageType`, `vipIndicator`).

### [R-3] Silent catch in FHIR patient search
- Source: refactor
- Severity: major
- Category: Error handling in clinical paths
- File: src/services/PatientService.ts:145
- Detail: The `searchPatients` method catches all errors and returns an empty array. Callers (patientRouter, PatientSearch) have no way to distinguish "no results" from "FHIR server unreachable."
- Guideline: Refactor pattern 9 — in clinical paths, propagate errors so callers can display appropriate messages and trigger alerts.

### Human-Factors Findings

### [HF-1] PatientSearch renders empty state and error state identically
- Source: human-factors
- Severity: major
- Category: Feedback & Status Visibility
- File: src/components/PatientSearch.tsx:88
- Detail: Both "no patients found" and "search failed" render the same "No results" message. Because PatientService swallows errors (R-3), the component cannot differentiate these states.
- Guideline: NISTIR 7804 §4.2 — provide distinct feedback for successful empty results vs. system errors so clinicians know whether to retry.

> Human-factors analysis: no additional findings beyond HF-1 for the reviewed files.

### Regulatory Findings

### [H-1] Audit logger does not record access to patient data
- Source: regulatory
- Severity: critical
- Category: Audit Trail
- File: src/utils/auditLogger.ts:1
- Detail: auditLogger.ts exposes `logEvent(event: string)` but PatientService never calls it when reading or searching patient data. Patient record access is not audited.
- Guideline: EU overlay — record access to health data with traceable audit events

### [H-2] Patient cache stores full FHIR Patient resource in memory
- Source: regulatory
- Severity: major
- Category: PHI Minimization
- File: src/services/PatientService.ts:55
- Detail: The in-memory cache stores the complete FHIR Patient resource (including SSN identifier, address, and contact details) even though callers only need name, MRN, and DOB. The cache has no entry limit or eviction beyond TTL.
- Guideline: EU overlay — data minimization for cached patient data

---

## Refactor Checklist

| # | Action | Refs | Status |
|---|--------|------|--------|
| 1 | Add audit logging calls to PatientService for every patient read and search operation | H-1 | [ ] |
| 2 | Reduce cached patient data to only the fields required by consumers (name, MRN, DOB); evict entries by count in addition to TTL | H-2 | [ ] |
| 3 | Replace silent catch in `searchPatients` with typed error propagation so callers can distinguish empty results from failures | R-3 | [ ] |
| 4 | Update PatientSearch to render distinct states for "no results" vs. "search error" once error propagation is in place | HF-1 | [ ] |
| 5 | Extract caching logic from PatientService into a dedicated PatientCache module | R-1 | [ ] |
| 6 | Rename generic DTO fields (`data1`, `data2`, `flag`) to clinical domain names (`coverageGroup`, `coverageType`, `vipIndicator`) | R-2 | [ ] |

---

## Risks & Notes

- **Item 1 is safety-critical**: absent audit logging for patient data access is a HIPAA compliance gap. Prioritize this above structural refactoring.
- **Item 3 before item 4**: PatientSearch (item 4) cannot show distinct error states until PatientService propagates errors (item 3). Implement in order.
- **Item 5 interacts with item 2**: extracting the cache (item 5) and minimizing cached fields (item 2) touch the same code. Consider doing both in one pass to avoid double-refactoring.
- **Item 6 is a wide rename**: `PatientDTO.data1`, `.data2`, and `.flag` are used in all three importers (patientRouter, PatientSearch, eligibilityWorker). Coordinate the rename across all files. A symbol rename tool can help.
- **Transitive dependencies not reviewed**: fhirClient.ts imports an HTTP client and auth module that were not analyzed. If audit logging (item 1) should happen at the HTTP layer instead, that would require expanding the scope.
- **eligibilityWorker.ts runs async**: changes to error propagation (item 3) may need special handling in the worker context where unhandled rejections could crash the process.
