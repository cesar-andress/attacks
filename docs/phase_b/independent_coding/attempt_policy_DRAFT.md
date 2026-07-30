# Qualification attempt and retraining policy — DRAFT

**Policy ID:** `QUAL-ATTEMPT-DRAFT-v1`  
**Status:** `DRAFT_PENDING_HUMAN_ADOPTION`  
**Effect:** Blocks qualification freeze authorization and `INDEPENDENT_CODER=READY` until adopted (see `data/phase_b/unresolved_coder_workflow_items.csv` item `UCW-001`).

This draft is conservative. Do not treat it as adopted merely because it exists in the repository.

## Proposed rules (pending adoption)

| Topic | Proposed rule |
|---|---|
| Maximum attempts | **2** (initial + one retrain attempt) |
| Minimum interval | ≥7 days after fail notification, unless technical invalidation |
| Same cases reused? | **No** for attempt 2 — requires `QUAL-SET-v2` alternate form **or** explicit human amendment allowing reuse |
| Answer explanations after fail | Process feedback only; **no** full answer-key study before a retake of the same set |
| Contamination | Failed attempt on SET-v1 contaminates SET-v1 for that person; retake needs alternate set or adopted exception |
| New forms | Material COI change or >90 days idle → new COI/confidentiality |
| Invalid attempts | Malformed CSV, missing cases, or identity mismatch → `QUALIFICATION_INVALID` (does not consume attempt if technical) |
| Technical failures | PI may authorize resubmission without consuming attempt |
| Withdrawal | Coder may withdraw anytime; submitted locked files remain archived under opaque ID |

## Adoption checklist (human)

- [ ] PI adopts or revises this draft  
- [ ] Version ID assigned (e.g. `QUAL-ATTEMPT-v1`)  
- [ ] Checksum recorded in freeze record  
- [ ] UCW-001 closed  

Until then: **no real qualification attempt is authorized.**
