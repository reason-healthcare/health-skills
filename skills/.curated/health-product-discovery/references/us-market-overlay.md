# US Market Overlay

Use this overlay when the product targets US healthcare delivery, reimbursement, or procurement. Apply for `us` or `us+eu` jurisdictions. This file makes US-specific assumptions explicit so they are challenged rather than defaulted into.

## Market Context

- **Buyer structure**: provider executives, health systems, group practices, payers, employers, or digital health platform channels
- **Payment model fragmentation**: fee-for-service, value-based care, shared savings, Medicare Advantage capitation, managed Medicaid MCO, employer self-insured, and bundled episodes often coexist within the same organization
- **Procurement shape**: committee buying, EHR governance and IT security review, pilot-first adoption, fragmented budget ownership across clinical, IT, finance, and quality functions
- **Evidence expectations**: clinical champion support, quality-measure performance data, pilot outcomes, payer ROI cases — peer-reviewed evidence raises credibility but operational data and comparable reference customers are often sufficient for initial contracting
- **Integration gravity**: Epic, Oracle Health/Cerner, athenahealth, eCW, and SMART on FHIR patterns constrain what is technically feasible and set the IT timeline

---

## Healthcare Economics

US healthcare economics operates as multiple overlapping financial systems simultaneously — often within the same patient encounter or organization. A product that is viable under one economic lens can be structurally unviable under another. These ambiguities are not resolvable by better analysis alone; they require explicit modeling for the specific buyer, payer mix, and contract type in scope.

### The Multi-Payer Fragmentation Problem

A typical health system holds contracts with 50–150 distinct payers simultaneously. Each payer has different fee schedules (negotiated independently from Medicare), different prior authorization requirements, different quality measure definitions and bonus structures, and different claims adjudication rules. No single revenue assumption applies across a patient population.

When a product's value case depends on "the payer saving money," the specific payer, the specific contract structure, and whether that contract lets the payer capture the savings all determine whether the claim is real. Challenge the value case at this level of specificity, not at the category level.

### Employer Self-Insurance and the TPA/PBM Layer

Approximately 65% of employer-sponsored coverage is self-funded — the employer bears actual claims risk and contracts a TPA (third-party administrator) to administer benefits. The commercial insurer appearing on the member ID card may be functioning only as a network-rental arrangement, not a risk-bearing entity. Pharmacy benefits are typically managed separately by a PBM (CVS Caremark, Express Scripts, or OptumRx manage approximately 80% of US prescriptions), creating a separate financial and data layer entirely.

Products promising cost reduction in employer-sponsored populations must model impact on incurred claims by claim type (medical vs. pharmacy vs. behavioral), identify whether the employer, TPA, or PBM captures the value, and determine who in the employer risk chain has authority to purchase.

### Fee-for-Service Revenue Survival Bias

In FFS markets, provider revenue depends on volume: encounters, procedures, admissions, and ancillary services. Most employed physicians are compensated on wRVU (work relative value unit) models — products that reduce wRVU-generating activities are financially harmful to the physician, even if the health system has VBC contracts that nominally benefit from reduced utilization.

Products that prevent admissions typically remove $15,000–$50,000+ of revenue per event from a hospital. A health system may purchase the product at the executive level while the clinical and finance teams quietly resist it, because they operate under FFS incentives. The buyer and the user can be at economic cross-purposes within the same organization.

### Value-Based Care: Real but Severely Fragmented

VBC adoption is real but uneven. Approximately 42% of Medicare payments flow through some form of value-based arrangement (CMS 2023), but this includes models with no meaningful downside risk. Population-level incentives create genuine purchasing motivation only when:

- The organization has reached its minimum savings rate (typically 3–3.5% for MSSP above benchmark)
- The shared savings flow back to the contracting entity with sufficient margin to justify product spend
- The organization's revenue mix is dominated by patients in the at-risk model, not split between FFS Medicare and risk-bearing tracks

An organization enrolled in an ACO may still have the majority of its revenue from FFS — making the product ROI case genuinely ambiguous for anything that depends on utilization reduction.

### Medicare Advantage Risk Adjustment and HCC Economics

Medicare Advantage plans receive CMS capitation payments adjusted by Hierarchical Condition Category (HCC) scores. Higher HCC scores (sicker patients) produce higher monthly per-member payments. This creates:

- Strong financial incentive for complete and accurate diagnosis documentation
- A multi-billion-dollar market for retrospective chart review, NLP-assisted coding, and supplemental clinical data programs
- Regulatory scrutiny from OIG and CMS on the boundary between documentation accuracy and fraudulent upcoding — RADV (Risk Adjustment Data Validation) audits create retrospective financial liability
- A distinction that must be made explicitly: HCC capture is about documenting diagnoses that are present and managed; upcoding is about claiming diagnoses that don't exist

