# Phase-B benchmark calibration package

**Status:** OPT-B **adopted** (`PA-2026-07-31-002`); execution still blocked  
**As of:** 2026-07-31

| Gate | Status |
|---|---|
| `benchmark_design_gate` | **GO** |
| `benchmark_source_gate` | **READY** (DOC-ALT-FNSS-001) |
| `independent_coder_gate` | **NOT_READY** |
| `benchmark_calibration_gate` | **NO_GO** |
| `COMPLETE_PILOT` | **INCOMPLETE** |
| `CORPUS_FREEZE` | **NO_GO** |
| CF-02 access | **NO_GO** (conceptual role only) |

## Operative design (OPT-B)

- **Conceptual source:** CF-02 (Kailes & Enders 2007) — bibliographic / anti-deficit grounding.  
- **Operational L1:** FEMA FNSS November 2010 — `DOC-ALT-FNSS-001` — SHA-256 `ab21f61b…`  
- **Not** a gold standard, positive control, or validation source.  
- Late CF-02 access: RULE-LATE-CF02 in `opt_b_decision_record.md`.

## Next human actions

1. Recruit independent coder; complete COI/confidentiality.  
2. Training + qualification (`independent_coding/`; scorer on synthetic fixtures already green).  
3. Assign `CODER_*` IDs; set manifest `coder_independence_verified=true` only after real pass.  
4. Independent unitization + coding of FNSS; lock raw files.  
5. Reliability + adjudication; resolve BDD-001…005; amend codebook if needed.  
6. Update pilot completion report; only then consider `BENCHMARK_CALIBRATION=COMPLETED`.

## Key files

| Path | Purpose |
|---|---|
| [`opt_b_decision_record.md`](opt_b_decision_record.md) | Adoption decision |
| [`opt_b_red_team_review.md`](opt_b_red_team_review.md) | Objections / mitigations |
| [`../protocol/amendments/PA-2026-07-31-002_operational_fnss_comparator.md`](../protocol/amendments/PA-2026-07-31-002_operational_fnss_comparator.md) | Operative amendment |
| [`independent_coding/`](independent_coding/) | Recruitment / training / qualification |
| `data/phase_b/phase_b_execution_manifest.csv` | Execution readiness (machine) |
