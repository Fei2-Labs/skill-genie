# aegis-protocol

High-confidence code security review workflow for changed code.

## What it does

`aegis-protocol` performs threat-informed security reviews on code changes using modern methodologies (NIST CSF, MITRE ATT&CK, OWASP, SLSA) with strict false-positive filtering and exploit-focused findings.

## When to use

- After making code changes that touch security-sensitive areas
- Before merging PRs that handle auth, payments, data access, or external inputs
- When you want a structured security audit of recent diffs

## Key features

- Threat-informed analysis using MITRE ATT&CK and OWASP Top 10
- Strict false-positive filtering — only reports exploitable findings
- CVSS v4.0 scoring for severity
- SLSA supply-chain verification
- Focuses on changed code, not entire codebase

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
