# Handoff Artifact Schema

The `.health-docs/analysis.md` file uses YAML frontmatter for structured data and a markdown body for human narrative.

## Fields

| Field | Type | Description |
|---|---|---|
| `generated_at` | ISO 8601 string | Timestamp when analyze mode wrote this artifact |
| `schema_version` | string | Schema version; currently `"1"` |
| `regime_detected` | map | One entry per regime key (`hipaa`, `onc`, `fda_samd`); each has `proposed` (bool), `confidence` (`high`/`medium`/`low`), and `evidence` (list of source-backed strings) |
| `jurisdiction_detected` | object | `value` (`us`/`eu`/`us+eu`/`unclear`), `confidence`, `evidence` |
| `doc_root_detected` | string or null | First detected documentation root path (`docs/`, etc.); `null` if not found |
| `coverage` | list | One entry per documentation dimension (see `doc-hierarchy.md`) |
| `requirements` | object | Populated by document mode interview; null until interview complete |

## Coverage Entry Shape

Each `coverage` entry:

```yaml
- dimension: "secure/audit-logs"       # canonical ID matching the file path slug
  status: "partial"                     # covered | partial | conflict | absent | absent-required
  sources:                              # file paths and line ranges; empty if absent
    - path: "README.md"
      lines: "45-60"
      note: "mentions audit logging exists but no schema or retention policy"
  regulatory: "HIPAA §164.312(b)"       # applicable regulation and section, or null
  required: null                        # null until document mode interview; then true/false
  confidence: high                      # high | medium | reduced (reduced if subagent unavailable)
```

## Requirements Shape

The `requirements` block is written by document mode after the interview:

```yaml
requirements:
  interview_completed_at: null          # ISO 8601 timestamp, null until interview complete
  regime: []                            # confirmed regimes (e.g., ["hipaa", "onc"])
  dimensions: {}                        # dimension path → true/false
  human_review_required: []             # file paths requiring human sign-off
```

## Full Example

```yaml
---
generated_at: "2026-03-28T14:00:00Z"
schema_version: "1"

regime_detected:
  hipaa:
    proposed: true
    confidence: high
    evidence:
      - "Patient model with mrn, dob fields (src/models/patient.rb:12)"
      - "'phi' in 14 variable names"
  onc:
    proposed: true
    confidence: medium
    evidence:
      - "SMART on FHIR scopes in config/oauth.yml"
  fda_samd:
    proposed: false
    confidence: low
    evidence: []

jurisdiction_detected:
  value: "us"
  confidence: high
  evidence:
    - "NPI and HIPAA references in app/models/patient.rb and docs/security.md"

doc_root_detected: "docs/"   # null if not found

coverage:
  - dimension: "understand/data-flows"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(a)(1)(ii)(A)"
    required: null
    confidence: high

  - dimension: "secure/audit-logs"
    status: "partial"
    sources:
      - path: "README.md"
        lines: "45-60"
        note: "mentions audit logging exists but no schema or retention policy"
    regulatory: "HIPAA §164.312(b)"
    required: null
    confidence: high

  - dimension: "comply/hipaa/baa-inventory"
    status: "absent-required"
    sources: []
    regulatory: "HIPAA §164.308(b)(1)"
    required: null
    confidence: high

requirements:
  interview_completed_at: null
  regime: []
  dimensions: {}
  human_review_required: []

---
```

See `examples/example-analysis-artifact.md` for a fully-populated example showing both pre- and post-interview states.
