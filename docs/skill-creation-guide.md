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
- `examples/`: sample output artifacts that demonstrate the expected report or design shape

Keep `SKILL.md` small and purposeful. Put large healthcare references such as workflow constraints, interoperability notes, or delivery checklists into `references/`.

Use the `health-` prefix for distributable healthcare skill names.

## Creation Workflow

New skills follow an OpenSpec-driven process:

### 1. Proposal

Describe the skill's purpose, healthcare context, target users, and intended output shape via an OpenSpec proposal.

### 2. Scaffold

Once the proposal is accepted, scaffold the skill directory:

```bash
python3 scripts/init_skill.py health-claims-workflow-review \
  --group .experimental \
  --description "claims workflow review" \
  --include references scripts assets examples
```

This creates a new skill under `skills/.experimental/` with the standard file layout.

### 3. Design and Specs

Continue through OpenSpec design and specs:

- **Design**: detail the workflow, review categories or modes, and output contract
- **Specs**: write delta specs covering SKILL.md structure, references, and examples

Use the scaffolded directory as the target — fill in `SKILL.md`, references, and examples as the specs take shape.

### 4. Tasks and Implementation

Generate tasks from the specs and implement them. Typical tasks include:

- Write the `SKILL.md` frontmatter, workflow, constraints, and output contract
- Create reference documents in `references/`
- Create an example output in `examples/`
- Write `agents/openai.yaml` metadata

### 5. Test

Compose the skill into local agent trees and exercise it:

```bash
python3 scripts/compose_skills.py
```

Then invoke the skill from your agent of choice (e.g., `$health-claims-workflow-review` in Copilot Chat). Verify:

- the skill triggers correctly from the frontmatter description
- the workflow steps produce coherent output
- references load when needed and stay out of context when not
- the output matches the contract defined in SKILL.md
- the example output in `examples/` is representative of real results

Iterate on `skills/.experimental/<skill-name>/` and re-compose until the skill is solid.

> **Pro tip**: Run your agent in unattended and capture the full transcript:
>
> ```bash
> claude -p "Review the patient intake form for human factors issues" 2>&1 | tee session-log.txt
> ```
>
> Use that transcript to iterate on refining the skill — review how the agent interpreted the trigger, which references it loaded, and whether the output matched the contract.

### 6. Promote

When the skill meets the curated standard, move it (see Promotion to Curated below).

## Initial Curated Categories

The first curated categories for this repository are:

1. Healthcare product discovery (`health-product-discovery`)
2. Clinical and workflow-aware experience design (`health-human-factors`)
3. Interoperability and FHIR-informed API design (`health-fhir-api-design`)
4. Security, privacy, and HIPAA-aware delivery (`health-hipaa-review`)
5. Operational readiness and healthcare product quality
6. Healthcare codebase refactoring and code quality (`health-refactor`)

## Skill Composition

Orchestrating skills can compose existing report-only skills by invoking them in **scoped mode**. A skill supports scoped invocation when its SKILL.md includes an "Invocation Modes" section that defines:

- **Standalone (default)** — existing behavior, triggered directly by users
- **Scoped** — triggered by an orchestrating skill with a pre-determined file list; returns findings-only output without interactive scope confirmation or executive summary

`health-human-factors` and `health-hipaa-review` both support scoped invocation. `health-refactor` uses this pattern to compose all three analysis lenses into a single bounded plan. When building a new orchestrating skill, check whether the target skills support scoped mode before embedding duplicate logic.

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

## Promotion to Curated

To promote an experimental skill to curated:

1. Move the skill: `mv skills/.experimental/<name> skills/.curated/<name>`
2. Validate: `python3 scripts/validate_skill_library.py`
3. Add the skill to `README.md` in alphabetical order with a link to its source directory.
4. Add any needed agent overlays in `profiles/<agent>/<skill>/`.
5. Publish: `python3 scripts/publish_dist_branch.py --branch dist`
6. Verify: `python3 scripts/verify_skills_sh_compat.py --dist-branch dist`

## Repository Conventions

- Use lowercase kebab-case for skill names.
- Use the `health-` prefix for distributed healthcare skills.
- Keep base skills in canonical source and treat agent trees as generated outputs.
- Use overlays only when an agent needs a real customization.
- Prefer explicit examples over long theory.
