# Example Model: Vital Sign Observation

This example demonstrates the full output of `health-fhir-modeling` in **model mode** for a common healthcare app use case.

---

## Domain Concept

> "We need to record a patient's heart rate measurement taken by a nurse during a clinic visit."

---

## Clarifying Questions Asked

Before recommending resources, the skill asked:

1. **What care setting?** — Ambulatory clinic visit
2. **Who produces this data vs. who consumes it?** — EHR produces; our app reads/displays
3. **Any specific interoperability profile required?** — System needs to be US Core compliant

---

## Candidate Resources Considered

| Resource | Fitness | Verdict |
|---|---|---|
| `Observation` | Measurements, findings, and assessments of any kind | **SELECTED** |
| `DiagnosticReport` | A report that groups observations — appropriate for a lab panel, not a single vital | REJECTED |
| `Procedure` | Actions performed — heart rate measurement is a finding, not a procedure | REJECTED |
| `DeviceUseStatement` | Device usage events — only relevant if the measurement device itself needs tracking | REJECTED |

**Primary resource: `Observation`**

Rationale: `Observation` is the canonical FHIR resource for any measurement or finding. A single vital sign is a direct `Observation` — not a report grouper (`DiagnosticReport`) and not an action record (`Procedure`). The US Core Vital Signs profile extends the base Observation to cover exactly this scenario.

---

## Applicable Profile

**US Core Vital Signs** — `http://hl7.org/fhir/us/core/StructureDefinition/us-core-vital-signs`

Must-support constraints relevant to this concept:

| Element | Constraint |
|---|---|
| `status` | Required; must be `final` for a completed measurement |
| `category` | Required slice: `vital-signs` from `http://terminology.hl7.org/CodeSystem/observation-category` |
| `code` | Must-support; LOINC code for the vital sign (see Terminology below) |
| `subject` | Must-support; Reference to `Patient` |
| `effective[x]` | Must-support; when the measurement was taken — prefer `effectiveDateTime` |
| `value[x]` | Must-support; the measurement value — `valueQuantity` with UCUM unit |
| `dataAbsentReason` | Must-support; required if `value[x]` is absent |

**Choice types**: `effective[x]` and `value[x]` are FHIR choice types — the `[x]` suffix is a polymorphic placeholder for multiple allowed types. `effectiveDateTime` (point-in-time) was selected over `effectivePeriod` (time range) because a nurse-taken measurement is recorded at a single instant. `valueQuantity` (numeric + UCUM unit) is the appropriate variant for a quantitative vital sign. See `references/fhir-r4-resources.md` — Choice Types section for the full type list for `Observation.value[x]` and `Observation.effective[x]`.

---

## Relationships Modeled

| Relationship | FHIR element | Notes |
|---|---|---|
| Measurement for a patient | `Observation.subject` → `Patient` | Literal reference recommended: `"reference": "Patient/123"` |
| Measurement during an encounter | `Observation.encounter` → `Encounter` | Include when encounter context is known |
| Measured by a clinician | `Observation.performer` → `Practitioner` or `PractitionerRole` | Use `PractitionerRole` if specialty/org context matters |

---

## Terminology

**Code for heart rate:**

| Element | Value |
|---|---|
| `Observation.code.coding.system` | `http://loinc.org` |
| `Observation.code.coding.code` | `8867-4` |
| `Observation.code.coding.display` | `Heart rate` |

**Binding**: US Core Vital Signs uses an extensible binding to LOINC vital sign codes. LOINC `8867-4` is in the ValueSet — use it.

**Unit for heart rate:**

| Element | Value |
|---|---|
| `valueQuantity.unit` | `beats/min` |
| `valueQuantity.system` | `http://unitsofmeasure.org` |
| `valueQuantity.code` | `/min` |

UCUM unit `"/min"` is the canonical form. The `unit` text field is human-readable only.

---

## Extension Usage

