# Healthcare Regulatory Review Report

**Skill**: `health-regulatory-review`
**Date**: 2026-03-15
**Auditor**: AI-assisted engineering review
**Target**: MedConnect Patient Portal — v2.4.1

> This report is an engineering review, not legal advice, certification, or a formal HIPAA compliance determination.

---

## Executive Summary

MedConnect Patient Portal is a Node.js + React application that allows patients to view appointments, lab results, medication lists, and message their care team. The system creates, receives, maintains, and transmits ePHI across a PostgreSQL database, Redis cache, S3 document storage, and several third-party integrations.

The review identified **19 findings** across 9 of 11 control areas. **3 critical** findings relate to PHI leaking into application logs, missing server-side authorization on patient-scoped API routes, and unredacted clinical data sent to an external error-tracking service. **5 high-severity** findings cover overly broad API responses, missing audit trails for document downloads, and production data in test fixtures.

The codebase demonstrates reasonable attention to transport security and authentication but has significant gaps in data minimization, audit logging, and third-party disclosure boundaries.

---

## In-Scope Components and Sensitive-Data Assumptions

| Component | PHI Present | Notes |
| --- | --- | --- |
| `api/` (Express routes) | Yes | Patient demographics, appointments, labs, medications, messages |
| `models/` (Sequelize) | Yes | Patient, Encounter, Observation, DocumentReference, Message |
| `workers/` (Bull queue jobs) | Yes | Lab result import, appointment sync, message notification |
| `lib/integrations/` | Yes | EHR FHIR adapter, Twilio SMS, SendGrid email |
| `frontend/` (React) | Yes | Renders patient-facing clinical data |
| Redis cache | Likely | Session data; patient search results cached with TTL |
| S3 (`medconnect-docs`) | Yes | Clinical documents, lab PDFs, scanned records |
| Sentry (error tracking) | Likely | Receives unfiltered request/response context |
| Mixpanel (analytics) | Uncertain | Event tracking; payload contents not clearly scoped |

---

## Findings

