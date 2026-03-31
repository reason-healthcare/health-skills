# EU Market Overlay

Use this overlay when the product targets EU healthcare systems or cross-border European deployment. Apply for `eu` or `us+eu` jurisdictions. Treat this as product and market-access guidance, not a compliance appendix.

## Market Context

- **Member-state fragmentation**: buyer structure, deployment pathways, reimbursement logic, and evidence expectations differ significantly across countries and often across regions within a country
- **Public procurement dominance**: tendering, framework agreements, and public or quasi-public procurement bodies shape the sales motion in most EU healthcare markets; relationship-driven sales is a secondary channel
- **HTA and reimbursement variation**: health technology assessment bodies, evidence thresholds, and funding pathways differ by country and are not harmonized at the EU level despite the EU HTA Regulation's joint clinical assessment layer
- **Localisation as a product requirement**: language, national clinical workflow conventions, patient communication standards, national patient identifier schemes, and procurement documentation are market-access requirements, not UX polish
- **Public-system incentives**: service efficiency, wait-list reduction, equity, and policy alignment with national digital health strategy may be the primary value dimensions — not margin improvement or revenue capture
- **Cross-border interoperability trajectory**: EHDS, MyHealth@EU exchange expectations, patient summaries, and ePrescription flows are becoming infrastructure requirements in some markets and must be assessed per target member state

---

## Healthcare Economics

EU healthcare economics differs from the US in fundamental ways — predominantly public funding, centralized procurement, and fragmented national systems — but is no less complex. A product viable in one EU member state may be economically unviable in the next with the same value framing.

### HTA Fragmentation and the EU HTA Regulation

Health Technology Assessment determines whether a product's clinical value justifies public funding. National HTA bodies operate distinct methodologies:

- **NICE** (England/Wales) — QALY-based cost-effectiveness; £20,000–£30,000/QALY threshold for standard decisions; higher for end-of-life or highly specialized technologies; SHTG in Scotland follows separate methodology
- **G-BA / IQWiG** (Germany) — early benefit assessment (AMNOG framework); no explicit cost-effectiveness threshold; comparative benefit relative to a defined comparator therapy (zweckmäßige Vergleichstherapie) is the criterion; "no added benefit" means reimbursement defaults to comparator price
- **HAS** (France) — medical service rendered (SMR) and improvement in medical service rendered (ASMR); five-level improvement scale determines price premium eligibility over existing treatments
- **AIFA** (Italy) — negotiated pricing with the national pricing committee (CTS); regional formulary variation is substantial even after national AIFA listing approval
- **TLV** (Sweden) — cost per QALY with explicit comparator; value-based pricing with negotiated managed entry agreements that may include outcome-based rebates

**EU HTA Regulation (2021/2282)** — mandatory joint clinical assessment for oncology drugs and ATMPs from January 2025, with class IIb and III medical devices added from 2030. The joint clinical assessment produces a common clinical evidence report for all member states, reducing duplication of evidence dossiers. However, national pricing and reimbursement decisions remain fully sovereign — each member state still determines whether to fund the product and at what price, and can weigh the joint clinical assessment report differently.

Products must budget for: joint clinical assessment evidence framing (even before medical devices are in scope), separate P&R dossiers and price negotiations for each target market, and country-specific HTA timelines ranging from 3 months (Germany benefit assessment) to 18+ months (Italy AIFA negotiation followed by regional formulary adoption).

### DRG Payment Variation Across Member States

Each EU member state operates its own diagnosis-related group (DRG) system with distinct case definitions, grouper logic, and reimbursement rates:

- Germany: G-DRG (annual InEK updates; case-mix points × base rates negotiated per hospital; supplement codes for high-complexity or new procedures)
- France: GHM/GHS (national tariff with hospital-specific supplements for teaching and research activity)
- Spain: CIE-10-ES-based GRD (national coding; tariff-setting by autonomous community)
- Netherlands: DBC-DOT (pathway-based; combination of main diagnosis and all treatments in one period)
- Italy: DRG-IT (national ICD-9-CM-based codes; regional tariff variation after national classification)

The same care pathway may be reimbursed at rates varying 3–5x across member states. A product that changes care protocols, reduces length of stay, substitutes outpatient for inpatient, or shifts resource intensity must model impact on each country's specific DRG reimbursement — not a pan-European average.

