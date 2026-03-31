---
name: health-regulatory-review
description: Produce a report-only healthcare regulatory review for codebases and delivery systems, with primary focus on HIPAA, PHI, and PII handling. Inspects code, configs, data flows, integrations, logging, and deployment boundaries for privacy and security gaps without modifying code.
---

# Healthcare Regulatory Review

## Overview

Use this skill to inspect healthcare software and produce an audit report of code and delivery areas where HIPAA-aligned handling of PHI, ePHI, or adjacent sensitive PII appears incomplete, risky, or unsupported by evidence.

## Operating Rules

- Never change code, configs, infrastructure, or documentation.
- Do not present the output as legal advice, certification, or a formal compliance determination.
- Bias toward code-observable evidence and clearly separate:
  - confirmed evidence from the code or config
  - likely inferences from nearby implementation
  - non-code dependencies that require policy, vendor, ops, or legal validation
- If a safeguard is addressable under HIPAA, treat missing implementation or missing documented alternative as a finding candidate, not an automatic pass.
- When PII appears without clear PHI, still report the privacy risk and note that HIPAA scope may depend on context.

## Workflow

1. Confirm whether the system creates, receives, maintains, or transmits PHI, ePHI, or related sensitive PII.
2. Map sensitive-data entry, storage, logging, transmission, export, analytics, and deletion paths across code and configuration.
3. Review those touchpoints against `references/control-areas.md`.
4. Assign severity and confidence for each issue, and mark where evidence is missing.
5. Produce a report only. Do not draft patches or implement remediations.

## What To Inspect

- models, schemas, serializers, DTOs, caches, queues, exports, and storage clients
- authentication, authorization, tenancy boundaries, and service identities
- logging, tracing, analytics, observability, error handling, and support tooling
- outbound integrations, webhooks, email or SMS paths, AI or LLM calls, and third-party SDKs
- secrets, environment variables, encryption hooks, background jobs, and deployment defaults
- tests, fixtures, seed data, migrations, and local development helpers

## Constraints

- Focus on engineering evidence, not broad legal interpretation.
- Highlight where assumptions depend on deployment context or organizational controls.
- Separate confirmed code issues from architectural or operational unknowns.

## Resources

- `references/control-areas.md`: baseline HIPAA, PHI, and PII audit criteria with sample findings and source links grounded in HHS and NIST guidance
- `examples/example-report.md`: example audit report showing expected output shape, finding format, and coverage matrix

## Invocation Modes

### Standalone (default)

When invoked directly by a user or without the phrase "scoped review," operate normally: confirm scope interactively, map sensitive-data paths, review against control areas, and produce the full report described in the Output Contract below.

### Scoped

When invoked with the phrase "scoped review" and a pre-determined list of file paths, operate in scoped mode:

- **Input**: a list of file paths to review. Scope is pre-determined — do not ask for confirmation.
- **Behavior**: skip interactive scope confirmation. Skip executive summary, coverage matrix, and open questions generation. Review only the provided files against the control areas.
- **Output**: return a findings-only list. Each finding uses this format:

  ```
  ### [H-{n}] {title}
  - Severity: critical | high | medium | low
  - Category: {control area from control-areas.md}
  - File: {path}:{line}
  - Detail: {what was observed and what evidence supports the finding}
  - Guideline: {HIPAA section, HHS guidance, or NIST reference}
  ```

  If no findings are discovered, return a single line: "No HIPAA findings for the provided files."

## Output Contract

When operating in **standalone** mode, return an audit report with:

- executive summary
- in-scope components and sensitive-data assumptions
- findings table with: ID, severity, category, affected area, evidence, risk, suggested remediation direction, and confidence
- coverage matrix by control area: met, partial, not met, or not enough evidence
- open questions and non-code dependencies
- source basis used for the review
