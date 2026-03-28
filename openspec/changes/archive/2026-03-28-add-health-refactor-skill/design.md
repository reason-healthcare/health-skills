## Context

The health-skills repository contains four curated skills (`health-fhir-api-design`, `health-hipaa-review`, `health-human-factors`, `health-product-discovery`). Each is standalone: one SKILL.md, one agent overlay, references, and examples. No skill currently composes another skill at invocation time.

An external generic `refactor` skill exists but has no healthcare awareness — it covers code smells, extraction patterns, and structural improvements without considering HIPAA, patient safety, or clinical domain patterns.

Developers refactoring healthcare codebases today either skip compliance/safety review or run multiple tools separately and reconcile manually. The `health-refactor` skill fills this gap by orchestrating three analysis lenses into a single bounded plan.

## Goals / Non-Goals

**Goals:**
- Produce a scope-bounded, plan-only refactoring assessment that a developer works through item by item
- Support three context modes that each resolve to a bounded file set: git range, file area, symbol/dependency
- Compose existing `health-human-factors` and `health-hipaa-review` skills rather than duplicating their knowledge
- Embed a new healthcare-aware refactoring reference for code-quality analysis
- Establish a reusable "scoped invocation mode" pattern for skill composition across the library
- Include one example plan output per context mode

**Non-Goals:**
- Broad full-codebase refactoring recommendations (scope is always bounded)
- Automated code modification (output is a plan, never patches)
- Replacing the standalone audit capabilities of `health-human-factors` or `health-hipaa-review`
- Transitive dependency resolution in symbol mode (direct imports only)
- Runtime tooling (no complexity analyzers, no AST parsers — the skill works with what the agent can read)

## Decisions

### Decision 1: Hybrid composition model (Approach C)

**Choice**: The refactoring sub-agent is embedded with its own reference material. The human-factors and HIPAA sub-agents compose the existing curated skills via scoped invocation.

**Alternatives considered**:
- **(A) Fully embedded** — all three sub-agents have their own reference material inside `health-refactor`. Rejected: duplicates HIPAA and HF knowledge, creates maintenance burden, violates single-source-of-truth for the library.
- **(B) Fully composed** — all three sub-agents delegate to external skills. Rejected: no existing healthcare-aware refactoring skill to compose; the refactoring reference is new and belongs in this skill.
- **(C) Hybrid** — chosen because the refactoring reference genuinely doesn't exist elsewhere (must be authored), while HIPAA and HF knowledge is already well-maintained in canonical skills. Updates to those skills automatically improve `health-refactor`.

**Rationale**: The library is designed for composition. The hybrid approach composes what exists (HIPAA, HF) and embeds what's new (refactoring patterns). This establishes the first skill-to-skill composition pattern in the library.

### Decision 2: Scoped invocation mode added to existing skills

**Choice**: Add an "Invocation Modes" section to `health-human-factors` and `health-hipaa-review` SKILL.md files that defines a "scoped" mode alongside the existing "standalone" mode.

In scoped mode:
- Input: a pre-determined list of file paths
- Behavior: skip interactive scope confirmation, skip executive summary generation
- Output: findings-only list using a consistent format (`[PREFIX-N] title`, severity, category, file:line, detail, guideline)

**Alternatives considered**:
- *Prompt wrapper* — orchestrator overrides the skill's output contract via prompt instructions. Rejected: conflicting instructions between skill and wrapper; fragile when the model follows the skill's output contract over the wrapper.
- *Post-process* — let skills produce full reports, then extract findings. Rejected: wastes context window on executive summaries and coverage matrices that get discarded; doesn't solve the interactive scope-confirmation problem.

**Rationale**: Scoped mode is a small addition (~15 lines per skill) that makes the skill composable. Any future orchestrating skill (incident review, pre-deployment checklist) can use the same pattern. The skill authors control the output contract for both modes.

### Decision 3: Three context modes resolving to bounded file sets

Every context mode resolves to the same thing: a list of files. The orchestrator resolves context first, then passes the file list to all three sub-agents.

**Git range** (`HEAD~5..HEAD`, `origin/main..HEAD`, etc.)
- Resolution: `git diff --name-only <range>` filtered to existing files
- Use case: "review what we just built" or "review this branch's changes"

**File area** (`app/dashboard`, `src/services/patient`)
- Resolution: all files under the given path, respecting `.gitignore`
- Use case: "this area needs cleanup" or "we're about to work in this area"

**Symbol/dependency** (`PatientService`, `MedList.tsx`)
- Resolution: find the file containing the symbol, then resolve direct imports (files it imports) and direct importers (files that import it)
- Depth: direct imports only, no transitive resolution
- Use case: "this class is tangled" or "we need to refactor this service"
- Requires reporting: the resolved file set and dependency graph are included in plan output so the user can see exactly what was and wasn't reviewed

**All modes** include a scope section in the output that lists every file analyzed.

### Decision 4: Plan output structure — findings + checklist

The output is plain text (markdown) with two main sections:

1. **Findings**: the evidence. Each finding has an ID, source sub-agent, severity, category, file location, detail, and guideline reference. Findings are the "what was discovered" section.

2. **Refactor Checklist**: the action plan. A prioritized table where each row is a concrete action and references one or more finding IDs. Priority order: safety-critical (P1) → structural (P2) → improvement (P3).

3. **Risks & Notes**: caveats, things that could go wrong during execution, dependencies between checklist items.

