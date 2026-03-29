# US Core Implementation Guide — Developer Reference

Full IG: `https://hl7.org/fhir/us/core/STU5.0.1/`

---

## Why US Core Exists

US Core is the **baseline conformance requirement for health IT systems in the United States**. It is not optional for systems that need to interoperate with hospitals, payers, or other providers.

### Regulatory Drivers

| Rule | Requirement |
|---|---|
| **21st Century Cures Act (2016)** | Prohibits information blocking; requires EHRs to support patient access APIs |
| **ONC 21st Century Cures Final Rule (2020)** | Mandates FHIR R4 + US Core for certified EHR technology |
| **CMS Interoperability and Patient Access Rule (2020)** | Requires payers to expose patient data via FHIR APIs conforming to US Core |
| **ONC HTI-1 Rule (2024)** | Strengthens USCDI requirements and extends to additional data classes |

### USCDI and US Core

The **United States Core Data for Interoperability (USCDI)** is an ONC-maintained list of data classes and elements that must be supported. US Core profiles are the FHIR representation of USCDI — each USCDI data element maps to one or more US Core must-support elements.

> **Practical implication for app developers**: If your app connects to a US-certified EHR, you will receive US Core-conformant resources. Building against US Core means your parsing logic will work across certified systems.

---

## Version in This Guide

This reference covers **US Core 5.0.1 (STU 5)**, which corresponds to USCDI v3 and is mandated by the ONC HTI-1 rule.

> **Coverage scope**: Detailed must-support tables are provided for five resources only: Patient, Observation, Condition, Encounter, and MedicationRequest. For any other US Core profile, consult the full IG at `https://hl7.org/fhir/us/core/STU5.0.1/` — do not generate must-support details from memory for uncovered resources.

---

## What "Must Support" Means in US Core

US Core defines Must Support (`MS`) more concretely than base FHIR:

- **Server (producer)**: SHALL be capable of populating this element. If the data exists in the source system, it MUST be sent. If it is never available for any patient, the server must document this in its CapabilityStatement.
- **Client (consumer)**: SHALL be capable of processing the element without error — cannot silently drop or fail when it is present.

Must Support does NOT mean the element is required to be present in every instance. An `Observation` without a result is still valid if the result is not yet available — but the server must support sending it when it exists.

---

## Binding Strength — Practical Guide

| Strength | What the developer MUST do |
|---|---|
| **required** | Code MUST come from this ValueSet. A server validates this; anything else will fail `$validate`. |
| **extensible** | Code SHOULD come from this ValueSet. Use another code only if the ValueSet has no suitable concept. Preferred in most US Core elements. |
| **preferred** | Code SHOULD come from this ValueSet; deviation is less tightly enforced. |
| **example** | ValueSet is illustrative only; no conformance obligation. |

**Practical rule**: if the ValueSet has a code that fits, use it — regardless of strength. Binding strength only governs what happens when no fitting code exists in the ValueSet.

---

## US Core Patient (v5.0.1)

Profile URL: `http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient`

### Must-Support Elements

| Element | Req | Notes |
|---|---|---|
| `Patient.identifier` | MS | At least one identifier required (slice: `us-core-uscdi-requirement`) |
| `Patient.identifier.system` | MS | URI identifying the namespace (e.g., MRN system URL) |
| `Patient.identifier.value` | MS | The identifier value |
| `Patient.name` | MS | At least one name required |
| `Patient.name.family` | MS | Last name |
| `Patient.name.given` | MS | First/middle name(s) |
| `Patient.telecom` | MS | Phone, email |
| `Patient.gender` | MS + required binding | `male | female | other | unknown` (AdministrativeGender) |
| `Patient.birthDate` | MS | ISO 8601 date |
| `Patient.address` | MS | Structured address |
| `Patient.address.line` | MS | Street address |
| `Patient.address.city` | MS | City |
| `Patient.address.state` | MS | Two-letter state code (extensible: USPS 2-letter codes) |
| `Patient.address.postalCode` | MS | ZIP code |
| `Patient.communication` | MS | |
| `Patient.communication.language` | MS + extensible binding | Language code (BCP-47) |
| `Patient.extension:race` | MS | US Core Race extension — up to 5 OMB category codes |
| `Patient.extension:ethnicity` | MS | US Core Ethnicity extension — OMB codes |
| `Patient.extension:birthsex` | MS | US Core Birth Sex extension — required binding to BirthSex codes |

