# Reason: Healthcare Tech Skills

Shared AI skills for building healthcare technology software and digital health products. These skills are created by [Vermonster](https://vermonster.com), a software studio with over 15 years of experience building healthcare technology systems.

## Install

Install the full skill collection from this repository:

```bash
npx skills add https://github.com/reason-healthcare/health-skills/tree/dist
```
See also: [npx skill docs](https://skills.sh/)

## Skills

### [`health-fhir-api-design`](skills/.curated/health-fhir-api-design)

Design FHIR R4 API interactions — search queries, operations (`$`), validation, workflow patterns, and custom SearchParameter / OperationDefinition resources. Provide your requirements; the skill recommends a concrete R4 approach with trade-offs.

### [`health-hipaa-review`](skills/.curated/health-hipaa-review)

Produce a report-only HIPAA, PHI, and PII audit for healthcare codebases and delivery systems. Inspects code, configs, data flows, integrations, logging, and deployment boundaries for privacy and security gaps without modifying code.

### [`health-human-factors`](skills/.curated/health-human-factors)

Review healthcare and EHR software interfaces against a comprehensive design style guide grounded in NIST, FDA, IEC 62366, ISO 9241, ISO 14971, WCAG 2.1, ONC SAFER, and HL7 FHIR standards. Produces a report-only assessment of patient safety, usability, accessibility, and data clarity without modifying code or designs.

### [`health-product-discovery`](skills/.curated/health-product-discovery)

Map incentive structures, adoption dynamics, and clinical workflow constraints before shaping solutions. Supports explore and document modes for early-stage ideation, consulting, pilot scoping, and strategic planning.

### [`health-refactor`](skills/.curated/health-refactor)

Produce a scope-bounded, plan-only refactoring assessment for healthcare codebases. Resolves a bounded file set via git range, file area, or symbol/dependency context, then orchestrates three analysis passes — healthcare-aware code refactoring, human-factors review, and HIPAA audit — into a unified plan with findings and a prioritized checklist. Never modifies code.

## Experimental Skills

The following skills are under active development and not yet published to the distribution branch.

### [`health-docs`](skills/.experimental/health-docs)

Audit and consolidate documentation for healthcare software systems. Supports two modes: **analyze** (coverage assessment against a seven-dimension hierarchy with regulatory regime detection) and **document** (consolidate existing docs and fill required gaps). Produces a persistent `.health-docs/analysis.md` handoff artifact and composes existing healthcare skills for deep review passes.

---

For contributing and skill development, see [DEVELOPER.md](https://github.com/reason-healthcare/health-skills/blob/main/DEVELOPER.md).
