# Healthcare Refactoring Patterns

Healthcare-specific refactoring patterns that go beyond standard code-quality practices. An agent already knows standard refactoring (extract method, eliminate duplication, reduce complexity, etc.). This reference covers only what is unique to healthcare software or where clinical context overrides standard refactoring heuristics.

Use this reference during the refactoring analysis pass. Flag findings only when the pattern is observable in the files under review.

---

# Part 1: Healthcare-Specific Patterns

These patterns address concerns that do not exist in general-purpose software.

---

## 1. Clinical Terminology Duplication

### What to look for

- LOINC, SNOMED CT, ICD-10, CPT, or RxNorm codes hardcoded as string literals in multiple files
- The same code value appearing in more than one location without a shared constant or lookup
- Inline mapping tables (e.g., `if code === '8867-4'`) scattered across services

### Healthcare context

Duplicated terminology codes are a patient-safety risk. When a code value needs updating (e.g., a LOINC code is deprecated), every occurrence must be found and changed. Missed occurrences produce silent clinical data errors.

### Refactoring direction

Extract codes to a shared terminology constants module or lookup service. Group by code system (LOINC, SNOMED, ICD-10). Include human-readable display names alongside codes. Prefer typed enums or objects over bare strings.

---

## 2. FHIR Resource Handling

### What to look for

- FHIR resources accessed via raw JSON paths (e.g., `resource.entry[0].resource.code.coding[0].code`) without type safety or null guards
- FHIR serialization/deserialization logic duplicated across endpoints or services
- Bundle processing that does not handle pagination or missing entries
- Resource type assumptions without checking `resourceType` field

### Healthcare context

Raw FHIR JSON access is fragile. FHIR resources have deeply nested optional fields, and different servers may populate profiles differently. Unguarded access paths cause runtime errors that silently drop clinical data.

### Refactoring direction

Wrap FHIR resources in typed accessors or use a FHIR client library that provides type safety. Centralize FHIR parsing into a resource layer. Handle missing fields explicitly rather than relying on optional chaining chains.

---

## 3. Clinical Data Formatting

### What to look for

- Date, time, unit, or numeric formatting logic duplicated across components or services
- Inconsistent date formats across the application (e.g., `MM/DD/YYYY` in one view, `YYYY-MM-DD` in another)
- Bare numbers displayed without units of measure
- Locale-sensitive formatting handled inline rather than through a shared utility

### Healthcare context

Inconsistent clinical data formatting is a patient-safety concern. Ambiguous date formats (`03/04/2026`) can be misread across international clinical teams. Missing units on measurements (displaying `98.6` without `°F`) create interpretation errors. Inconsistent numeric precision (e.g., `1.3` alongside `7.200`) erodes trust.

### Refactoring direction

Extract formatting utilities: `formatClinicalDate()`, `formatMeasurement()`, `formatLabValue()`. Store dates internally as ISO-8601; render using an unambiguous display format (DD Mon YYYY). Always pair values with UCUM-standard units.

---

## 4. Audit Trail Integrity

### What to look for

- Audit log statements that do not include the acting user identity
- Before/after data snapshots missing from update audit entries
- Audit logging concentrated in a middleware layer but absent in background jobs or async handlers
- Refactoring targets (e.g., extracting a service) that would move code away from existing audit instrumentation

### Healthcare context

HIPAA §164.312(b) requires audit controls. If refactoring breaks audit trail continuity — for example, by extracting a function that no longer triggers the audit middleware — access to ePHI becomes untracked. This is a compliance gap, not just a code-quality issue.

### Refactoring direction

Before extracting services or moving logic, verify that audit instrumentation follows the code path. If audit logging is middleware-based, ensure extracted services either remain in the middleware chain or implement their own audit events. Always include: actor identity, timestamp, action, affected resource, and before/after state for mutations.

---

## 5. Tenant Isolation

### What to look for

- Shared services that accept tenant or organization context as a parameter but do not enforce it at the data layer
- Query builders or ORM scopes that rely on callers to pass tenant filters
- Caching that uses keys without tenant namespacing
- Background jobs that process data across tenants in a shared context

### Healthcare context

Healthcare systems are frequently multi-tenant (multiple practices, hospitals, or organizations). A refactoring that introduces shared state, removes a tenant filter, or changes a cache key scheme can leak PHI across tenant boundaries. This is both a HIPAA violation and a patient-safety risk.

