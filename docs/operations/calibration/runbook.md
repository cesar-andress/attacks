# Calibration runbook (post-READY)

**Gate today:** BENCHMARK_CALIBRATION=NO_GO until this runbook completes with a real qualified coder.  
**Comparator:** FEMA FNSS 2010 (`DOC-ALT-FNSS-001`) under OPT-B / PA-2026-07-31-002. Not a gold standard.

## Prerequisites

- Independent coder READY  
- Target package authorized to OPEN for that coder only  
- QUAL-FREEZE intact  
- No discussion of case answers before reliability  

## Steps

1. Verify FNSS checksum against authorized source record.  
2. Release calibration package with version ID + checksum + timestamp.  
3. Confirm coding environment (CSV schema `coding_form_schema.csv`).  
4. Set coding deadline; start no-discussion period.  
5. Receive locked submissions (coder A independent; second pass per protocol).  
6. Validate schema / unit IDs (no target peeking beyond authorized text).  
7. Compute reliability: exact agreement, ordinal/nominal α where estimable, marginals, n, missingness, PA-003 estimability state; optional pre-specified collapsed sensitivities.  
8. Hold review meeting using states below.  
9. Record calibration gate decision (human) without inventing thresholds beyond protocol.

## Reliability states (PA-003)

| State | Progression guidance |
|---|---|
| ESTIMABLE_PASS | May support progression if other exit criteria met |
| ESTIMABLE_BELOW_THRESHOLD | Investigate; may block confirmatory use per variable-class rules |
| NOT_ESTIMABLE_NO_VARIATION | Not automatic coder failure; report; do not demote manifest core solely for empty high rungs |
| NOT_ESTIMABLE_INSUFFICIENT_CATEGORIES | Report; review |
| NOT_ESTIMABLE_INSUFFICIENT_UNITS | Report; review sample/plan |
| COMPUTATION_ERROR | Repair; recompute |
| PROTOCOL_DEVIATION | Document; may block |
| PENDING_ADJUDICATION | Do not substitute adjudicated α |

If protocol text does not fully specify a gate consequence for a state, record a **bounded human decision** rather than inventing a rule.

## Outputs

- Machine-readable reliability table  
- Human-readable summary  
- Dashboard update  
- Still no corpus freeze until freeze runbook prerequisites met
