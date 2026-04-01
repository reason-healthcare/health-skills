# HIPAA, PHI, and PII Audit Baseline

Use this reference to drive report-only code and configuration audits for healthcare systems.

## Scope Notes

- This baseline is for engineering review, not legal advice or a formal HIPAA certification.
- Code review can surface likely HIPAA, PHI, and PII gaps, but it usually cannot prove workforce training, sanctions, physical safeguards, or full policy compliance.
- Focus on evidence in code, configuration, deployment defaults, logs, data flows, tests, and integrated services.
- Treat PII as a broader privacy category than HIPAA PHI. If sensitive personal data is present, report it even when HIPAA applicability is uncertain.

## Control Areas

### 1. Sensitive-Data Inventory and Scope

Review for whether the system clearly identifies where PHI, ePHI, and sensitive PII are created, received, maintained, transmitted, or exported.

Flag when:

- sensitive fields are mixed into generic JSON blobs or untyped metadata
- upload, import, export, or sync paths move personal data without clear classification
- search indexes, caches, queues, or backups appear to copy patient or member data without explicit handling rules

Example findings:

- `patient_notes` and diagnosis values are serialized into a generic `metadata` field used across unrelated services
- a background export job emits full patient records instead of a smaller purpose-specific payload

### 2. Minimum Necessary and Data Minimization

Review for whether endpoints, jobs, admin tools, and integrations use or disclose only the information reasonably needed for the purpose.

Flag when:

- endpoints return full patient or member objects where a subset would satisfy the use case
- logs, analytics, or support tools receive full request or response payloads with unnecessary identifiers
- admin or reporting queries expose diagnosis, notes, or identifiers by default

Example findings:

- a search endpoint returns date of birth, diagnosis, and full address when the UI only needs name and appointment status
- error tracking receives full webhook payloads with patient identifiers and clinical text

### 3. Access Control, Identity, and Authorization

Review for whether only authorized users and services can access ePHI and whether the implementation ties access to distinct identities and resource-level checks.

Flag when:

- role checks exist only in the UI and not at the API or job layer
- shared service accounts or broad admin bypasses make actions hard to attribute to one actor
- multi-tenant or patient-scoped access checks are absent, inconsistent, or easy to bypass

Example findings:

- a staff-only page hides controls in the frontend, but the underlying route lacks a server-side role check
- a background worker reads all patient rows with a shared credential instead of a scoped service identity

### 4. Audit Controls and Traceability

Review for whether the system records and can examine access to systems containing ePHI, especially reads, changes, exports, and disclosures.

Flag when:

- read access to patient charts, documents, or exports is not logged
- logs omit actor, action, target record, timestamp, or outcome
- audit trails can be disabled, overwritten, or are mixed with ordinary debug logs

Example findings:

- file downloads are served directly from storage without a durable access log
- patient record edits are logged without the user ID that triggered the change

### 5. Integrity and Change Protection

Review for whether ePHI can be improperly altered or destroyed without detection and whether sensitive changes carry provenance.

Flag when:

- direct database updates bypass audit history or provenance fields
- file or message processing lacks integrity checks for sensitive payloads
- records can be overwritten without versioning, before or after values, or actor context

Example findings:

- a migration script rewrites clinical values in place with no audit trail
- inbound clinical documents are processed from a queue without any signature, checksum, or provenance validation

### 6. Transmission and Storage Security

Review for whether the implementation guards against unauthorized access to ePHI in transit and whether storage protections are explicit enough to support a reasonable safeguard determination.

Flag when:

- PHI appears in URLs, query strings, email bodies, cookies, local temp files, or public object storage paths
- transport security is absent, optional, or unclear for internal or external service calls that carry PHI
- sensitive storage, cache, backup, or export paths appear unencrypted or their protection is undocumented

Example findings:

- patient identifiers and visit details are embedded in webhook query parameters
- support bundles write raw patient payloads to temporary disk files with no cleanup evidence

### 7. Secrets, Keys, and Boundary Separation

Review for whether credentials, API tokens, signing keys, and decryption material are handled separately from the data they protect.

Flag when:

