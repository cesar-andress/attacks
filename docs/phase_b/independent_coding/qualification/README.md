# Qualification exercise

**Data:** `data/phase_b/qualification_*.csv`  
**Scorer:** `python -m school_security_audit.phase_b_qualification`

## Critical errors (any one → fail)

1. Treating `ambiguous_memo` as positive demand/support evidence.  
2. Coding Branch B / Family F material into confirmatory executability aggregates.  
3. Missing source_location on coded PEs.  
4. Auto-coding support from setting catalogs alone.

## Non-critical thresholds

- Unitization: ≥80% of cases with correct PE count (± justification memo).  
- Rung: ≥80% exact match on Q-02…Q-05.  
- Locus: ≥80% on locus-focused cases.  
- Explicit vs entailed: no repeated over-entailment pattern.

## Synthetic fixtures

- Pass: `synthetic_qualification_pass.csv`  
- Fail: `synthetic_qualification_fail.csv`  

These are **not** empirical reliability.
