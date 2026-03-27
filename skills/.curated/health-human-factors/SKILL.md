---
name: health-human-factors
description: Review healthcare and EHR software interfaces against a comprehensive design style guide grounded in NIST, FDA, IEC 62366, ISO 9241, ISO 14971, WCAG 2.1, ONC SAFER, and HL7 FHIR standards. Produces a report-only assessment without modifying code or designs. Use when an agent needs to evaluate clinical UI screens, data display, forms, alerts, or workflows for patient-safety, usability, accessibility, and data-clarity compliance.
---

# EHR Design Review

## Overview

Use this skill to inspect healthcare or EHR software screens, components, mockups, or code and produce a structured report of design issues mapped to established healthcare usability and safety standards. The review covers patient identity, layout, color, typography, data display, numeric formatting, units, dates, alerts, medication safety, forms, accessibility, workflow, audit logging, error prevention, terminology, interoperability, internationalization, security, and documentation.

## Operating Rules

- Never change code, designs, configurations, or documentation.
- Do not present the output as a formal certification or regulatory determination.
- Bias toward observable evidence from the artifacts under review and clearly separate:
  - confirmed violations from the code, markup, design, or config
  - likely inferences from surrounding implementation
  - areas that require runtime testing, user research, or policy validation
- When a guideline cannot be evaluated from the provided artifacts, mark it as not assessable rather than passing or failing.

## Workflow

1. Confirm the scope: which screens, components, modules, or code paths to review.
2. Load `references/style-guide.md` to access the full design criteria.
3. Walk through each review category (see categories below) against the artifacts in scope.
4. Assign severity and confidence for each finding.
5. Produce a report only. Do not draft fixes, patches, or redesigns unless explicitly asked.

## Review Categories

Each category maps to a section of the style guide reference.

1. **Patient Context and Identity** — persistent header, required identifiers, patient-switch confirmation, environment indicators
2. **Layout and Information Hierarchy** — summary order, navigation depth, click efficiency, cross-module consistency
3. **Color Standards** — semantic color use, dual-coding (never color-only), WCAG contrast ratios
4. **Typography** — font legibility, size minimums, avoidance of condensed or decorative fonts
5. **Data Tables and Clinical Data Display** — alignment, column consistency, sorting, filtering, reference ranges, abnormal value marking
6. **Numeric Formatting** — thousands separators, decimal precision, trailing zeros
7. **Units of Measure** — units always displayed, UCUM preference, no bare numbers
8. **Date and Time Formatting** — ISO-8601 storage, unambiguous display (DD Mon YYYY), 24-hour time
9. **Alerts and Clinical Decision Support** — alert levels, fatigue prevention, override documentation, clear explanations
10. **Medication Safety** — dangerous abbreviation avoidance, structured order display, trailing-zero prevention
11. **Forms and Data Entry** — structured input preference, autocomplete, range display, immediate validation
12. **Accessibility** — WCAG 2.1 AA compliance, keyboard navigation, screen reader support, focus indicators, no hover-only information
13. **Workflow Optimization** — click reduction, persistent key data, minimal modals, quick patient navigation
14. **Audit Logging** — user, timestamp, action, before/after data, location in audit records
15. **Error Prevention** — proactive constraints, range warnings, input validation before submission
16. **Clinical Terminology Standards** — SNOMED CT, LOINC, ICD-10 usage for coded concepts
17. **Interoperability and Data Exchange** — HL7 FHIR resource alignment, structured data exchange
18. **Internationalization** — multi-language support, locale-aware formatting, standardized internal representation
19. **Security and Privacy** — RBAC, session timeouts, encryption, audit logs, HIPAA alignment
20. **Documentation and Help** — contextual help, error explanations, training materials, workflow guides

## Constraints

- Review only — do not propose code changes unless the user explicitly requests remediation guidance.
- Stay within the scope described in the frontmatter.
- Surface patient-safety implications with the highest priority.
- Distinguish between must-fix safety issues and nice-to-have improvements.
- When artifacts are insufficient to evaluate a category, say so rather than guessing.

## Resources

- `references/style-guide.md`: full Healthcare Software Design Style Guide with criteria, examples, and source standards

## Output Contract

Return a review report with:

- **Executive Summary**: overall assessment, highest-risk findings, and scope of review
- **Scope**: artifacts reviewed, categories assessed, categories not assessable
- **Findings Table** with columns:
  - ID
  - Severity (critical / major / minor / info)
  - Category (from the 20 review categories)
  - Location (file, screen, component, or line reference)
  - Finding (what was observed)
  - Guideline (which standard or rule applies)
  - Risk (patient-safety or usability impact)
  - Confidence (confirmed / likely / unclear)
- **Category Coverage Matrix**: for each of the 20 categories — compliant, partial, non-compliant, or not assessable
- **Positive Observations**: areas where the design follows the guidelines well
- **Open Questions**: areas requiring runtime testing, user research, or additional artifacts
- **Standards Basis**: list of standards referenced in the review
