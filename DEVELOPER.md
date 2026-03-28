# Developer Guide

This guide is for contributors maintaining the canonical skill source in this repository.

## Source Of Truth

The `main` branch holds the canonical source for all skills. Author and review skills in `skills/`.

Everything else is generated:

- **Local agent trees** (`.claude/skills/`, `.codex/skills/`, `.gemini/skills/`, `.github/skills/`) are built by `compose_skills.py` for use within this repo. Do not hand-edit these.
- **The `dist` branch** is a clean, publishable layout built by `publish_dist_branch.py`. Consumers install from `dist` via `npx skills add`. It contains only composed output — no source authoring happens there.

Edit `skills/` on `main` → validate → compose → publish to `dist`.

## Current Repository Model

- `skills/.curated/`: distributable healthcare skills intended for the `dist` branch
- `skills/.experimental/`: draft skills that are not yet published to `dist`
- `profiles/<agent>/<skill>/`: optional overlays applied during composition
- `templates/skill/`: starter template used by `scripts/init_skill.py`
- `docs/`: repository conventions and authoring guidance
- `scripts/`: validation, composition, and publishing tooling

Current curated skills on disk:

- `health-fhir-api-design`
- `health-hipaa-review`
- `health-human-factors`
- `health-product-discovery`

Current overlay examples on disk:

- `profiles/codex/health-fhir-api-design/agents/openai.yaml`
- `profiles/github/health-product-discovery/SKILL.append.md`

## Distribution Model

This repo has two related outputs:

1. Canonical authored content in `skills/`
2. Generated install layouts built from that content

The scripts support two composition paths:

- `python3 scripts/compose_skills.py`
  - Copies authored skills into the local agent install trees under `.claude/skills`, `.codex/skills`, `.gemini/skills`, and `.github/skills`
- `python3 scripts/compose_skills.py --dist-root /tmp/vermonster-dist`
  - Builds a clean distribution tree containing `README.md` and `skills/.curated/*`

`npx skills add https://github.com/reason-healthcare/health-skills/tree/dist` installs from the published `dist` branch, not from the working branch layout.

For normal authoring work:

- edit `skills/`
- add overlays in `profiles/` only when an agent needs a real customization
- validate before publishing
- use `--dist-root` or `publish_dist_branch.py` when you need the clean distribution output

## Contributing Workflow

1. Choose the right group: `.curated` or `.experimental`.
2. Create or update the skill under `skills/`.
3. Keep `SKILL.md` concise and put large reference material in supporting files.
4. Add overlays only when the agent-facing output must differ from the base skill.
5. Validate the authored library.
6. Build and verify a dist tree when preparing a release.
7. Publish the `dist` branch when the curated library is ready to distribute.

## Create A New Skill

### 1. Proposal

Start with an OpenSpec proposal. Describe the skill's purpose, healthcare context, target users, and intended output shape.

### 2. Scaffold

Once the proposal is accepted, scaffold the skill directory:

```bash
python3 scripts/init_skill.py health-claims-workflow-review \
  --group .experimental \
  --description "claims workflow review" \
  --include references scripts assets
```

This creates a new skill under `skills/.experimental/health-claims-workflow-review/` with the standard file layout.

### 3. Design and Specs

Continue through the OpenSpec artifacts:

- **Design**: detail the workflow, review categories or modes, and output contract
- **Specs**: write the delta specs covering SKILL.md structure, references, and examples

Use the scaffolded directory as the target — fill in `SKILL.md`, references, and examples as the specs take shape.

### 4. Tasks and Implementation

Generate tasks from the specs and implement them. Typical tasks include:

- Write the `SKILL.md` frontmatter, workflow, constraints, and output contract
- Create reference documents in `references/`
- Create an example output in `examples/`
- Write `agents/openai.yaml` metadata

### 5. Test the Experimental Skill

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

### 6. Promote to Curated

When the skill meets the curated standard (see below), move it:

```bash
mv skills/.experimental/health-claims-workflow-review skills/.curated/health-claims-workflow-review
```

Then:

1. Validate: `python3 scripts/validate_skill_library.py`
2. Add the skill to `README.md` (alphabetical order, with a link to the source directory)
3. Add any needed overlays in `profiles/<agent>/<skill>/`
4. Publish: `python3 scripts/publish_dist_branch.py --branch dist`
5. Verify: `python3 scripts/verify_skills_sh_compat.py --dist-branch dist`

## Authoring Rules

- Use lowercase kebab-case for skill names.
- Use the `health-` prefix for distributed healthcare skills.
- Put trigger conditions in frontmatter `description`.
- Keep `SKILL.md` focused on workflow, constraints, and output contract.
- Use `references/` for large domain guidance.
- Use `scripts/` for deterministic helpers.
- Use `assets/` for files that are consumed by the output.
- Keep optional folders purposeful. `examples/` is acceptable when a concrete sample artifact materially improves the skill.
- Prefer healthcare-specific utility over generic advice for curated skills.

## Curated Skill Standard

A curated skill should:

- have clear healthcare software or digital health relevance
- validate successfully
- have coherent metadata and workflow guidance
- avoid hidden assumptions
- be safe to share with other teams

If a skill is still taking shape, keep it in `skills/.experimental/`.

## Overlays

Use overlays only for true agent-specific differences.

Supported overlay files today:

- `profiles/<agent>/<skill>/SKILL.append.md`
- `profiles/<agent>/<skill>/agents/openai.yaml`

Do not add new overlay file types unless `scripts/validate_skill_library.py` and `scripts/compose_skills.py` are updated together.

## Commands

Validate canonical skills and overlays:

```bash
python3 scripts/validate_skill_library.py
```

Compose authored skills into the local agent install trees:

```bash
python3 scripts/compose_skills.py
```

Build a clean dist tree:

```bash
python3 scripts/compose_skills.py --dist-root /tmp/vermonster-dist
```

Verify the canonical source layout:

```bash
python3 scripts/verify_skills_sh_compat.py
```

Verify a clean dist tree:

```bash
python3 scripts/verify_skills_sh_compat.py --dist-root /tmp/vermonster-dist
```

Verify the published dist branch:

```bash
python3 scripts/verify_skills_sh_compat.py --dist-branch dist
```

Build and publish the dist branch:

```bash
python3 scripts/publish_dist_branch.py --branch dist
```

Build only, without publishing:

```bash
python3 scripts/publish_dist_branch.py --branch dist --build-only
```

Recommended release sequence:

```bash
python3 scripts/validate_skill_library.py
python3 scripts/publish_dist_branch.py --branch dist
python3 scripts/verify_skills_sh_compat.py --dist-branch dist
```

## References

- [docs/repository-model.md](docs/repository-model.md)
- [docs/skill-creation-guide.md](docs/skill-creation-guide.md)
- [templates/skill/SKILL.md](templates/skill/SKILL.md)
