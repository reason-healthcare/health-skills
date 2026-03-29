# FHIR R4 Resource Reference

FHIR R4 organizes its ~150 resources into categories. This reference covers the categories and individual resources most relevant to app developers, plus common modeling patterns.

---

## Resource Categories

### Clinical Resources
Represent patient health data — the core of most healthcare apps.

| Resource | Purpose |
|---|---|
| `Patient` | Demographics, identifiers, contact info for the person receiving care |
| `Practitioner` | Individual clinician or provider |
| `PractitionerRole` | Practitioner's role at an organization (specialty, location) |
| `Organization` | Healthcare org, payer, or other entity |
| `RelatedPerson` | Non-practitioner with a relationship to the patient (guardian, spouse) |
| `Observation` | Measurements and findings: vitals, lab results, social history, survey answers |
| `Condition` | Diagnosis, problem, or health concern |
| `Procedure` | Action performed on or for a patient (surgery, vaccination, counseling) |
| `AllergyIntolerance` | Allergy or intolerance, with reaction details |
| `MedicationRequest` | Prescription or order for a medication |
| `MedicationStatement` | Patient's reported or observed medication use |
| `Medication` | A specific medication (drug product) |
| `Immunization` | Vaccine administration event |
| `DiagnosticReport` | Result report for labs, imaging, genomics; groups Observations |
| `DocumentReference` | Pointer to a clinical document (CCD, PDF, FHIR Document) |
| `Encounter` | An interaction between patient and care provider (visit, admission, telehealth) |
| `EpisodeOfCare` | A period of care for a condition across multiple encounters |
| `CarePlan` | Planned set of actions for patient care |
| `Goal` | Desired health outcome for a patient |
| `ServiceRequest` | Order for a service (lab, imaging, referral, procedure) |
| `Appointment` | Booked time slot for an encounter |
| `Location` | Physical place where care is delivered |
| `Device` | Medical device (implant, wearable, equipment) |
| `DeviceUseStatement` | Record that a device was used by a patient |

### Workflow Resources
Coordinate tasks and activities across systems.

| Resource | Purpose |
|---|---|
| `Task` | A unit of work to be performed; tracks status (requested → in-progress → completed) |
| `Communication` | A message or communication event between parties |
| `CommunicationRequest` | A request for a communication to occur |
| `Flag` | Alert or note to draw attention (e.g., fall risk) |
| `RequestGroup` | Group of related requests with fulfillment logic |

### Financial Resources
Billing and coverage — relevant for revenue cycle and payer apps.

| Resource | Purpose |
|---|---|
| `Coverage` | Insurance coverage and payer details |
| `Claim` | Request for reimbursement or prior authorization |
| `ClaimResponse` | Payer's adjudication response to a Claim |
| `ExplanationOfBenefit` | Final processed claim with adjudication detail (EOB) |

### Infrastructure / Conformance Resources
Define structure and behavior — mostly read by developers, not authored in apps.

| Resource | Purpose |
|---|---|
| `StructureDefinition` | Defines a FHIR profile or extension |
| `ValueSet` | Set of coded values |
| `CodeSystem` | Defines a code system (LOINC, SNOMED, etc.) |
| `CapabilityStatement` | Server's declared supported interactions |
| `Bundle` | Container for multiple resources (transaction, search result set, document) |
| `OperationOutcome` | Error or warning messages from server operations |

---

## Key Resources by Domain

### Demographics and Identity
- **Patient** is the anchor. Every clinical resource references it.
- Use `Patient.identifier` for MRN, SSN, or other business identifiers. Use `id` (the FHIR logical ID) for internal server references.
- **Organization** for the care entity. **Practitioner** + **PractitionerRole** for the clinician with their role context.

### Observations (Vitals, Labs, Survey Responses)
- **Observation** covers almost all measurements. `Observation.code` (LOINC preferred) identifies what was measured. `Observation.value[x]` holds the result.
- Panel/battery results: use a parent `Observation` with `hasMember` references to component `Observation` resources — do not nest them as contained.
- **DiagnosticReport** groups observations into a result report. Labs are typically `DiagnosticReport` + `Observation` members. Imaging is `DiagnosticReport` + reference to `ImagingStudy`.

### Orders and Requests
- FHIR uses a request-event split: the *order* is a request resource, the *fulfillment* is an event resource.
  - `ServiceRequest` (order) → `Procedure` or `DiagnosticReport` (fulfillment)
  - `MedicationRequest` (order) → `MedicationDispense` or `MedicationAdministration` (fulfillment)
