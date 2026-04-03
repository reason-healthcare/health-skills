---
marp: true
theme: default
paginate: true
title: Reason Health Skills
description: Marp slide deck for the healthcare skills repository
style: |
  section {
    font-size: 22px;
    line-height: 1.3;
  }
  code, pre, pre code {
    font-size: 0.75em;
  }
  table {
    font-size: 0.85em;
  }
---

# Reason Health Skills

## https://github.com/reason-healthcare/health-skills

---

# Why We Built This

Shared AI skills for building healthcare technology software and digital health products. Built by Vermonster, a software studio with 15+ years building healthcare technology systems.

- The cost of shallow guidance is high
- Regulation, interoperability, and safety constraints show up early
- Generic coding agents miss workflow, compliance, and clinical context
- Teams need reusable patterns, not one-off prompts

This repo packages those patterns into shareable skills.

---

# What The Team Experience Brings

Real healthcare delivery software work tends to involve:

- EHR and FHIR integration realities
- HIPAA, GDPR, ONC, FDA, MDR, AI Act, and adjacent constraints
- documentation gaps that matter during audits
- UX decisions with patient-safety implications
- long procurement and adoption cycles

The skills encode that operating reality into repeatable workflows.

---

# Design Principles

- Keep one canonical skill per domain
- Put regional behavior in overlays, not forked skill trees
- Prefer evidence-backed outputs over generic advice
- Support scoped review for composition
- Keep authored source separate from generated runtime installs
- Make distribution predictable and validator-friendly

---

# CI/CD


```
validate_skill_library  →  audit_skill_security  →  publish_dist_branch  →  verify_skills_sh_compat
```

The security audit (`audit_skill_security.py`) approximates the scanner checks run by skills.sh, catching three failure classes before distribution:

| Code | Scanner model | Triggered when |
|---|---|---|
| `COMMAND_EXECUTION` | Gen Agent Trust Hub | shell command uses user input without a validation rule |
| `PROMPT_INJECTION` | Gen Agent Trust Hub | skill reads codebase files without a prompt-injection boundary rule |
| `CREDENTIAL_HANDLING` | Snyk W007 | verbatim content copy with no secret-redaction rule |

Any `FAIL` exits non-zero and blocks the dist branch publish.

---

# Compatibility With Spec Frameworks

Skills drop in as domain overlays — no framework lock-in.

| Health Skill | OpenSpec | Spec-Kit | BMAD |
|---|---|---|---|
| `init` | — | `constitution` | `bmad-analyst` |
| `product-discovery` | `explore`, `new-change` | `specify` | `bmad-analyst`, `bmad-pm` |
| `fhir-modeling` | `continue-change` | `plan` | `bmad-architect` |
| `fhir-api-design` | `continue-change` | `plan` | `bmad-architect` |
| `refactor` | `apply-change`, `verify-change` | `analyze`, `implement` | `bmad-agent-dev` |
| `docs` | `apply-change`, `verify-change` | `analyze` | `bmad-tech-writer` |
| `compliance-review` | `verify-change` | `analyze` | `bmad-analyst`, `bmad-agent-dev` |
| `human-factors` | `verify-change` | `analyze` | `bmad-ux-designer` |

---

# Repository Model & Distribution Workflow

Author once, distribute many ways.

**Canonical source**: `skills/` on `main`

**Distribution output**: published `dist` branch

The release flow is built to stay compatible with `skills.sh`. Typical sequence:

```bash
python3 scripts/validate_skill_library.py
python3 scripts/publish_dist_branch.py --branch dist
python3 scripts/verify_skills_sh_compat.py --dist-branch dist
```
...

Consumer install https://skills.sh/reason-healthcare/health-skills :

```bash
npx skills add https://github.com/reason-healthcare/health-skills/tree/dist
```

---

# Multi-Agent Efficiency

Several skills are designed for composed or multi-agent use.

- `health-docs` can dispatch deep analysis in parallel
- `health-refactor` orchestrates multiple review lenses over one bounded scope
- scoped review mode keeps downstream analysis focused and findings-only

...

A single pass is often not enough. Example:

- code structure issue
- documentation gap
- compliance exposure
- human-factors risk

Those may all show up in the same change, but they are different review disciplines. Composed skills let the agent split work without losing a shared context.

---

# Jurisdiction Overlays

Skills stay jurisdiction-neutral by default. Overlays activate only when evidence supports them. Each skill selects `us`, `eu`, `us+eu`, or `unclear` from:
- `.health-context.yaml` (set by `health-init`)
- repository signals and user prompt context

From `health-product-discovery`:

```md
## Jurisdiction Overlay Selection

Keep the base discovery flow jurisdiction-neutral. Apply market
overlays only after selecting one of `us`, `eu`, `us+eu`, or `unclear`.

1. Read `.health-context.yaml` if it exists and note the stored jurisdiction.
2. Check the user prompt, provided materials, and repository evidence
   for confirming or conflicting market signals.
3. Load `references/us-market-overlay.md` and/or
   `references/eu-market-overlay.md` only for the selected overlay set.
4. If evidence is mixed, say so explicitly and avoid silently defaulting
   to US market assumptions.
```

_Overlays add market-specific depth — HIPAA vs GDPR, FDA vs MDR, ONC vs EU AI Act — without forking the skill._

---

# Health Skills at a Glance

| Skill | Purpose | Output | When |
|---|---|---|---|
| `health-init` | Infer jurisdiction, audience, project stage | `.health-context.yaml` | Start of any project |
| `health-product-discovery` | Stress-test product direction against healthcare market reality | Explore or document report | Before specs harden |
| `health-fhir-modeling` | Map domain concepts to FHIR R4 resources and profiles | Annotated example instances | During design |
| `health-fhir-api-design` | Design or review FHIR R4 search, operations, and workflow APIs | API design recommendations | During design |
| `health-refactor` | Bounded refactor assessment across code, compliance, and UX lenses | Prioritized plan (no code changes) | Before or during implementation |
| `health-docs` | Audit documentation coverage and fill gaps | Coverage analysis or draft docs | During or after implementation |
| `health-compliance-review` | Deterministic regulatory and security findings from engineering evidence | Findings report with severity | Verify or gate release |
| `health-human-factors` | Review clinical UI for usability, accessibility, and patient-safety risks | Design review report | Design or verify |

---

# How The Skills Work Together

One practical path:

1. `health-init` establishes context
2. `health-product-discovery` frames the opportunity
3. `health-fhir-modeling` and `health-fhir-api-design` shape the solution
4. `health-refactor`, `health-docs`, `health-compliance-review`, and `health-human-factors` verify quality from multiple angles

The system is modular, but the lifecycle is coherent.

---

# Closing

Reason Healthcare **Health Skills** is a reusable healthcare capability layer for AI-assisted work.

It combines:

- domain expertise
- explicit specs
- portable skill packaging
- multi-agent composition
- release discipline
- compatability with existing agile and SDLC skills frameworks

A practical option for real healthcare tech teams.
