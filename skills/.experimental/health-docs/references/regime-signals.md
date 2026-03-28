# Regulatory Regime Signals

Use this reference in analyze mode Pass 1 to detect applicable regulatory regimes from codebase evidence. Present findings during the evidence-informed interview with confidence level and source locations.

Confidence levels: **high** (strong, specific indicators), **medium** (circumstantial but meaningful), **low** (weak signals, mention but do not assume).

---

## HIPAA / PHI Signals

A PHI-bearing system under HIPAA is one that creates, receives, maintains, or transmits protected health information. Look for these signals across code, configuration, schemas, tests, and documentation.

### High-Confidence PHI Signals

**Field and variable names** (case-insensitive, any naming convention):
- `ssn`, `social_security`, `social_security_number`
- `dob`, `date_of_birth`, `birth_date`, `birthdate`
- `mrn`, `medical_record_number`, `medical_record`
- `npi`, `national_provider_identifier`
- `patient_id`, `patientId`, `patient_identifier`
- `member_id`, `memberId`
- `diagnosis`, `diagnosis_code`, `icd_code`, `icd10`, `icd9`
- `rx`, `prescription`, `medication`, `drug_name`, `ndc_code`
- `insurance_id`, `payer_id`, `plan_id`
- `phi`, `ephi` (in comments, variable names, class names)

**Model / class / table names**:
- `Patient`, `patients`
- `Member`, `members`
- `Encounter`, `encounters`
- `Claim`, `claims`
- `Prescription`, `prescriptions`
- `MedicalRecord`, `ClinicalNote`, `LabResult`, `VitalSign`
- `Beneficiary`, `Enrollee`, `Insured`

**FHIR resource types** (any reference in code, configs, or routes):
- `Patient`, `Practitioner`, `Organization`, `Location`
- `Observation`, `Condition`, `MedicationRequest`, `Procedure`
- `Encounter`, `DiagnosticReport`, `DocumentReference`
- `Claim`, `Coverage`, `ExplanationOfBenefit`
- `Bundle`, `Composition`, `CarePlan`, `CareTeam`

**HL7 references**:
- HL7 v2 message segments: `MSH`, `PID`, `OBX`, `OBR`, `ORC`, `ADT`
- HL7 v3 namespace references
- `hl7` in dependency names, import paths, or comments

**Explicit HIPAA references** in code or docs:
- "HIPAA", "covered entity", "business associate", "PHI", "ePHI"
- "minimum necessary", "de-identified", "limited data set"

**Dependencies** (package names, gem names, pip packages):
- `hl7`, `ruby-hl7`, `health_seven`
- `fhir_models`, `fhir.resources`, `fhirclient`
- `blue-button`, `smart-on-fhir`
- `centrak`, `redox`, `health-gorilla` (vendor integrations)

---

### Medium-Confidence PHI Signals

- Fields named `dob`, `age`, `address`, `zip`, `zipcode`, `postal_code` — common but not specific to healthcare without corroborating signals
- `provider`, `physician`, `clinician`, `doctor` in model or field names
- References to clinical coding systems: `CPT`, `SNOMED`, `LOINC`, `RxNorm`, `NDC`
- File uploads with names like `clinical_document`, `lab_report`, `radiology`
- Audit log fields tracking `record_accessed`, `chart_viewed`, `patient_record`
- Environment variables named `PHI_*`, `HIPAA_*`, `BAA_*`

---

## ONC / 21st Century Cures Act Signals

Applies when the system creates, maintains, or provides access to electronic health information (EHI) subject to information blocking rules, or if it participates in health information exchange.

### High-Confidence ONC Signals

**SMART on FHIR auth patterns**:
- OAuth2 scopes containing `patient/`, `user/`, `system/` + FHIR resource type
- `.well-known/smart-configuration` endpoint or reference
- `launch`, `launch/patient`, `launch/encounter` scopes

**USCDI data elements** referenced in code or docs:
- "USCDI", "United States Core Data for Interoperability"
- Explicit mapping to USCDI v1/v2/v3 data classes

**EHR vendor SDKs and integrations**:
- Epic: `epicSDK`, `epic_sdk`, `fhir.epic.com`, `apporchard.epic.com`
- Cerner: `cerner`, `fhir.cerner.com`, `millennia`
- athenahealth: `athenahealth`, `athenanet`
- Allscripts, eClinicalWorks, NextGen in dependency or config

**FHIR bulk export / $everything operations**:
- `$everything`, `$export`, `$patient-everything`
- `_type`, `_since`, `_outputFormat` FHIR bulk parameters

### Medium-Confidence ONC Signals

- Any FHIR R4 API with patient-facing scopes
- References to "information blocking", "data sharing", "interoperability"
- CMS rule references ("CMS-9115", "interoperability rule")

---

## FDA SaMD Signals

Applies when the software is intended to diagnose, treat, mitigate, or prevent disease and meets the FDA's definition of a medical device or Software as a Medical Device.

### High-Confidence FDA SaMD Signals

**ML/AI clinical inference**:
- Model loading and inference in clinical pathways: `model.predict()`, `model.infer()`, `classify()` used with patient data
- Clinical risk score computation: "sepsis score", "readmission risk", "deterioration index", "early warning score"
- Triage or acuity scoring: "ESI", "NEWS2", "MEWS", "acuity", "triage_score"

**Diagnostic or treatment language in docs/comments**:
- "diagnose", "diagnosis", "differential diagnosis" in README, docs, or inline comments describing what the system does
- "recommend treatment", "treatment recommendation", "prescribe", "dosing recommendation"
- "detect", "screen for" used in clinical context

**Clinical terminology code lookups driving output**:
- ICD-10, SNOMED CT, or LOINC code lookups that drive displayed recommendations or alerts
- Risk stratification based on diagnosis codes
- Alert generation based on lab result thresholds

**Explicit regulatory references**:
- "SaMD", "software as a medical device", "FDA 510(k)", "De Novo", "PMA"
- "IEC 62304", "ISO 14971" in docs, comments, or project management artifacts

### Medium-Confidence FDA SaMD Signals

- "clinical decision support" in README or product description — may or may not be device-exempt CDS
- AI/ML feature flags in configs that toggle clinical-facing features
- Validation datasets described as "clinical" or containing patient outcomes

---

## Summary Detection Table

| Signal Type | Example | Regime | Confidence |
|---|---|---|---|
| `Patient` model with `mrn` field | `patient.mrn` | HIPAA | High |
| FHIR `MedicationRequest` resource | any reference | HIPAA | High |
| HL7 v2 `PID` segment parsing | `PID\|1\|...` | HIPAA | High |
| SMART on FHIR scope `patient/Patient.read` | OAuth2 config | ONC | High |
| `$export` FHIR operation | route or docs | ONC | High |
| `model.predict()` on patient vitals | clinical code | FDA SaMD | High |
| "readmission risk score" in README | documentation | FDA SaMD | High |
| `dob` field without other signals | schema | HIPAA | Medium |
| `provider` model name | schema | HIPAA | Medium |
| "clinical decision support" in README | documentation | FDA SaMD | Medium |
| `zipcode` field alone | schema | None | Low |
