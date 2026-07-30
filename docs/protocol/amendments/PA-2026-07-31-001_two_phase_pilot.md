# Protocol amendment PA-2026-07-31-001 — Two-phase pilot

**Amendment ID:** `PA-2026-07-31-001`  
**Date:** 2026-07-31  
**Version:** 1.0  
**Status:** adopted for protocol development  
**Does not rewrite history:** original complete-pilot gate remains `PILOT_SOURCE_NO_GO`.

## 1. Original pilot design

The pilot sampling plan (`docs/pilot/pilot_sampling_plan.md`, 2026-07-31) required authorized local text for **P1–P5**, including the sole benchmark comparator **P5 / CF-02**, before any pilot coding. Target: 3–5 L1 documents, ~20–40 PEs, full double-coding, then codebook amendments, then corpus freeze eligibility.

## 2. Source-access problem

Authorized full text is available for P1–P4 (`ready_for_pilot` / `ready_with_conditions`).  
**P5 / CF-02** remains without authorized full text (`hold_authorization`).  
Therefore the **complete pilot source gate** correctly remains:

`complete_pilot_source_gate = NO_GO` / `PILOT_SOURCE_NO_GO`

## 3. Why P5 remains required

P5 is the **sole** pilot benchmark comparator oriented to functional diversity / AFN language. Without it the pilot cannot:

- calibrate ladder distinctions against an explicitly function-based framework;
- test comparator-specific decision rules;
- resolve benchmark-dependent codebook ambiguities;
- support RQ-style benchmark comparison or any statement that the coding system behaves appropriately on AFN-oriented doctrine.

No silent substitution of CF-02 is authorized by this amendment.

## 4. Why P1–P4 can still test operational coding mechanics

P1–P4 jointly supply procedural variation (planning prescriptions, protective-action language, drills/exercises, revision, setting differentiation, multilingual unitization, archive-HTML conditions). These suffice to test **instrument usability and workflow**, not benchmark calibration or substantive corpus claims.

## 5. Decomposition

### Phase A — Operational pilot (`operational_pilot_sample` = P1–P4)

**Permitted:** unitization; source-location recording; codebook usability; variable interpretation; explicit/entailed/`ambiguous_memo`; ladder; locus; demand categories; setting differentiation; raw/adjudication workflow; schema validation; identification of ambiguities and source-format problems; procedural feasibility.

**Not permitted:** benchmark calibration/comparison; prevalence; framework ranking; inferential claims; final reliability claims; corpus-freeze decisions; preregistration submission; full coding; confirmatory analysis.

### Phase B — Benchmark calibration (`benchmark_calibration_sample` = P5 / CF-02 or formally approved CMIST L1)

**Required before complete pilot:** code comparator L1; evaluate ladder discrimination on functional-diversity doctrine; verify comparator decision rules; resolve benchmark-dependent ambiguities; only then mark complete pilot eligible to proceed toward freeze.

## 6. Formal dependency

```
Phase A COMPLETED  ─┐
                    ├─→  Complete pilot still requires Phase B GO
Phase B GO         ─┘
Corpus freeze / full coding / prereg submission remain blocked until complete pilot GO.
```

Phase A success **does not** open later gates.

## 7. What Phase A cannot establish

- Acceptable study reliability (α/κ thresholds);
- Final stability of benchmark-sensitive variables;
- Instrument validation for confirmatory use;
- Any claim about comparator engagement or corpus prevalence;
- Freeze readiness of the candidate set.

## 8. Decisions remaining blocked

| Decision | Status after this amendment |
|---|---|
| Complete pilot | Incomplete / NO_GO |
| Benchmark calibration | NO_GO until P5 (or approved substitute amendment) |
| Corpus freeze | NO_GO |
| Full coding | NO_GO |
| Preregistration submission | Not ready |
| Confirmatory analyses | Not authorized |

## 9. Record labelling (mandatory on all Phase A units)

Every Phase A PE and coding row must carry:

- `pilot_phase=A_operational`
- `pilot_flag=PILOT`
- `inference_flag=NOT_FOR_SUBSTANTIVE_INFERENCE`
- `benchmark_flag=NOT_FOR_BENCHMARK_COMPARISON`
- `protocol_flag=PROTOCOL_DEVELOPMENT_ONLY`

Phase A outputs must not enter `data/coding/` confirmatory paths automatically.

## 10. Hypotheses / confirmatory analyses

**Unaffected.** No confirmatory hypothesis is tested in Phase A. No preregistered analysis plan is altered except by adding this phased gate structure. Outcome-dependent selection is avoided because:

1. P1–P4 were fixed in the original sampling plan before coding;
2. Phase A does not drop or add candidates based on coded results;
3. P5 remains required; absence is a source gate, not a finding-driven exclusion.

## 11. Outcome-dependent selection — explicit non-introduction

This amendment responds to **access constraints documented before coding**, not to coded content. Selection rule for Phase A units is recorded in `docs/pilot/phase_a_sampling_plan.md` **before** final coding values are treated as complete.

## 12. Related artefacts

- Gate register: `data/gates/gate_register.csv`
- Dependency map: `docs/pilot/pilot_dependency_map.md`
- Phase A sampling: `docs/pilot/phase_a_sampling_plan.md`
- CF-02 access track remains active: `docs/sources/unresolved_blockers.md`
