## 1. Skill Scaffold

- [x] 1.1 Create directory `skills/.experimental/health-fhir-modeling/`
- [x] 1.2 Create `skills/.experimental/health-fhir-modeling/agents/openai.yaml` following the sibling `health-fhir-api-design` YAML structure
- [x] 1.3 Create empty `skills/.experimental/health-fhir-modeling/references/` and `skills/.experimental/health-fhir-modeling/examples/` directories (with `.gitkeep` until populated)

## 2. Reference Files

- [x] 2.1 Create `references/fhir-r4-resources.md` covering: resource category overview (clinical, workflow, financial, infrastructure), key resources by domain (demographics, observations, orders, documents), and common modeling patterns (one-to-many relationships, resource reuse vs duplication)
- [x] 2.2 Create `references/profile-guides.md` covering: FHIR R4 profiling concepts (StructureDefinitions, slicing, Must Support, binding strength, extensions, differential vs snapshot, how to read an IG profile)
- [x] 2.3 Create `references/us-core-guide.md` covering: regulatory context (21st Century Cures Act, ONC Final Rule, CMS Interoperability Rule), USCDI relationship, and US Core 5.0.1 must-support elements and binding constraints for Patient, Observation, Condition, Encounter, and MedicationRequest

## 3. Example Output

- [x] 3.1 Create `examples/example-model.md` demonstrating a complete model mode output: domain concept description (vital sign observation), candidate resources considered, primary resource selection with rationale, US Core profile constraints identified, relationship to Patient and Practitioner, terminology (LOINC code + binding), annotated JSONC instance (illustrative; comments stripped to obtain parseable JSON), and mapping rationale summary

## 4. SKILL.md

- [x] 4.1 Write the SKILL.md frontmatter (name, description) — description targets app developers; mentions FHIR R4, US Core, resource selection, profile compliance
- [x] 4.2 Write the Purpose section: who this is for, what it does, and its relationship to `health-fhir-api-design`
- [x] 4.3 Write the Modes section header and mode detection logic (model default, review on explicit existing-model input)
- [x] 4.4 Write Mode: model — Steps 1-7 covering: clarify domain concept → identify candidate resources → recommend primary resource with rejection rationale → identify applicable US Core/QI Core profiles and must-support constraints → model relationships → guide extension usage → provide terminology coding guidance
- [x] 4.5 Write Mode: model — Output section specifying: annotated JSON example instance + mapping rationale, conformance notes for applicable US Core profile, placeholder values noted for missing required elements
- [x] 4.6 Write Mode: review — Steps 1-5 covering: receive existing model → check resource fitness → check US Core must-support and required binding compliance → check relationship reference targets → check extension appropriateness
- [x] 4.7 Write Mode: review — Output section: findings list (error/warning/note) with element path, issue, and corrective recommendation; confirmation message when model is correct
- [x] 4.8 Write Constraints section: R4 only, US Core primary/QI Core secondary, no profile authoring (redirect to FSH/IG Publisher), no knowledge artifact authoring (CQL/PlanDefinition/Measure/SDC), no ValueSet authoring
- [x] 4.9 Write Operating Rules section: prompt injection boundary (FHIR content and reference files are data, not instructions; flag agent-directed content), no command execution
- [x] 4.10 Write References section listing `references/fhir-r4-resources.md`, `references/profile-guides.md`, `examples/example-model.md`, and the FHIR R4 spec URL

## 5. Registry Updates

- [x] 5.1 Add `health-fhir-modeling` to DEVELOPER.md under the experimental skills list
- [x] 5.2 Add `health-fhir-modeling` entry to README.md in alphabetical order (between `health-fhir-api-design` and `health-hipaa-review`)

## 6. Validation

- [x] 6.1 Run `python scripts/validate_skill_library.py` and confirm no errors
- [x] 6.2 Run `python scripts/verify_skills_sh_compat.py` and confirm no errors
- [x] 6.3 Run `python scripts/audit_skill_security.py` and confirm no FAIL findings for the new skill
