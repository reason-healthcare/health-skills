## Why

Healthcare codebases need refactoring guidance that goes beyond generic code-smell detection. A refactoring plan in a clinical system must account for HIPAA compliance risks, patient-safety implications in UI changes, and domain-specific patterns like FHIR resource handling and clinical terminology coupling. Today, `health-human-factors` and `health-hipaa-review` exist as standalone audit skills, and a generic `refactor` skill exists externally, but nothing composes these three lenses into a unified, scope-bounded refactoring plan. Without this, developers either skip compliance/safety review during refactoring or run three separate tools and reconcile the output manually.

## What Changes

- Add a new curated skill `health-refactor` that produces a plan-only, scope-bounded refactoring assessment
- The skill supports three context modes for scoping what to analyze: git range, file area, and symbol/dependency graph (direct imports only)
- The skill orchestrates three sub-agent analyses: an embedded healthcare-aware refactoring review, a composed invocation of `health-human-factors`, and a composed invocation of `health-hipaa-review`
- Output is a text-based plan with findings (evidence) and a prioritized checklist (actions referencing findings). No code is modified.
- The skill uses a hybrid composition model: the refactoring sub-agent is embedded with its own reference material; the human-factors and HIPAA sub-agents compose the existing skills via scoped invocation
- Add a "scoped invocation mode" to `health-human-factors` and `health-hipaa-review` so they can accept a pre-determined file list and return findings-only output (no executive summary, no coverage matrix, no interactive scope confirmation)

## Capabilities

### New Capabilities
- `health-refactor-skill`: the orchestrator skill, context modes (git-range, file-area, symbol-dependency), embedded refactoring reference, sub-agent dispatch, plan output format with findings and checklist

### Modified Capabilities
- `healthcare-skill-library`: adds `health-refactor` to the curated skill catalog and establishes the scoped invocation pattern for skill composition

## Impact

- **New files**: `skills/.curated/health-refactor/SKILL.md`, `skills/.curated/health-refactor/agents/openai.yaml`, `skills/.curated/health-refactor/references/refactor-patterns.md`, `skills/.curated/health-refactor/examples/example-plan-git-range.md`, `skills/.curated/health-refactor/examples/example-plan-file-area.md`, `skills/.curated/health-refactor/examples/example-plan-symbol.md`
- **Modified files**: `skills/.curated/health-human-factors/SKILL.md` (add scoped invocation mode section), `skills/.curated/health-hipaa-review/SKILL.md` (add scoped invocation mode section)
- **Dependencies**: `health-refactor` requires both `health-human-factors` and `health-hipaa-review` to be installed for full operation
- **Distribution**: `health-refactor` added to `dist` branch via existing publish pipeline; consumer install pulls all three skills as a set