### National Digital Health Certification Pathways

Several member states have created reimbursement pathways for digital health applications that serve simultaneously as regulatory approval, reimbursement mechanism, and a primary market discovery channel:

- **Germany — DiGA (Digitale Gesundheitsanwendungen)**: BfArM Fast-Track process; GKV-reimbursed if classified; provisional reimbursement available without positive clinical evidence during a 12-month evaluation period; permanent reimbursement requires demonstrated positive care effects; realistic timeline 24–36 months for provisional listing, 48+ months for permanent; listed DiGAs typically price in the €200–€700/year range per patient, subject to negotiated price ceilings after the provisional period
- **France — PECAN / HAS MED-EV / Mon Espace Santé**: ANS certification required for integration with national health data infrastructure; HAS MED-EV evaluation for digital medical devices; PECAN pathway for connected medical devices seeking reimbursement; significant complexity across pathways; realistic timeline 12–24 months depending on classification
- **Belgium — Evidence-based m.Health pathway**: reimbursement classification for validated mobile health applications; clinical evidence requirements scale by tier; limited volume of approvals annually
- **UK — NHS DTAC (Digital Technology Assessment Criteria)**: mandatory for NHS procurement; covers clinical safety (DCB0129/DCB0160 standards), data protection (NHS DSP Toolkit), interoperability, and usability; not a reimbursement pathway but a procurement prerequisite; approval does not guarantee local adoption by ICBs

Each pathway has different clinical evidence requirements, acceptable study designs, timelines, costs, and reimbursement structures. Evidence packaged for one pathway may not satisfy another.

### Public vs. Private Healthcare Split

EU member states differ substantially in public/private mix, and this determines the buyer archetype and procurement dynamic:

- **Predominantly public** (>80% public funding): UK NHS, Nordic systems (Denmark, Sweden, Norway, Finland), Spain, Portugal — products sell to national or regional health authorities; discretionary purchasing is rare; procurement is formal, transparent, and slow
- **Social insurance with private complement**: Germany (GKV covers ~90%; 95+ competing statutory Krankenkassen funds with separate contracts), France (assurance maladie + complémentaire santé ~95% saturation), Netherlands (mandatory social insurance with regulated private carriers)
- **High private activity**: Switzerland, Ireland (large private hospital sector alongside the public HSE); private channels are accessible but represent a smaller total addressable market in most geographies

Germany's GKV structure deserves specific attention: a product that negotiates directly with statutory health funds (rather than entering through the DiGA pathway or hospital procurement) must manage contracts with dozens of independent funds. The top five — TK, Barmer, DAK-Gesundheit, KKH, and the AOK group — cover the majority of the insured population and are the realistic negotiation counterparties for selective contracting.

### Regional Procurement Fragmentation Within Countries

Even within states with nominally national health systems, procurement authority is substantially devolved:

- **Spain**: 17 Autonomous Communities each operate independent health systems with separate formulary committees, IT procurement, and clinical governance; a national rollout requires 17 separate regional procurement processes or a national framework agreement through the INGESA/Consejo Interterritorial del SNS mechanism — which itself takes years to establish
- **Italy**: 21 regions set independent formularies, reimbursement tariffs, and technology adoption policies; AIFA national approval is necessary but not sufficient — regional HTA bodies (with varying levels of formality) make final adoption decisions
- **Germany**: G-BA makes coverage decisions at federal level, but hospital capital investment (Investitionsmittel) is a Länder responsibility — creating a split between operational purchasing and capital equipment that affects different product types differently
- **UK**: 42 Integrated Care Boards in England have substantial procurement autonomy below NHS England thresholds; a product with national NHS approval still requires individual ICB adoption decisions

### Tendering, OJ/TED, and Framework Agreement Cycles

EU procurement law (Directive 2014/24/EU, transposed nationally) governs public procurement above threshold values (services: ~€221,000 for central government; ~€443,000 for sub-central authorities). Above these thresholds:

- Purchases must be advertised in TED (Tenders Electronic Daily — the EU Official Journal supplement)
- Competitive tender with defined award criteria and weightings is mandatory
- Process from tender notice to contract typically takes 4–12 months
- Framework agreements — typically 4-year duration, multi-supplier — are common procurement vehicles; access requires being selected at framework award time

