# FHIR Patterns

Use this reference when the task needs deeper interoperability reasoning.

## Review Areas

- which actor owns the resource lifecycle
- whether FHIR is the system contract or an external projection
- profile and extension strategy
- search and event boundaries
- mapping between internal models and canonical exchange models

## Decision Rule

Prefer using standard resources and profiles when they preserve the intended workflow semantics. Introduce custom structures only when the workflow or product contract cannot be represented cleanly with existing patterns.