Products touching MA diagnosis capture, coding, or chart review must distinguish documentation completeness (appropriate) from risk score optimization (regulatory exposure) at both the product design and product framing level.

### ACO and CMMI Model Fragmentation

CMS Innovation Center (CMMI) runs dozens of simultaneous payment model experiments. A single organization's economics may be governed by a combination of:

- **MSSP** — ACO shared savings, optional downside risk tracks; minimum savings rate required before any sharing
- **ACO REACH** (formerly GPDC) — global capitation, mandatory two-sided risk; total cost of care is the metric
- **BPCI-A** — episode-based bundles for specific DRG groups (orthopedic, cardiac); costs within a defined episode window are the metric
- Comprehensive ESRD Care, Oncology Care Model successors, and others with distinct episode definitions

The economic rules differ fundamentally across models. A product's value under BPCI-A (post-acute cost reduction within an episode window) has no relationship to its value under an MSSP ambulatory quality care gap program. Verify which CMMI models the target organization participates in before asserting a value case built from general VBC assumptions.

### Prior Authorization as a Revenue Mechanism

Prior authorization is not merely administrative friction — for commercial payers, utilization management and denial rates are explicit medical loss ratio management tools. Commercial payers denied approximately 17% of in-network claims in 2022 (KFF analysis). Products that promise to reduce prior auth burden must grapple with:

- Payers' financial incentive to maintain authorization friction — denied or delayed claims reduce paid-claims volume and improve the payer's MLR
- Gold carding legislation (being enacted in multiple states) — exempting high-performing providers from PA requirements — which, if expanded, reduces the market size for PA automation tools
- CMS Interoperability and Prior Authorization Final Rule (effective 2026+) mandating electronic PA APIs, which creates a regulatory floor that may commoditize portions of the PA automation market

### 340B Drug Pricing Program

Safety-net hospitals (DSH patient percentage ≥ 11.75%) and FQHCs can purchase covered outpatient drugs at 340B ceiling prices — typically 25–50% below invoice price. This program generates substantial revenue for qualifying entities:

- Large academic medical centers and safety-net health systems may generate $50M–$200M+ annually in 340B savings
- 340B revenue cross-subsidizes care for underserved populations but also funds broader system operations
- Drug manufacturers have restricted 340B pricing access for contract pharmacies, creating ongoing program uncertainty
- A product that changes prescription patterns, site of care, or pharmacy dispensing channel in a 340B-eligible setting may have unintended revenue consequences for that entity

Any product touching medication management, specialty pharmacy routing, or care coordination in DSH-qualified or FQHC settings must assess 340B implications explicitly.

### Medicaid Fiscal Architecture

Medicaid is jointly federally-state funded (FMAP ratios typically 50–76%, higher for expansion states). Key economic dynamics:

- More than 75% of Medicaid beneficiaries are enrolled in managed care organizations (MCOs) — creating a commercial payer layer with public funding and its own prior auth, quality incentive, and contracting dynamics
- Directed payment programs allow states to increase MCO capitation rates tied to quality or value-based arrangements, creating provider-level financial incentives within what appears to be a simple public-payer structure
- DSH and UPL supplemental payments are revenue streams for safety-net providers that depend on Medicaid volume; products that shift care sites or patterns may affect DSH qualification or payment levels
- FQHC Prospective Payment System reimburses at a per-visit rate regardless of payer — creating per-encounter economics different from standard fee schedule billing

### Hospital Financial Conditions

Approximately 50% of US hospitals operated at negative operating margins in 2022 (AHA data). Capital constraints affect technology purchasing timelines significantly — products with high upfront implementation costs or multi-year commitments face sustained resistance in margin-stressed environments. Deferred capital investment, workforce cost inflation, and regulatory mandate spending all compete for the same constrained procurement budget.

---

## Explore Mode: Challenge Prompts

Use these to pressure-test product assumptions that are frequently understated or silently defaulted in US healthcare. The goal is to surface economic contradictions before they become post-launch surprises.

**On payment model specifics:**

- Which specific payment contracts apply to the target organization — not just the category (VBC) but the actual model (MSSP, ACO REACH, BPCI-A bundle, MA capitated, Medicaid MCO, commercial shared savings)?
- Does the organization have downside financial risk in any at-risk arrangement, or only upside-only shared savings? Upside-only MSSP does not create the urgency to reduce utilization that a risk-bearing model does.
- If the product creates cost savings, which entity captures those savings — and is that the same entity whose budget funds the product purchase? If not, what contract mechanism bridges the gap?
- Does the business case hold in pure FFS settings? What fraction of the target market operates under genuine downside risk?

**On payer and revenue cycle:**

