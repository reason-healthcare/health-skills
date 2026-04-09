# Example: Document Mode Pre-Flight Plan — Multi-Market

```text
CONSOLIDATE (copying to target path — no rewrites; originals flagged in place):
  README.md:12-44                 → docs/orient/README.md
  docs/privacy.md:1-52            → docs/comply/eu/gdpr/data-roles-and-lawful-basis.md
  docs/integrations.md:10-40      → docs/understand/integrations.md

MERGE (combining sources — conflicts flagged for your review):
  docs/security.md:18-39          → docs/secure/audit-logs.md
  AGENTS.md:22-29                 → docs/agent-context/phi-rules.md

DRAFT NEW (no existing source — requires human review where noted):
  docs/comply/hipaa/risk-analysis.md                         ⚠ REVIEW
  docs/comply/eu/gdpr/vendor-and-transfer-boundaries.md      ⚠ REVIEW
  docs/comply/eu/mdr-ivdr/classification-and-intended-use.md ⚠ REVIEW
  docs/comply/eu/nis2/incident-coordination-and-cyber-risk.md ⚠ REVIEW

SKIP (not required by your profile):
  docs/comply/fda/

Proceed? [yes / no / edit plan]
```
