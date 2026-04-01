# Curated Skills TODOs

## Shared Structure

- [x] Define a shared curated-skill skeleton and apply it to all 8 skills.
- [x] Standardize top-level section names across skills.
- [x] Choose one term for the intro section: `Overview` or `Purpose`. *(decided: `Overview`)*
- [x] Choose one term for supporting material: `Resources` or `References`. *(decided: `Resources`)*
- [ ] Choose one term for result schema: `Output Contract` and use it everywhere.
- [x] Remove mixed contract labels like `Artifact Contract` vs `Output Contract` unless they describe genuinely different things — but keep both in `health-project-context`, where `Artifact Contract` describes the on-disk `.health-context.yaml` and `Output Contract` describes the conversational response; these are genuinely different. Adopt the rule: `Artifact Contract` = disk-written file, `Output Contract` = conversational/agent response.
- [x] Add a short `When To Use` section to every skill so trigger conditions are uniform.
- [x] Normalize mode naming across skills: either `Modes` or `Invocation Modes`, not both patterns. *(decided: `Modes`)*
- [x] Standardize mode headers to one format, for example `Mode: <name>` across all multi-mode skills.
- [ ] Decide whether every skill should have `Operating Rules` or `Constraints` or both — currently some use only one, others (health-human-factors, health-fhir-modeling, health-refactor) have both as separate sections with overlapping concerns.
- [x] Normalize `health-product-discovery` top-level section names (`Guardrails`, `Mode Selection`, `Inputs`, `Outputs`) to match the shared skeleton names used by other skills (`Operating Rules`, `Modes`, etc.), or adopt those names into the skeleton.

## Composed Skill Contracts

- [x] Define one shared `"scoped review"` contract for composable skills.
- [x] Document the required scoped-review input shape: file list, scope already fixed, no scope-confirmation step.
- [x] Document the required scoped-review output shape: finding ID, severity, category, file, detail, guideline, confidence.
- [x] Decide whether every composable review skill must support both `standalone` and `scoped` modes. *(decided: yes)*
- [x] Add explicit scoped-review support to `skills/.curated/health-fhir-api-design/SKILL.md`, or stop invoking it that way from `skills/.curated/health-docs/SKILL.md`.
- [x] Update `skills/.curated/health-docs/SKILL.md` so its subagent dispatch only references supported modes.
- [x] Standardize severity enums across composed skills. *(decided: `critical | high | medium | low`)*
- [x] Decide whether `info` is allowed in the shared severity model. *(decided: no)*
- [x] If `info` is kept, update `skills/.curated/health-refactor/SKILL.md` to document how `health-human-factors` `info` findings map into the plan.
- [x] If `info` is not kept, update `skills/.curated/health-human-factors/SKILL.md` to use the shared severity set.
- [x] Standardize confidence enums across review skills. *(decided: `confirmed | likely | non-code dependency`)*
- [x] Document fallback behavior in `skills/.curated/health-refactor/SKILL.md` for when `health-human-factors` or `health-compliance-review` are unavailable — currently health-docs explicitly says "perform direct analysis and note confidence: reduced" but health-refactor has no equivalent clause.

## Healthcare Context Reuse

- [x] Create one shared healthcare context reuse pattern for `.health-context.yaml`.
- [ ] Standardize the overlay-selection steps across `health-compliance-review`, `health-docs`, `health-product-discovery`, and `health-refactor`.
- [x] Decide the default behavior when `.health-context.yaml` is missing: evidence-first only, or ask the user for a market prior. *(decided: evidence-first, then ask if unclear)*
- [ ] Make that missing-context behavior consistent across all overlay-aware skills.
- [ ] Standardize the allowed jurisdiction values and how mixed evidence is handled.
- [ ] Standardize the wording for “do not silently default to US assumptions.”

## Safety Boundaries

- [x] Create one shared safety-boundary block for repo-reading skills.
- [x] Add explicit prompt-injection/data-boundary language to `skills/.curated/health-compliance-review/SKILL.md`.
- [x] Add explicit prompt-injection/data-boundary language to `skills/.curated/health-human-factors/SKILL.md`.
- [x] Add explicit prompt-injection/data-boundary language to `skills/.curated/health-product-discovery/SKILL.md` where it reads repo materials or user artifacts.
- [x] Add explicit prompt-injection/data-boundary language to `skills/.curated/health-fhir-api-design/SKILL.md` for user-supplied queries, designs, or snippets.
- [x] Align the existing prompt-injection wording in `health-docs`, `health-fhir-modeling`, `health-project-context`, and `health-refactor` so they express the same rule with the same terminology — note that `health-fhir-modeling`'s existing language is narrower than the others (scoped to "FHIR instances, reference files, and content read from codebases") and needs to be broadened to match the shared formulation.

