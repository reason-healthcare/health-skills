# Regulatory And Jurisdiction Signals

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
| "GDPR" in code or docs | any file | EU (GDPR) | High |
| `DataSubjectRequest` model | schema | EU (GDPR) | High |
| `lawful_basis` field | schema | EU (GDPR) | High |
| `data_controller` / `data_processor` config | config | EU (GDPR) | High |
| "NIS2" or "essential entity" in docs | docs | EU (NIS2) | High |
| "MDR 2017/745" or "CE mark" in docs | docs | EU (MDR/IVDR) | High |
| "AI Act" or "high-risk AI" in docs | docs | EU (AI Act) | High |
| "EHDS" or "MyHealth@EU" reference | any file | EU (EHDS) | High |
| `consent_record` model without GDPR ref | schema | EU (GDPR) | Medium |
| EU member-state locale config | config | EU (jurisdiction) | Medium |

---

## EU Jurisdiction Signals

Use these signals to determine whether the repository likely targets EU healthcare delivery, EU health-data handling, or EU regulatory programs. The EU section is organized by regulatory regime, matching the structure of the US section above.

---

## GDPR Signals

Applies when the system processes personal data of EU residents, including health data (Article 9 special category).

### High-Confidence GDPR Signals

**Field and variable names** (case-insensitive, any naming convention):
- `data_subject`, `data_controller`, `data_processor`, `joint_controller`
- `lawful_basis`, `lawful_basis_code`, `processing_purpose`
- `consent_record`, `consent_withdrawn`, `consent_version`
- `right_to_erasure`, `erasure_request`, `deletion_request`
- `portability_request`, `data_portability`, `dsr` (data subject request)
- `dpa_url`, `dpo_email`, `supervisory_authority`
- `retention_policy`, `data_retention_days`

**Model / class / table names**:
- `DataSubjectRequest`, `ConsentRecord`, `ProcessingActivity`
- `LawfulBasis`, `DataRetentionPolicy`, `PrivacyNotice`
- `DataProtectionImpactAssessment`, `DPIA`

**API routes and endpoint strings**:
- `/gdpr/`, `/data-subject/`, `/erasure/`, `/portability/`, `/consent/`
- `/dsar/`, `/privacy/`, `/rights/`

**Explicit references** in code, comments, config, or docs:
- "GDPR", "General Data Protection Regulation", "Regulation (EU) 2016/679"
- "Article 6", "Article 9", "Article 13", "Article 17", "Article 28"
- "special categories", "special category data", "sensitive health data"
- "data protection officer", "DPO", "supervisory authority", "lead supervisory authority"
- "controller-processor agreement", "data processing agreement", "DPA"
- "standard contractual clauses", "SCC", "adequacy decision", "transfer impact assessment"
- "data breach notification", "72-hour notification"

**Dependencies** (package names, gem names, pip packages):
- `gdpr`, `django-gdpr-assist`, `gdpr-tools`, `consent-manager`
- Libraries with `dsar`, `privacy`, `consent` in their names in a healthcare context

### Medium-Confidence GDPR Signals

- `consent` model or table without explicit GDPR reference but alongside PHI fields
- Cookie consent configuration (`cookieconsent`, `consent_banner`, `cookie_policy`)
- `locale` config containing EU member-state codes (`de`, `fr`, `nl`, `es`, `it`, `pl`, etc.) with no US locales
- `privacy_by_design`, `privacy_by_default` comments or flags
- `anonymize`, `pseudonymize`, `de-identify` methods in a European context
- EU hosting or data residency config (`eu-west`, `eu-central`, `frankfurt`, `ireland`) without controller language

---

## EHDS Signals

Applies when the system participates in European Health Data Space primary-use or secondary-use data exchange.

### High-Confidence EHDS Signals

- Explicit references to `EHDS`, `European Health Data Space`, `Regulation (EU) 2025/327`
- `MyHealth@EU`, `cross-border patient summary`, `ePrescription cross-border`, `eLaboratory`
- IHE XCA (Cross-Community Access) or IHE XDS in a European deployment context
- `IPS` (International Patient Summary) with EU cross-border deployment context
- References to national contact points (NCP) or MyHealth@EU gateway integration

### Medium-Confidence EHDS Signals
- "primary use", "secondary use" of health data in an EU policy context
- "health data access body", "HDAB" references
- Cross-border patient identity matching in a European context

---

## MDR / IVDR Signals

Applies when the software may qualify as a medical device or in vitro diagnostic under EU Regulation 2017/745 (MDR) or 2017/746 (IVDR).

### High-Confidence MDR / IVDR Signals

- Explicit references to `MDR`, `MDR 2017/745`, `IVDR`, `IVDR 2017/746`
- `CE mark`, `CE marking`, `notified body`, `authorized representative`, `EU representative`
- `clinical evaluation`, `clinical evaluation report`, `CER`, `post-market clinical follow-up`, `PMCF`
- `unique device identifier`, `UDI`, `EUDAMED`
- `intended purpose`, `intended use` in a CE-marking or device-regulatory context
- IEC 62304, EN ISO 14971 referenced in a CE-marking or MDR context (note: these also appear in FDA contexts — require corroborating MDR evidence)
- `Summary of Safety and Clinical Performance`, `SSCP`

### Medium-Confidence MDR / IVDR Signals

- "device classification", "rule 11", "rule 22" (EU MDR device classification rules)
- "clinical investigation" in an EU device context
- "technical documentation" in a CE-marking context (may overlap FDA)

---

## EU AI Act Signals

Applies when the system includes AI or ML components that may qualify as high-risk AI under Regulation (EU) 2024/1689.

### High-Confidence EU AI Act Signals

- Explicit references to `AI Act`, `Regulation (EU) 2024/1689`, `high-risk AI system`
- `conformity assessment`, `technical documentation` in an AI Act context
- `fundamental rights impact assessment`, `FRIA`
- `human oversight`, `human-in-the-loop`, `meaningful human control` in an AI Act compliance context
- `EU database registration` for AI systems
- `post-market monitoring` plan for AI (in EU context)

### Medium-Confidence EU AI Act Signals

- AI/ML clinical decision support in a product that also has EU MDR signals (Annex III high-risk category)
- `risk management` documentation for AI/ML that cites EU rather than FDA guidance
- `transparency`, `explainability`, `bias` audit language in a clinical AI EU deployment context

---

## NIS2 Signals

Applies when the organization may qualify as an essential or important entity under Directive (EU) 2022/2555 (NIS2). Healthcare providers and digital health infrastructure in EU member states are in scope.

### High-Confidence NIS2 Signals

- Explicit references to `NIS2`, `NIS 2`, `Directive (EU) 2022/2555`
- `essential entity`, `important entity`, `CSIRT`, `national cybersecurity authority`
- `incident reporting` with a reference to an EU authority or 24/72-hour reporting obligation
- Supply chain security documentation referencing NIS2 obligations

### Medium-Confidence NIS2 Signals

- Incident response runbook in an EU healthcare deployment context (without explicit NIS2 citation)
- Cybersecurity risk management policy citing EU or member-state regulatory frameworks
- Business continuity and disaster recovery documentation with EU authority notification steps

---

## Jurisdiction Selection Heuristic

- Strong US-only evidence and no EU signals → `us`
- Strong EU-only evidence and no US signals → `eu`
- Meaningful evidence for both → `us+eu`
- Weak or contradictory evidence → `unclear`
- When `us+eu` is proposed, record US and EU evidence separately in the artifact so the interview can confirm each market independently.
