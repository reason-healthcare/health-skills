## 1. Scaffold and Modify Existing Skills

- [x] 1.1 Add scoped invocation mode section to `skills/.curated/health-human-factors/SKILL.md` — add an "Invocation Modes" section after the Output Contract that defines standalone (default, existing behavior) and scoped (input: file list, output: findings-only with `HF-` prefix, skip scope confirmation and executive summary)
- [x] 1.2 Add scoped invocation mode section to `skills/.curated/health-hipaa-review/SKILL.md` — add an "Invocation Modes" section after the Output Contract that defines standalone (default, existing behavior) and scoped (input: file list, output: findings-only with `H-` prefix, skip scope confirmation and executive summary)

## 2. Scaffold health-refactor Skill

- [x] 2.1 Run `python3 scripts/init_skill.py health-refactor --group .curated --description "healthcare codebase refactoring" --include references examples` to create the base skill directory structure
- [x] 2.2 Replace the generated `skills/.curated/health-refactor/agents/openai.yaml` with the customized agent overlay (display name, short description, default prompt referencing context modes)

## 3. Author Refactoring Reference

- [x] 3.1 Create `skills/.curated/health-refactor/references/refactor-patterns.md` with healthcare-aware refactoring patterns covering: long method / god class (healthcare context), clinical terminology duplication, FHIR resource handling, clinical data formatting centralization, audit trail integrity, tenant isolation risks, dead code and clinical feature flags, clinical domain naming, error handling in clinical paths, and test coverage awareness

## 4. Author Orchestrator SKILL.md

- [x] 4.1 Replace the generated `skills/.curated/health-refactor/SKILL.md` with the full orchestrator skill — frontmatter (name, description), overview, operating rules (plan-only, never modify code)
- [x] 4.2 Add context mode resolution section to SKILL.md — instructions for resolving git range (`git diff --name-only`), file area (directory listing), and symbol/dependency (locate file, resolve direct imports and importers)
- [x] 4.3 Add sub-agent dispatch section to SKILL.md — instructions for running the embedded refactoring analysis (load `references/refactor-patterns.md`, produce `R-` prefixed findings), then composing `health-human-factors` in scoped mode (`HF-` prefix), then composing `health-hipaa-review` in scoped mode (`H-` prefix)
- [x] 4.4 Add plan output section to SKILL.md — output contract specifying Scope section (context mode, resolved file list, dependency graph for symbol mode), Findings section (per sub-agent), Refactor Checklist (prioritized table with finding references and checkboxes), and Risks & Notes
- [x] 4.5 Add constraints and guardrails to SKILL.md — plan-only, never modify code, warn if file set exceeds threshold, require context mode before proceeding

## 5. Author Example Plans

- [x] 5.1 Create `skills/.curated/health-refactor/examples/example-plan-git-range.md` — example plan using a git range context (e.g., `origin/main..feature-branch`) showing scope with changed file list, findings from all three sub-agents, prioritized checklist, and risks
- [x] 5.2 Create `skills/.curated/health-refactor/examples/example-plan-file-area.md` — example plan using a file area context (e.g., `src/dashboard`) showing scope with directory file list, findings from all three sub-agents, prioritized checklist, and risks
- [x] 5.3 Create `skills/.curated/health-refactor/examples/example-plan-symbol.md` — example plan using a symbol/dependency context (e.g., `PatientService`) showing scope with dependency graph (root, direct imports, direct importers), findings from all three sub-agents, prioritized checklist, and risks

## 6. Validation

- [x] 6.1 Run `python3 scripts/validate_skill_library.py` to verify the new skill passes library validation
- [x] 6.2 Verify `health-human-factors` and `health-hipaa-review` still pass validation after scoped invocation mode additions