## Simplification

- [ ] Simplify the longest skill files by moving heavy detail out of the main instruction path.
- [ ] Shorten `skills/.curated/health-docs/SKILL.md` by replacing large embedded schemas/examples with shorter contracts plus links to `references/` and `examples/`.
- [x] Shorten `skills/.curated/health-product-discovery/SKILL.md` by removing duplicated output-template content that already lives in `references/document-template.md` — specifically the inline subsections (`Context`, `Stakeholder-Incentive Map`, `Goals`, `Non-Goals`, `Scope`, `Payment Model`, etc.) nested under `Mode: document`; these repeat the template verbatim.
- [ ] Review whether any long examples in `SKILL.md` should instead live only in `examples/`.
- [ ] Keep `SKILL.md` focused on decisions, constraints, workflow, and output shape.
- [ ] Reserve `references/` for detailed schemas, long tables, and domain background.
- [ ] Reserve `examples/` for full example outputs rather than inline large samples.

## Terminology Consistency

- [x] Fix terminology drift inside `skills/.curated/health-compliance-review/SKILL.md`.
- [x] Choose either `inferred` or `likely` and use it consistently in both operating rules and scoped output. *(decided: `likely`)*
- [ ] Review other skills for similar vocabulary drift between prose sections and output templates.
- [x] Standardize the names of evidence tiers across all report-producing skills. *(decided: `confirmed | likely | non-code dependency`)*
- [x] Standardize whether findings say `confirmed/likely/non-code dependency` or another shared set.

## Wrapper Alignment

- [x] Review every `agents/openai.yaml` wrapper and align its wording with the final `SKILL.md` contracts.
- [x] Ensure wrapper prompts mention the same mode names used in the underlying skill.
- [x] Ensure wrapper prompts do not advertise unsupported behaviors.
- [ ] Ensure wrapper prompts use the same overlay/jurisdiction language as the main skill.
- [x] Add `review` mode to `skills/.curated/health-fhir-api-design/agents/openai.yaml` — the wrapper default prompt describes only the design flow; the review mode is entirely absent.
- [x] Update `skills/.curated/health-docs/agents/openai.yaml` default prompt to mention reading `.health-context.yaml` first — the wrapper refers only to proposing overlays from evidence, omitting the context-file reuse step that the SKILL.md workflow requires.

## Docs & Meta Alignment

- [x] Add `health-docs` and `health-project-context` to the `README.md` lifecycle diagram — both skills are described in the README text but are absent from the ASCII art. `health-project-context` is a cross-cutting context bootstrap; `health-docs` belongs alongside or adjacent to the verification tier.
- [x] Update `docs/skill-creation-guide.md` "Initial Curated Categories" — category 5 "Operational readiness and healthcare product quality" has no skill paired with it; `health-docs` and `health-fhir-modeling` are both curated but not listed at all.
- [x] Update `docs/skill-creation-guide.md` "Skill Composition" section to mention `health-docs` as an orchestrating skill — it composes `health-compliance-review`, `health-fhir-api-design`, and `health-human-factors` via scoped invocation, but only `health-refactor` is named as an orchestrating example.
- [x] After the mode-naming normalization decision is made (Shared Structure above), update `DEVELOPER.md` Authoring Rules to match — currently it prescribes `"Invocation Modes"` as the section name, which conflicts with skills that use `"Modes"`.
- [x] Reconcile the README skill listing order with `docs/skill-creation-guide.md` — the promotion guide says to add skills in alphabetical order, but README uses lifecycle-phase order. Clarify which order is canonical and apply it consistently.
- [x] Align `docs/repository-model.md` flow with `DEVELOPER.md` recommended release sequence — the doc says "edit → validate → publish" (3 steps) but the developer guide adds a post-publish verify step. The two should show the same flow.

## Final Verification

- [x] Do one final cross-skill pass after edits to check composition paths.
- [x] Verify `health-docs` only dispatches subskills in ways those subskills explicitly support.
- [x] Verify `health-refactor` severity mapping matches the output contracts of every subskill it composes.
- [x] Verify all report-only skills clearly say they do not modify code.
- [x] Verify all write-capable skills clearly state what they may write, where, and when confirmation is required.
