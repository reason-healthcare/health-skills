---
name: health-docs
description: Audit and consolidate documentation for healthcare engineering systems. Supports two modes — analyze (coverage audit — writes only .health-docs/analysis.md) and document (consolidate existing docs + fill gaps). Detects applicable regulatory regimes (HIPAA, ONC, FDA SaMD) from codebase signals, composes existing skills as subagents for deep-dimension analysis, and produces a structured handoff artifact consumed by document mode.
---

# Healthcare System Documentation

## Overview

Healthcare engineering systems require documentation that serves multiple audiences simultaneously — developers, operators, auditors, AI agents, and regulators. That documentation rarely exists in a usable state: it's scattered across README files, inline comments, AGENTS.md, and external wikis, with critical regulatory-required content simply absent.

This skill audits what exists, maps it to what's required given the system's regulatory context, and consolidates it into a structured, maintainable hierarchy.

## Modes

### Mode: analyze

Scan the repository, detect applicable regulatory regimes, assess documentation coverage across seven dimensions, and produce a structured handoff artifact. **No repository files are modified — only `.health-docs/analysis.md` is written.**

### Mode: document

Read the handoff artifact from analyze mode, conduct an evidence-informed interview to confirm requirements, then consolidate existing documentation into the target hierarchy and draft new content for required gaps. **Confirms before writing.**

---

## Operating Rules

- Never modify code, tests, configurations, or infrastructure files.
- Never silently resolve conflicts between documentation sources — always flag for human resolution.
- Always mark documents in `comply/` directories with `⚠ REQUIRES HUMAN REVIEW` regardless of operation type (consolidate, merge, or draft new) — the skill can transcribe and draft from evidence, but cannot certify compliance.
- If a relevant subagent is unavailable, fall back to direct analysis for that dimension; note reduced confidence in the artifact.
- Treat external links (Confluence, Notion, GDrive) as "unverifiable — content not assessed" — mark coverage as partial, not covered.
- The `.health-docs/` directory is the skill's work directory in the target repo. Do not treat it as part of the documentation hierarchy.

---

## Analyze Mode Workflow

### Pass 1: Broad Scan and Regime Signal Detection

Inventory the repository without subagents:

1. Find all markdown files at every level (`**/*.md`)
2. Find all agent instruction files: `AGENTS.md`, `.github/copilot-instructions.md`, `.cursor/rules`, `.cursorrules`, `CLAUDE.md`
3. Find CI/CD configs: `.github/workflows/`, `Jenkinsfile`, `.circleci/`, `Makefile`
4. Detect existing documentation root: search for `docs/`, `documentation/`, `wiki/`, `doc/` in that precedence order. Select the first match by precedence (not filesystem order). If multiple directories exist, note the others in the artifact narrative. Record `null` in `doc_root_detected` if none are found.
5. Scan code and configuration for regime signals using `references/regime-signals.md`:
   - PHI signals → HIPAA candidate (record confidence level and specific evidence)
   - ONC/EHR API signals → ONC candidate
   - SaMD/AI clinical signals → FDA SaMD candidate
6. Record all external links found in documentation (flag as unverifiable)

### Pass 2: Parallel Subagent Dispatch

Invoke available subagents in parallel against the Pass 1 file inventory. Dispatch only those relevant to detected signals:

| Subagent | Condition | Invocation | Coverage dimensions fed |
|---|---|---|---|
| `$health-hipaa-review` | PHI signals found (see `references/regime-signals.md`) | "scoped review" + file list | `secure/`, `comply/hipaa/` |
| `$health-fhir-api-design` | FHIR or ONC signals found (FHIR resource types, SMART auth, EHR SDK imports, USCDI references) | "scoped review" + file list | `understand/integrations`, `comply/onc/` |
| `$health-human-factors` | UI source files found (`.html`, `.tsx`, `.jsx`, `.vue`, `.erb`, or directories matching `app/views/`, `src/components/`, `templates/`) | "scoped review" + file list | `build/testing` |

If a subagent is not installed: perform direct analysis for that dimension and note `confidence: reduced` in the artifact.

**Translating subagent findings to coverage dimensions:**

Each subagent returns a findings report. Translate to coverage dimensions using this mapping:

