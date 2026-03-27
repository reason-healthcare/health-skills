# Developer Guide

This guide is for contributors building or maintaining skills in this repository.

## Core Rule

Author skills in `skills/` only.

Do not hand-edit base skill content in:

- `.claude/skills/`
- `.codex/skills/`
- `.gemini/skills/`
- `.github/skills/`

Those directories are composed outputs.
On the working branch, they should contain local repo tooling only, not generated distributable `health-*` skills.

## Directory Model

- `skills/.curated/`: stable healthcare skills intended for reuse
- `skills/.experimental/`: draft or exploratory skills
- `profiles/<agent>/<skill>/`: optional per-agent overlays
- `templates/skill/`: base template for new skills
- `docs/`: repository conventions and skill authoring guidance
- `scripts/`: tooling for initialization, validation, and composition

OpenSpec files under `.claude/`, `.codex/`, `.gemini/`, and `.github/` are repo-local development tooling. They help build this library but are not part of the distributed healthcare skill source model.

## How `npx skills add` Relates To This Repo

This repo has two layers:

1. Canonical authoring source in `skills/`
2. A clean distribution branch rooted at `skills/`

Author and edit distributable healthcare skills in `skills/`.

`npx skills add` installs from the published repository layout. For this repo, the published `dist` branch should expose a clean `skills/` tree, not the local agent-specific development directories.

For this repo, the intended workflow is:

1. Create or update a skill in `skills/.curated/` or `skills/.experimental/`
2. Add any needed overlays in `profiles/<agent>/<skill>/`
3. Build or update the clean dist tree
4. Force-update the `dist` branch from that generated output

That build step is what makes the canonical source visible in the layout that `skills.sh` consumers can install from.

In practice:

- `skills/` is for maintainers
- the working branch should not carry generated `health-*` installs in local agent skill directories
- the clean `dist` branch is a repo-shaped export with `README.md` and `skills/.curated/*`
- `npx skills add <owner>/<repo>@dist` should be the distribution target
- local agent directories on the working branch are for repo tooling such as OpenSpec

## Contributing Workflow

1. Choose the right group: `.curated` or `.experimental`.
2. Initialize a skill from the template.
3. Write a concise `SKILL.md` with strong trigger wording in frontmatter.
4. Add `references/`, `scripts/`, or `assets/` only when needed.
5. Validate the canonical library.
6. Add overlays only when an agent needs a real customization.
7. Build the clean dist tree and verify it.
8. Publish the `dist` branch.

## Create A New Skill

Example:

```bash
python3 scripts/init_skill.py health-claims-workflow-review --group .experimental --include references scripts
```

This creates a skill under `skills/.experimental/health-claims-workflow-review/`.

## Authoring Rules

- Use lowercase kebab-case for skill names.
- Use the `health-` prefix for distributed healthcare skills.
- Put trigger conditions in frontmatter `description`.
- Keep `SKILL.md` focused on workflow, constraints, and output contract.
- Move large domain guidance into `references/`.
- Put deterministic helpers into `scripts/`.
- Put templates or output files into `assets/`.
- Prefer healthcare-specific utility over generic advice for curated skills.

## Curated Skill Standard

A curated skill should:

- have clear healthcare software or digital health relevance
- validate successfully
- have coherent metadata and workflow guidance
- avoid hidden assumptions
- be safe to share with other teams

If the skill is still taking shape, keep it in `skills/.experimental/`.

OpenSpec stays outside this model as repo-local development tooling.

## Overlays

Use overlays only for true agent-specific differences.

Supported files today:

- `profiles/<agent>/<skill>/SKILL.append.md`
- `profiles/<agent>/<skill>/agents/openai.yaml`

Do not invent new overlay file types unless the validator and composer are updated together.

## Commands

Validate canonical skills and overlays:

```bash
python3 scripts/validate_skill_library.py
```

Build a clean dist tree:

```bash
python3 scripts/compose_skills.py --dist-root /tmp/vermonster-dist
```

Verify a clean dist tree:

```bash
python3 scripts/verify_skills_sh_compat.py --dist-root /tmp/vermonster-dist
```

Verify the published dist branch:

```bash
python3 scripts/verify_skills_sh_compat.py --dist-branch dist
```

Recommended release sequence:

```bash
python3 scripts/validate_skill_library.py
python3 scripts/publish_dist_branch.py --branch dist
python3 scripts/verify_skills_sh_compat.py --dist-branch dist
```

## References

- [docs/repository-model.md](/Users/bkaney/projects/vermonster-skills/docs/repository-model.md)
- [docs/skill-creation-guide.md](/Users/bkaney/projects/vermonster-skills/docs/skill-creation-guide.md)
- [templates/skill/SKILL.md](/Users/bkaney/projects/vermonster-skills/templates/skill/SKILL.md)
