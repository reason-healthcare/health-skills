# Discovery Checklist

Use this reference to reinforce the `explore` and `document` modes defined in `SKILL.md`. These prompts are designed to surface dynamics that are specific to healthcare and commonly missed in generic product discovery.

## Explore Mode Prompts

### Problem Framing

- What clinical, operational, or administrative problem exists — and in which care setting?
- Which clinician roles, patient populations, or operational staff feel this most directly?
- What triggers the problem — a specific clinical event, workflow step, or system gap?
- What is the cost of inaction — in patient outcomes, clinician time, revenue, or organizational risk?
- Is this a problem people are actively trying to solve, or one they've stopped noticing?
- Has this problem persisted because it's genuinely hard, or because incentives don't reward fixing it?

### Stakeholder and Incentive Mapping

- Who experiences the problem day-to-day (the user)?
- Who would make the purchase or approval decision (the buyer)?
- Who benefits most from a better outcome (the beneficiary)?
- Who pays — and through what mechanism (the funder)?
- Where do these four roles overlap, and where do they diverge?
- Which stakeholder absorbs the operational burden of adopting a new process or tool?
- Who has veto power — IT governance, compliance, the CMIO, the CFO, nursing leadership?
- Are there stakeholders who benefit from the status quo and would resist change?

### Workflow and Integration Context

- What is the clinical or operational workflow today, step by step?
- Where does the EHR sit in this workflow — is it the system of record, the user interface, or both?
- What are the handoffs, care transitions, or timing constraints that shape the workflow?
- Which existing tools already cover part of the job — and how entrenched are they?
- Would a solution add steps, screens, clicks, or cognitive load for clinicians?
- Is the workflow different across shifts, sites, or care settings?
- What data is generated during the workflow, and where does it live?

### Payment Model and Business Viability

- What payment model governs the care being delivered (fee-for-service, value-based, capitated, bundled, grant)?
- Does the payment model reward or penalize the improvement this product would create?
- Who captures the financial value from a better outcome — and is that the same party who would buy the product?
- What is the realistic procurement cycle — months, quarters, or years?
- Is there a budget line for this, or would it need to be created?
- Could this be funded through quality improvement, innovation grants, or value-based incentive savings?

### Evidence and Trust

- What evidence would a clinical champion need to advocate for this internally?
- Is peer-reviewed clinical evidence expected, or would operational data and pilot results suffice?
- What would a skeptical CMIO, CNO, or medical director need to see before endorsing?
- Are there existing quality measures, clinical registries, or benchmarks this could reference?
- Has a similar approach been tried and failed — and if so, why?
- What is the trust hierarchy for this audience (peer-reviewed > society guidelines > vendor data > anecdote)?

### Adoption Readiness

- Is there an identifiable internal champion at a target organization?
- What is the committee and approval path for new clinical or operational tools?
- How much change management is required for frontline staff?
- What competing priorities, initiative fatigue, or "pilot graveyard" dynamics exist?
- What is the switching cost from the current state — technical, behavioral, and political?
- Would this require training, and who would deliver and maintain it?
- Does the product need to prove value during a free pilot, or can it sell on evidence?

### Constraint and Risk Discovery

- Regulatory: does this touch FDA jurisdiction (SaMD), state-specific rules, ONC certification, or information blocking?
- Privacy: beyond HIPAA, are there consent, data use agreement, or de-identification requirements?
- Clinical safety: could the product cause harm through incorrect action, omission, or alert fatigue?
- Operational: what staffing, training, downtime, or support burden would this create?
- Financial: what is the expected ROI timeline, and does it fit the buyer's budget cycle?
- Which constraints are hard blockers vs negotiable tradeoffs?

### Early Solution Shaping

- Given the incentive map, which stakeholder should the product serve first to unlock adoption?
- Is the opportunity best framed as automation, decision support, care coordination, or operational visibility?
- What is the minimum integration surface needed to be useful in the workflow?
- What tradeoffs exist across clinical safety, workflow burden, implementation effort, and time to adoption?
- Should the team proceed to deeper discovery, refine the framing, pivot to a different angle, or stop?

## Document Mode Checklist

### Context

- Name the specific care setting, clinical specialty, and patient population.
- Describe the current workflow with enough detail that a clinician would recognize it.
- Distinguish clinician burden from organizational pain from patient harm in the pain points.

### Stakeholder-Incentive Map

- For each stakeholder, state their role: user, buyer, beneficiary, funder, or veto holder.
- Call out where interests align and where they conflict.
- Identify who bears the cost of change vs who captures the value.

### Goals

- Map goals to measurable healthcare dimensions: clinical outcomes, operational efficiency, financial impact, patient experience, clinician burden.
- State what evidence or metric would demonstrate success.

### Non-Goals

- Be specific about what is excluded and why — "not in this phase" vs "never in scope."

### Scope

- Include EHR integration surface and strategy as a first-class scope item.
- Distinguish features from workflows from data from integrations.
- State the target scale (single site, health system, multi-organization).

### Payment Model and Business Viability

- State the applicable payment model and how it affects product viability.
- Describe value capture alignment.
- Note the procurement path and realistic timeline.

### Technical Approach

- Describe EHR and system integration approach.
- State data sources, ownership, quality assumptions, and interoperability requirements.
- Separate AI/ML roles from deterministic logic from human judgment.
- Note deployment model and who operates the system.

### Evidence and Validation Plan

- State what evidence is needed, for whom, and when.
- Describe pilot design if applicable.
- Define success metrics and how they'll be measured.

### Adoption Strategy

- Identify the target champion profile and organizational entry point.
- Describe change management, training, and support requirements.
- State the rollout approach.

### Acceptance Criteria

- Include clinical workflow criteria, not just functional specs.
- State safety and monitoring requirements explicitly.

### Risks and Open Questions

- Separate clinical safety risks from business risks from technical risks.
- Capture unresolved dependencies and who can resolve them.

### Recommended Next Step

- End with `proceed`, `validate`, `spike`, or `defer`.
- Include rationale, near-term actions, and which stakeholders need to be involved.

## Healthcare Review Areas

These are cross-cutting concerns to revisit throughout discovery:

- workflow before and after the proposed change — with specificity about who does what and when
- patient safety implications — including risks from action, omission, and alert fatigue
- clinician burden impact — time, cognitive load, workflow interruption, documentation overhead
- incentive alignment — whether the payment model and organizational incentives support the proposed change
- EHR integration dependency — whether the product can succeed outside the EHR, or requires deep integration
- interoperability requirements — data exchange standards, system boundaries, and data quality assumptions
- regulatory surface — FDA, HIPAA, state laws, ONC certification, information blocking
- adoption barriers — procurement cycles, committee approvals, champion availability, competing priorities
- evidence gaps — what needs clinical validation vs operational proof vs buyer testimony
- health equity considerations — whether the product serves or excludes underserved populations, languages, or care settings
