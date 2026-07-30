# Security and research-integrity red team (coder workflow)

| # | Risk | Severity | Mitigation | Residual blocker? |
|---|---|---|---|---|
| 1 | Target text leaked into training | High | Overlap checker; package forbidden-file scan | No if checks green |
| 2 | Answer-key in coder pack | High | ADMIN_ONLY path; generator excludes reference CSV | No |
| 3 | Coder PII in public git | High | `private/coder_admin/` gitignored; validators scan | No |
| 4 | Independence pressure | High | COI + READY criteria; no PI-as-sole-coder claim | Process risk — human |
| 5 | Post-hoc threshold change | High | Freeze record + checksum; validator | UCW-001 until attempt policy adopted |
| 6 | Selective qualification reporting | Med | Locked hashed submissions; attempt log | Human |
| 7 | Unlimited retakes | High | Draft max 2 attempts; blocked until adopted | **UCW-001 blocker** |
| 8 | Shared-sheet contamination | High | Separate coder files; lock before adjudication | Human at execution |
| 9 | Premature adjudication | High | Gate order validators | No |
| 10 | Reliability after harmonization | High | Pre-adjudication-only rule in reliability docs | No |
| 11 | Expected-result cues in training | High | Training guide forbids directional RQ4 | Review on pack generate |
| 12 | Gold-standard drift | High | Existing Phase-B validators | No |
| 13 | CF-02 restored as operational L1 | High | Role validators | No |
| 14 | Unauthorized redistribution | Med | Confidentiality agreement | Human |
| 15 | Hidden metadata / NFS / PDF staging | Med | gitignore `*.pdf`; release-check | Ops hygiene |

**Open blocker:** `UCW-001` attempt-policy adoption required before real qualification.
