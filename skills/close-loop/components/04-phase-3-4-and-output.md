## Phase 3: Review and Apply Improvements

Review the session for actionable findings:

- Skill gap
- Friction
- Missing knowledge
- Automation opportunity

Apply low-risk improvements immediately:

1. Update relevant `CLAUDE.md` or scoped rule files.
2. Save stable insights to memory with confidence labels.
3. Draft skill or hook specs for repetitive patterns.
4. Commit improvement changes separately from feature commits when possible.

If the session is routine with no actionable findings, state: `Nothing to improve`.

## Phase 4: Publish Queue

Scan the session for publishable material:

- Debugging story with clear lesson
- Reusable technical pattern
- Milestone or release-worthy update
- Educational walkthrough

If suitable content exists:

1. Create draft(s) under `Drafts/<slug>/<Platform>.md`.
2. Propose the best first post and schedule spacing for the rest.
3. Do not auto-post unless explicitly requested.

If nothing is suitable, state: `Nothing worth publishing from this session`.

## Output contract

Return two artifacts.

### Artifact A: human-readable report

Sections:

1. `Ship State`
2. `Mode Decision`
3. `Memory Writes`
4. `Findings (applied)`
5. `No action needed`
6. `Publish queue`
7. `Blocked items` (only if any)

Every memory write must include:

- destination
- item text
- confidence (`low`, `medium`, `high`)
- evidence source

### Artifact B: machine-readable JSON

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

Use `assets/templates/wrap-report-template.md` as the default report skeleton.

### KPI tracking

- `noiseRate = rejected_candidates / total_candidates`
- `reuseRate = reused_memories / total_memories_read`
- `correctionRate = corrected_memories / total_writes`
- `memoryPrecision = accepted_writes / total_writes`
- `tokenOverhead = retrievedTokenSize / baselineTokenSize`
- `costPerUsefulWrite = endToEndMemoryCost / accepted_writes`
- `decisionConfidence = margin(selectedStrategy, secondBestStrategy)`

## Guardrails

- Do not claim deployment if no deploy command was run.
- Do not claim push if push was gated.
- Do not create extra summary files unless the user asks.
- Keep edits scoped to requested outcomes.

## Framework alignment

- InfiAgent: infinite-horizon state and cross-session continuity.
- Letta + LangGraph: explicit memory blocks and typed state separation.
- A-MEM: selective memory formation and consolidation.
- Rowboat: event-threaded orchestration and observability.
- AgentSys and A-MemGuard: memory integrity and poisoning defenses.

## Resources

- `references/memory-frameworks.md`
- `assets/templates/wrap-report-template.md`
