# Reason: Healthcare Tech Skills

[![Skill Quality Gate](https://github.com/reason-healthcare/health-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/reason-healthcare/health-skills/actions/workflows/ci.yml)

Shared AI skills for building healthcare technology software and digital health products. These skills are created by [Vermonster](https://vermonster.com), a software studio with over 15 years of experience building healthcare technology systems.

## Install

Install the full skill collection from this repository:

```bash
npx skills add https://github.com/reason-healthcare/health-skills/tree/dist
```
See also: [npx skill docs](https://skills.sh/)

## Skills

Each skill works independently — invoke any one in isolation for its specific purpose. They are also designed to work in concert across a natural development lifecycle: discover the problem space, model and implement a solution, then verify it.

```
                    Health Skills — Development Lifecycle

┌───────────────────────┐
│   Planning            │
├───────────────────────┤
│ ┌───────────────────┐ │
│ │ Health            │ │ ◀─────────────────────────┐ 
│ │ Product Discovery │ │                           │
│ └───────────────────┘ │                           │
└───────────────────────┘                           │
          │                                         │
          ▼                                         │
┌─────────────────────────────────────────┐         │
│   Implementation                        │         │
├─────────────────────────────────────────┤         │
│ ┌─────────────────┐ ┌─────────────────┐ │         │
│ │ Health          │ │ Health          │ │ ◀───────┤
│ │ FHIR API Design │ │ FHIR Modeling   │ │         │
│ └─────────────────┘ └─────────────────┘ │         │
└─────────────────────────────────────────┘         │
          │                                         │
          ▼                                         │
┌─────────────────────────────────────────────────────────────┐
│   Verification                                              │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │ 
│ │ Health          │ │ Health          │ │ Health          │ │
│ │ Refactor        │ │ HIPAA Review    │ │ Human Factors   │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

### [`health-docs`](skills/.curated/health-docs)

Audit and consolidate documentation for healthcare software systems. Supports two modes: **analyze** (coverage assessment against a seven-dimension hierarchy with regulatory regime detection across HIPAA, HL7 FHIR, ONC 21st Century Cures, and FDA frameworks) and **document** (consolidate existing docs and fill required gaps). Produces a persistent `.health-docs/analysis.md` handoff artifact and composes existing healthcare skills for deep review passes.

### [`health-fhir-api-design`](skills/.curated/health-fhir-api-design)

Design FHIR R4 API interactions — search queries, operations (`$`), validation, workflow patterns, and custom SearchParameter / OperationDefinition resources. Provide your requirements; the skill recommends a concrete R4 approach with trade-offs.

### [`health-fhir-modeling`](skills/.curated/health-fhir-modeling)

Map domain concepts to FHIR R4 resources and understand profile compliance. Select the right base resources, read US Core and QI Core constraints, model relationships, find existing extensions, and apply terminology bindings (LOINC, SNOMED CT, RxNorm). Outputs annotated example instances — for app developers, not profile authors.

### [`health-hipaa-review`](skills/.curated/health-hipaa-review)

Produce a report-only HIPAA, PHI, and PII audit for healthcare codebases and delivery systems. Inspects code, configs, data flows, integrations, logging, and deployment boundaries for privacy and security gaps without modifying code.

### [`health-human-factors`](skills/.curated/health-human-factors)

Review healthcare and EHR software user interfaces against a comprehensive design style guide grounded in NIST, FDA, IEC 62366, ISO 9241, ISO 14971, WCAG 2.1, ONC SAFER, and HL7 FHIR standards. Produces a report-only assessment of patient safety, usability, accessibility, and data clarity without modifying code or designs.

### [`health-project-context`](skills/.experimental/health-project-context)

Bootstrap reusable healthcare project context from repository evidence. Infers jurisdiction, primary audience, and whether the repo is greenfield or existing, then persists that context in `.health-context.yaml` for future skills.

### [`health-product-discovery`](skills/.curated/health-product-discovery)

Map incentive structures, adoption dynamics, and clinical workflow constraints before shaping solutions. Supports explore and document modes for early-stage ideation, consulting, pilot scoping, and strategic planning.

### [`health-refactor`](skills/.curated/health-refactor)

Produce a scope-bounded, plan-only refactoring assessment for healthcare codebases. Resolves a bounded file set via git range, file area, or symbol/dependency context, then orchestrates three analysis passes — healthcare-aware code refactoring, human-factors review, and HIPAA audit — into a unified plan with findings and a prioritized checklist. Never modifies code.

---

For contributing and skill development, see [DEVELOPER.md](https://github.com/reason-healthcare/health-skills/blob/main/DEVELOPER.md).