Missing a framework agreement window means waiting until the next cycle opens — typically 4–7 years. Products entering a market where relevant frameworks already exist must qualify as a catalog item under an existing framework, win a standalone contract through an above-threshold open procedure, or wait. This is a market-access constraint that must be modeled from the outset, not discovered after product launch.

### Realistic EU Market Access Timelines

Combining HTA review, national P&R negotiation, regional adoption, procurement, and system integration, realistic market access timelines are:

| Country | Pathway | Realistic Timeline to First Revenue |
|---|---|---|
| Germany (DiGA) | BfArM provisional listing → GKV reimbursement | 24–36 months from dossier submission |
| Germany (hospital direct) | G-BA coverage + hospital tender | 18–30 months from clinical engagement |
| France | HAS MED-EV + CEPS pricing negotiation | 18–30 months |
| Italy | AIFA national listing + regional formulary | 24–42 months |
| Spain | National framework or autonomous community procurement | 24–48 months |
| UK (NHS) | NHS DTAC clearance + ICB procurement | 12–24 months (highly variable by ICB) |
| Netherlands | Zorginstituut advice + ZN contracting | 18–30 months |

Products assuming EU market access within 12–18 months are almost certainly underestimating unless entering through a private channel, piggybacking on an existing certified national pathway, or operating in a funded pilot that does not constitute general market access.

### International Reference Pricing Risk

Many EU member states set or negotiate prices in part by reference to prices already agreed in other countries. Germany, Spain, Italy, Netherlands, and others use formal or informal reference pricing baskets. A low price committed in one market to achieve early access can become a price ceiling in subsequent markets — potentially undermining the entire EU pricing strategy. Products setting multi-country EU prices sequentially must model the reference pricing dynamics in each target market before setting the first price.

---

## Explore Mode: Challenge Prompts

Use these to pressure-test product assumptions that routinely fail when teams approach EU markets without country-specific modeling — or when product design implicitly reflects a single-country template.

**On market selection and country-specificity:**

- Which specific member state or region is the first deployment market — and which assumptions in the product design or value case fail when extended to the next country?
- Has the team modeled the HTA evidence requirements for the first target market's specific body: NICE QALY model, G-BA comparative benefit framework, HAS SMR/ASMR scale? Has clinical evidence been reviewed against local methodology rather than FDA endpoints?
- Does the product qualify for any national digital health reimbursement pathway (DiGA, HAS/PECAN, NHS DTAC), or is it entering a private channel only? If private-only, what is the realistic addressable market size given the public/private mix of the target country?

**On procurement and sales motion:**

- Is the buyer a national health authority, a regional health authority, an integrated care board, a hospital group, a public hospital, or a private group? Each implies a fundamentally different procurement path, timeline, and evidence requirement.
- Has the team budgeted for mandatory tender processes above EU thresholds — including preparation timeline, documentation burden, scoring criteria definition, and the possibility of legal challenge to the procurement outcome?
- Is there an existing framework agreement the product could qualify for in the target market? If not, what is the timeline for the next framework cycle, and is the product roadmap compatible with that timeline?
- What is the realistic timeline from first clinical engagement to signed contract under the target country's actual procurement rules — and is that timeline compatible with the product runway and investor expectations?

**On HTA and reimbursement:**

- Has the team modeled the evidence requirements of the target market's HTA body — including accepted study designs, minimum sample sizes, acceptable comparators, and specific outcome endpoints?
- Is real-world evidence accepted by the target HTA body, or is a randomized controlled trial required for reimbursement? If an RCT is required, has the 2–4 year timeline and £2M–£10M+ cost been modeled?
- If the product is AI-enabled or constitutes medical device software, has the team assessed whether MDR/IVDR CE marking and AI Act conformity assessment are both required — and whether they can run concurrently or must be sequential?
- What is the reimbursement mechanism — DRG-embedded, separate technology supplement, service tariff, or bundled capitation — and which entity in the funding chain captures the value the product creates?

**On national infrastructure and localisation:**

