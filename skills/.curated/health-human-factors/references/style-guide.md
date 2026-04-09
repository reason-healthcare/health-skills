# Healthcare Software Design Style Guide (EHR Systems)

Comprehensive design criteria synthesized from NIST Health IT Usability Guides, FDA Human Factors Engineering, IEC 62366 Usability Engineering, ISO 9241 Human-Computer Interaction, ISO 14971 Risk Management, WCAG 2.1 Accessibility, ONC SAFER Guides, clinical informatics best practices, and HL7 FHIR interoperability standards.

Use this reference during reviews. Each section maps to a review category in the skill.

---

## 1. Core Design Principles

All design decisions must prioritize:

1. Patient safety
2. Error prevention
3. Clarity of clinical information
4. Low cognitive load
5. Traceability and auditability
6. Consistency across the application
7. Accessibility for all users

Clinical users operate under time pressure; interfaces must support rapid interpretation and minimal navigation.

---

## 2. Patient Context and Identity

Patient identity must always be visible.

### Required header elements

Every patient view must display:

- Full patient name
- Date of birth
- Medical record number
- Age
- Sex or gender (if clinically relevant)
- Photograph (if available)

Example layout:

```
John Smith | DOB: 1975-02-21 | Age: 51 | MRN: 482194
```

### Safety rules

- Patient identifiers must appear in a persistent header
- When switching patients, the interface must visually confirm the change
- Color changes or banner alerts should indicate test vs production environments

---

## 3. Layout and Information Hierarchy

Clinical interfaces must prioritize critical information.

### Standard patient summary order

1. Patient identity
2. Allergies
3. Active medications
4. Problem list
5. Vitals
6. Lab results
7. Orders
8. Notes
9. Historical data

### Design rules

- Avoid deep navigation trees
- Reduce clicks for frequent workflows
- Use consistent layouts across modules

---

## 4. Color Standards

Color must support meaning but never be the sole indicator.

| Color  | Meaning              |
| ------ | -------------------- |
| Red    | critical / abnormal  |
| Orange | warning              |
| Yellow | caution              |
| Green  | normal               |
| Blue   | informational        |
| Gray   | disabled or inactive |

### Accessibility rules

Follow WCAG contrast standards:

| Element     | Minimum Contrast |
| ----------- | ---------------- |
| normal text | 4.5:1            |
| large text  | 3:1              |

Violations to flag:

- red/green only indicators
- low contrast color palettes
- decorative color gradients

---

## 5. Typography

Readable typography is essential for clinical accuracy.

### Font requirements

Use highly legible sans-serif fonts:

- Inter
- Source Sans
- Roboto
- Segoe UI

### Typography rules

| Element   | Size     |
| --------- | -------- |
| body text | 16 px    |
| tables    | 14–16 px |
| headers   | 18–24 px |

Violations to flag:

- condensed fonts
- italics for important data
- decorative fonts

---

## 6. Data Tables and Clinical Data Display

Most clinical information is presented in tables.

### Table design rules

- align numbers to the right
- align text left
- maintain consistent column order
- support sorting and filtering
- show reference ranges for labs

Example:

| Test       | Value | Unit  | Reference Range |
| ---------- | ----- | ----- | --------------- |
| Creatinine | 1.34  | mg/dL | 0.6–1.3         |

Abnormal values must be visually marked:

```
Creatinine: 1.34 mg/dL ▲
```

---

## 7. Numeric Formatting

Clinical numbers must be precise and readable.

### Rules

- use thousands separators when appropriate
- limit decimals to clinically relevant precision
- avoid trailing zeros unless meaningful

| Measurement    | Format       |
| -------------- | ------------ |
| Blood pressure | integer      |
| Temperature    | 1 decimal    |
| Lab values     | 1–3 decimals |

Example:

```
Temperature: 37.2 °C
Weight: 72 kg
```

---

## 8. Units of Measure

All measurements must display units.

Preferred unit system: Unified Code for Units of Measure (UCUM).

