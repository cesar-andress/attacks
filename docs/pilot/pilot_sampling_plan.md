# Pilot sampling plan

**Status:** amended by PA-2026-07-31-001 (two-phase)  
**NOT_FOR_SUBSTANTIVE_INFERENCE:** true  
**Selection date (original):** 2026-07-31 (rationale recorded **before** any coding)

## Purpose

Test unitization, codebook usability, ladder/locus/demand-source rules, validation, and reliability workflow — **not** prevalence or hypothesis support.

## Two-phase structure

| Phase | Sample name | Sources | Gate |
|---|---|---|---|
| A — Operational | `operational_pilot_sample` | P1–P4 | `operational_pilot_gate` |
| B — Benchmark calibration | `benchmark_calibration_sample` | P5 / CF-02 (or approved L1) | `benchmark_calibration_gate` |

P1–P4 are **not** the final complete pilot sample. Complete pilot = Phase A + Phase B.

See `phase_a_sampling_plan.md` and `pilot_dependency_map.md`.

## Target size (complete pilot, when text available)

- 3–5 L1 documents including comparator
- ~20–40 PEs
- Full double-coding for reliability (independent human coders)

## Selected pilot materials (purposive difficulty)

| Priority | L0 | L1 | Why selected (difficulty/variation) | Jurisdiction | Phase |
|---|---|---|---|---|---|
| P1 | CF-16 | DOC-CF16-01 | Protective-security + preparedness; supports/differentiation; counterexample surface | England | A |
| P2 | CF-03 | DOC-CF03-01 | Layered physical security; assessment-tool companion | US | A |
| P3 | CF-15 | DOC-CF15-01 | Regulatory setting taxonomy (docente/disability thresholds); L0 G1 stress | Spain | A |
| P4 | CF-13 | DOC-CF13-01 | Active-assailant/PPMS; multimodal alerting; non-English; archive HTML conditions | France | A |
| P5 (comparator) | CF-02 | DOC-CF02-01 *or* later CMIST L1 if pinned | Function-based comparator language | US-origin | B |

## Coverage checklist (design intent)

- [x] ≥2 jurisdictions (US, England, + ES/FR if P3/P4 runnable)
- [x] ≥2 framework families (physical security; EOP/regulatory; comparator AFN)
- [ ] Benchmark comparator pathway (CF-02) — **Phase B blocked**
- [x] Likely explicit prescriptions / supports / assessment language (Phase A)
- [x] Likely entailed-demand and inhibitory cases (Phase A)
- [x] Setting differentiation (CF-15 / CF-13 / CF-16)
- [x] Likely rung 0–1 and possible higher rungs **if genuinely present** (not presupposed)

## Execution gates

- **Phase A:** authorized local copies for P1–P4 + amendment PA-2026-07-31-001 → `operational_pilot_gate`  
- **Complete pilot:** Phase A + Phase B (P5) → still blocked while `PILOT_SOURCE_NO_GO`  
- Until complete pilot closes: no corpus freeze; no full coding; no substantive inference