| Subagent | Finding type | Coverage dimension |
|---|---|---|
| `$health-hipaa-review` | Access control / session management gaps | `secure/auth-model` |
| `$health-hipaa-review` | Audit log / retention gaps | `secure/audit-logs` |
| `$health-hipaa-review` | Encryption at-rest or in-transit gaps | `secure/encryption` |
| `$health-hipaa-review` | Risk analysis / risk management gaps | `comply/hipaa/risk-analysis`, `comply/hipaa/risk-management` |
| `$health-hipaa-review` | BAA / business associate documentation gaps | `comply/hipaa/baa-inventory` |
| `$health-fhir-api-design` | Integration / vendor API documentation gaps | `understand/integrations` |
| `$health-fhir-api-design` | SMART / bulk API access documentation gaps | `comply/onc/api-access` |
| `$health-human-factors` | Missing usability test docs / acceptance criteria | `build/testing` |

For any finding that does not map to a row above, record the gap verbatim in the narrative and assign the closest matching dimension with `confidence: reduced`.

### Pass 3: Synthesize Coverage Matrix

For each documentation dimension in `references/doc-hierarchy.md`, assign a coverage status:

| Status | Meaning |
|---|---|
| `covered` | Exists, appears current and complete |
| `partial` | Exists but stale, thin, or incomplete — note what's missing |
| `conflict` | Multiple sources cover the topic with contradictory content |
| `absent` | No evidence found in the repository |
| `absent-required` | Absent and mandated by applicable regulation |

Enumerate **every** dimension listed in `references/doc-hierarchy.md` in the coverage matrix — including `covered` dimensions. Do not omit covered entries. The complete matrix allows document mode to present an accurate inclusion/skip list to the user.

For each dimension, record:
- `dimension`: canonical ID matching the file path slug (e.g., `secure/audit-logs`, `operate/runbooks/breach-notification`)
- `status`: one of the above
- `sources`: file paths and line ranges where related content was found (empty if absent)
- `regulatory`: applicable regulation and section (from `references/regulatory-mapping.md`), or `null` if none
- `required`: `null` — populated by document mode after the interview
- `confidence`: `high`, `medium`, or `reduced` (reduced if subagent was unavailable)

### Write Handoff Artifact

Write `.health-docs/analysis.md` with:
1. YAML frontmatter containing the structured coverage matrix (see Artifact Schema below)
2. Human-readable narrative body:
   - Regime detection summary with evidence
   - Coverage findings organized by dimension
   - Conflicts and their sources
   - External links flagged as unverifiable
   - Priority gaps (absent-required items listed first)

---

## Document Mode Workflow

### Step 1: Read Handoff Artifact

Read `.health-docs/analysis.md`. If it does not exist, tell the user to run analyze mode first.

Check the `generated_at` timestamp. If older than 90 days, warn the user that the analysis may be stale and recommend re-running analyze mode before proceeding.

If a `requirements` profile already exists in the artifact (from a previous document mode run), present it to the user and ask whether to use it or re-interview.

### Step 2: Evidence-Informed Interview (3 Confirmations)

Present findings from the artifact and ask the user to confirm, not discover.

**Confirmation 1 — Regime:**
Present the regime signals found with evidence and confidence levels. Example:
> "I found these indicators: Patient model with MRN and DOB fields (src/models/patient.rb), FHIR R4 resources in src/fhir/, 'phi' in 14 variable names. I'm proposing HIPAA track. Correct?"

**Confirmation 2 — Dimension inclusion:**
Show a fast-scan list of each dimension with proposed status (INCLUDE / SKIP / REVIEW). The user can override any entry. Mark regulatory-required dimensions that are absent as `INCLUDE ⚠ required`.

**Confirmation 3 — Target directory:**
- If an existing documentation directory was detected in Pass 1, inform (no confirmation required): "Writing to `[detected-root]/` — your existing documentation root. Say otherwise to override." Do not wait for a response.
- If no documentation directory was detected, require a response: "No documentation directory found. I'll create `docs/`. Use a different path?"

### Step 3: Write Requirements Profile

Write the confirmed `required: true/false` values for each dimension back into `.health-docs/analysis.md` frontmatter. This persists across sessions — future document mode runs skip the interview unless overridden.

### Step 4: Pre-Flight Confirmation

Before writing any files, show the full plan:

