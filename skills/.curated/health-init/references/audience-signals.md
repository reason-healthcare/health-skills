# Audience Signals

Use this reference to infer who the repository primarily serves.

## Output Values

- `provider`
- `patient`
- `payer`
- `administrative`
- `mixed`
- `unknown`

## Provider

Common signals:

- clinician, nurse, physician, MA, care team, chart, encounter, order entry
- EHR workflow language
- provider-facing dashboards, inboxes, documentation, or scheduling tools
- clinical decision support or workflow reduction for staff delivering care

## Patient

Common signals:

- portal, intake, self-scheduling, results access, messaging, remote monitoring
- patient education, self-service flows, member-facing app language
- consent capture, patient reminders, symptom tracking

## Payer

Common signals:

- claims, eligibility, prior auth, utilization management, reimbursement
- benefit design, network management, payer operations
- plan administration, adjudication, risk adjustment

## Administrative

Common signals:

- front-desk, revenue cycle, call center, referrals coordination, scheduling ops
- staff workflow not centered on direct clinical delivery
- registration, prior auth operations, billing follow-up, fax queue handling

## Mixed

Use `mixed` when multiple audiences are clearly first-class and no single one dominates.

Examples:

- dual provider + patient workflow products
- payer + provider collaboration systems
- systems with clearly separated experiences for operations and clinicians

## Unknown

Use `unknown` when the repository does not provide enough product evidence to infer who it serves and the user should confirm the audience directly.

Examples:

- blank or near-empty repos
- repos containing mostly `.agents/`, `.claude/`, `.codex/`, or similar assistant configuration
- reusable prompt, skill, or automation libraries with no visible product workflows
- generic platform or infra scaffolding without healthcare user-facing evidence

## Evidence Sources

Good signals include:

- role names in docs, UX copy, and permissions
- route names, feature names, and component names
- integration language that implies who uses the product
- success metrics or business outcomes tied to a particular user group

Avoid overfitting to a single word. Prefer repeated signals across multiple parts of the repository.
Do not infer an audience from meta-tooling alone.