### Key Notes
- `gender` is administrative gender (for records), not clinical gender — important distinction.
- Race and ethnicity use US Core-defined extensions, not base R4 elements.
- `Patient.deceased[x]` and `Patient.maritalStatus` are base R4 elements; not MS in US Core but commonly populated.

---

## US Core Observation (v5.0.1)

Applies to: laboratory results, vitals, smoking status, survey responses, and more.

Profile URL (laboratory): `http://hl7.org/fhir/us/core/StructureDefinition/us-core-observation-lab`
Profile URL (vitals): `http://hl7.org/fhir/us/core/StructureDefinition/us-core-vital-signs`

### Must-Support Elements (Laboratory)

| Element | Req | Notes |
|---|---|---|
| `Observation.status` | MS + required binding | `final | preliminary | amended | corrected | cancelled | entered-in-error` |
| `Observation.category` | MS | Slice: `laboratory` code from `http://terminology.hl7.org/CodeSystem/observation-category` |
| `Observation.code` | MS + extensible binding | LOINC code identifying what was measured |
| `Observation.subject` | MS | Reference to `Patient` |
| `Observation.effective[x]` | MS | When the observation was made |
| `Observation.value[x]` | MS | The result — Quantity, CodeableConcept, string, etc. |
| `Observation.dataAbsentReason` | MS | Required when `value[x]` is absent — says why |
| `Observation.interpretation` | MS | High/Low/Normal indicator |
| `Observation.referenceRange` | MS | Normal range context |

### Key Notes
- When there is no value, `dataAbsentReason` MUST be present. Do not send an empty `value[x]`.
- For **vital signs**, use the `us-core-vital-signs` profile; it requires `Observation.category` = `vital-signs` and has UCUM units constraints.
- For a **multi-component observation** (e.g., blood pressure), use `Observation.component` — not separate Observation resources.

---

## US Core Condition (v5.0.1)

Profile URL: `http://hl7.org/fhir/us/core/StructureDefinition/us-core-condition-problems-health-concerns`

### Must-Support Elements

| Element | Req | Notes |
|---|---|---|
| `Condition.clinicalStatus` | MS + required binding | `active | recurrence | relapse | inactive | remission | resolved` |
| `Condition.verificationStatus` | MS + required binding | `unconfirmed | provisional | differential | confirmed | refuted | entered-in-error` |
| `Condition.category` | MS + extensible binding | `problem-list-item` or `health-concern` |
| `Condition.code` | MS + extensible binding | ICD-10-CM or SNOMED CT |
| `Condition.subject` | MS | Reference to `Patient` |
| `Condition.onset[x]` | MS | When condition started |
| `Condition.abatement[x]` | MS | When condition resolved/abated |
| `Condition.recordedDate` | MS | When this was recorded |

### Key Notes
- **Both** `clinicalStatus` and `verificationStatus` are required together. A common mistake is populating only one.
- `Condition.code` binding is extensible — ICD-10-CM is standard in the US; SNOMED CT is acceptable.
- US Core has a second Condition profile for encounter diagnoses: `us-core-condition-encounter-diagnosis` — same structure, `category` sliced to `encounter-diagnosis`.

---

## US Core Encounter (v5.0.1)

Profile URL: `http://hl7.org/fhir/us/core/StructureDefinition/us-core-encounter`

### Must-Support Elements

