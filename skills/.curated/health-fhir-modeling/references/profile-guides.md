# FHIR R4 Profiling Concepts

*Summarized from [hl7.org/fhir/R4/profiling.html](https://hl7.org/fhir/R4/profiling.html)*

FHIR is a "platform specification" — a common foundation on which many different solutions are built. Profiles are how that foundation is adapted to particular contexts (jurisdiction, institution, use case).

> **Scope of this reference**: The concepts here are for understanding what a profile *requires you to populate and how to structure it* — i.e., data modeling decisions. Comprehensive conformance validation (cardinality enforcement, terminology validation, invariant checking) is deterministic and is best delegated to tooling such as the HL7 FHIR validator (`https://confluence.hl7.org/display/FHIR/Using+the+FHIR+Validator`) or server-side `$validate`. This skill does not attempt to replicate validator output.

---

## What Is a Profile?

A **profile** is a `StructureDefinition` resource with `kind = constraint`. It declares a set of rules about how elements in a FHIR resource are used in a specific context. Profiles are published as part of an **Implementation Guide (IG)**.

| Artifact | Description |
|---|---|
| **Implementation Guide (IG)** | A coherent, bounded set of adaptations published as a single unit |
| **Profile** | A set of constraints on a resource — a StructureDefinition with `kind = constraint` |
| **Extension** | A new element not in the base spec, defined in a StructureDefinition with `kind = complex-type` or `kind = primitive-type` |

Each profile is identified by a **canonical URL** (e.g., `http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient`). Resources declare conformance to a profile in `meta.profile`.

---

## What Profiles CAN Do

- **Restrict cardinality**: narrow `0..*` to `1..1`; prohibit an element with `0..0`
- **Fix values**: require a specific code, system, or value
- **Restrict types**: limit polymorphic elements (e.g., `value[x]`) to specific types
- **Rebind terminology**: point to a different ValueSet, or tighten binding strength (but never loosen it)
- **Mark Must Support**: flag elements that conformant systems must be able to populate and process
- **Slice repeating elements**: split a list into named sub-lists with different constraints
- **Prescribe extensions**: require or allow specific extensions

## What Profiles CANNOT Do

- Break rules from the base specification (cardinality can only be tightened, never widened)
- Specify default values for base-spec elements
- Rename or add elements to the base resource
- Make a resource unsafe to process by a system unaware of the profile

---

## Must Support — Base FHIR Definition

`mustSupport = true` on an element is a declaration, not a fixed rule. What it means depends on the IG that defines the profile. The IG MUST describe what "support" requires — examples include:

- The system must be able to store and retrieve the element
- The system must display it to the user
- The system must not ignored it when processing

**Must Support ≠ mandatory.** An element can have `mustSupport = true` and `min = 0`. Cardinality governs presence; Must Support governs capability.

For US Core's specific definition of Must Support, see `references/us-core-guide.md`.

---

## Binding Strength

Coded elements have a binding that links to a ValueSet and a strength that governs how tightly the codes are interpreted. A profile can only make bindings *more* restrictive — never looser.

| Strength | Rule |
|---|---|
| **required** | Code MUST come from this ValueSet exactly. Any other code is invalid. |
| **extensible** | Code SHOULD come from this ValueSet. Use another code only if the ValueSet has no suitable concept. |
| **preferred** | Code SHOULD come from this ValueSet; deviation is less strictly enforced. |
| **example** | ValueSet is illustrative only; no conformance obligation. |

**Changing binding strength in a derived profile**: `required → required` only; `extensible → required|extensible`; `preferred → any tighter or same`; `example → any`.

---

## Slicing

Slicing splits a repeating element into named sub-lists, each with its own constraints. It is how profiles distinguish, for example, a systolic component from a diastolic component within `Observation.component`.

Key terms:
- **Discriminator**: the element (and type of comparison) used to tell slices apart. Common types: `value` (exact value match), `pattern` (CodeableConcept match), `type` (resource type on a reference), `exists` (presence/absence).
- **Slice name**: a label defined in the profile, never serialized in the instance — it is invisible to consuming code.
- **Closed vs open**: an open slice allows elements that match none of the named slices; a closed slice does not.

**Extensions are always sliced by `url`** — this is why an extension's canonical URL is its identity.

Reading sliced elements in practice: when a profile shows `Observation.category` sliced on `value`, look for a fixed code in the discriminator element to understand what value is expected.

---

## Extensions

An extension adds a new element not in the base resource. Every extension is identified by its canonical URL — that URL IS the extension's identity. Two extensions with different URLs are different elements, regardless of similar names or structures.

Extensions appear under the `extension` array on any resource or element, or under `modifierExtension` when the extension changes the meaning of the containing element (rare).

### Simple Extension

A simple extension carries a single `value[x]`. The shape in an instance:

```jsonc
{
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
      "valueCode": "F"
    }
  ]
}
```

The property name is always `value` + the type (e.g., `valueCode`, `valueString`, `valueBoolean`, `valueQuantity`, `valueCodeableConcept`). Only one `value[x]` variant is present per extension instance.

### Complex Extension

A complex extension nests sub-extensions instead of a `value[x]`. Each sub-extension has its own `url` (a relative name, not a full URL) and its own `value[x]`:

```jsonc
{
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
      "extension": [
        {
          "url": "ombCategory",            // sub-extension name (relative url)
          "valueCoding": {
            "system": "urn:oid:2.16.840.1.113883.6.238",
            "code": "2106-3",
            "display": "White"
          }
        },
        {
          "url": "text",                   // second sub-extension
          "valueString": "White"
        }
      ]
    }
  ]
}
```

### Modifier Extensions

A `modifierExtension` changes the meaning of the resource or element it is on — consuming systems that do not understand it MUST NOT process the containing resource. Use only when mandated by a profile. Structure is identical to `extension`:

```jsonc
{
  "modifierExtension": [
    {
      "url": "http://example.org/fhir/StructureDefinition/some-modifier",
      "valueBoolean": true
    }
  ]
}
```

### Finding the Right Extension for Modeling

1. Check the profile's Snapshot Table — required extensions appear as must-support slices of the `extension` list with their canonical URL shown
2. Check the R4 core extension registry: `https://hl7.org/fhir/R4/extensibility-registry.html`
3. Check US Core extension URLs in `references/us-core-guide.md`
4. Only define a custom extension if no existing one fits — the canonical URL must be globally unique and dereferenceable

> **Validation scope**: Verifying that an extension URL is registered, that the `value[x]` type matches the StructureDefinition, or that a required extension is present is the job of a FHIR validator. This skill helps you understand what to put in the instance; the validator tells you whether it is correct.

---

## Differential vs Snapshot

A `StructureDefinition` may carry two views:

| View | What it contains |
|---|---|
| **Differential** | Only the changes relative to the parent profile or base resource. Sparse — only lists constrained elements. |
| **Snapshot** | The fully calculated structure including inherited elements. Complete — safe to read in isolation. |

In practice, IG viewers show both. When reviewing a profile to understand what you must populate, use the **Snapshot Table** — it shows every element with all accumulated constraints. The Differential alone may omit inherited must-support elements.

---

## Conformance Assertions

Resources declare which profiles they conform to in `meta.profile`:

```jsonc
{
  "resourceType": "Patient",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"]
  }
}
```

A producer system SHOULD populate `meta.profile` for any resource that conforms to a declared profile. This enables receivers and servers to index and filter by profile using the `_profile` search parameter.

---

## How to Read a Profile in an IG

IGs present profiles in five views (using US Core as an example):

| View | Use it for |
|---|---|
| **Text Summary** | Quick orientation — what the profile is for |
| **Differential Table** | Seeing what this profile adds on top of base R4 |
| **Snapshot Table** | Complete element list — use this to understand what you must populate |
| **XML Template** | Structural shape in XML |
| **JSON Template** | Structural shape in JSON |

**Reading the Snapshot Table column by column**:
- `Flag` — `S` means Must Support; `?!` means IsModifier
- `Card.` — cardinality; `1..1` is required; `0..0` is prohibited
- `Type` — data type or reference target
- `Description & Constraints` — binding information, invariants, fixed values