| Measurement    | Unit  |
| -------------- | ----- |
| Blood pressure | mmHg  |
| Temperature    | °C    |
| Weight         | kg    |
| Glucose        | mg/dL |

Never display numbers without units.

---

## 9. Date and Time Formatting

Ambiguous dates are a major safety risk.

### Internal storage

Use ISO-8601:

```
YYYY-MM-DD
```

### Display format

Preferred display:

```
11 Mar 2026
```

### Time

Use 24-hour format:

```
14:30
```

Violations to flag:

```
03/04/2026
```

because it is ambiguous internationally.

---

## 10. Alerts and Clinical Decision Support

Alerts must be carefully designed to prevent alert fatigue.

### Alert levels

| Level    | Use                     |
| -------- | ----------------------- |
| Info     | informational message   |
| Warning  | potential issue         |
| Critical | immediate clinical risk |

### Design rules

- limit non-critical alerts
- allow overrides with documentation
- clearly explain reason for alert

Example:

```
⚠ Drug interaction detected
Warfarin + Trimethoprim
Risk: increased bleeding
```

---

## 11. Medication Safety

Medication interfaces must follow strict conventions.

### Dangerous abbreviations to flag

| Unsafe | Use Instead         |
| ------ | ------------------- |
| U      | units               |
| IU     | international units |
| qd     | daily               |
| qod    | every other day     |

Correct order example:

```
Morphine 5 mg IV every 4 hours
```

Violation to flag:

```
Morphine 5.0 mg
```

(trailing zero creates dosing ambiguity)

---

## 12. Forms and Data Entry

Data entry errors are common in clinical systems.

### Design principles

- minimize free text where structured data exists
- provide autocomplete for medications and diagnoses
- display allowable ranges for numeric values
- validate inputs immediately

Example:

```
Dose: 0.5 mg
Allowed range: 0.1–1 mg
```

---

## 13. Accessibility

Healthcare systems must meet WCAG 2.1 AA.

Requirements:

- keyboard navigation
- screen reader compatibility
- clear focus indicators
- descriptive labels
- accessible error messages

Violations to flag:

- color-only indicators
- hover-only information
- inaccessible charts

---

## 14. Workflow Optimization

Clinical workflows must reduce cognitive burden.

### Design rules

- reduce clicks for frequent actions
- keep key patient data visible
- avoid modal dialogs that hide information
- allow quick navigation between patients

---

## 15. Audit Logging

All clinically relevant actions must be logged.

Required audit record elements:

- user
- timestamp
- action
- data before
- data after
- location

Example:

```
Dr. Smith
2026-03-11 14:32
Changed insulin dose
10 units → 12 units
```

---

## 16. Error Prevention

Systems must prevent errors rather than rely on correction.

Good example:

```
Dose range: 0.1–1 mg
Entered: 5 mg
⚠ Out of range
```

Bad example:

```
Dose: ______
```

(no constraints or guidance)

---

## 17. Clinical Terminology Standards

Clinical concepts must use standardized codes.

Required standards:

- SNOMED CT
- LOINC
- ICD-10

These ensure interoperability between systems.

---

## 18. Interoperability and Data Exchange

Healthcare software should support structured data exchange.

Recommended standard: HL7 FHIR

FHIR resources commonly used in EHRs:

- Patient
- Observation
- Medication
- Condition
- Encounter
- Procedure
- AllergyIntolerance

---

## 19. Internationalization

Healthcare systems should support:

- multiple languages
- locale-specific date formatting
- metric and imperial unit display

Internal data representation must remain standardized regardless of display locale.

---

## 20. Security and Privacy

Systems must protect patient data.

Key requirements:

- role-based access control
- session timeouts
- encrypted data storage
- audit logs
- HIPAA compliance where applicable

---

## 21. Testing and Validation

Usability testing must include real clinicians.

Testing methods:

- task-based usability testing
- simulation of clinical workflows
- error scenario testing
- accessibility testing

---

## 22. Documentation and Help

Clinical software must include:

- contextual help
- clear error explanations
- training documentation
- workflow guides
