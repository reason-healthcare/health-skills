# Healthcare Skill Mapping For Spec-Kit, OpenSpec, and BMAD

This document maps the curated `health-*` skills in this repository to the points in three common structured agent workflows where they are most useful:

- **Spec-Kit**: best mapped to greenfield, exploration, and brownfield phases
- **OpenSpec**: mapped to the workflow used in this repo: proposal, design, specs, tasks, implementation, verification, archive
- **BMAD**: mapped to the four-phase method: analysis, planning, solutioning, implementation


## Mapping Table

| Skill | Primary Use | Best Fit In Spec-Kit | Best Fit In OpenSpec | Best Fit In BMAD |
|---|---|---|---|---|
| `health-init` | Establish reusable project context: jurisdiction, audience, project stage | Before `constitution` in **0-to-1** and **Iterative Enhancement** | No direct OpenSpec equivalent; run before or alongside `explore` | `bmad-analyst` at the start of **Analysis** |
| `health-product-discovery` | Stress-test product direction, incentives, adoption, workflow fit | During `specify` in **Creative Exploration** and early **0-to-1** | During `explore` and `new-change` in **Explore / Proposal** | `bmad-analyst` and `bmad-pm` in **Analysis** and **Planning** |
| `health-fhir-modeling` | Choose the right FHIR R4 resources, profiles, extensions, terminology | During `plan` in **0-to-1** once product direction is clear | During `continue-change` in **Design / Specs** | `bmad-architect` in **Planning** and **Solutioning** |
| `health-fhir-api-design` | Design or review FHIR R4 interactions, search, operations, validation, workflow APIs | During `plan` in **0-to-1** and **Iterative Enhancement** | During `continue-change` in **Design / Specs** and sometimes **Apply** | `bmad-architect` in **Planning** and **Solutioning** |
| `health-refactor` | Produce a bounded, plan-only refactor assessment with code, compliance, and human-factors lenses | During `analyze` and `implement` in **Brownfield** | During `apply-change` and `verify-change` | `bmad-agent-dev` in **Solutioning** and early **Implementation** |
| `health-docs` | Analyze documentation coverage and consolidate or draft missing docs | During `analyze` in **Brownfield** or release hardening | During `apply-change` and `verify-change` for documentation-heavy changes | `bmad-tech-writer` in late **Planning**, **Solutioning**, or **Implementation** |
| `health-compliance-review` | Produce deterministic regulatory and security findings from engineering evidence | During `analyze` as a gate in **Brownfield** and before release | During `verify-change`; also useful in `continue-change` for early constraint checks | `bmad-analyst` and `bmad-agent-dev` in **Solutioning** and **Implementation** |
| `health-human-factors` | Review clinical UI, workflow, accessibility, and patient-safety risks | During `analyze` in **Creative Exploration** and **Brownfield** | During `continue-change` for UI review and `verify-change` for implemented flows | `bmad-ux-designer` in **Solutioning** and **Implementation** |

## Practical Guidance By Framework

### Spec-Kit

Use the healthcare skills as domain overlays on top of the normal spec-driven flow:

- Run `health-init` before `constitution` when project context, jurisdiction, audience, or stage is unclear
- Run `health-product-discovery` during `specify` so healthcare market assumptions do not get baked into specs too early
- Run `health-fhir-modeling` and `health-fhir-api-design` during `plan` while turning specs into concrete solution plans
- Run `health-refactor`, `health-docs`, `health-compliance-review`, and `health-human-factors` during `analyze` in brownfield and verification-heavy work

### OpenSpec

The cleanest mapping in this repo is:

1. `health-product-discovery` during `explore` and `new-change` in **Explore / Proposal**
2. `health-fhir-modeling` and `health-fhir-api-design` during `continue-change` in **Design / Specs**
3. `health-refactor` and `health-docs` during `apply-change` when implementation spans multiple review disciplines
4. `health-compliance-review`, `health-human-factors`, `health-docs`, and `health-refactor` during `verify-change`

### BMAD

BMAD’s structure maps cleanly to the healthcare skill set:

- **Analysis** (`bmad-analyst`): `health-init`, `health-product-discovery`
- **Planning** (`bmad-pm`, `bmad-architect`): `health-product-discovery`, `health-fhir-modeling`, `health-fhir-api-design`
- **Solutioning** (`bmad-architect`, `bmad-ux-designer`): `health-fhir-modeling`, `health-fhir-api-design`, `health-human-factors`, `health-compliance-review`, `health-refactor`
- **Implementation** (`bmad-agent-dev`, `bmad-tech-writer`): `health-refactor`, `health-docs`, `health-compliance-review`, `health-human-factors`

