---
name: health-hipaa-secure-delivery
description: Produce a report-only HIPAA, PHI, and PII audit for healthcare codebases and delivery systems. Use when an agent needs to inspect code, configs, data flows, integrations, logging, or deployment boundaries for privacy and security gaps without modifying code.
---

# HIPAA Code Audit

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

## Output Contract

Return an audit report with:

- executive summary
- in-scope components and sensitive-data assumptions
- findings table with: ID, severity, category, affected area, evidence, risk, suggested remediation direction, and confidence
- coverage matrix by control area: met, partial, not met, or not enough evidence
- open questions and non-code dependencies
- source basis used for the review