| ID | Severity | Category | Affected Area | Evidence | Risk | Remediation Direction | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H-01 | Critical | 6. Transmission and Storage Security | `lib/logger.js` | Request body is logged at `debug` level with no field filtering. Patient names, DOBs, SSNs, and clinical text appear in CloudWatch when debug is enabled. | PHI disclosed to log aggregation systems; broad access to logs exposes ePHI beyond minimum necessary. | Implement structured log filtering to strip or mask PHI fields before emission. | Confirmed |
| H-02 | Critical | 3. Access Control | `api/routes/patients.js` | `GET /api/patients/:id/labs` checks authentication but does not verify the authenticated user owns or is authorized for the requested patient ID. Any authenticated patient can retrieve another patient's lab results by changing the URL parameter. | Unauthorized disclosure of ePHI; broken object-level authorization. | Add patient-scoped authorization middleware that verifies the authenticated user's relationship to the requested patient resource. | Confirmed |
| H-03 | Critical | 9. Third-Party Services | `lib/integrations/sentry.js` | Sentry `beforeSend` hook is configured but does not redact `request.data`. Full POST bodies from patient-facing endpoints — including demographics, clinical notes, and medication lists — are transmitted to Sentry's cloud infrastructure. | PHI disclosed to a third-party processor without evidence of BAA, redaction, or boundary controls. | Filter or redact request and response bodies in the Sentry `beforeSend` hook; confirm BAA coverage. | Confirmed |
| H-04 | High | 2. Minimum Necessary | `api/routes/patients.js` | `GET /api/patients/:id` returns the full Patient model including SSN, emergency contacts, insurance details, and clinical notes. The frontend patient header only renders name, DOB, MRN, and photo. | Overly broad API response; excess ePHI transmitted to the client increases exposure surface. | Return purpose-scoped DTOs; move sensitive fields to dedicated endpoints with stricter access. | Confirmed |
| H-05 | High | 4. Audit Controls | `api/routes/documents.js` | `GET /api/patients/:id/documents/:docId/download` streams files directly from S3. No audit log entry is created for document access. | Patient document access is invisible to audit review; no evidence trail for disclosure tracking. | Log document access events with actor, patient, document ID, timestamp, and outcome. | Confirmed |
| H-06 | High | 4. Audit Controls | `models/patient.js` | Sequelize `beforeUpdate` hook writes changes to an `audit_log` table but does not capture the acting user. The `userId` column is nullable and most rows contain `NULL`. | Audit entries cannot be attributed to a specific actor; weakens investigation and accounting of disclosures. | Pass authenticated user context through to the model layer and enforce non-null actor on audit writes. | Confirmed |
| H-07 | High | 8. De-identification | `tests/fixtures/patients.json` | Test fixture file contains 14 patient records with realistic names, valid-format SSNs, dates of birth, and clinical notes labeled "copied from staging 2025-11-02" in a comment. | Test data derived from real or realistic patient data; risk of re-identification and inappropriate disclosure in CI logs or developer machines. | Replace with synthetic data generated from a faker library; remove staging-derived fixtures. | Confirmed |
| H-08 | High | 1. Sensitive-Data Inventory | `workers/lab-import.js` | Lab results from the upstream EHR FHIR endpoint are deserialized into a generic `metadata` JSONB column on the `observations` table. The same column is used for non-clinical feature flags and UI preferences. | PHI mixed into an untyped shared field; difficult to apply scoped access, audit, retention, or encryption rules. | Store clinical observations in a dedicated, typed structure separate from non-clinical metadata. | Confirmed |
| H-09 | Medium | 6. Transmission and Storage Security | `lib/integrations/twilio.js` | SMS notifications include appointment date, provider name, and clinic location in the message body. No option to send a minimal "You have a new message" notification instead. | PHI-adjacent data transmitted via SMS, which is not encrypted end-to-end; content visible on lock screens and carrier logs. | Reduce SMS content to a generic notification with a link to the secure portal for details. | Confirmed |
| H-10 | Medium | 3. Access Control | `api/middleware/auth.js` | Admin role check (`req.user.role === 'admin'`) grants unrestricted access to all patient data. No scoping to department, care team, or facility. | Admin users can access any patient record without clinical relationship; violates minimum necessary for role-based access. | Implement scoped admin access tied to organizational unit or care team context. | Confirmed |
| H-11 | Medium | 5. Integrity | `workers/appointment-sync.js` | Appointment records received from the upstream EHR are upserted without integrity validation. No checksum, signature, or version comparison is performed. | Corrupted or tampered appointment data could overwrite valid records without detection. | Validate inbound payloads against expected schema and version; log discrepancies. | Likely |
| H-12 | Medium | 10. Retention and Deletion | `api/routes/patients.js` | `DELETE /api/patients/:id` soft-deletes the patient row (`deleted_at` timestamp) but does not cascade to S3 documents, Redis cache entries, or the `audit_log` table. | Patient data persists in derived stores after deletion; no credible full-purge path. | Implement cascading cleanup across all stores or document the retention rationale. | Confirmed |
| H-13 | Medium | 7. Secrets and Keys | `.env.example` | Contains `FHIR_CLIENT_SECRET=sk_live_abc123...` value that appears to be a live credential, not a placeholder. | Live secret in version control; anyone with repo access can authenticate to the ePHI-bearing FHIR endpoint. | Rotate the credential immediately; replace with a placeholder value. | Confirmed |
| H-14 | Medium | 9. Third-Party Services | `lib/integrations/mixpanel.js` | Mixpanel `track()` calls include `patientId` and `appointmentType` as event properties. No documentation of what Mixpanel receives or whether a BAA is in place. | Patient identifiers disclosed to analytics vendor; scope and boundary unclear. | Audit all Mixpanel event properties; remove or pseudonymize patient identifiers; confirm BAA if PHI is intentional. | Likely |
| H-15 | Medium | 2. Minimum Necessary | `api/routes/messages.js` | `GET /api/messages` returns full message threads including clinical content for all care team conversations. The inbox view only displays sender, subject, and timestamp. | Excess clinical text transmitted to the client on every inbox load. | Return a summary DTO for the inbox list; load full message content only when a thread is opened. | Confirmed |
| H-16 | Low | 11. Addressable Safeguards | `config/session.js` | Session TTL is set to 24 hours (`maxAge: 86400000`). No idle timeout or re-authentication prompt is configured. | Long session lifetime increases risk window if a device is left unattended in a clinical setting. | Implement idle timeout with re-authentication; consider shorter active session duration. | Confirmed |
| H-17 | Low | 4. Audit Controls | `api/routes/messages.js` | Patient message reads are not logged. Only message creation triggers an audit entry. | Read access to care team messages containing clinical content is not traceable. | Log message read events with actor and timestamp. | Confirmed |
| H-18 | Low | 6. Transmission and Storage Security | `config/redis.js` | Redis connection does not enable TLS (`tls: undefined`). Redis is assumed to be on a private network, but no configuration enforces this. | If Redis is reachable beyond the private network, cached session and patient data could be intercepted. | Enable TLS for Redis connections; verify network isolation. | Likely |
| H-19 | Low | 1. Sensitive-Data Inventory | `models/` | No schema-level annotation distinguishes PHI fields from non-PHI fields across models. | Makes it difficult to systematically apply encryption, masking, audit, or retention rules to sensitive fields. | Annotate or tag PHI fields in the schema to enable automated policy enforcement. | Confirmed |

