---
name: health-regulatory-review
description: Produce a report-only healthcare regulatory review for codebases and delivery systems. Selects `us`, `eu`, or `us+eu` overlays from evidence before inspecting code, configs, data flows, integrations, logging, and deployment boundaries.
---

# Healthcare Regulatory Review

## Overview

Use this skill to inspect healthcare software and produce an engineering review of privacy, security, and healthcare-regulatory risks.

Select one of `us`, `eu`, `us+eu`, or `unclear` before reviewing:

1. Read `.health-context.yaml` if it exists.
2. Check the repository scope for confirming or conflicting signals.
3. Load `references/us-regulatory-overlay.md` and/or `references/eu-regulatory-overlay.md` based on the selected overlay set.
4. If the evidence is mixed, surface that uncertainty instead of forcing a single market.

## Operating Rules

- Never change code, configs, infrastructure, or documentation.
- Do not present the output as legal advice, certification, or a formal compliance determination.
- Bias toward code-observable evidence and clearly separate:
  - confirmed evidence from the code or config
  - likely inferences from nearby implementation
  - non-code dependencies that require policy, vendor, ops, or legal validation
- Treat missing implementation or missing documented alternatives as finding candidates when a selected overlay expects those safeguards.
- When PII appears without clear PHI, still report the privacy risk and note that final regulatory scope may depend on deployment context.

## Workflow

1. Select jurisdiction overlays from `.health-context.yaml`, repository evidence, and the user's task context.
2. Confirm whether the system creates, receives, maintains, or transmits PHI, ePHI, health data, or adjacent sensitive PII.
3. Map sensitive-data entry, storage, logging, transmission, export, analytics, AI, and deletion paths across code and configuration.
4. Review those touchpoints against `references/control-areas.md` plus the active jurisdiction overlays.
5. Assign severity and confidence for each issue, and mark where evidence is missing.
6. Produce a report only. Do not draft patches or implement remediations.

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
- When `us+eu` applies, separate shared findings from US-specific and EU-specific findings.

## Resources

- `references/control-areas.md`: baseline healthcare privacy and security audit criteria with sample findings and source links grounded in HHS and NIST guidance
- `references/us-regulatory-overlay.md`: US-oriented regulatory overlay for HIPAA, ONC, FDA, and adjacent delivery signals
- `references/eu-regulatory-overlay.md`: EU-oriented regulatory overlay for GDPR, EHDS, MDR/IVDR, AI Act, and NIS2 applicability signals
- `examples/example-report.md`: example US-oriented audit report showing expected output shape and overlay selection
- `examples/example-report-eu.md`: example EU-oriented audit report
- `examples/example-scoped-findings-us-eu.md`: example scoped findings for a multi-market review

## Invocation Modes

### Standalone (default)

When invoked directly by a user or without the phrase "scoped review," operate normally: confirm scope interactively, select overlays, map sensitive-data paths, review against the active overlays, and produce the full report described in the Output Contract below.

### Scoped

When invoked with the phrase "scoped review" and a pre-determined list of file paths, operate in scoped mode:

- **Input**: a list of file paths to review. Scope is pre-determined — do not ask for confirmation.
- **Behavior**: skip interactive scope confirmation. Skip executive summary, coverage matrix, and open questions generation. Review only the provided files against the active control areas and jurisdiction overlays.
- **Output**: return a findings-only list. Each finding uses this format:

  ```
  ### [H-{n}] {title}
  - Severity: critical | high | medium | low
  - Category: {control area or overlay area}
  - File: {path}:{line}
  - Detail: {what was observed and what evidence supports the finding}
  - Guideline: {overlay source, regulatory section, or baseline guidance}
  ```

  If no findings are discovered, return a single line: "No healthcare regulatory findings for the provided files."

## Output Contract

When operating in **standalone** mode, return an audit report with:

- selected overlays and the evidence used to choose them
- executive summary
- in-scope components and sensitive-data assumptions
- findings table with: ID, severity, category, affected area, evidence, risk, suggested remediation direction, and confidence
- coverage matrix by control area: met, partial, not met, or not enough evidence
- open questions and non-code dependencies
- source basis used for the review
