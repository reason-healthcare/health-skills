# Healthcare Skill Creation Guide

This repository exists to create and distribute shared skills for healthcare technology software and digital health product work. New curated skills should help teams make better product, engineering, security, interoperability, or operational decisions in healthcare contexts.

## Domain Fit

Treat healthcare relevance as a gating requirement for curated skills.

A curated skill should clearly support one or more of these areas:

- product strategy and discovery for healthcare workflows
- clinical workflow-aware UX or service design
- healthcare data interoperability and APIs
- regulated software delivery, privacy, or security
- operational readiness, analytics, or support in healthcare environments

If a skill is broadly useful but not meaningfully healthcare-specific, place it in `skills/.experimental/` or keep it out of the curated catalog.

## Authoring Structure

Use the standard skill layout:

- `SKILL.md`: concise trigger conditions, workflow, constraints, and output expectations
- `agents/openai.yaml`: user-facing metadata and default prompt
- `references/`: detailed domain material that should be loaded only when needed
- `scripts/`: deterministic helpers for repeated operations
- `assets/`: templates or files used in the final output

Keep `SKILL.md` small and purposeful. Put large healthcare references such as workflow constraints, interoperability notes, or delivery checklists into `references/`.

Use the `health-` prefix for distributable healthcare skill names.

## Initial Curated Categories

The first curated categories for this repository are:

1. Healthcare product discovery
2. Clinical and workflow-aware experience design
3. Interoperability and FHIR-informed API design
4. Security, privacy, and HIPAA-aware delivery
5. Operational readiness and healthcare product quality

## Progressive Disclosure

Write the skill so another agent can trigger it from the frontmatter and understand the core workflow quickly.

- Put trigger conditions and task selection in `SKILL.md`
- Put detailed domain rules in `references/`
- Put repetitive actions in `scripts/`
- Put reusable output artifacts in `assets/`

## Validation Workflow

Before a skill is considered ready for shared distribution:

1. Validate the skill structure and frontmatter.
2. Validate any agent overlays against the base skill.
3. Compose install outputs for supported agents.
4. Verify the composed result still matches standard Agent Skills conventions.
5. Review the skill for healthcare relevance and clarity.

## Curated vs Experimental

Use `skills/.curated/` only when all of the following are true:

- the skill has clear healthcare domain fit
- the structure validates successfully
- required metadata is present
- the workflow is coherent without hidden assumptions
- the skill is safe to distribute to other teams

Use `skills/.experimental/` when any of the following are true:

- the scope is still being refined
- the healthcare fit is promising but not yet clear
- references or helpers are incomplete
- the team wants feedback before wider distribution

## Repository Conventions

- Use lowercase kebab-case for skill names.
- Use the `health-` prefix for distributed healthcare skills.
- Keep base skills in canonical source and treat agent trees as generated outputs.
- Use overlays only when an agent needs a real customization.
- Prefer explicit examples over long theory.
