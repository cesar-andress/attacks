# Reliability sparsity audit (pre-coding) — 2026-07-31

**Outcome:** OPTION B — limited amendment `PA-2026-07-31-003` adopted.  
**Does not change:** OPT-B, QUAL-FREEZE-v1, sealed target, PE definition, ladder.

## Variables receiving α

| Variable | Scale | Confirmatory? | Notes |
|---|---|---|---|
| Unitization | boundary / % | Yes (report) | Not α alone |
| `executability_rung` | ordinal α | Yes | Primary ladder |
| Locus | nominal α | Yes when estimable | Sparse joint cells caution |
| Manifest support/assessment/testing/revision cues | nominal/ordinal | Yes | Map to ladder evidence |
| Demand-source (explicit/entailed/ambiguous_memo) | nominal | Yes (report separate) | Never pool |
| Entailed / inhibitory / responder-interaction | nominal | Contingent | Demote if below floor |
| Family F (Branch B) | — | No | Inactive |

## Risks found

1. High rungs (4–5) may be rare or empty → α undefined or unstable.  
2. Perfect agreement on a single category → `NOT_ESTIMABLE_NO_VARIATION`.  
3. Joint ladder×locus tables may be sparse → descriptive caution, not automatic failure.  
4. Conflating undefined α with coder failure would over-demote the confirmatory core.

## Policy adopted

- Exact agreement + marginals alongside α.  
- Explicit estimability states (see `reliability_estimability.py`).  
- Empty high rungs = distributional findings.  
- No post-hoc primary collapse.  
- Optional secondary collapsed sensitivities pre-specified.  
- Qualification scoring remains separate from target reliability.

## Confirmatory-core resilience

Paper remains interpretable on manifest engagement distributions, locus (when estimable), counterexamples, and bounded document-specific FNSS contrast even if sparse codes or RQ4 contrast are null/weak.
