# Audience Signals

Use this reference to infer who the repository primarily serves.

## Output Values

- `provider`
- `patient`
- `payer`
- `administrative`
- `other`
- `mixed`

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

## Other

Use `other` when the repository is healthcare-relevant but not primarily built for one of the audience classes above.

Examples:

- SDKs and API platforms
- internal compliance tools
- infrastructure, developer tooling, or migration utilities
- consulting artifacts, documentation frameworks, or strategy outputs

## Mixed

Use `mixed` when multiple audiences are clearly first-class and no single one dominates.

Examples:

- dual provider + patient workflow products
- payer + provider collaboration systems
- systems with clearly separated experiences for operations and clinicians

## Evidence Sources

Good signals include:

- role names in docs, UX copy, and permissions
- route names, feature names, and component names
- integration language that implies who uses the product
- success metrics or business outcomes tied to a particular user group

Avoid overfitting to a single word. Prefer repeated signals across multiple parts of the repository.
