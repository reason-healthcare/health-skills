---
name: health-product-discovery
description: Healthcare product discovery skill that maps incentive structures, adoption dynamics, and clinical workflow constraints before shaping solutions. Uses a jurisdiction-neutral core workflow plus explicit US and EU market overlays. Supports explore and document modes for early-stage ideation, consulting, pilot scoping, and strategic planning.
---

# Skill: health-product-discovery

## Purpose

Guide healthcare product discovery through the dynamics that make health products succeed or fail:

* **Incentive mapping** — the person who uses, buys, benefits from, and pays for healthcare products are almost never the same person
* **Adoption physics** — clinician burnout, EHR gravity, procurement cycles, and committee-based decisions dominate what ships
* **Evidence requirements** — healthcare trust runs on clinical evidence and peer validation, not demos and testimonials
* **Payment model dependency** — fee-for-service vs value-based care changes what's viable, not just what's valuable
* **Workflow integration** — products that add clinician burden fail regardless of clinical merit

This skill is intended for:

* early-stage ideation and problem framing
* consulting engagements and opportunity assessment
* pilot definition and scope negotiation
* internal product planning and strategic alignment

## Jurisdiction Overlay Selection

Keep the base discovery flow jurisdiction-neutral. Apply market overlays only after selecting one of `us`, `eu`, `us+eu`, or `unclear`.

Use this order:

1. Read `.health-context.yaml` if it exists and note the stored jurisdiction.
2. Check the user prompt, provided materials, and repository evidence for confirming or conflicting market signals.
3. Load `references/us-market-overlay.md` and/or `references/eu-market-overlay.md` only for the selected overlay set. Each overlay provides market-specific challenge prompts for explore mode, required content additions for document mode, and healthcare economics depth for both.
4. If evidence is mixed, say so explicitly and avoid silently defaulting to US market assumptions.

---

## Modes

### Mode: explore

#### Intent

Understand the problem space through healthcare-specific lenses before committing to a solution. Surface the dynamics that generic discovery misses.

#### Setup

Before beginning explore steps, load:

- `references/discovery-checklist.md` — full step-by-step prompt set for each explore step
- `references/stakeholder-incentives.md` — incentive pattern reference: four-role model, payment model dynamics, buyer-user split tables
- `references/adoption-dynamics.md` — adoption barrier reference: clinician, organizational, and market layer barriers, champion models, procurement timelines
- Active jurisdiction overlay(s) — for market-specific adversarial challenge prompts

#### Behavior

* Interactive and adversarial — the goal is a merit-based analysis, not affirmation
* Actively challenges assumptions about market fit, incentive alignment, adoption feasibility, and evidence basis
* Names what is likely to go wrong, not just what must be figured out
* Expands context and surfaces unknowns the user has not considered
* Avoids premature solution design
* Holds the user's framing up against healthcare market realities and pushes back when they don't hold

#### Steps

1. Problem Framing

   * What clinical, operational, or administrative problem exists?
   * Which care setting, specialty, or population is affected?
   * What happens today — and what is the cost of inaction?
   * Is this a problem people are actively trying to solve, or one they've normalized?

2. Stakeholder and Incentive Mapping

   * Who experiences the problem (user)?
   * Who makes the purchase decision (buyer)?
   * Who benefits from a solution (beneficiary)?
   * Who pays — directly or indirectly (funder)?
   * Is the buyer a provider organization, payer, public system, ministry, regional health authority, or framework procurement body?
   * Where do these roles align, and where do they conflict?
   * Which stakeholder absorbs the workflow burden of a new process?
   * Who has veto power (IT governance, compliance, CMO, CFO, procurement, regional authority)?

3. Workflow and Integration Context

   * What is the clinical or operational workflow before any proposed change?
   * Where does the EHR sit in this workflow — is it the center of gravity?
   * What are the handoffs, transitions, and timing constraints?
   * What existing tools cover part of the job today?
   * Would a solution add steps, screens, or cognitive load for clinicians?

4. Payment Model and Business Viability

   * What payment or funding model applies (fee-for-service, value-based, capitated, public budget, tender-funded, grant-funded)?
   * Does the payment model reward or penalize the proposed improvement?
   * Who captures the financial value — and is it the same party who pays for the product?
   * What is the realistic procurement timeline (committee path, budget cycle, tender cycle, months to years)?

5. Evidence and Trust Requirements

   * What evidence would a clinical champion need to advocate internally?
   * Is peer-reviewed evidence expected, or is operational data sufficient?
   * What would a skeptical CMIO or CNO need to see?
   * Are there existing quality measures, registries, or benchmarks to reference?

6. Adoption Readiness

   * Is there an identifiable internal champion at a target organization?
   * What is the committee and approval path for new tools in this setting?
   * How much change management is required for frontline staff?
   * What competing priorities or initiative fatigue exists?
   * What is the switching cost from the current state?

7. Constraint and Risk Discovery

   * Regulatory: FDA (SaMD), state regulations, certification (ONC), information blocking rules
   * Privacy and security: HIPAA is table stakes — what else applies?
   * Clinical safety: could the product cause harm through action or omission?
   * Operational: staffing, training, downtime, support expectations
   * Financial: ROI timeline, budget cycles, reimbursement dependencies

8. Early Solution Shaping (lightweight)

   * Given the incentive map, who would this product need to serve first?
   * Is the opportunity automation, decision support, coordination, or visibility?
   * What is the minimum integration surface to be useful?
   * What tradeoffs exist across safety, workflow burden, implementation effort, and adoption?

#### Output

