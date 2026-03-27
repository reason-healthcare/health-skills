---
name: health-fhir-api-design
description: Design healthcare APIs and data flows with FHIR-aware patterns. Use when an agent needs help with interoperability requirements, resource modeling, API boundaries, implementation trade-offs, or healthcare data exchange design.
---

# FHIR API Design

## Overview

Use this skill to shape interoperability-aware APIs and service boundaries for healthcare products that exchange clinical or operational data.

## Workflow

1. Identify the workflow, system boundary, and exchanging actors.
2. Determine whether the problem maps cleanly to existing FHIR resources or profiles.
3. Separate business workflow decisions from resource representation details.
4. Produce concrete API and data-model recommendations with trade-offs.

## Constraints

- Prefer standard resource use before inventing custom structures.
- Note where implementation convenience diverges from interoperability value.
- Make lifecycle, ownership, and versioning assumptions explicit.

## Resources

- `references/fhir-patterns.md`: patterns for resource selection and boundary design

## Output Contract

- Provide proposed resources, boundaries, trade-offs, and unresolved interoperability risks.