- **Task** tracks the fulfillment workflow state across systems.

### Encounters and Visits
- **Encounter** represents a single visit or interaction. Multiple encounters roll up to an **EpisodeOfCare**.
- Room/location changes during a hospitalization: `Encounter.location` is an array; each entry has a `period` and a reference to `Location`.
- `Encounter.class` (code: `AMB`, `IMP`, `EMER`, etc.) distinguishes care setting.

### Documents and Notes
- **DocumentReference** points to a document (PDF, CDA, or a FHIR Document Bundle). The document itself is not stored inside the resource — only a reference plus metadata.
- For structured clinical notes, use a FHIR Document Bundle (a `Bundle` with `type: document`) attached via `DocumentReference.content.attachment`.

---

## Complex Data Types

FHIR elements are not primitives alone. Most clinically meaningful elements are **complex data types** — composable structures with their own sub-elements. Understanding their composition is essential for correctly populating resources.

### Identifier

Used for business identifiers (MRN, NPI, SSN). Always include `system`.

| Element | Type | Notes |
|---|---|---|
| `system` | uri | Namespace URI that defines the identifier. E.g., `http://hospital.org/mrn` |
| `value` | string | The identifier value within that namespace |
| `use` | code | `usual | official | temp | secondary | old` |
| `type` | CodeableConcept | Category of identifier (e.g., `MR` for medical record) |
| `period` | Period | Time range when valid |
| `assigner` | Reference(Organization) | Org that issued the identifier |

```jsonc
{
  "identifier": [
    {
      "use": "usual",
      "system": "http://hospital.example.org/mrn",
      "value": "MRN-00123"
    }
  ]
}
```

### HumanName

Used on `Patient.name`, `Practitioner.name`.

| Element | Type | Notes |
|---|---|---|
| `use` | code | `usual | official | temp | nickname | anonymous | old | maiden` |
| `text` | string | Full name as a single string (fallback display) |
| `family` | string | Surname. Single value in R4 (not an array) |
| `given` | string[] | Given names — first element is first name, second is middle |
| `prefix` | string[] | Titles before name (Dr., Mr.) |
| `suffix` | string[] | Credentials or titles after name (Jr., MD) |
| `period` | Period | When name was/is in use |

```jsonc
{
  "name": [
    {
      "use": "official",
      "family": "Smith",
      "given": ["Jane", "Marie"],
      "prefix": ["Dr."]
    }
  ]
}
```

### Address

Used on `Patient.address`, `Organization.address`.

| Element | Type | Notes |
|---|---|---|
| `use` | code | `home | work | temp | old | billing` |
| `type` | code | `postal | physical | both` |
| `text` | string | Full address as a single string |
| `line` | string[] | Street lines — can have multiple |
| `city` | string | City or town |
| `district` | string | County or district |
| `state` | string | State/province (US: 2-letter code for US Core) |
| `postalCode` | string | ZIP or postal code |
| `country` | string | Country (ISO 3166 2-letter code recommended) |
| `period` | Period | Period when address was in use |

### ContactPoint

Used for phone, email, fax on Patient, Practitioner, Organization.

| Element | Type | Notes |
|---|---|---|
| `system` | code | `phone | fax | email | pager | url | sms | other` |
| `value` | string | The actual contact value (number, address) |
| `use` | code | `home | work | temp | old | mobile` |
| `rank` | positiveInt | Preferred order — lower is more preferred |
| `period` | Period | When in use |

### CodeableConcept

The most common coded type. Combines machine codes with a human display.

| Element | Type | Notes |
|---|---|---|
| `coding` | Coding[] | One or more coded representations |
| `text` | string | Human-readable string; used when no code fits or for display |

**Coding sub-elements**:

| Element | Type | Notes |
|---|---|---|
| `system` | uri | Code system URI (e.g., `http://loinc.org`) |
| `version` | string | Code system version; omit unless version-specific |
| `code` | code | The actual code |
| `display` | string | Human-readable name for the code in its system |
| `userSelected` | boolean | True if a user directly selected this code |

```jsonc
{
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "8867-4",
        "display": "Heart rate"
      }
    ],
    "text": "Heart rate"
  }
}
```

> Always include `system`. A code alone (without a system URI) is ambiguous and cannot be validated. `coding` is an array — you can include both a standard code and a local code; validators treat multiple codings as all being true simultaneously.

### Quantity

Used for measured values with units.

