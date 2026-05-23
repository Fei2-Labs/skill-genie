# Modern Methodologies for Aegis Protocol

Load this reference when a security review needs stronger threat intelligence, prioritization rigor, or supply-chain coverage.

## Framework Stack

### 1) NIST CSF 2.0

Use CSF 2.0 to frame risk context, especially governance and software supply-chain accountability.

Apply in Aegis by:
- Flagging gaps in ownership, policy, and risk acceptance
- Elevating findings that cross critical business functions

### 2) NIST SP 800-218 (SSDF 1.1)

Use SSDF practices to move recommendations from one-off patching to recurring defect prevention.

Apply in Aegis by:
- Requiring root-cause controls in recommendations
- Suggesting engineering process fixes (review gates, secure coding checks, release controls)

### 3) CISA Secure by Design / Secure by Default

Use this lens to push responsibility toward product-side secure defaults, not user-side compensating controls.

Apply in Aegis by:
- Preferring fixes that are safe by default
- Rejecting recommendations that depend on perfect user configuration

### 4) MITRE ATT&CK

Use ATT&CK to describe attacker behavior for exploit narratives.

Apply in Aegis by:
- Mapping each strong finding to tactic/technique when possible
- Using mappings to improve triage and communication with detection teams

### 5) OWASP Top 10:2025 + ASVS v5

Use OWASP Top 10:2025 for broad app-risk classification and ASVS v5 for verification-oriented remediation.

Apply in Aegis by:
- Tagging findings with OWASP category + CWE
- Adding ASVS requirement IDs for actionable control validation

### 6) CISA KEV Catalog

Use KEV to identify vulnerabilities with known exploitation in the wild.

Apply in Aegis by:
- Marking KEV-linked issues as immediate priority
- Escalating remediation timelines for KEV-matched components

### 7) SSVC + CVSS v4

Use SSVC for action-oriented prioritization and CVSS v4 for consistent severity context.

Apply in Aegis by:
- Providing `Track/Attend/Act` recommendation
- Adding a short CVSS v4 lens note for exploit maturity and impact

### 8) SLSA v1.2

Use SLSA when changes touch build pipelines, dependencies, provenance, or release automation.

Apply in Aegis by:
- Checking artifact integrity and provenance expectations
- Flagging trust breaks in CI/CD and dependency ingestion

## Operational Triage Pattern

1. Classify vulnerability type (OWASP + CWE).
2. Prove exploit path (entry, path, bypassed control, impact).
3. Map attacker behavior (ATT&CK).
4. Set urgency (KEV + SSVC + CVSSv4 lens).
5. Recommend immediate patch + durable prevention (SSDF + Secure by Design).

## Minimum Reporting Metadata

For each reported vulnerability include:
- OWASP Top 10:2025 category
- CWE class
- ATT&CK mapping when applicable
- KEV signal (`Yes`/`No`)
- SSVC recommendation (`Track`/`Attend`/`Act`)
- CVSS v4 short context note