---

## Coverage Matrix

| Control Area | Status |
| --- | --- |
| 1. Sensitive-Data Inventory and Scope | Partial |
| 2. Minimum Necessary and Data Minimization | Not Met |
| 3. Access Control, Identity, and Authorization | Not Met |
| 4. Audit Controls and Traceability | Not Met |
| 5. Integrity and Change Protection | Partial |
| 6. Transmission and Storage Security | Partial |
| 7. Secrets, Keys, and Boundary Separation | Not Met |
| 8. De-identification, Test Data, and Re-identification Risk | Not Met |
| 9. Third-Party Services and Business Associate Boundaries | Not Met |
| 10. Retention, Deletion, and Disposal Signals | Not Met |
| 11. Addressable Safeguards and Documentation | Partial |

---

## Open Questions and Non-Code Dependencies

1. **BAA coverage**: Are Business Associate Agreements in place with Sentry, Mixpanel, Twilio, and SendGrid? Code review cannot determine this.
2. **Network isolation**: Is the Redis instance on a VPC-isolated subnet with no public ingress? Deployment configuration was not in scope.
3. **Encryption at rest**: Is PostgreSQL configured with storage-level encryption? No application-level encryption was observed, but infrastructure-level controls may exist.
4. **Workforce training**: Are staff trained on minimum necessary access and PHI handling? This is outside code review scope.
5. **Incident response**: Is there a documented breach notification process? No evidence in the codebase.
6. **S3 bucket policy**: Is `medconnect-docs` configured with private-only access and server-side encryption? Bucket policy was not available for review.

---

## Source Basis

- HHS, "Summary of the HIPAA Security Rule" — https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html
- HHS FAQ, "Minimum Necessary" — https://www.hhs.gov/hipaa/for-professionals/faq/207/how-are-covered-entities-to-determine-what-is-minimum-necessary/index.html
- NIST SP 800-66r2, "Implementing the HIPAA Security Rule: A Cybersecurity Resource Guide"
- 45 CFR § 164.312 — Technical Safeguards
- 45 CFR § 164.530(j) — Retention of documentation
- `references/control-areas.md` — audit baseline used for this review