- secrets are hardcoded in source, tests, images, or environment samples
- encryption keys are stored beside the encrypted payloads with the same access boundary
- debug tools or admin pages expose tokens, connection strings, or decrypted payloads

Example findings:

- a checked-in `.env.example` contains live integration tokens for a PHI-bearing service
- the same storage location contains encrypted files and the application-managed keys used to decrypt them

### 8. De-identification, Test Data, and Re-identification Risk

Review for whether data described as anonymous, synthetic, or safe for lower environments still contains identifiers or combinations that can identify a person.

Flag when:

- production snapshots or support exports are reused in development or tests
- "de-identified" datasets retain dates, ZIP codes, images, device IDs, or free text that can identify a patient
- deterministic hashes or reversible transforms stand in for direct identifiers without a re-identification analysis

Example findings:

- integration tests use real appointment payloads copied from production incidents
- a dataset labeled anonymous still includes full dates, postal codes, and clinician notes

### 9. Third-Party Services, External Disclosures, and Business Associate Boundaries

Review for where PHI or adjacent PII leaves the primary trust boundary and whether vendor usage appears intentional and controlled.

Flag when:

- analytics, chat, AI, error tracking, or support SaaS receives PHI-bearing payloads
- webhook, email, or messaging integrations send more sensitive data than required
- the code depends on vendors that may create, receive, maintain, or transmit PHI, but the boundary and safeguard assumptions are unclear

Example findings:

- a tracing SDK captures full request bodies for patient-facing endpoints
- an LLM integration forwards raw clinical notes to an external API without redaction or documented boundary controls

### 10. Retention, Deletion, and Disposal Signals

Review for whether the code shows a credible path to retain, delete, purge, or sanitize sensitive data across primary and derived stores.

Flag when:

- soft deletes hide records in the app but retain data indefinitely in primary or derived stores
- caches, exports, search indexes, and object storage copies have no purge path
- temporary files, reusable disks, or snapshots may retain retrievable sensitive data

Example findings:

- deleting a patient record removes only the row while leaving documents and exports in object storage
- attachment processing writes files to `/tmp` with no visible cleanup or retention rule

### 11. Addressable Safeguards, Documentation, and Risk Management Evidence

Review for whether code and configuration reflect reasoned safeguard choices or documented alternatives when direct implementation is absent.

Flag when:

- encryption, auto logoff, or other safeguard-related features are missing with no documented alternative or rationale
- security toggles disable controls in production-like paths without an explicit justification
- the implementation depends on unstated policy or manual process to close obvious technical gaps

Example findings:

- database encryption is described as handled elsewhere, but the repository contains no deployment evidence or documented alternative
- an environment flag disables audit logging for performance and no compensating control is visible

## Report Expectations

For each finding, include:

- finding ID
- severity
- control area
- affected code path, component, or integration
- direct evidence
- risk explanation
- suggested remediation direction without changing code
- confidence level and open assumptions

## Source Basis

Use these authoritative sources when grounding the review:

- HHS, "Summary of the HIPAA Security Rule"
  - https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html
  - Use for confidentiality, integrity, availability, technical safeguards, required vs. addressable specifications, and business associate agreement references.
- HHS FAQ, "How are covered entities expected to determine what is the minimum necessary information..."
  - https://www.hhs.gov/hipaa/for-professionals/faq/207/how-are-covered-entities-to-determine-what-is-minimum-necessary/index.html
  - Use for minimum necessary and reasonableness-based disclosure limits.
- HHS, "Methods for De-identification of PHI"
  - https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html
  - Use for safe harbor, expert determination, and re-identification caution.
- HHS, "Business Associates"
  - https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html
  - Use when third-party vendors create, receive, maintain, or transmit PHI on behalf of a covered entity or business associate.
- HHS, "Guidance to Render Unsecured Protected Health Information Unusable, Unreadable, or Indecipherable..."
  - https://www.hhs.gov/hipaa/for-professionals/breach-notification/guidance/index.html
  - Use for encryption and media sanitization examples tied to breach-risk reduction.
- NIST SP 800-122, "Guide to Protecting the Confidentiality of Personally Identifiable Information (PII)"
  - https://csrc.nist.gov/pubs/sp/800/122/final
  - Use for broader PII handling expectations and risk-based protection of personal data.
