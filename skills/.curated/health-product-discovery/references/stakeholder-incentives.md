# Stakeholder Incentives in Healthcare

Use this reference to understand the structural incentive dynamics that shape whether healthcare products succeed or fail. The core pattern: the person who uses a healthcare product, the person who buys it, the person who benefits from it, and the person who pays for it are almost never the same person. Products designed for only one of these roles routinely fail.

---

## The Four-Role Model

### User
The person who interacts with the product day-to-day. Often a clinician, care coordinator, medical coder, or administrative staff member.

- **Primary motivations:** reduce documentation burden, avoid alert fatigue, maintain clinical autonomy, protect patient safety
- **Veto mechanism:** non-adoption — the product is purchased but unused; clinicians route around it
- **What wins them:** it removes steps from their workflow, not adds them; it integrates into the EHR they already live in

### Buyer
The person or committee with purchasing authority. Often a CIO, CMIO, VP of Operations, or department head.

- **Primary motivations:** cost reduction, compliance, demonstrable quality improvement, strategic alignment, risk avoidance
- **Veto mechanism:** no contract; procurement blocked at committee
- **What wins them:** ROI evidence, reference customers in same care setting, minimal integration risk, clear ownership of ongoing support

### Beneficiary
The person who receives better outcomes if the product works. Often the patient, but sometimes a population, a payer, or the organization itself.

- **Primary motivations:** better clinical outcome, reduced burden, faster access, lower cost of care
- **Veto mechanism:** none — beneficiaries rarely have purchase authority; their interests must be represented by champions
- **Key risk:** beneficiary and buyer interests diverge — a product that saves payers money may not be purchased by a hospital that profits from the status quo

### Funder
The entity whose money ultimately pays for the product or its outcomes. Could be a payer (Medicare, Medicaid, commercial), employer, health system, grant agency, or patient.

- **Primary motivations:** cost containment, outcomes improvement, regulatory compliance, population health metrics
- **Veto mechanism:** reimbursement — if the funder doesn't pay for the outcome the product creates, the product has no business model
- **Key pattern:** in fee-for-service, funders pay for volume; products that reduce utilization harm revenue even if they improve outcomes

---

## Common Incentive Misalignment Patterns

### Clinician burden vs. organizational value
Health systems purchase predictive analytics tools that add 3 clicks per patient to a clinician workflow. Outcome: tool is purchased but not used. The buyer saw organizational value; the user absorbed cost.

### Payer savings vs. provider adoption
A care management platform reduces readmissions, saving Medicare $1,200 per patient. The hospital loses the readmission revenue. The hospital won't buy the platform without a value-based contract that redirects those savings back to them.

### Patient benefit vs. payor coverage
Remote monitoring devices demonstrably improve chronic disease outcomes. If the device isn't reimbursed under the patient's plan, adoption stalls at the funder layer. Clinical evidence is necessary but not sufficient.

### IT governance vs. clinical innovation
A clinical team identifies a tool that would reduce nursing documentation time by 40%. The IT committee table it for 18 months due to integration complexity and security review. Buyer and user interests are aligned, but the veto path runs through a third party.

### Compliance-driven purchase vs. frontline use
A hospital buys a clinical decision support tool to satisfy a regulatory requirement. Clinicians see it as checkbox burden. Adoption is nominal; true behavior change never occurs.

---

## Payment Model Dynamics

### Fee-for-Service (FFS)
Revenue tied to volume — encounters, procedures, admissions.

- Products that reduce utilization reduce revenue for FFS organizations, even if they improve outcomes
- Products that add billable encounters or capture missed charges have aligned incentives
- Efficiency tools must demonstrate ROI in staff time or cost avoidance, not in care utilization reduction

### Value-Based Care (VBC) and Accountable Care Organizations (ACOs)
Revenue tied to outcomes and cost efficiency for a defined population.

- Products that reduce readmissions, improve chronic disease management, or prevent avoidable utilization align directly with financial incentives
- Strong match for care coordination, remote monitoring, risk stratification, and population health tools
- Slower to adopt because shared savings accrue over time; ROI is real but lagging

### Capitation
Fixed per-member-per-month payment for a defined population regardless of utilization.

- Strong incentive to reduce cost of care — prevention, chronic disease management, and utilization management products align well
- Common in Medicaid managed care, Medicare Advantage, and some employer-sponsored plans
- Risk-bearing entities (IPAs, MSOs, capitated medical groups) are the most financially aligned buyers

### Hierarchical Condition Category (HCC) Risk Adjustment
Medicare Advantage and ACO REACH models use HCC scores to adjust capitated payments. Higher-acuity patients generate higher payments.

- Products that improve specificity of diagnosis coding (chart review, CDI, NLP) increase risk-adjusted revenue without changing care
- This creates an incentive to ensure documented diagnoses are accurate and complete — distinct from upcoding
- Differentiate clearly: HCC capture is about documentation accuracy; charge capture is about billing for services rendered

### Bundled Payments
Single payment for an episode of care (e.g., hip replacement, heart failure hospitalization + 90-day post-discharge).

- Strong incentive to reduce complications, readmissions, and post-acute care costs within the episode
- Products targeting post-acute coordination, discharge planning, and care transitions align well
- Limited appeal to FFS components of the bundle with no downside risk

### Quality Incentives (HEDIS, Star Ratings, MIPS)
Payers and federal programs tie bonus payments or penalties to quality measure performance.

- Products that close care gaps, improve preventive care rates, or document clinical quality measures have measurable, measurable incentive alignment
- Health systems with poor quality scores are more receptive than those already performing well
- Timing matters: organizations focus on measurement-year performance in specific windows

---

## Buyer-User Split Patterns by Setting

| Care Setting | Common Buyer | Common User | Key Tension |
|---|---|---|---|
| Hospital / Health System | CIO, CMIO, VP Operations | Hospitalists, nurses, coders | IT governance slows clinical innovation |
| Ambulatory / Physician Group | Practice administrator, CMO | Primary care physicians | Physicians own the workflow; must opt in |
| Medicare Advantage plan | VP Medical Management, CTO | Care managers, coders | Closed systems; vendor approval long |
| Medicaid Managed Care | CMO, VP Quality | Case managers, social workers | Budget-constrained; ROI window short |
| Federally Qualified Health Center (FQHC) | Executive Director, CMO | PCPs, care coordinators | Grant-dependent; limited IT capacity |
| Home Health / Post-Acute | Administrator, DON | Field nurses, aides | High turnover; mobile-first required |
| Behavioral Health | Medical Director | Therapists, prescribers | EHR fragmentation; data-sharing limits |

---

## Revenue Capture vs. Cost Avoidance

Many healthcare products must choose which financial argument to make:

**Revenue capture framing:**
- We help you capture more of the revenue you're already entitled to (HCC, charge capture, coding accuracy)
- Buyer sees direct top-line impact; faster ROI conversation
- Risk: perceived as enabling upcoding; must be positioned around documentation accuracy

**Cost avoidance framing:**
- We reduce readmissions, ED visits, or unnecessary procedures (VBC, capitation)
- Strong in at-risk organizations; weak in FFS settings without downside risk
- ROI is real but requires actuarial modeling to make concrete

**Operational efficiency framing:**
- We reduce staff documentation time, denials, or manual rework
- Universal appeal; directly measurable; doesn't depend on payment model
- Risk: efficiency gains are often absorbed by the organization rather than returned as savings
