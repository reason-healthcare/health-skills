## Context

The skill library currently has `health-fhir-api-design` covering FHIR R4 REST interactions — search, operations, workflow coordination. It presupposes the developer already knows which resources and profiles to use. In practice, app developers get stuck at an earlier step: mapping a domain concept to the right FHIR resource, understanding what profile constraints they will encounter at runtime, and modeling relationships before writing a single query.

No current skill addresses this upstream modeling layer. `health-fhir-modeling` fills that gap as a peer to `health-fhir-api-design`, not a replacement.

Existing skills to be aware of:
- `skills/.curated/health-fhir-api-design/` — the downstream counterpart; references `SKILL.md` structure as the structural model
- `openspec/specs/healthcare-skill-library/spec.md` — inventory to be updated

## Goals / Non-Goals

**Goals:**
- Help app developers map domain concepts to the correct FHIR R4 base resources, with clear rationale for rejecting near-miss alternatives
- Teach profile reading: given a US Core or QI Core profile, what constraints does the developer need to satisfy in their instances?
- Guide relationship modeling: reference vs contained, identifier types, `Reference.display` vs `Reference.reference`, chained lookups
- Guide extension usage: find an existing R4 or US Core extension before inventing one; understand when a new extension is unavoidable
- Provide practical terminology guidance: which code system to use for a given clinical concept, what required/extensible/preferred binding strength means for a developer consuming or producing data

**Non-Goals:**
- Profile authoring — the skill does not help write StructureDefinition resources or publish Implementation Guides
- Knowledge artifact authoring — PlanDefinition, Measure, CQL, SDC Questionnaire are out of scope; those target clinical informaticists, not app developers
- FHIR Logical Model publishing — useful conceptually but not a deliverable of this skill
- R5 features — skill targets R4 (v4.0.1) only, consistent with sibling
- Da Vinci IG deep-dives — covered in a potential future skill; US Core and QI Core are sufficient for MVP

## Decisions

### D1: Two modes — Model and Review

**Decision**: Parallel to `health-fhir-api-design`, the skill exposes a **model** mode (default) and a **review** mode.

**Rationale**: Developers use the skill in two distinct contexts — greenfield (I need to figure out what FHIR resources represent my concept) and evaluation (I have an existing model, tell me what's wrong). Conflating them into one flow would either over-ask or under-ask questions.

**Alternative considered**: Single mode that detects intent from context. Rejected because mode ambiguity leads to poor first-question UX.

---

### D2: Output is annotated JSONC instances, not FSH or StructureDefinition

**Decision**: The skill outputs annotated JSONC instances (JSON-with-Comments) with inline comments explaining modeling choices, alongside prose mapping rationale. JSONC is illustrative — comments must be stripped to obtain parseable JSON.

**Rationale**: App developers write code that creates/reads JSON instances. They don't write FSH or compile IGs. Showing an actionable example instance with inline explanations is immediately useful — they can paste it as a test fixture, a template, or documentation for a server team. StructureDefinition output would require IG toolchain knowledge they don't have.

**Alternative considered**: FSH (FHIR Shorthand) output. Rejected — FSH is a profile-authoring format, inappropriate for the target persona.

---

### D3: US Core as primary profile context, QI Core as secondary

**Decision**: When profile guidance is needed, the skill defaults to US Core 5.0.1 semantics. QI Core is referenced for quality measurement contexts.

**Rationale**: US Core is the most common profile set app developers encounter in real implementations (EHR integrations, SMART apps, CMS API compliance). QI Core is a superset relevant for quality-measure-adjacent apps but less universally encountered.

**Alternative considered**: Treat all profiles equally. Rejected — providing undifferentiated coverage would be shallow on everything and practically helpful for nothing.

---

### D4: Terminology guidance is practical, not authoring

**Decision**: The skill explains which code system to use for a given clinical concept, what the four binding strengths mean for a developer consuming or producing data, and common lookup patterns. It does not help the developer author ValueSets.

**Rationale**: App developers need to know "use LOINC 8867-4 for pulse rate" and "this is a required binding — you must send a code from this ValueSet or the resource will fail $validate." They don't need to know how to design a ValueSet hierarchy.

---

### D5: Skill starts in `.experimental/`

**Decision**: New skill placed at `skills/.experimental/health-fhir-modeling/`. Promotion to `.curated/` follows normal review process.

**Rationale**: Consistent with all other new skills in this repository.

---

### D6: Reference files follow sibling pattern

**Decision**: Skill includes a `references/` directory with three files:
- `fhir-r4-resources.md` — resource categories, common modeling patterns, complex data types, and choice type (polymorphism) reference
- `profile-guides.md` — FHIR R4 profiling concepts: StructureDefinitions, slicing, binding strength, extension shapes, differential vs snapshot, and how to read a profile in an IG
- `us-core-guide.md` — US Core regulatory context (21st Century Cures Act, ONC rules), and must-support elements and binding constraints for five key resources (Patient, Observation, Condition, Encounter, MedicationRequest)

Mirrors `health-fhir-api-design/references/fhir-patterns.md`.

**Rationale**: Keeps SKILL.md concise while giving the agent grounded, citable reference material. Splitting US Core into its own file keeps profiling concepts portable and prevents conflation of base FHIR semantics with implementation profile requirements.

## Risks / Trade-offs

- **Resource selection is context-dependent** → Mitigation: Model mode starts with clarifying questions before recommending anything. Skill should ask about care setting, actors, and whether the concept is being produced or consumed before narrowing resource candidates.
- **US Core is version-specific** → Mitigation: Skill notes that US Core versions differ (5.0.1 vs 6.1.0) and flags where constraints differ materially. Default to 5.0.1 (widely deployed) unless user specifies otherwise.
- **Profile compliance surface is large** → Mitigation: Focus on must-support and required binding constraints; skip optional/should elements unless directly asked. This keeps output tractable for a developer.
- **Extension discovery depends on knowing where to look** → Mitigation: Reference files catalog common US Core extensions. For gaps, skill directs developer to the correct HL7 registry URL rather than inventing.
- **Scope creep toward profile authoring** → Mitigation: Explicit constraint in SKILL.md `## Constraints` section — if a user asks for help writing a StructureDefinition, redirect to IG tooling documentation.

## Open Questions

- Should the skill include a worked example file (`examples/example-model.md`) in the initial version, or defer to a follow-on task? Recommend including one example (a US Core Patient + Observation pair) to set output format expectations.
- QI Core coverage depth: should review mode check QI Core `must-have` elements, or US Core only? Leave as US Core only for MVP; QI Core can be added when a real use case surfaces.
