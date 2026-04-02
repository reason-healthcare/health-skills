## Context

This repository is intended to become the shared source for AI skills used to build healthcare technology software and digital health products. The skills need to be reusable across agents, compatible with `skills.sh`, and structured so teams can author, validate, and distribute them consistently.

The current repository already contains local install directories such as `.agents/skills`, `.claude/skills`, and `.github/skills`. That layout is useful for local consumption, but it is not a strong long-term authoring model for a shared healthcare skill library because the primary value of the repo is the curated skill content itself, not runtime copies.

Healthcare-oriented skills also need stronger structure than generic prompt assets. They will likely accumulate reusable references, templates, workflow guidance, and possibly scripts for deterministic transformations. That makes repository conventions, packaging rules, and validation gates part of the product, not just implementation detail.

Stakeholders include:
- Skill authors creating shared healthcare engineering and product-development skills
- Teams consuming those skills through `skills.sh` or agent-specific installations
- Maintainers responsible for validation, versioning, and distribution quality

## Goals / Non-Goals

**Goals:**
- Define a canonical source-of-truth layout for a shared healthcare skill library.
- Preserve compatibility with `skills.sh` and standard Agent Skills `SKILL.md` conventions.
- Support optional per-agent overlays without duplicating the base skill.
- Standardize how new skills are scaffolded, documented, validated, and prepared for distribution.
- Establish a repository model that can scale from a few curated skills to a maintained healthcare-tech skill catalog.

**Non-Goals:**
- Define the full content of every healthcare skill in this change.
- Introduce a custom runtime or proprietary packaging format beyond what `skills.sh` and agent skill conventions already support.
- Solve healthcare compliance implementation details inside this foundational change.
- Guarantee behavioral parity across all agents beyond what can be enforced through shared source structure and overlays.

## Decisions

### Use a canonical `skills/` tree as the authored source of truth for distributed healthcare skills

The repository SHALL treat `skills/` as the primary authored skill library for distributed healthcare skills, with `.curated` and `.experimental` used to communicate stability.

Rationale:
- It matches the mental model of a reusable skill library better than agent-specific folders.
- It works naturally with `skills.sh`-style discovery and distribution patterns.
- It makes the healthcare skill catalog the product, rather than a set of mirrored installations.

Alternatives considered:
- Keep `.agents/skills`, `.claude/skills`, and similar directories as co-equal sources. Rejected because it creates drift and weak ownership boundaries.
- Store all skills in a flat repository root. Rejected because it scales poorly as references, assets, and helper scripts grow.

OpenSpec workflow skills used to operate this repository are local development tooling and are not part of the distributed healthcare skill source model.

### Separate agent-specific behavior into overlays under `profiles/`

Agent-specific differences SHALL live under `profiles/<agent>/<skill>/` and SHALL be treated as optional overlays applied on top of a base skill.

Expected overlay contents may include:
- `SKILL.patch.md` or a similar delta mechanism for instruction differences
- `agents/openai.yaml` or other agent-facing metadata overrides
- Small agent-specific support files when necessary

Rationale:
- The healthcare domain logic should stay in one base skill.
- Agent-specific prompt tuning and metadata differences are real, but they should be explicit and isolated.
- Overlay composition keeps portability while allowing practical adaptation.

Alternatives considered:
- Fork each skill per agent. Rejected because it increases maintenance cost and content divergence.
- Forbid agent-specific customization. Rejected because some agents will require different metadata or prompting constraints.

### Standardize a single reusable skill template

New skills SHALL be scaffolded from a common template containing:
- `SKILL.md`
- `agents/openai.yaml`
- Optional `scripts/`
- Optional `references/`
- Optional `assets/`

The template SHALL be optimized for progressive disclosure:
- Core trigger and workflow guidance stays in `SKILL.md`
- Large domain documentation moves to `references/`
- Deterministic or repetitive actions move to `scripts/`
- Non-context assets move to `assets/`

Rationale:
- This follows the strongest current skill-authoring pattern: concise triggerable core, deeper resources loaded only when needed.
- Healthcare skills will often require structured references such as terminology, workflow constraints, interoperability notes, or product templates.
- A single template reduces ambiguity for contributors and keeps repository quality consistent.

Alternatives considered:
- Allow each skill author to choose arbitrary structure. Rejected because discoverability and validation degrade quickly.
- Put all instructions in `SKILL.md`. Rejected because it bloats context and does not scale for domain-heavy skills.

### Treat validation and distribution as first-class repository workflows

The repository SHALL define scripts and conventions for:
- Skill initialization
- Frontmatter and naming validation
- Optional metadata generation
- Profile composition into install targets
- Distribution readiness checks for curated skills

Validation SHOULD enforce at least:
- Valid `SKILL.md` frontmatter
- Stable skill naming rules
- Presence and correctness of required files
- Overlay compatibility with the base skill

Rationale:
- Shared healthcare skills need predictable quality before distribution.
- Manual review alone will not scale once the library grows.
- `skills.sh` compatibility is easier to preserve when install and validation flows are explicit.

Alternatives considered:
- Rely on ad hoc manual conventions. Rejected because it is too fragile for a shared library.
- Build a fully custom publishing platform now. Rejected because it adds unnecessary scope to the foundation change.

### Position the repository around healthcare product-development workflows

The first-class organizational model SHALL assume the skill library serves healthcare software and product teams. The repository structure, templates, and creation guide SHOULD make room for categories such as:
- Product strategy and discovery
- Clinical workflow-aware UX and service design
- Healthcare data and interoperability engineering
- Regulated software delivery and documentation support
- Security, privacy, and operational readiness guidance

Rationale:
- The repo’s value is domain specificity.
- Generic skill infrastructure is not enough; the authoring guide and examples need to steer contributors toward healthcare-relevant patterns.

Alternatives considered:
- Keep the foundation fully domain-agnostic. Rejected because it would underspecify the actual purpose of the repository.

## Risks / Trade-offs

- [Overlay composition becomes ambiguous] -> Mitigation: define a narrow supported overlay contract up front and validate overlay file types explicitly.
- [Healthcare scope remains too broad for contributors] -> Mitigation: use the creation guide and curated categories to constrain what “in-scope” skills look like.
- [Agent-specific install paths drift from canonical source] -> Mitigation: make generated/composed installs derived artifacts, not authoring locations.
- [Validation becomes burdensome early] -> Mitigation: start with lightweight structural checks and add stricter rules only where repeated failures occur.
- [Base skills become overloaded with compliance or policy detail] -> Mitigation: keep core workflow concise and move domain-heavy guidance into `references/`.

## Migration Plan

1. Introduce the canonical `skills/`, `profiles/`, `templates/`, `docs/`, and `scripts/` repository structure.
2. Define the skill template and the healthcare-focused authoring guide.
3. Add validation and composition scripts for base skills and overlays.
4. Migrate existing reusable skills into canonical source locations.
5. Generate or compose agent-specific install trees from canonical skills plus overlays.
6. Deprecate direct authoring in agent-specific skill folders once composed output is validated.

Rollback strategy:
- If composition or install automation proves unstable, continue consuming the existing agent-specific folders temporarily while retaining the new canonical structure as the emerging source of truth.
- Avoid destructive migration of existing skill folders until composed outputs are verified.

## Open Questions

- What exact `skills.sh` packaging and install commands should the repo optimize for first?
- Should overlays use patch files, append-only fragments, or fully overridden metadata files as the default mechanism?
- What initial healthcare skill categories should be considered “curated” for the first release of the library?
- How much healthcare-specific governance should live in the authoring guide versus in individual skill references?
