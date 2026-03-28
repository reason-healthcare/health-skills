## 1. Scaffold Skill Directory

- [x] 1.1 Run `python scripts/init_skill.py health-docs --group .experimental --description "healthcare system documentation coverage and consolidation"` to scaffold the skill directory
- [x] 1.2 Verify `skills/.experimental/health-docs/` was created with `SKILL.md`, `agents/openai.yaml`
- [x] 1.3 Create `skills/.experimental/health-docs/references/` directory with placeholder files: `doc-hierarchy.md`, `regime-signals.md`, `regulatory-mapping.md`
- [x] 1.4 Create `skills/.experimental/health-docs/examples/` directory with placeholder files: `example-analysis.md`, `example-analysis-artifact.md`

## 2. Write References

- [x] 2.1 Write `references/doc-hierarchy.md` — canonical seven-dimension documentation tree (orient, understand, build, operate, secure, comply, agent-context) with all file paths, descriptions, and audience notes
- [x] 2.2 Write `references/regime-signals.md` — PHI signal patterns (field names, model names, FHIR types, HL7 refs), ONC signals (SMART, USCDI, EHR SDKs), FDA SaMD signals (ML inference, clinical scoring, diagnostic language)
- [x] 2.3 Write `references/regulatory-mapping.md` — table mapping each documentation dimension to the regulatory requirement it satisfies (HIPAA §, ONC rule, FDA guidance), with required vs. addressable classification

## 3. Write SKILL.md

- [x] 3.1 Write the Overview section describing the skill's purpose, two-mode design, and healthcare regulatory context
- [x] 3.2 Write the analyze mode workflow: Pass 1 (broad scan + regime signal detection), Pass 2 (parallel subagent dispatch), Pass 3 (synthesize coverage matrix), write `.health-docs/analysis.md`
- [x] 3.3 Write the document mode workflow: read artifact, present evidence-informed interview (3 confirmations), write requirements profile, pre-flight plan, execute consolidate → merge → draft, update run record
- [x] 3.4 Write the subagent dispatch contract section: how to invoke `$health-hipaa-review`, `$health-fhir-api-design`, `$health-human-factors` in scoped mode and how to translate their findings to coverage dimensions
- [x] 3.5 Write the `.health-docs/analysis.md` artifact schema section: YAML structure, coverage matrix fields, requirements profile fields, run record format
- [x] 3.6 Write Operating Rules: never modify code or tests; never silently resolve conflicts; always mark regulatory-class drafts for human review; degrade gracefully without subagents
- [x] 3.7 Write the Output Contract for each mode (analysis mode → `.health-docs/analysis.md`; document mode → structured docs + run record)

## 4. Write Examples

- [x] 4.1 Write `examples/example-analysis.md` — realistic sample analyze mode output for a fictional FHIR-based healthcare app showing: coverage matrix, regime detection narrative, conflict flags, external link flags, summary
- [x] 4.2 Write `examples/example-analysis-artifact.md` — sample `.health-docs/analysis.md` file showing full YAML structure with coverage entries, null required fields pre-interview, and populated required fields post-interview

## 5. Update agents/openai.yaml

- [x] 5.1 Update `agents/openai.yaml` with accurate name, description, and tool permissions appropriate for a skill that reads files, runs subagents, and writes to `.health-docs/` and `docs/`

## 6. Update Repository Documentation

- [x] 6.1 Add `health-docs` entry to `README.md` skill listing with name, link, and one-line description consistent with other skill entries
- [x] 6.2 Add `health-docs` to the experimental skills list in `DEVELOPER.md`
- [x] 6.3 Update `docs/skill-creation-guide.md` if the guide references the list of available skills or composition patterns that `health-docs` exemplifies (subagent orchestration, two-mode design)
- [x] 6.4 Run `python scripts/validate_skill_library.py` and resolve any validation errors

## 7. Verify

- [x] 7.1 Run `python scripts/verify_skills_sh_compat.py` to confirm SKILL.md shell compatibility
- [x] 7.2 Review SKILL.md against `references/doc-hierarchy.md` — confirm all seven dimensions are addressed in the workflow
- [x] 7.3 Review SKILL.md against `references/regulatory-mapping.md` — confirm all HIPAA-required dimensions are flagged in the workflow
- [x] 7.4 Verify example analysis artifact accurately reflects the YAML schema documented in SKILL.md
- [x] 7.5 Confirm SKILL.md documents existing-directory detection and `docs/` fallback behavior (Decision 3): existing convention is used silently; `docs/` is proposed only when no directory is found, with pre-flight override available