### Refactoring direction

When refactoring shared services, verify tenant isolation at every data access point. Prefer row-level security or mandatory tenant scoping in the data layer over application-level filtering. Audit cache key patterns after any refactoring that touches cached data.

---

## 6. Clinical Domain Naming

### What to look for

- Generic variable names for clinical concepts (e.g., `data`, `item`, `record` instead of `patient`, `observation`, `encounter`)
- Domain terms that have been genericized through abstraction (e.g., a `ResourceProcessor` that processes FHIR Patient and Observation identically without type distinction)
- Inconsistent naming for the same concept across modules (e.g., `patient_id`, `patientId`, `pid`, `subject` all referring to the same entity)

### Healthcare context

Clinical software benefits from ubiquitous language that matches domain terminology. When refactoring, renaming a variable from `encounter` to `session` or `visit` can break shared understanding between clinical and engineering teams. FHIR resource names (`Patient`, `Observation`, `Encounter`, `Condition`) are standard terms with precise meanings.

### Refactoring direction

Preserve clinical domain names during refactoring. Standardize on FHIR resource names when working with FHIR data. When consolidating naming, prefer the clinical term over the generic one. Document naming conventions in the codebase.

---

## 7. Error Handling in Clinical Paths

### What to look for

- Catch-all error handlers that silently swallow errors in clinical data processing
- Missing validation on clinical data inputs (lab values, medication dosages, patient identifiers)
- Error responses that expose internal implementation details or PHI in error messages
- Fail-open patterns where a service error results in displaying default or stale clinical data without indication

### Healthcare context

Error handling in clinical paths must be fail-safe: when something goes wrong, the system should make the failure visible rather than presenting potentially incorrect clinical data. A lab result display that silently falls back to cached data without indicating staleness could lead to clinical decisions based on outdated values.

### Refactoring direction

When refactoring error handling, prefer explicit failure surfaces over graceful degradation for clinical data. Display clear error states rather than stale data. Never include PHI in error messages, logs, or stack traces. Validate clinical data at input boundaries rather than trusting upstream systems.

---

# Part 2: Healthcare Overrides to Standard Refactoring

Standard refactoring heuristics apply to healthcare code, but the following clinical nuances modify how you apply them. When an agent or existing refactoring skill identifies a standard code smell, apply these overrides before recommending a fix.

---

### Long method / god class

- **Do not flag** a class solely for having many methods if the methods cohesively serve one clinical workflow (data ingestion → validation → transformation → audit is often correct in one unit).
- **Do flag** when patient-facing logic mixes with administrative logic or when clinical data transformation couples to infrastructure (caching, queues).
- When splitting classes, **preserve audit trail continuity** — extracted services must remain in the audit instrumentation chain.

### Dead code and feature flags

- Before removing dead code paths gated by feature flags, **verify clinical feature flags are not safety gates**. A flag gating a medication interaction check has compliance implications — removing it without confirming the feature is permanently active could disable a safety check.
- Check that deprecated endpoints are not referenced by **external integrations or partner systems** (EHR integrations, pharmacy networks, lab interfaces).

### Test coverage

- For clinical logic (dosage calculations, decision support rules, alert thresholds, eligibility checks), tests are a **prerequisite to refactoring**, not an afterthought. If tests are absent, the first refactoring step is adding characterization tests.
- Edge cases in clinical software are where **patient-safety incidents occur**. A dosage calculation that works for typical adult weights but fails for neonatal weights is a safety gap. Recommend equivalence partitioning for clinical value ranges (pediatric, adult, geriatric).
- Audit test quality, not just coverage percentage. High mock-to-assertion ratios provide false confidence.

### Code modularity and dependency direction

- Clear dependency direction is especially important in healthcare: domain/clinical logic at the center, infrastructure at the edges. This enables safe adoption of **new FHIR versions**, swapping EHR integrations, or meeting new **certification requirements** without cascading changes.

### Inline documentation

- Focus documentation effort on **clinical rationale** — the *why*, not the *what*. A threshold value of `140` in a blood-pressure check means stage-2 hypertension per ACC/AHA guidelines; a developer unfamiliar with the domain cannot infer this.
- **Document the source authority** for clinical magic numbers: guideline name, version, section.
- Clinical decision support rules, regulatory compliance logic, and safety checks **require documented intent** — refactoring risks breaking silently encoded invariants.
