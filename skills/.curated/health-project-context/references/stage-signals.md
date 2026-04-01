# Project Stage Signals

Use this reference to determine whether the target repository is `greenfield`, `existing`, or `unclear`.

## Output Values

- `greenfield`
- `existing`
- `unclear`

## Existing

Strong evidence for `existing` includes:

- application source trees with non-trivial implementation
- tests, fixtures, migrations, or seeded data
- CI/CD workflows
- lockfiles or dependency manifests tied to real app code
- deployment manifests, infrastructure configs, or runtime environments
- operational docs, runbooks, support notes, or architecture diagrams

One or two of these alone may be enough if the repository clearly represents an active system.

## Greenfield

Strong evidence for `greenfield` includes:

- mostly empty repository
- template-only structure
- proposal/spec/task artifacts without implementation code
- placeholder README and minimal setup files only
- examples or starter kits with no actual product implementation

Treat aspirational docs as weaker than real implementation evidence.

## Unclear

Use `unclear` when the repository does not clearly fit either category.

Examples:

- a partial migration repo with some scaffolding but little real implementation
- a mono-repo slice that contains docs and configs but not enough product code to classify
- a tooling repo that supports an existing product but does not itself reveal maturity clearly

## Heuristic Priorities

1. Prefer on-disk implementation evidence over stated intent.
2. Prefer multiple small maturity signals over a single generic claim.
3. Do not use git history depth alone as the deciding factor.
4. If evidence conflicts, say so and use `unclear` rather than forcing a label.
