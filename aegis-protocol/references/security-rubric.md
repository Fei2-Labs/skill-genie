# Security Rubric (Aegis Protocol)

Use this rubric to keep findings high-signal and exploit-focused.

## Scope Gate

Only review code introduced or changed in the current diff.

Do not report:
- Pre-existing issues outside the diff
- Style, maintainability, or performance-only concerns
- Test-only or documentation-only changes

## Confidence Gate

Report only findings with confidence `>= 8/10`.

A finding must include all of the following:
- Concrete vulnerable code path in changed code
- Realistic attacker-controlled input or controllable condition
- Credible exploit path to impact
- Precise file and line reference

If any item is missing, do not report.

## Methodology Mapping Gate

Every finding should include:
- OWASP Top 10:2025 category
- CWE classification
- ATT&CK tactic/technique when applicable

For application control gaps, include ASVS v5 requirement IDs when practical.

If meaningful mapping is not possible, explain why briefly and keep confidence conservative.

## Severity Gate

### High

Use `High` when exploitation can reasonably lead to one of:
- Unauthorized access or privilege escalation
- Sensitive data disclosure at meaningful scale
- Remote code execution or system compromise

### Medium

Use `Medium` when:
- A concrete vulnerability exists
- Impact is meaningful
- Exploitation requires stricter preconditions than High

### Low

Do not report Low severity issues in Aegis output.

## Priority Signal Gate

Add urgency metadata in addition to severity:
- `KEV`: `Yes` if affected CVE/component is in CISA KEV, else `No`
- `SSVC`: `Track`, `Attend`, or `Act`
- `CVSSv4-Lens`: short note on exploitability and impact context

KEV-linked findings should generally receive `SSVC=Act` unless strong compensating controls are proven.

## Vulnerability Categories to Prioritize

- Injection: SQL, NoSQL, command, template, path traversal, XXE
- AuthN/AuthZ failures: bypasses, broken authorization, privilege escalation
- Crypto/secret misuse: hardcoded secrets, weak/incorrect cryptography, trust bypass
- Unsafe execution: unsafe deserialization, eval-like execution, unsafe shell use
- Data exposure: sensitive logging, over-broad responses, PII leaks

## Mandatory False-Positive Exclusions

Do not report standalone findings for:
- DoS/resource exhaustion/rate limiting concerns
- Theoretical race conditions without concrete exploit path
- Pure hardening gaps without direct vulnerability
- Dependency outdatedness (handled by dedicated tooling)
- Client-side-only auth checks as primary findings
- Regex injection/ReDoS by itself

## Exploit Narrative Standard

For each reported finding, articulate:
1. Entry point (how attacker input reaches the code)
2. Trust boundary crossed
3. Security control missing or bypassed
4. Resulting impact

If the narrative is weak or speculative, drop the finding.

## Remediation Standard

Every recommendation must include:
1. Immediate code-level remediation
2. Durable prevention step aligned to SSDF/Secure-by-Design thinking
3. Concrete verification action (test/assertion/check)

## Reporting Standard

Use this format exactly:

```md
# Vuln <N>: <Category>: `<file>:<line>`
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
