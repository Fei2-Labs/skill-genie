# Session Wrap Report Template

Use this template for the final inline wrap-up output.

Mode: `execute` or `dry-run`

## Ship State

- Repos checked:
- Commits created:
- Push status:
- Deploy status:
- File placement fixes:
- Task cleanup actions:

## Memory Evaluation

- Evaluation mode: static/dynamic
- Runs:
- Result: pass/fail
- Success-rate delta:
- Retrieved token size:
- End-to-end memory cost:

## Mode Decision

- Selected strategy input: safe/balanced/openclaw/adaptive
- Selected strategy (canonical): safe/balanced/openclaw
- Decision reason:
- Fallback strategy: safe/balanced/openclaw/adaptive

| Candidate | Utility gain | Risk penalty | Cost penalty | Strategy score |
|---|---|---|---|---|
| safe |  |  |  |  |
| balanced |  |  |  |  |
| openclaw (adaptive alias) |  |  |  |  |

## Archive Update

- Candidate ID:
- Parent ID:
- Decision: promote/hold/reject
- Decision reason:

## Memory Writes

| Destination | Item | Confidence | Evidence source | TTL | Status |
|---|---|---|---|---|---|
|  |  | low/medium/high |  |  | active/needs-review |

## Findings (applied)

1. ✅ Category: 
   Action: 
   Target: 

## No action needed

1. Category: 
   Reason: 

## Publish queue

- Candidate title:
- Platform:
- Draft path:
- Post status:

## KPIs

- Noise rate:
- Reuse rate:
- Correction rate:
- Memory precision:
- Token overhead:
- Cost per useful write:
- Decision confidence:

## Blocked items

- Item:
- Blocker:
- Next action:

## Machine-readable JSON

```json
{
  "mode": "execute|dry-run",
  "selectedStrategyInput": "safe|balanced|openclaw|adaptive",
  "selectedStrategy": "safe|balanced|openclaw",
  "modeSelection": {
    "candidates": [
      {
        "name": "safe|balanced|openclaw|adaptive",
        "utilityGain": 0,
        "riskPenalty": 0,
        "costPenalty": 0,
        "strategyScore": 0
      }
    ],
    "decisionReason": "",
    "fallbackStrategy": "safe|balanced|openclaw|adaptive"
  },
  "shipState": {},
  "memoryEvaluation": {
    "mode": "static|dynamic",
    "runs": 0,
    "result": "pass|fail",
    "metrics": {
      "successRateDelta": 0,
      "retrievedTokenSize": 0,
      "endToEndMemoryCost": 0
    }
  },
  "archiveUpdate": {
    "candidateId": "",
    "parentId": "",
    "decision": "promote|hold|reject",
    "reason": ""
  },
  "memoryWrites": [],
  "findingsApplied": [],
  "noActionNeeded": [],
  "publishQueue": [],
  "blockedItems": [],
  "safety": {
    "sandboxed": true,
    "reflectionRetries": 0
  },
  "kpis": {
    "noiseRate": 0,
    "reuseRate": 0,
    "correctionRate": 0,
    "memoryPrecision": 0,
    "tokenOverhead": 0,
    "costPerUsefulWrite": 0,
    "decisionConfidence": 0
  }
}
```

## Optional appendices

- Risk notes:
- Follow-up checks:
