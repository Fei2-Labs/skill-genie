---
name: aegis-protocol
description: High-confidence code security review workflow for changed code, using modern threat-informed methodologies with strict false-positive filtering and exploit-focused findings.
license: MIT
metadata:
  version: 1.1.0
  references:
    - https://github.com/anthropics/claude-code-security-review
    - https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
    - https://csrc.nist.gov/pubs/sp/800/218/final
    - https://www.cisa.gov/resources-tools/resources/secure-by-design
    - https://attack.mitre.org/
    - https://owasp.org/www-project-application-security-verification-standard/
    - https://owasp.org/Top10/2025/
    - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
    - https://www.cisa.gov/stakeholder-specific-vulnerability-categorization-ssvc
    - https://www.first.org/cvss/v4.0/specification-document
    - https://slsa.dev/spec/v1.2/
---

# Aegis Protocol

Security review skill for changed code only. This workflow is tuned for high-confidence findings, low noise, and modern attacker-informed prioritization.

## Use when

- User asks for security review of a PR, branch, or diff.
- You need exploit-focused findings, not a general code review.
- You must filter speculative issues before reporting.

## Do not use when

- The request is a full quality review (use regular code review workflow).
- The target has no meaningful code changes yet.

## Inputs

- Git base reference (default `origin/HEAD`)
- Changed files and diff
- Optional runtime architecture and trust boundaries
- Optional custom security policies

## Workflow

### Phase 1: Collect change scope

Run:

```bash
git status
git diff --name-only origin/HEAD...
git log --no-decorate origin/HEAD...
git diff --merge-base origin/HEAD
```

Rules:
- Review only newly introduced security risk in changed code.
- Ignore pre-existing vulnerabilities outside the change scope.
- Prioritize server, auth, crypto, data-access, deserialization, and command execution paths.

### Phase 2: Threat context (modern methodology layer)

For each changed security-relevant path:
- Identify attacker-controlled inputs, trust boundaries, and privilege transitions.
- Map likely attacker behavior to MITRE ATT&CK tactics/techniques when possible.
- Tag weakness classes using OWASP Top 10:2025 and CWE terminology.
- For application control gaps, map to OWASP ASVS v5 requirement IDs when practical.
- For build/dependency/provenance changes, check supply-chain risk using SLSA and existing CI trust assumptions.

Then inspect repository context:
- Existing validation and sanitization patterns
- Existing auth and permission boundaries
- Existing secret management conventions
- Existing secure build and release practices

Look for concrete vulnerabilities in changed code:
- Injection: SQL, command, template, NoSQL, path traversal, XXE
- AuthZ/AuthN: bypasses, privilege escalation, broken session checks
- Crypto/secrets: hardcoded secrets, weak algorithms, cert validation bypass
- Code execution: unsafe deserialization, eval-like execution, unsafe shell execution
- Data exposure: sensitive logging, over-broad API responses, PII leaks
- Supply chain: unsigned/unverified artifacts, unsafe dependency ingestion, provenance gaps

### Phase 3: Exploitability proof gate

A candidate vulnerability must include all of:
- Entry point attacker can influence
- Reachable vulnerable operation in changed code
- Missing or bypassed security control
- Credible impact path

If any element is missing, do not report.

### Phase 4: Prioritization layer

Use High/Medium severity only, then enrich urgency using:
- KEV signal: If affected component/CVE is in CISA KEV, prioritize immediate remediation.
- SSVC action framing: `Track`, `Attend`, or `Act` to guide operational urgency.
- CVSS v4 lens: Include Base + Threat thinking where exploit maturity is known.

These signals improve prioritization only; they do not override confidence policy.

### Phase 5: False-positive filter (mandatory)

Hard exclusions:
- DOS/resource exhaustion/rate limiting concerns
- Theoretical race conditions without concrete exploit path
- Pure hardening gaps without concrete vulnerability
- Dependency outdatedness findings handled by other tooling
- Test-only files and documentation files
- Client-side-only auth checks as a primary finding
- Regex injection/ReDoS as standalone report

Confidence policy:
- Report only findings with confidence `>= 8/10`
- Prefer missing weak findings over reporting noisy findings

### Phase 6: Remediation quality gate

For each finding, provide:
- Immediate code-level fix
- Durable prevention recommendation tied to SSDF/Secure-by-Design mindset
- Concrete verification step (test/assertion/check)

## Output format

Return markdown findings only, one section per issue:

```md
# Vuln 1: <Category>: `<file>:<line>`
* Severity: High|Medium
* Confidence: 8-10
* Methodology Mapping: ATT&CK (if applicable), OWASP Top 10:2025, CWE, ASVS v5 (if applicable)
* Priority Signal: KEV=<Yes|No>; SSVC=<Track|Attend|Act>; CVSSv4-Lens=<short note>
* Description: Concrete vulnerability summary
* Exploit Scenario: Specific attack path
* Recommendation: Practical fix in this codebase
* Verification: Specific way to validate the fix
```

If no qualifying findings:

```md
No high-confidence security vulnerabilities found in the reviewed changes.
```

## Severity policy

- High: exploitable for unauthorized access, data breach, system compromise
- Medium: concrete vulnerability with meaningful impact but stricter conditions
- Low: do not report

## Quick prompts

- `Run Aegis Protocol on current branch vs origin/HEAD`
- `Security-review this PR diff with confidence >= 8 only`
- `Audit changed files for auth bypass, injection, and data exposure only`
- `Run Aegis with ATT&CK/OWASP/CWE mapping and SSVC-style priority signals`

## Anti-patterns

- Reporting speculative vulnerabilities without exploit path
- Reviewing the entire repository when only diff review is requested
- Mixing style/performance feedback into security results
- Emitting findings without precise file and line references

## Reference

- Anthropic reference workflow: `anthropics/claude-code-security-review`
- Local note: `references/security-rubric.md`
- Modern methodology map: `references/modern-methodologies.md`
