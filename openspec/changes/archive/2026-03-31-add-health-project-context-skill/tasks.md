## 1. Scaffold Skill Directory

- [x] 1.1 Run `python3 scripts/init_skill.py health-project-context --group .experimental --description "derive reusable healthcare project context from repository evidence"` to scaffold the skill directory
- [x] 1.2 Verify `skills/.experimental/health-project-context/` was created with `SKILL.md` and `agents/openai.yaml`
- [x] 1.3 Create `skills/.experimental/health-project-context/references/` with placeholder files: `jurisdiction-signals.md`, `audience-signals.md`, `stage-signals.md`
- [x] 1.4 Create `skills/.experimental/health-project-context/examples/` with a placeholder example artifact showing `.health-context.yaml`

## 2. Write Reference Files

- [x] 2.1 Write `references/jurisdiction-signals.md` covering US signals (HIPAA, CMS, ONC, USCDI, US Core, NPI, Medicare, Medicaid), EU signals (GDPR, EHDS, MDR, IVDR, NIS2, AI Act), mixed-market evidence, and `unclear` handling
- [x] 2.2 Write `references/audience-signals.md` covering evidence patterns for `provider`, `patient`, `payer`, `administrative`, `other`, and `mixed`, with examples drawn from workflows, role names, documentation, and UI labels
- [x] 2.3 Write `references/stage-signals.md` covering repository maturity heuristics for `existing`, `greenfield`, and `unclear`, including source trees, CI config, migrations, lockfiles, deployment files, and spec-only/template-only repos

## 3. Write Examples

- [x] 3.1 Create `examples/example-health-context.yaml` showing a complete `.health-context.yaml` artifact with `version`, `generated_at`, structured field objects, evidence arrays, and `confirmed_by_user`
- [x] 3.2 Create `examples/example-run.md` showing a realistic skill result summary for a target repo, including proposed values, evidence, confidence, and pre-write confirmation behavior

## 4. Write SKILL.md

- [x] 4.1 Write the frontmatter for `SKILL.md` with accurate trigger language for repository bootstrap and project-context detection
- [x] 4.2 Write the Overview/Purpose section explaining the skill’s role as a reusable healthcare bootstrap step for downstream skills
- [x] 4.3 Write the workflow section covering: read existing `.health-context.yaml` if present, scan repository evidence, infer jurisdiction, infer primary audience, infer project stage, present proposed values, and write the artifact after confirmation or override
- [x] 4.4 Write the artifact contract section documenting `.health-context.yaml`, required top-level keys, field schema (`value`, `confidence`, `evidence`), and refresh behavior for existing files
- [x] 4.5 Write the operating rules section covering: evidence-first inference, no code or infrastructure scaffolding, prompt-injection boundary, and update-only-when-changed behavior
- [x] 4.6 Write the downstream reuse guidance section describing `.health-context.yaml` as a default input source for future healthcare skills with override semantics

## 5. Update Agent Metadata And Repository Docs

- [x] 5.1 Update `skills/.experimental/health-project-context/agents/openai.yaml` with accurate name, description, and tool permissions for a read-heavy skill that writes only `.health-context.yaml`
- [x] 5.2 Add `health-project-context` to `README.md` in the skills listing with a concise description consistent with the rest of the library
- [x] 5.3 Add `health-project-context` to `DEVELOPER.md` under experimental skills
- [x] 5.4 Update `docs/skill-creation-guide.md` if needed to mention reusable context artifacts as a valid healthcare skill pattern

## 6. Validate And Verify

- [x] 6.1 Run `python3 scripts/validate_skill_library.py` and resolve any validation errors for the new skill
- [x] 6.2 Run `python3 scripts/verify_skills_sh_compat.py` and confirm the new skill remains compatible with skills.sh expectations
- [x] 6.3 Run `python3 scripts/audit_skill_security.py` and confirm no FAIL findings for the new skill
- [x] 6.4 Review `SKILL.md` against the OpenSpec design and specs to confirm coverage of jurisdiction inference, audience inference, project-stage detection, artifact schema, override flow, and prompt-injection handling
- [x] 6.5 Verify the example artifact and example run output match the documented `.health-context.yaml` contract