The `health-*` skills work best as specialist overlays on top of the BMAD agent roles, not as replacements for them.

## Best Cases For Multi-Agent Composition

The biggest efficiency gains come from composing skills when a change needs more than one kind of review:

| Situation | Recommended Composition |
|---|---|
| A healthcare code change needs structural, compliance, and UX review | `health-refactor` + `health-compliance-review` + `health-human-factors` |
| A documentation push needs technical, regulatory, and integration coverage | `health-docs` + `health-compliance-review` + `health-fhir-api-design` + `health-human-factors` |
| A FHIR-heavy feature needs both modeling and interaction design | `health-fhir-modeling` + `health-fhir-api-design` |
| A new healthcare product idea needs market validation before specs are written | `health-init` + `health-product-discovery` |

Use composition when:

- the same scope needs multiple specialist lenses
- the review is bounded and parallelizable
- findings-only outputs can be merged back into one decision point

Prefer a single skill when the task is narrow and one domain clearly dominates.

## AGENTS.md Snippets

The following snippets are designed to be copied into an `AGENTS.md` file so a project can signal how to use the `health-*` skills within a specific workflow framework.

### OpenSpec Snippet

```md
## Healthcare Skill Overlay

This project uses an OpenSpec-style workflow. When healthcare-specific work is in scope, use the `health-*` skills as domain overlays on top of the normal OpenSpec lifecycle.

- dispatch subagent or use `health-product-discovery` during `explore` and `new-change`
- dispatch subagents or use `health-fhir-modeling` and `health-fhir-api-design` during `continue-change` (design / specs)
- dispatch subagents or use `health-refactor` and `health-docs` during `apply-change` when a bounded change needs structural or documentation review
- dispatch subagents or use `health-compliance-review`, `health-human-factors`, `health-docs`, and `health-refactor` during `verify-change`

Additional rules:
- reuse `.health-context.yaml` when present
- prefer scoped review modes when composing one healthcare skill from another
- use multi-skill composition when one bounded scope needs more than one specialist lens
```

### Spec-Kit Snippet

```md
## Healthcare Skill Overlay

This project uses a Spec-Kit style workflow. When healthcare-specific work is in scope, use the `health-*` skills as domain overlays on top of the normal spec-driven lifecycle.

- use `health-init` before `constitution` when project context, jurisdiction, audience, or stage is unclear
- dispatch subagent or use `health-product-discovery` during `specify` so healthcare market assumptions do not get baked into specs too early
- dispatch subagents or use `health-fhir-modeling` and `health-fhir-api-design` during `plan` while turning specs into concrete healthcare solution plans
- dispatch subagents or use `health-refactor`, `health-docs`, `health-compliance-review`, and `health-human-factors` during `analyze` in brownfield, validation, and release-hardening work

Additional rules:
- treat the healthcare skills as specialist overlays, not replacements for the core spec workflow
- prefer bounded, evidence-backed review over broad generic advice
- use composition when the same scope needs code, compliance, documentation, or UX review together
```

### BMAD Snippet

```md
## Healthcare Skill Overlay

This project uses BMAD. When healthcare-specific work is in scope, use the `health-*` skills as specialist overlays for the BMAD agent roles.

- `bmad-analyst`: run `health-init` and `health-product-discovery` during analysis
- `bmad-pm` and `bmad-architect`: run `health-product-discovery`, `health-fhir-modeling`, and `health-fhir-api-design` during planning
- `bmad-architect` and `bmad-ux-designer`: run `health-fhir-modeling`, `health-fhir-api-design`, `health-human-factors`, `health-compliance-review`, and `health-refactor` during solutioning
- `bmad-agent-dev` and `bmad-tech-writer`: run `health-refactor`, `health-docs`, `health-compliance-review`, and `health-human-factors` during implementation and validation

Additional rules:
- use the healthcare skills as specialist overlays on top of the BMAD agent roles, not as replacements for them
- prefer multi-skill composition when one change needs structural, regulatory, documentation, and usability review in parallel
- reuse `.health-context.yaml` when it exists instead of re-deriving healthcare context from scratch
```

## Sources

- Spec-Kit: <https://github.com/github/spec-kit>
- Spec-Kit docs: <https://github.github.com/spec-kit/index.html>
- BMAD Method: <https://github.com/bmad-code-org/BMAD-METHOD>
- Repository OpenSpec workflow contract: [openspec/specs/skill-authoring-guide/spec.md](/Users/bkaney/projects/vermonster-skills/openspec/specs/skill-authoring-guide/spec.md)
- Repository model and distribution workflow: [docs/repository-model.md](/Users/bkaney/projects/vermonster-skills/docs/repository-model.md)
