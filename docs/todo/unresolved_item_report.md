# Unresolved-item report (human-readable)

**Generated:** 2026-07-31  
**Public HEAD baseline:** `c06fd76` (v0.4.0) prior to this sprint  
**Machine register:** `unresolved_item_register.csv`

## Summary counts (register rows)

| Bucket | Count (approx.) |
|---|---|
| Total registered items | 33 |
| Resolved in Sprint 1 | 9 |
| Blocked (active) | 18 |
| Intentional placeholders | 5 |
| Validation/build tooling | 2 |

Exact machine counts come from the CSV `current_status` / `category` columns.

## Immediate methodological blockers (P0/P1)

| ID | Priority | Gate | Condition to resolve |
|---|---|---|---|
| TODO-SRC-001 | P0 | `complete_pilot_source_gate` | Authorized CF-02 / CMIST L1 full text + checksum, or formal amendment |
| TODO-SRC-002 | P0 | `benchmark_calibration_gate` | Pin operative L1 after access/amendment |
| TODO-FRZ-001 | P0 | `corpus_freeze_gate` | Clear freeze register after complete pilot |
| TODO-PIL-001 | P0 | `complete_pilot_source_gate` | Phase B after CF-02 |
| TODO-COD-001 | P0 | `full_coding_gate` | Freeze + prereg before main coding |
| TODO-SRC-003 | P1 | `corpus_freeze_gate` | CF-15 supersession decision |
| TODO-PIL-002 | P1 | independent coding | ≥2 independent human coders; pre-consensus α |
| TODO-PRE-001 | P1 | preregistration | Real registry ID (never invent) |

## Manuscript blockers (P2)

Corpus N, prereg ID, Results/Discussion/Conclusion shells (TODO-MAN-001–006, 008, 014–017). Reader-safe controlled wording is used in the private manuscript until gates clear; numeric insertion remains editorial.

## First-release blockers

**v0.1.0 / current methodological pre-release (v0.4.0 lineage):** May ship with documented blockers if no false completeness claims. P0 source/freeze items must remain transparent, not deleted.

**v0.2.0 experimental pack:** Already released as synthetic pack; human execution not required for pack validity.

## Future-programme / experiment-pack items (P3)

TODO-EXP-001/002 — ethics then EXP-01–04 priority; SLAPA field work later.

## Resolved in this sprint (evidence in commits)

| ID | Resolution |
|---|---|
| TODO-MAN-007 | Eligibility aligned to operative `corpus_selection.md` draft; freeze still pending |
| TODO-MAN-009 | Highest ordinal depth = codebook E1 |
| TODO-MAN-010 / TODO-PRO-002 | Small corpus ≤15 L1 and ≤250 PEs → 100% double-coding |
| TODO-MAN-011 / TODO-PRO-001 | Krippendorff (2018) Content Analysis 4th ed. |
| TODO-MAN-012 | Swain & Guttmann (1983) THERP NUREG/CR-1278 |
| TODO-MAN-013 | FEMA (2010) FNSS guidance (+ Kailes & Enders 2007); does **not** unlock CF-02 coding |
| TODO-VAL-001 | `validate_todos` + allowlist |
| TODO-BLD-001 | Development vs submission-ready manuscript modes |
| TODO-REL-001 | CITATION.cff already at 0.4.0 |

## Views

See also: `resolution_sprint_plan.md`, `release_implications.md`, `preregistration_readiness_matrix.md`, `citation_completion_audit.md`.
