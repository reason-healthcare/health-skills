# Example Run: Sparse Repo With Agent Tooling Only

## Repository Snapshot

- `.agents/`
- `.claude/`
- `README.md`
- no application source, migrations, deployment manifests, or product docs

## Proposed Values

- `jurisdiction`: `unclear`
  - Confidence: `low`
  - Evidence:
    - "No HIPAA, ONC, CMS, GDPR, EHDS, MDR, or similar market-specific evidence found in product code or docs"
- `primary_audience`: `unknown`
  - Confidence: `low`
  - Evidence:
    - "Repository contains assistant configuration and prompt assets, but no workflows, UI copy, or domain docs showing whether the product serves providers, patients, payers, or operations staff"
- `project_stage`: `greenfield`
  - Confidence: `medium`
  - Evidence:
    - "No application implementation, tests, migrations, deployment config, or operational docs found"
    - "Repository structure is mostly assistant/tooling setup rather than product code"

## Pre-Write Confirmation

I found too little product evidence to make confident market or audience claims.

I am proposing:

- `jurisdiction: unclear`
- `primary_audience: unknown`
- `project_stage: greenfield`

Shall I write `.health-context.yaml` with these values, or would you like to override any of them?
