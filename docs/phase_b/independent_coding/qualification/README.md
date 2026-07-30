# Qualification exercise (coder-facing)

**Qualification-set version:** `QUAL-SET-v1` (**frozen** — `QUAL-FREEZE-v1`)  
**Scorer:** `python -m school_security_audit.phase_b_qualification` (`QUAL-SCORER-v1`)  
**Attempt policy:** [`../attempt_policy.md`](../attempt_policy.md) (`QUAL-ATTEMPT-v1`, **adopted**)  
**Answer key:** ADMIN_ONLY — not in this folder  

## Data the coder receives

- Stimuli: `data/phase_b/qualification_cases.csv` (case text + skill tags only)  
- Blank response template: copy schema headers without answer values, or use the blank template from the package generator  

## Critical errors (any one → fail)

1. Treating `ambiguous_memo` as positive demand/support evidence.  
2. Coding Branch B / Family F into confirmatory executability aggregates.  
3. Missing `source_location` on coded PEs.  
4. Auto-coding support from setting catalogs alone.

## Non-critical / dimension thresholds (frozen `QUAL-THRESH-v1`)

- Unitization: ≥80% correct on unitization-focused cases.  
- Rung: ≥80% exact match on Q-02…Q-05.  
- Locus: scored on locus-focused cases (reported; overall pass uses critical + rung + unitization rules in scorer).  
- Overall: no critical fails **and** rung/unitization thresholds met.

Thresholds and cases are immutable under `QUAL-FREEZE-v1` without a formal amendment.

## Synthetic fixtures (admin validation only)

- Pass: `data/phase_b/synthetic_qualification_pass.csv`  
- Fail: `data/phase_b/synthetic_qualification_fail.csv`  

These are **not** empirical reliability and **not** a real coder result.
