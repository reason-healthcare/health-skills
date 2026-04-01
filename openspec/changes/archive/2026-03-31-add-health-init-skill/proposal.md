## Why

Healthcare-oriented skills repeatedly need the same top-level project context before they can give accurate guidance: which regulatory market applies, who the product primarily serves, and whether the repository is an existing system or a greenfield effort. Today that context is inferred ad hoc on each run, which creates repeated questioning, inconsistent assumptions, and unnecessary US-default bias.

## What Changes

- Add a new `health-init` skill that inspects a target repository, gathers evidence, and determines three reusable context fields: jurisdiction (`US`, `EU`, `US+EU`, or `unclear`), primary audience (`provider`, `patient`, `payer`, `administrative`, `other`, or `mixed`), and project stage (`greenfield`, `existing`, or `unclear`).
- The skill writes a durable root-level context artifact in the target repository so future healthcare skills can reuse confirmed context instead of re-deriving it from scratch.
- The skill treats `project stage` as agent-determined from repository evidence rather than a required user prompt, while still allowing override when the evidence is mixed.
- The skill records confidence and evidence for each inferred field so downstream skills can decide when to trust the stored answer versus when to ask for confirmation.
- The skill is designed as a bootstrap step for future healthcare skill orchestration, not as a generic repository initializer or code scaffold.

## Capabilities

### New Capabilities

- `health-init-skill`: A repository bootstrap skill that infers healthcare project context from repo evidence, persists it in a root-level artifact, and exposes jurisdiction, audience, and project-stage signals for downstream skills.

### Modified Capabilities

- `healthcare-skill-library`: Add the project-context bootstrap skill to the healthcare skill catalog and define it as a reusable context source for future skills.

## Impact

- New skill directory added at `skills/.experimental/health-init/`
- New artifact contract for a root-level persistent context file in target repositories
- New references and examples for jurisdiction detection, audience inference, and repository stage detection
- README and DEVELOPER.md updated with the new skill entry when implemented
- Future healthcare skills may read the persisted context artifact to avoid repeated discovery and to make jurisdiction- and audience-aware decisions more consistently