| Element | Type | Notes |
|---|---|---|
| `value` | decimal | Numeric value |
| `unit` | string | Human-readable unit string |
| `system` | uri | Code system for the unit — `http://unitsofmeasure.org` for UCUM |
| `code` | code | Coded unit (UCUM expression, e.g., `'/min'`, `'mg/dL'`) |
| `comparator` | code | `< | <= | >= | >` — when value is a bound, not exact |

```jsonc
{
  "valueQuantity": {
    "value": 72,
    "unit": "beats/minute",
    "system": "http://unitsofmeasure.org",
    "code": "/min"
  }
}
```

> For US Core vital signs, UCUM units are required (binding: required). Always populate both `unit` (human-readable) and `code` (UCUM).

### Reference

Links from one resource to another. See Pattern 1 below for when to use each form.

| Element | Type | Notes |
|---|---|---|
| `reference` | string | Relative or absolute URL to the target resource. E.g., `"Patient/123"` |
| `type` | uri | Resource type hint. Useful when `reference` is absent |
| `identifier` | Identifier | Logical reference by business identifier (cross-server) |
| `display` | string | Human-readable label only — not for machine processing or querying |

### Period

A time range with optional start and/or end. Open-ended on either side is valid.

| Element | Type | Notes |
|---|---|---|
| `start` | dateTime | Start of period (inclusive) |
| `end` | dateTime | End of period (exclusive per spec semantics) |

### Range

A bounded interval using two `SimpleQuantity` values.

| Element | Type | Notes |
|---|---|---|
| `low` | SimpleQuantity | Lower bound (value + unit only — no comparator) |
| `high` | SimpleQuantity | Upper bound |

### Ratio

A ratio of two quantities — common for medication concentrations and titers.

| Element | Type | Notes |
|---|---|---|
| `numerator` | Quantity | Numerator |
| `denominator` | Quantity | Denominator |

### Annotation

A text note with optional author and timestamp.

| Element | Type | Notes |
|---|---|---|
| `author[x]` | Reference(Practitioner\|Patient\|RelatedPerson\|Organization) or string | Who wrote the note — choice type (see below) |
| `time` | dateTime | When the note was written |
| `text` | markdown | The note content |

### Attachment

Binary or referenced content (documents, images, audio).

| Element | Type | Notes |
|---|---|---|
| `contentType` | code | MIME type (e.g., `application/pdf`, `image/png`) |
| `url` | url | Where to retrieve the content |
| `data` | base64Binary | Inline content, base64-encoded — use sparingly; prefer `url` |
| `title` | string | Human-readable label |
| `size` | unsignedInt | Bytes |
| `hash` | base64Binary | SHA-1 hash of the content at `url` |
| `language` | code | BCP-47 language code |
| `creation` | dateTime | When the attachment was created |

---

## Choice Types (Polymorphism)

FHIR uses `[x]` notation to mark **polymorphic elements** — elements that can hold one of several types. In an instance, you replace `[x]` with the PascalCase type name. Only one type variant may be present per element in a given instance.

### The Pattern

In the spec/profile: `onset[x]`
In the instance — pick exactly one:

```jsonc
{ "onsetDateTime": "2023-04-01" }           // or
{ "onsetAge": { "value": 45, "unit": "a" } } // or
{ "onsetPeriod": { "start": "2023-01-01" } } // or
{ "onsetString": "adolescence" }
```

You cannot have both `onsetDateTime` and `onsetAge` in the same resource instance.

### Common Choice Types by Resource

#### `Observation.value[x]`
The result of an observation. Choose the type that matches the measurement:

| Type | Use when |
|---|---|
| `valueQuantity` | Numeric measurement with units (heart rate, glucose) |
| `valueCodeableConcept` | Coded result (blood type, smoking status) |
| `valueString` | Free-text result |
| `valueBoolean` | Yes/No result |
| `valueInteger` | Whole-number result (APGAR score) |
| `valueRange` | A measurement expressed as a range |
| `valueRatio` | A ratio (e.g., titer 1:80) |
| `valueSampledData` | Time-series data (ECG waveform) |
| `valueTime` | A time-of-day result |
| `valueDateTime` | A point-in-time result |
| `valuePeriod` | A duration result |

If no value is available, omit `value[x]` entirely and populate `Observation.dataAbsentReason` instead.

#### `Condition.onset[x]` and `Condition.abatement[x]`