```
CONSOLIDATE (copying to target path — no rewrites; originals flagged in place):
  README.md:12-45      → docs/orient/README.md
  AGENTS.md:23-31      → docs/agent-context/phi-rules.md

MERGE (combining sources — conflicts flagged for your review):
  README.md:78-85  ⚠ CONFLICT  → docs/secure/auth-model.md
  AGENTS.md:23-31              (session timeout description differs)

DRAFT NEW (no existing source — requires human review where noted):
  docs/operate/runbooks/breach-notification.md    ← HIPAA §164.408 ⚠ REVIEW
  docs/comply/hipaa/risk-analysis.md              ← HIPAA §164.308 ⚠ REVIEW

SKIP (not required by your profile):
  docs/comply/onc/
  docs/comply/fda/

Proceed? [yes / no / edit plan]
```

Do not write any files until the user confirms.

### Step 5: Execute Plan

Execute in strict order:

1. **Consolidate** — copy content from source locations to target paths. Do not rewrite — preserve substance, fix location. Do not delete the source file; the flag-originals step handles that. Add `⚠ REQUIRES HUMAN REVIEW` header to any `comply/` target file.
2. **Merge** — when multiple sources cover the same topic, merge them into the target file. Insert a visible conflict marker where descriptions differ:
   ```
   <!-- ⚠ CONFLICT: session timeout described as 30min in README.md and 60min in AGENTS.md. Resolve before treating this document as authoritative. -->
   ```
   Add `⚠ REQUIRES HUMAN REVIEW` header to any `comply/` target file.
3. **Draft new** — generate content for required dimensions with no source. Ground drafts in codebase evidence where possible. Add `⚠ REQUIRES HUMAN REVIEW` header to all `comply/` documents.
4. **Flag originals** — add a comment or note to original file locations indicating content was copied to the new path. Do not delete originals.

### Step 6: Update Run Record

Append a dated entry to `.health-docs/runs/YYYY-MM-DD.md` recording:
- What was consolidated (source → target)
- What was merged (sources → target, conflicts noted)
- What was drafted (path, regulatory basis)
- What was skipped
- Any human review items outstanding

---

## Handoff Artifact Schema

The `.health-docs/analysis.md` file uses YAML frontmatter for structured data and a markdown body for human narrative.

```yaml
---
generated_at: "2026-03-28T14:00:00Z"
schema_version: "1"

regime_detected:
  hipaa:
    proposed: true
    confidence: high
    evidence:
      - "Patient model with mrn, dob fields (src/models/patient.rb:12)"
      - "'phi' in 14 variable names"
  onc:
    proposed: true
    confidence: medium
    evidence:
      - "SMART on FHIR scopes in config/oauth.yml"
  fda_samd:
    proposed: false
    confidence: low
    evidence: []

doc_root_detected: "docs/"   # null if not found

coverage:
  - dimension: "understand/data-flows"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(a)(1)(ii)(A)"
    required: null          # populated by document mode
    confidence: high

  - dimension: "secure/audit-logs"
    status: "partial"
    sources:
      - path: "README.md"
        lines: "45-60"
        note: "mentions audit logging exists but no schema or retention policy"
    regulatory: "HIPAA §164.312(b)"
    required: null
    confidence: high

  - dimension: "comply/hipaa/baa-inventory"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(b)(1)"
    required: null
    confidence: high

requirements:               # populated after document mode interview
  interview_completed_at: null   # ISO 8601 timestamp, null until interview complete
  regime: []                     # confirmed regimes (e.g., ["hipaa", "onc"])
  dimensions: {}                 # dimension path → true/false
  human_review_required: []      # file paths requiring human sign-off

---
```

---

## Resources

- `references/doc-hierarchy.md`: canonical seven-dimension documentation tree with target file paths, audience notes, and minimum required files
- `references/regime-signals.md`: PHI, ONC, and FDA SaMD signal patterns for Pass 1 detection
- `references/regulatory-mapping.md`: dimension → regulatory requirement mapping with classification (required / addressable / recommended)
- `examples/example-analysis.md`: sample analyze mode output narrative
- `examples/example-analysis-artifact.md`: sample `.health-docs/analysis.md` showing YAML structure pre- and post-interview

## Output Contract

### Analyze mode
- Writes `.health-docs/analysis.md` with YAML frontmatter (coverage matrix) and human narrative
- No other files written

### Document mode
- Writes or updates files within the target documentation directory
- Updates `.health-docs/analysis.md` with requirements profile
- Appends to `.health-docs/runs/YYYY-MM-DD.md` with run record
- Does not modify code, tests, or configurations
- Does not delete original files — flags them for human-reviewed cleanup