| Element | Req | Notes |
|---|---|---|
| `Encounter.identifier` | MS | Encounter identifier (visit number, etc.) |
| `Encounter.status` | MS + required binding | `planned | arrived | triaged | in-progress | onleave | finished | cancelled` |
| `Encounter.class` | MS + extensible binding | `AMB` (ambulatory), `IMP` (inpatient), `EMER` (emergency), etc. — ActEncounterCode |
| `Encounter.type` | MS + extensible binding | Type of encounter (SNOMED or CPT) |
| `Encounter.subject` | MS | Reference to `Patient` |
| `Encounter.participant` | MS | Practitioners involved |
| `Encounter.participant.type` | MS | Role of the participant |
| `Encounter.participant.period` | MS | When they participated |
| `Encounter.participant.individual` | MS | Reference to `Practitioner` or `PractitionerRole` |
| `Encounter.period` | MS | Start and end of encounter |
| `Encounter.reasonCode` | MS | Reason for visit (extensible: ICD-10, SNOMED) |
| `Encounter.reasonReference` | MS | Reference to Condition, Procedure, etc. |
| `Encounter.hospitalization.dischargeDisposition` | MS | Discharge destination |
| `Encounter.location` | MS | Location(s) during encounter |
| `Encounter.location.location` | MS | Reference to `Location` |
| `Encounter.serviceProvider` | MS | Reference to `Organization` |

### Key Notes
- `class` uses ActEncounterCode from v3 — not intuitive; common values: `AMB`, `IMP`, `EMER`, `VR` (virtual).
- Location changes during inpatient: add multiple `Encounter.location` entries each with a `period`. Do not create new Encounter resources per room.

---

## US Core MedicationRequest (v5.0.1)

Profile URL: `http://hl7.org/fhir/us/core/StructureDefinition/us-core-medicationrequest`

### Must-Support Elements

| Element | Req | Notes |
|---|---|---|
| `MedicationRequest.status` | MS + required binding | `active | on-hold | cancelled | completed | entered-in-error | stopped | draft | unknown` |
| `MedicationRequest.intent` | MS + required binding | `proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option` |
| `MedicationRequest.reported[x]` | MS | Whether this is patient-reported |
| `MedicationRequest.medication[x]` | MS + extensible binding | Either `medicationCodeableConcept` (RxNorm) or `medicationReference` → `Medication` |
| `MedicationRequest.subject` | MS | Reference to `Patient` |
| `MedicationRequest.encounter` | MS | Associated encounter |
| `MedicationRequest.authoredOn` | MS | When the prescription was written |
| `MedicationRequest.requester` | MS | Prescribing practitioner |
| `MedicationRequest.dosageInstruction` | MS | Dosing details |
| `MedicationRequest.dosageInstruction.text` | MS | Human-readable dosage |
| `MedicationRequest.dosageInstruction.timing` | MS | Schedule |
| `MedicationRequest.dosageInstruction.doseAndRate` | MS | Dose amount |
| `MedicationRequest.dosageInstruction.doseAndRate.dose[x]` | MS | Quantity |

### Key Notes
- `medication[x]` — for most modern implementations, prefer `medicationCodeableConcept` with RxNorm over a referenced `Medication` resource; simpler and more widely supported.
- `intent = order` for a prescriber-initiated order; `intent = plan` for a suggested/protocol medication.
- `MedicationRequest.reported[x]` — `reportedBoolean: true` when the patient reports taking something not ordered in this system.

---

## Common US Core Extension URLs

| Extension | URL |
|---|---|
| US Core Race | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-race` |
| US Core Ethnicity | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity` |
| US Core Birth Sex | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex` |
| US Core Gender Identity | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity` |
| US Core Tribal Affiliation | `http://hl7.org/fhir/us/core/StructureDefinition/us-core-tribal-affiliation` |

Use these extensions as-is. Do not invent parallel extensions for the same concepts.
