# Reliability pipeline readiness

**Policy:** `docs/protocol/reliability_policy_v0.1.md` + PA-2026-07-31-003.  
**Modules:** `school_security_audit.reliability_estimability`, `school_security_audit.reliability_pipeline`.

## Required joint outputs

Exact agreement + alpha (when estimable) + category marginals + n + missingness + estimability state — in machine-readable JSON and human-readable Markdown.

Primary coefficient remains Krippendorff's α (nominal/ordinal as specified). Additional descriptive coefficients are secondary only if already authorized.

## Fixture coverage (synthetic only)

`tests/test_reliability_pipeline.py` and `data/operations/fixtures/reliability/` exercise:

- perfect agreement; partial / ordinal / nominal disagreement  
- missing values; one invariant coder; both invariant with agreement  
- insufficient units; sparse high rungs (via classifier); absent rare categories  
- malformed values; duplicate unit IDs; mismatched unit sets  
- missing coder file; invalid coder identity  
- protocol deviation; computation failure  

Banner: `SYNTHETIC_NOT_FOR_MANUSCRIPT`. Target findings must never be simulated into manuscript Results.

## Distinctions preserved

- `ESTIMABLE_PASS` / `ESTIMABLE_BELOW_THRESHOLD`  
- Valid non-estimable states (not automatic coder failure; no automatic demotion of manifest confirmatory core for invariance alone)  
- Operational/computation errors  
- Protocol failures  
