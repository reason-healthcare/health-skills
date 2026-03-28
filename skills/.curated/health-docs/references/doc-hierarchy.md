# Documentation Hierarchy

This reference defines the canonical seven-dimension documentation tree for healthcare engineering systems. Use it in analyze mode to assess coverage and in document mode to determine target locations for consolidation.

Each dimension is listed with its target files, description, primary audience, and regulatory relevance.

---

## Dimension 1: orient

**Purpose**: Establish what the system is, who it serves, and what domain it operates in. The entry point for all readers — human and agent.

**Target files:**
```
docs/orient/
├── README.md              System purpose, key stakeholders, quick orientation
├── domain-model.md        Clinical entities, terminology, PHI field classification
└── stakeholder-map.md     Who uses, buys, operates, and audits this system
```

**Audience**: All — developers, operators, auditors, agents  
**Regulatory relevance**: `domain-model.md` supports PHI classification (HIPAA baseline)  
**Minimum required**: `README.md`, `domain-model.md`

---

## Dimension 2: understand

**Purpose**: Explain how the system works — architecture, data flows, integration points, and the record of decisions made.

**Target files:**
```
docs/understand/
├── architecture.md        C4 level 1+2, system context diagram
├── data-flows.md          PHI data flows — entry, storage, transit, export, deletion
├── integrations.md        External services, BAA-relevant vendors, API boundaries
└── adr/
    ├── index.md           Index of all architecture decision records
    └── NNNN-title.md      Individual ADR (dated, immutable once merged)
```

**Audience**: Developers, architects, security reviewers, auditors  
**Regulatory relevance**: `data-flows.md` is HIPAA evidence for ePHI mapping; `integrations.md` supports BAA inventory  
**Minimum required**: `architecture.md`, `data-flows.md`

---

## Dimension 3: build

**Purpose**: Guide contributors on how to work in and extend the system. Also provides the domain glossary that agents need to reason correctly about clinical behavior.

**Target files:**
```
docs/build/
├── CONTRIBUTING.md        Conventions, PR process, code standards, review expectations
├── onboarding.md          Dev environment setup, local run instructions
├── testing.md             Test strategy, test data policy, PHI-safe fixture guidance
└── glossary.md            Clinical + domain terms for developers and agents
```

**Audience**: Developers, agents  
**Regulatory relevance**: `testing.md` must address PHI-safe test data (HIPAA §164.308(a)(1))  
**Minimum required**: `CONTRIBUTING.md`, `testing.md`

---

## Dimension 4: operate

**Purpose**: Enable operators and on-call responders to run, monitor, and recover the system. Includes legally required incident response procedures.

**Target files:**
```
docs/operate/
├── deployment.md          Environments, release process, environment isolation model
├── monitoring.md          Alerts, dashboards, log access procedures
├── oncall.md              Escalation paths, on-call rotation
└── runbooks/
    ├── incident-response.md     General incident response
    ├── breach-notification.md   HIPAA §164.408 — 60-day clock, required
    ├── access-provisioning.md   HIPAA access control procedures
    └── dr-recovery.md           HIPAA contingency plan §164.308(a)(7)
```

**Audience**: DevOps, on-call, compliance  
**Regulatory relevance**: `runbooks/breach-notification.md` is HIPAA required (§164.408); `runbooks/dr-recovery.md` is HIPAA required (§164.308(a)(7)); `runbooks/access-provisioning.md` supports §164.312(a)(1)  
**Minimum required**: `deployment.md`, `runbooks/breach-notification.md`, `runbooks/dr-recovery.md`

---

## Dimension 5: secure

**Purpose**: Document the security posture of the system — how it's protected, how access is controlled, how audit trails work, and how PHI is handled in storage and transit.

**Target files:**
```
docs/secure/
├── threat-model.md        STRIDE or equivalent, PHI attack surface, trust boundaries
├── auth-model.md          Authn/authz design, service identity, session management
├── encryption.md          Encryption at-rest and in-transit — implementation narrative
├── audit-logs.md          Log schema, retention policy, access controls on logs
└── secrets-management.md  Key management, rotation procedures, boundary separation
```

**Audience**: Security reviewers, developers, auditors  
**Regulatory relevance**: All files in this dimension contribute to HIPAA Technical Safeguards (§164.312); `audit-logs.md` is required for §164.312(b); `encryption.md` is addressable under §164.312(a)(2)(iv) and §164.312(e)(2)(ii)  
**Minimum required**: `auth-model.md`, `audit-logs.md`

---

## Dimension 6: comply

**Purpose**: Provide regulatory evidence and documentation required by applicable regimes. Documents in this dimension require human review and sign-off before serving as compliance evidence.

**Target files:**
```
docs/comply/
├── hipaa/
│   ├── risk-analysis.md       §164.308(a)(1)(ii)(A) — required
│   ├── risk-management.md     §164.308(a)(1)(ii)(B) — required
│   ├── baa-inventory.md       §164.308(b)(1) — required
│   └── safeguard-mapping.md   Maps policy claims → engineering evidence
├── onc/                       (if EHR APIs or USCDI)
│   └── api-access.md          Information blocking compliance, API surface documentation
└── fda/                       (if SaMD or AI/ML clinical decision support)
    ├── srs.md                 Software Requirements Specification
    ├── sdd.md                 Software Design Description
    └── risk-management.md     ISO 14971 / IEC 62304 risk management file
```

**Audience**: Compliance, legal, auditors  
**Regulatory relevance**: All files are directly required or strongly recommended by their respective regulatory regime  
**Minimum required (HIPAA)**: `hipaa/risk-analysis.md`, `hipaa/risk-management.md`, `hipaa/baa-inventory.md`  
**Warning**: All files in `comply/` generated by the skill carry `⚠ REQUIRES HUMAN REVIEW` — they cannot serve as compliance evidence without human sign-off

---

## Dimension 7: agent-context

**Purpose**: Provide AI agents with the synthesized, unambiguous context they need to reason correctly about the system — PHI handling rules, domain context, and hard constraints. This dimension is derived from the other six, not invented independently.

**Target files:**
```
docs/agent-context/
├── AGENTS.md              Primary agent entry point — short, structural, links to below
├── phi-rules.md           PHI handling rules — explicit, unambiguous, no prose padding
├── domain-context.md      Clinical context agents need to reason about system behavior
└── constraints.md         What agents must never do in this system
```

**Audience**: AI agents (primary), developers reviewing agent behavior  
**Regulatory relevance**: Ensures PHI rules from `comply/` and `secure/` propagate to agent instructions  
**Minimum required**: `AGENTS.md`, `phi-rules.md`  
**Note**: Content here is synthesized from `secure/`, `comply/`, and `build/glossary.md`. When those docs change, `agent-context/` should be updated accordingly.

---

## Coverage Assessment Quick Reference

| Dimension | Minimum Required Files | HIPAA Required? |
|---|---|---|
| orient | README.md, domain-model.md | Indirectly (PHI classification) |
| understand | architecture.md, data-flows.md | data-flows.md yes |
| build | CONTRIBUTING.md, testing.md | testing.md PHI data policy |
| operate | deployment.md, breach-notification.md, dr-recovery.md | breach + dr yes |
| secure | auth-model.md, audit-logs.md | Both yes |
| comply | risk-analysis.md, risk-management.md, baa-inventory.md | All three yes |
| agent-context | AGENTS.md, phi-rules.md | No (but enforces HIPAA rules) |
