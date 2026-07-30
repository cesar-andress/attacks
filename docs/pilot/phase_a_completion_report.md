# Phase A completion report — operational codebook pilot

**Date:** 2026-07-31  
**Amendment:** PA-2026-07-31-001  
**Labels:** `NOT_FOR_SUBSTANTIVE_INFERENCE` · `NOT_FOR_BENCHMARK_COMPARISON` · `PROTOCOL_DEVELOPMENT_ONLY`

## Gate outcomes

| Gate | Status |
|---|---|
| OPERATIONAL_PILOT | **COMPLETED** |
| BENCHMARK_CALIBRATION | **NO_GO** |
| COMPLETE_PILOT | **INCOMPLETE** |
| CORPUS_FREEZE | **NO_GO** |
| FULL_CODING | **NO_GO** |

Complete-pilot source gate remains **`PILOT_SOURCE_NO_GO`** (P5/CF-02).

## Sample

- **operational_pilot_sample:** P1/CF-16, P2/CF-03, P3/CF-15, P4/CF-13  
- **benchmark_calibration_sample:** P5/CF-02 (not coded)  
- **PE count:** 29 (target 20–32)  
- **Selection rule:** recorded in `phase_a_sampling_plan.md` before treating coding as complete  

## Coding procedure

1. Unitization with location + short public stems; full short excerpts gitignored under `local_sources/pilot_coding/`.  
2. Primary human coding (`coder_A`) on all Phase A PEs.  
3. `simulated_procedural_second_pass` (not an independent second human coder).  
4. Adjudication retaining coder_A values; disagreements logged without rule-chasing agreement.  
5. Schema/coding validation + pilot-phase validation.

## Independence / reliability boundary

- Independent human coder pairs: **0** (only one primary human pass).  
- **No** Krippendorff’s α / empirical intercoder reliability reported.  
- Disagreement counts are **procedural usability** signals only.  
- Reliability policy v0.1 unchanged; empirical reliability **must be repeated after Phase B** when independent double-coding of the complete pilot (including P5) is feasible.

## Disagreement summary (procedural)

| Type (examples) | Role |
|---|---|
| ladder ambiguity | rung 1/4/5 for drills, REX, illustrations |
| codebook gap | generic inclusivity vs named support; capacidades language |
| explicit-versus-entailed confusion | inhibitory acoustic from LOCKDOWN/HIDE |
| locus ambiguity | setting vs subgroup vs not_specified |
| benchmark-dependent | PAI/attention; comparator-sensitive supports |
| document-level vs PE-level | BTAM descriptive text (Branch B out of scope) |

See `data/pilot/disagreement_log.csv`.

## Codebook / protocol amendments

See `data/pilot/amendment_log.csv`. Distinctions:

- **operationally_resolved** (usable for further Phase A development)  
- **benchmark_dependent / provisional** (must not finalize without P5)  
- **unresolved_for_freeze** (CF-15 supersession note)

## What Phase A does **not** claim

- Study reliability acceptable  
- Instrument validated  
- Benchmark comparison  
- Corpus prevalence or framework ranking  
- Freeze readiness  

## Next required step

Obtain authorized CF-02 (or approved CMIST L1 via formal amendment) → Phase B → only then complete-pilot candidacy.