- Which payer mix dominates the target population: commercial, Medicare, Medicaid, Medicare Advantage? How does each segment's payment model affect the ROI model independently?
- Does the product require payer cooperation — prior authorization streamlining, a new reimbursement code, or a covered service designation — to be viable at scale? If so, what is the timeline and who controls it?
- If the product reduces utilization, what specific revenue does the provider lose — and does an existing VBC incentive actually offset it under the specific contract, not just in theory?
- Is there a revenue cycle or charge capture incumbency at the target organization that this product needs to integrate with, displace, or avoid conflicting with?

**On Medicare Advantage and HCC:**

- If the product involves diagnosis capture, documentation completeness, or coding, have the HCC revenue implications for MA plan capitation been modeled explicitly?
- Is there a clear legal and operational boundary between documentation accuracy and risk score optimization? Has legal reviewed the product's framing against OIG fraud and abuse guidance?
- Which entity — the MA plan or the provider organization — is the primary financial beneficiary of improved diagnosis documentation, and does the contract structure align incentives accordingly?

**On employer and self-insured channels:**

- If targeting employer-sponsored populations, is the employer self-insured or fully insured? Who is the actual financial decision-maker — employer risk management, HR, benefits broker, or TPA?
- Is there a TPA or PBM relationship that controls access to the data or financial flows the product depends on? Is that entity a partner, a gatekeeper, or a latent competitor?
- Which budget owns the cost the product reduces — medical claims, pharmacy benefit, disability, or workers' compensation? Budget owners in large employers frequently do not coordinate.

**On structural market dynamics:**

- Which EHR vendor dominates the target market segment, and is that EHR currently building or acquiring a competing module? Epic, Oracle Health, and athenahealth have active module strategies across most product categories.
- Is the target health system in an active M&A integration or EHR consolidation? Enterprise technology decisions are routinely frozen during these periods.
- Is the organization under financial stress — negative operating margin, active layoffs, or deferred capital investment? If so, how does that affect capital spend availability and procurement timeline?
- Has this product category failed at the target site before, and does the team have a plan to find out?

---

## Document Mode Additions

When producing a discovery document for a US market product, include the following in the relevant sections:

**In Payment Model and Business Viability:**
- State the specific payment model(s) by name: FFS Medicare, MSSP track, ACO REACH, BPCI-A clinical episode, MA capitated rate, Medicaid MCO capitation, commercial shared savings — do not write "value-based care" without specifying the model
- State whether the buyer has downside financial risk or only upside-only shared savings, and how this affects purchasing motivation
- Model value capture by entity: who purchases the product vs. who realizes the financial benefit, and whether a contract mechanism exists to align them
- Note whether the product requires a new CPT code, LCD/NCD coverage policy change, or payer authorization to generate reimbursable value — with realistic timeline
- Identify the payer mix for the target population and describe how each segment affects ROI assumptions
- Assess 340B implications if the target is a DSH-qualified hospital or FQHC with in-scope pharmacy or care coordination workflows

**In Scope:**
- Name the target EHR and the specific integration approach: SMART on FHIR launch context, CDS Hooks, HL7 ADT feeds, standalone with read-only FHIR access, or direct EHR integration via vendor API
- Distinguish SMART on FHIR app (lower IT lift, sandboxed) from native EHR module (higher IT lift, deeper workflow) from standalone tool requiring a separate EHR integration
- State whether the product changes any billable activity, encounter count, or procedure volume — and the revenue impact under the provider's current payer mix

**In Risks and Open Questions:**
- Note any dependency on specific CMMI model enrollment at target organizations — and the risk that enrollment changes or a model winds down
- Flag prior authorization automation regulatory and legislative risk if PA workflow is in scope
- Call out HCC / risk adjustment audit exposure if diagnosis documentation or coding outputs are in scope
- Note EHR incumbent module risk — if the target EHR vendor has or is building a competing capability in the product category

---

## Common Failure Modes

- Asserting a VBC business case without confirming downside risk exists in the target organization's specific contract structure
- Building a ROI case on payer savings when the provider operates under FFS and does not capture those savings
- Treating CPT reimbursement as a solved problem when the relevant code is Category II, Category III, or subject to restrictive LCD coverage policies
- Conflating safety-net organization economics with general health system economics — 340B, DSH, UPL, and FQHC PPS create distinct financial logic
- Ignoring the RCM and coding vendor ecosystem when building in revenue integrity, charge capture, or coding accuracy domains
- Assuming employer self-funded channels behave like commercial insurer channels when the financial decision-maker and data owner are different entities
- Launching a sales motion or pilot at an organization in active M&A integration or post-merger EHR consolidation
- Underestimating the EHR incumbent's module roadmap and the stickiness of governance-approved tools already inside the EHR
- Assuming clinical user enthusiasm will translate to organizational adoption without a buyer champion who has committee authority and budget alignment