- Which national health data infrastructure standards does the product need to support: national FHIR profiles (DE BASISPROFIL, FHIR UK Core, Finnish base profiles), national patient identifier schemes (NHS Number, Finnish HETU, German Krankenversichertennummer), national terminology extensions (ICD-10-GM vs ICD-10-CM, national SNOMED CT extensions)?
- Does the product need to interoperate with national infrastructure systems — NHS Spine/GPConnect, Mon Espace Santé (France), Telematikinfrastruktur (Germany TI), LSP (Netherlands), Kanta (Finland)?
- Is language and clinical terminology localisation scoped and budgeted as a first-class product requirement — including regulatory document and patient consent translation — or is it treated as a post-launch activity?

**On EU economics and value capture:**

- If the value case is operational efficiency savings, which entity captures them — the payer, the regional authority, or the hospital — and are efficiency savings returned to the budget holding entity that is purchasing the product?
- Does the value case depend on DRG-based revenue impact? If so, has it been modeled for the target country's specific DRG system, not a generic pan-European assumption?
- If multi-country EU pricing is being set, has the international reference pricing dynamic been modeled — specifically, does the entry price in Country A create a binding ceiling or floor in Countries B and C?
- Is the reimbursement model sustainable if the product is successful — i.e., does high utilization stress a fixed GKV or NHS budget and risk triggering usage caps, price renegotiation, or de-listing?

---

## Document Mode Additions

When producing a discovery document for a EU market product, include the following in the relevant sections:

**In Payment Model and Business Viability:**
- State which member state(s) are in scope and the applicable HTA or reimbursement pathway for each — do not aggregate to "EU"
- Note whether any national digital health certification pathway applies (DiGA, HAS/PECAN, NHS DTAC) and the realistic timeline, cost structure, and clinical evidence requirements for each
- State whether the reimbursement model is public tender, framework agreement, private-pay, or pilot-funded — and describe the procurement pathway and timeline for each country in scope
- Model the realistic market access timeline by country, distinguishing HTA review → national P&R → regional formulary/adoption → procurement phases
- Address international reference pricing risk if multi-country pricing is being set simultaneously or sequentially
- Note which EU procurement thresholds apply and whether an OJ/TED open tender process is required

**In Scope:**
- State the first deployment market explicitly and acknowledge which product assumptions require separate validation in each subsequent target country
- List localisation as a first-class scope item: language, national clinical terminology, national patient identifier support, and integration with any required national infrastructure system
- State MDR/IVDR classification assessment and AI Act conformity assessment status if any AI component, clinical decision support, or device software is in scope — both may be required with independent timelines

**In Risks and Open Questions:**
- Note HTA evidence gap risk — if clinical evidence was designed for US FDA endpoints, assess alignment with target HTA body's accepted methodology and comparator framework
- Flag national digital infrastructure dependency risk — if the product requires a specific national system integration (TI connector, NHS Spine access) before it can operate at scale, that dependency is on the critical path
- Note multi-country expansion assumption risk — document which first-market assumptions require separate validation per subsequent country
- Identify international reference pricing risk if price commitments in one market affect P&R negotiation in others

---

## Common Failure Modes

- Treating the EU as a single homogeneous market — procurement rules, reimbursement logic, HTA methodology, and clinical workflow conventions differ by country and often by region within a country
- Designing clinical evidence for US FDA endpoints and assuming it transfers without modification to NICE QALY, G-BA comparative benefit assessment, or HAS SMR requirements
- Underestimating national digital health certification timelines and treating certification as a technical formality rather than an 18–36+ month market access exercise with genuine evidence requirements
- Missing framework agreement award windows and discovering that ad hoc procurement above EU thresholds is not legally permissible without a full open tender process
- Building the business case primarily around private-pay channels in predominantly public healthcare systems, where private-pay is a small fraction of the total healthcare economy
- Treating localisation as a post-launch activity — national infrastructure integration, clinical terminology mapping, and regulatory document translation are market-access requirements, not UX polish
- Conflating MDR/IVDR CE marking with AI Act conformity assessment — both may be required for AI-enabled clinical tools, with separate technical documentation, different notified body involvement, and independent timelines
- Assuming first-market evidence and pricing commitments do not affect subsequent EU markets — international reference pricing can make the entry price in Country A a permanent constraint on pricing in Countries B, C, and D
