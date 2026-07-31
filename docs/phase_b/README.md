# Phase-B benchmark calibration package

**Status:** OPT-B **adopted**; qualification freeze **AUTHORIZED**; execution blocked on real coder  
**As of:** 2026-07-31

| Gate | Status |
|---|---|
| `benchmark_design_gate` | **GO** |
| `benchmark_source_gate` | **READY** (DOC-ALT-FNSS-001) |
| Coder workflow infrastructure | **READY** |
| Qualification freeze | **AUTHORIZED** (`QUAL-FREEZE-v1`) |
| Attempt policy | **ADOPTED** (`QUAL-ATTEMPT-v1`) |
| `independent_coder_gate` | **NOT_READY** (no real coder) |
| Target package | **SEALED** |
| `benchmark_calibration_gate` | **NO_GO** |
| `COMPLETE_PILOT` | **INCOMPLETE** |
| `CORPUS_FREEZE` | **NO_GO** |
| CF-02 access | **NO_GO** (conceptual role only) |

## Operative design (OPT-B)

- **Conceptual source:** CF-02 (Kailes & Enders 2007) — bibliographic / anti-deficit grounding.  
- **Operational L1:** FEMA FNSS November 2010 — `DOC-ALT-FNSS-001` — SHA-256 `ab21f61b…`  
- **Not** a gold standard, positive control, or validation source.  
- Late CF-02 access: RULE-LATE-CF02 in `opt_b_decision_record.md`.

## Only remaining operational prerequisite for calibration

Successful recruitment and qualification of a **real** independent coder (UCW-003 resolved; recruit by direct contact).

## Next human actions

See [`next_human_actions.md`](next_human_actions.md).

## Key files

| Path | Purpose |
|---|---|
| [`opt_b_decision_record.md`](opt_b_decision_record.md) | Adoption decision |
| [`independent_coding/`](independent_coding/) | Recruitment / training / qualification |
| [`independent_coding/attempt_policy.md`](independent_coding/attempt_policy.md) | Adopted attempt policy |
| `data/phase_b/qualification_freeze_record.csv` | Frozen checksums |
| `data/phase_b/phase_b_execution_manifest.csv` | Execution readiness (machine) |