No extensions required. Heart rate is a first-class vital sign in FHIR R4 with a standard LOINC code and UCUM unit. Do not add extensions for data that fits within the base resource.

---

## Annotated Instance (JSONC — illustrative)

> **Note**: This uses JSON-with-Comments (JSONC) format for readability. It is illustrative, not directly parseable as standard JSON. To obtain a valid, parseable instance, strip all `//` comment lines.

```jsonc
{
  "resourceType": "Observation",
  "id": "heart-rate-example-001",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/us/core/StructureDefinition/us-core-vital-signs"
    ]
  },
  "status": "final",
  // status: "final" = measurement was completed and verified
  // Other options: "preliminary" (not yet confirmed), "amended" (corrected after finalization)

  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "vital-signs",
          "display": "Vital Signs"
        }
      ]
    }
  ],
  // category: CodeableConcept (complex data type — outer text label + one or more Coding entries)
  // required by US Core Vital Signs; must include "vital-signs" slice

  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "8867-4",
        "display": "Heart rate"
      }
    ],
    "text": "Heart rate"
  },
  // code.coding: LOINC 8867-4 is the standard code for heart rate
  // text is a human-readable fallback; always include system+code for machine use

  "subject": {
    "reference": "Patient/example-patient-001"
    // Literal reference: Patient must exist on the same server
    // Use identifier-based reference if Patient FHIR ID is not known:
    // "identifier": { "system": "http://hospital.example.org/mrn", "value": "MRN-12345" }
  },

  "encounter": {
    "reference": "Encounter/example-encounter-001"
    // Include when the visit context is available; improves data provenance
  },

  "effectiveDateTime": "2026-03-28T10:15:00-05:00",
  // effective[x] choice type: effectiveDateTime selected (point-in-time); use effectivePeriod for a measured time range
  // ISO 8601 with timezone offset is strongly preferred over UTC Z for clinical data

  "performer": [
    {
      "reference": "PractitionerRole/example-practitioner-role-001"
      // PractitionerRole preferred over bare Practitioner
      // when the role/organization context matters for the measurement
    }
  ],

  "valueQuantity": {
    // value[x] choice type: valueQuantity selected — Quantity is a FHIR complex data type (value + human-readable unit + UCUM system + UCUM code)
    "value": 72,
    "unit": "beats/min",
    "system": "http://unitsofmeasure.org",
    "code": "/min"
    // value: the numeric reading
    // unit: human-readable; "beats/min" is conventional
    // system + code: machine-processable UCUM canonical form
    // UCUM code for per-minute is "/min" — confirm against http://unitsofmeasure.org
  }

  // dataAbsentReason: omitted here because value[x] is present
  // If heart rate could not be obtained, omit valueQuantity and include:
  // "dataAbsentReason": {
  //   "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
  //                "code": "unable-to-obtain" }]
  // }
}
```

---

## Mapping Rationale Summary

| Decision | Choice | Why |
|---|---|---|
| Resource | `Observation` | Single measurement; not a grouped report or performed action |
| Profile | US Core Vital Signs | Required for US Core compliance; fits the scenario |
| Code system | LOINC | Standard for observations in US Core; extensible binding with existing LOINC code |
| Unit system | UCUM | Required by US Core for quantitative vitals |
| Subject link | Literal reference | Patient FHIR ID assumed available in the EHR system |
| Encounter link | Included | Improves clinical provenance and supports encounter-based queries |
| Extensions | None | All data fits base R4 elements |

---

## Conformance Notes

- The real instance (comments stripped) will pass `$validate?profile=http://hl7.org/fhir/us/core/StructureDefinition/us-core-vital-signs` on a server with US Core support.
- If the FHIR server does not support US Core validation, validate locally using the FHIR Validator jar: `https://github.com/hapifhir/org.hl7.fhir.core`.
- The `meta.profile` declaration is informational — the server validates based on the profile URL in the `$validate` call, not the `meta.profile` value.