* Problem summary with care setting and population context
* Stakeholder-incentive map (user / buyer / beneficiary / funder splits)
* Workflow integration assessment
* Payment model fit
* Evidence and adoption readiness
* Key constraints and risks
* Recommendation (proceed / refine / pivot / stop) with rationale

---

### Mode: document

#### Intent

Produce a structured strategic planning artifact grounded in healthcare market realities.

#### Setup

Before producing output, load:

- `references/document-template.md` — full output structure, section-by-section guidance, and placeholder conventions
- `references/discovery-checklist.md` — document mode checklist for section completeness
- Active jurisdiction overlay(s) — for required content additions specific to the selected market

#### Output Structure

Use `references/document-template.md` for the full output structure. Required sections are listed below; overlay-specific additions are in each overlay's **Document Mode Additions** section.

### Context

* Problem description with clinical or operational specificity
* Care setting, specialty, and population
* Current state workflow
* Pain points — distinguish clinician burden from organizational pain from patient harm

### Stakeholder-Incentive Map

* For each stakeholder: role in buying, using, benefiting, funding
* Alignment and conflicts between stakeholder interests
* Who bears the burden of change vs who captures the value

### Goals

* Outcome-oriented goals mapped to measurable healthcare dimensions:
  * Clinical outcomes (quality measures, safety events)
  * Operational efficiency (throughput, wait times, staff utilization)
  * Financial impact (cost avoidance, revenue, reimbursement)
  * Experience (patient satisfaction, clinician burden reduction)

### Non-Goals

* Explicit exclusions with rationale

### Scope

#### In Scope

* Features, workflows, data, integrations
* EHR integration surface and strategy
* Target care setting and scale

#### Out of Scope

* Explicit exclusions

### Payment Model and Business Viability

* Applicable payment or funding models
* Value capture alignment (who pays vs who benefits)
* Procurement path and timeline
* Revenue or funding model assumptions
* Market-specific assumptions for `us`, `eu`, or `us+eu` overlays

### Technical Approach

* Architecture overview
* EHR and system integration approach
* Data sources, ownership, and quality assumptions
* Decision logic: AI vs deterministic vs hybrid
* Interoperability requirements (FHIR, HL7, custom)
* Deployment model and operational responsibilities

### Evidence and Validation Plan

* What evidence is needed and for whom
* Clinical validation approach (if applicable)
* Pilot design considerations
* Success metrics and measurement approach

### Adoption Strategy

* Target champion profile and organizational entry point
* Change management requirements
* Training and support model
* Rollout approach (phased, site-by-site, population-based)

### Acceptance Criteria

* Clinical workflow criteria
* Integration and data criteria
* Performance and reliability expectations
* Safety and monitoring requirements

### Risks and Open Questions

* Clinical safety risks
* Adoption risks
* Regulatory and compliance risks
* Technical and integration risks
* Unresolved dependencies

### Notes

* Assumptions requiring validation
* Constraints
* References and prior art

### Recommended Next Step

* Proceed / validate / spike / defer
* Include rationale, near-term actions, and who needs to be in the room

---

## Mode Selection

Use explore when:

* problem is vague or the opportunity is unvalidated
* stakeholder incentives and adoption dynamics are unclear
* the team needs to decide whether to invest further

Use document when:

* problem and context are understood
* a strategic artifact is needed for alignment, funding, or proposal
* stakeholders need a shared reference to evaluate scope and tradeoffs

---

## Inputs

* User prompt
* Domain context (care setting, specialty, population, payment model)
* Jurisdiction context from `.health-context.yaml` when present
* Existing notes, artifacts, or prior discovery output (if provided)

---

## Outputs

* Structured discovery output with incentive and adoption analysis (explore)
* Strategic planning artifact with healthcare-specific sections (document), see `references/document-template.md`
* `examples/example-explore.md` — example explore output showing expected structure, stakeholder-incentive map, and recommendation format
* `examples/example-document-multi-market.md` — example document-mode output showing shared findings plus market-specific US and EU assumptions

---

## Guardrails

* **Challenge assumptions directly** — do not mirror the user's framing back to them as validation; the purpose of discovery is to stress-test ideas, not endorse them
* **Do not make users feel good about weak ideas** — if the incentive structure is misaligned, the adoption path is implausible, or the evidence basis is thin, say so clearly and early
* **Asymmetry of harm** — a false positive (encouraging a bad idea) is worse than a false negative (pushing back on a good one); erring toward skepticism is the correct default in healthcare
* Do not modify repository files, code, or configuration; produce analysis or document content only
* Do not flatten healthcare into generic product language — name the care setting, the clinician role, the payment model, the regulatory constraint
* Surface incentive misalignment explicitly — do not assume the user, buyer, and beneficiary are the same
* Treat clinician workflow burden as a first-class adoption risk
* Distinguish clinical safety concerns from business risks
* Be direct about evidence gaps and adoption barriers — optimism without evidence is harmful in healthcare
* Prefer specificity over comprehensiveness — a focused discovery is more useful than a thorough but generic one

---

## Resources

- `references/discovery-checklist.md`: healthcare discovery prompts organized by exploration area
- `references/document-template.md`: output shape template for document mode — use as the starting structure for strategic planning artifacts
- `references/stakeholder-incentives.md`: incentive structures, buyer-user splits, and payment model dynamics
- `references/adoption-dynamics.md`: healthcare adoption barriers, champion models, and procurement realities
- `references/us-market-overlay.md`: US-specific payment, buyer, and procurement assumptions that should not remain implicit defaults
- `references/eu-market-overlay.md`: EU product and market-access overlay covering fragmentation, procurement, reimbursement, localisation, interoperability, and public-system incentives
