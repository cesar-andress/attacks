# Phase-B reliability operationalization

Policy source: `docs/protocol/reliability_policy_v0.1.md` (Krippendorff 2018).  
Amendment: `PA-2026-07-31-003` (estimability / sparsity).

| Object | Coefficient | Notes |
|---|---|---|
| Unitization | Boundary agreement / identical-span % | Report disagreement types |
| Nominal codes | α nominal | locus, demand presence, sources, binary supports |
| Ordinal rung | α ordinal | executability_rung |
| Demand-source | α nominal | explicit/entailed/ambiguous_memo |
| Support/assessment/testing/revision cues | α nominal or ordinal as applicable | Map to ladder evidence |

## Rules

- Independent humans only for confirmatory α.  
- Pre-consensus statistics before adjudication.  
- Adjudication after α computation.  
- Missing data: pairwise deletion per Krippendorff; document.  
- Insufficient variation: report `NOT_ESTIMABLE_*`; do not invent α; do not equate with coder failure.  
- Exact agreement + category marginals required alongside α.  
- Empty high rungs are distributional findings, not reliability failures.  
- No post-hoc primary-ladder collapse; optional secondary collapsed sensitivities only if pre-specified.  
- Small-N: warn; Phase B single-document α is calibration not prevalence.  
- Bands: ≥0.80 confirmatory; 0.67–0.80 cautious; <0.67 exploratory/uninterpretable when estimable.  
- Synthetic qualification scores ≠ empirical α.  
- Phase-A simulated second pass ≠ empirical α.  
- Classifier helper: `school_security_audit.reliability_estimability`.