This separation means findings can be reviewed independently ("do I agree with the assessment?") before committing to the checklist ("do I agree with the plan?").

### Decision 5: Healthcare refactoring reference — two-part structure composing with baseline skills

**Choice**: The `references/refactor-patterns.md` file is organized in two parts. Standard refactoring is delegated to a baseline refactoring skill (e.g., `$refactor`) or the agent's innate knowledge. The reference covers only what an agent cannot figure out on its own.

**Part 1 — Healthcare-Specific Patterns** (7 full entries for concerns unique to healthcare):
- **Clinical terminology duplication** — hardcoded LOINC, SNOMED, ICD-10 codes across files
- **FHIR resource handling** — raw JSON vs. typed resource wrappers, serialization coupling
- **Clinical data formatting** — date, time, unit, and numeric formatting scattered vs. centralized
- **Audit trail integrity** — refactoring that risks breaking audit log continuity or losing actor attribution
- **Tenant isolation** — shared services where refactoring could introduce cross-tenant data exposure
- **Clinical domain naming** — clinical domain terms that should be preserved in code (not genericized)
- **Error handling in clinical paths** — fail-safe vs. fail-secure patterns for patient-facing code

**Part 2 — Healthcare Overrides to Standard Refactoring** (compact clinical nuances that modify standard heuristics):
- **Long method / god class** — do not flag cohesive clinical workflows; preserve audit trail when splitting
- **Dead code and feature flags** — verify clinical flags are not safety gates before removing
- **Test coverage** — clinical logic requires tests as a prerequisite; edge cases cause safety incidents
- **Code modularity** — dependency direction enables safe FHIR version and EHR integration evolution
- **Inline documentation** — document clinical rationale and source authority for magic numbers

**Rationale**: Any agent already knows standard refactoring (extract method, eliminate duplication, reduce complexity). Including those patterns dilutes the healthcare-specific signal. The two-part structure keeps the reference focused: Part 1 is what's unique, Part 2 is where clinical context overrides standard advice.

When a baseline refactoring skill is available, Step 2 composes with it: delegate standard analysis, then layer healthcare patterns on top, then apply healthcare overrides to adjust or suppress standard findings.

### Decision 6: Scaffold via init_skill.py

**Choice**: Use the existing `scripts/init_skill.py` scaffold tool to initialize the skill directory structure, then customize the generated files.

```bash
python3 scripts/init_skill.py health-refactor \
  --group .curated \
  --description "healthcare codebase refactoring" \
  --include references examples
```

This produces:
```
skills/.curated/health-refactor/
  SKILL.md              ← template, to be replaced with full orchestrator instructions
  agents/openai.yaml    ← template, to be customized
  references/           ← will contain refactor-patterns.md
  examples/             ← will contain example-plan-{git-range,file-area,symbol}.md
```

The scaffold handles naming normalization, directory creation, and template expansion. The generated SKILL.md and openai.yaml are starting points that get replaced with the full skill content during implementation.

### Decision 7: Sub-agent dispatch is sequential in SKILL.md instructions

The orchestrator SKILL.md instructs the agent to run sub-agents in order: (1) refactor, (2) human-factors, (3) HIPAA. This is a logical ordering in the instructions, not a technical parallelism constraint — the agent resolves files once and passes the same list to each analysis pass.

The refactor analysis runs first because it identifies structural issues that inform how HF and HIPAA findings relate to code organization. HF and HIPAA findings then layer compliance and safety concerns onto the structural picture.

## Risks / Trade-offs

**[Risk] Scoped invocation mode may not constrain output reliably** → The scoped mode section in each skill is explicit about input/output format. If models drift toward full-report output, the orchestrator's instructions reinforce "findings-only." Two layers of instruction (skill + orchestrator) provide redundancy.

**[Risk] Symbol/dependency resolution depends on import parsing** → The agent reads source files and follows import/require/include statements. Complex re-exports, dynamic imports, or non-standard module systems may produce incomplete file sets. Mitigation: the plan always reports what was resolved, so gaps are visible. Direct-imports-only constraint limits blast radius.

**[Risk] Refactoring reference may overlap with generic refactor skill** → Resolved. The reference was restructured into two parts: Part 1 covers only healthcare-specific patterns (7 entries), and Part 2 provides clinical overrides to standard refactoring heuristics. Standard patterns (extract method, rename variable, reduce complexity) are explicitly excluded — they are handled by the baseline refactoring skill or the agent's innate knowledge. Step 2 composes with a baseline `$refactor` skill when available.

**[Risk] Three sub-agent passes consume significant context window** → Each pass reads the same file set. For large file areas this could exceed context limits. Mitigation: the bounded-scope constraint exists precisely to prevent this. Git range and symbol modes naturally produce small file sets. File area mode should warn if the resolved file count exceeds a threshold (suggest narrowing scope).

**[Trade-off] Composed skills must be installed alongside health-refactor** → Unlike fully embedded skills, health-refactor requires `health-human-factors` and `health-hipaa-review` to be present. This is acceptable because all three are curated skills distributed via the same `dist` branch. The install tooling can handle this as a set.

## Open Questions

- **File count threshold**: Resolved — set to 30 files in SKILL.md Operating Rules.
- **Example plan fidelity**: Resolved — examples use a fictional healthcare app with realistic file paths and clinical patterns.
- **Refactoring reference depth**: Resolved — Part 1 has 7 full pattern entries (moderate detail, similar to control-areas.md), Part 2 is a compact override section (~30 lines). Total length is shorter than the HF style guide.