| Type | Use when |
|---|---|
| `onsetDateTime` | Exact or approximate date known |
| `onsetAge` | Age at onset known but not date |
| `onsetPeriod` | Onset occurred within a date range |
| `onsetRange` | Onset age is within an age range |
| `onsetString` | Only a text description is available |

`abatement[x]` uses the same set of types.

#### `Observation.effective[x]`

| Type | Use when |
|---|---|
| `effectiveDateTime` | Single point in time (most common) |
| `effectivePeriod` | Measurement taken over a duration |
| `effectiveTiming` | Recurring measurement schedule |
| `effectiveInstant` | Precise instant with timezone |

#### `MedicationRequest.medication[x]`

| Type | Use when |
|---|---|
| `medicationCodeableConcept` | Medication identified by code (RxNorm preferred) — simpler, more common |
| `medicationReference` | Reference to a `Medication` resource — use when dose form, ingredient, or lot details are needed |

#### Other Common Choice Types

| Element | Common types |
|---|---|
| `Patient.deceased[x]` | `deceasedBoolean` (is deceased), `deceasedDateTime` (date of death) |
| `MedicationRequest.reported[x]` | `reportedBoolean`, `reportedReference` (→ Practitioner/Patient/etc.) |
| `Annotation.author[x]` | `authorReference` (→ Practitioner/Patient/org), `authorString` (free text) |
| `Procedure.performed[x]` | `performedDateTime`, `performedPeriod`, `performedString`, `performedAge`, `performedRange` |
| `DiagnosticReport.effective[x]` | `effectiveDateTime`, `effectivePeriod` |
| `AllergyIntolerance.onset[x]` | `onsetDateTime`, `onsetAge`, `onsetPeriod`, `onsetRange`, `onsetString` |

### Querying Choice Types

FHIR search parameters for choice types use a single parameter name without the type suffix. For example, `Observation?date=2024-01-01` matches both `effectiveDateTime` and `effectivePeriod`. You do not need separate queries per type variant when searching.

---

### Pattern 1: The Reference Graph
FHIR models data as a graph of resources linked by `Reference`. The important decisions:

1. **Literal reference** (`reference: "Patient/123"`) — links by FHIR logical ID. Requires the target to be on the same server or accessible by the client.
2. **Logical (identifier) reference** (`identifier: { system: "...", value: "..." }`) — links by business identifier. Useful for cross-server scenarios or when the FHIR ID is unknown.
3. **`Reference.display`** — a human-readable string only; not machine-processable. Never rely on it for queries.

### Pattern 2: Contained Resources
A contained resource is fully embedded inside its parent (inside `resource.contained[]`). Use sparingly:
- **Use when**: the contained resource has no independent identity and will never be referenced from outside this resource (e.g., a one-time-use `Medication` inside a `MedicationRequest`).
- **Avoid when**: the contained resource needs to be searched, referenced from multiple places, or versioned independently.
- Contained resources cannot be contained themselves.

### Pattern 3: One-to-Many Relationships
FHIR handles one-to-many differently depending on direction:

| Relationship | FHIR approach |
|---|---|
| One Encounter → many Observations | Each Observation references the Encounter (`Observation.encounter`) |
| One DiagnosticReport → many Observations | `DiagnosticReport.result` array of references |
| One Patient → many Conditions | Each Condition references the Patient (`Condition.subject`) |
| One Observation with multiple components | `Observation.component` array (e.g., systolic + diastolic BP) |

### Pattern 4: Code + Text
Most coded elements follow the `CodeableConcept` pattern:
```json
{
  "coding": [
    {
      "system": "http://loinc.org",
      "code": "8867-4",
      "display": "Heart rate"
    }
  ],
  "text": "Heart rate"
}
```
- Always include `system` — codes without a system are ambiguous.
- `coding` can have multiple entries (LOINC + local code). The first is typically the primary.
- `text` is a fallback; do not use it as the primary machine-processable value.

### Pattern 5: Status and Lifecycle
Most resources have a `status` element that must be populated. Common patterns:
- `Condition.clinicalStatus` and `Condition.verificationStatus` are separate and both required in US Core.
- `Observation.status`: `registered | preliminary | final | amended | corrected | cancelled | entered-in-error | unknown`
- `Encounter.status`: `planned | arrived | triaged | in-progress | onleave | finished | cancelled`

Never omit `status` — many FHIR queries filter on it by default.

---

## FHIR R4 Spec Reference

Full resource list: `https://hl7.org/fhir/R4/resourcelist.html`

Each resource page includes: purpose, boundaries, relationships, formal definition, examples, and notes.
