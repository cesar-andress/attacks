# Qualification decision rules and coder-readiness criteria

## Coder workflow states

| State | Meaning |
|---|---|
| `NOT_STARTED` | No candidate |
| `TRAINING_ASSIGNED` | Pre-qualification pack delivered |
| `TRAINING_COMPLETED` | Human attested training done |
| `QUALIFICATION_ASSIGNED` | Qual pack delivered (requires freeze auth) |
| `QUALIFICATION_SUBMITTED` | Submission locked + hashed |
| `QUALIFICATION_PASS` | Scorer pass |
| `QUALIFICATION_FAIL_RETRAIN_ALLOWED` | Fail; attempt remains |
| `QUALIFICATION_FAIL_FINAL` | No further attempt under policy |
| `QUALIFICATION_INVALID` | Technical/invalid submission |
| `QUALIFICATION_REVIEW_REQUIRED` | Human review needed (e.g. disclosed COI) |

## `INDEPENDENT_CODER=READY` requires all of

1. Opaque coder ID assigned  
2. Independence/COI form `COMPLETED_NO_CONFLICT` **or** disclosed case reviewed and approved  
3. Confidentiality `COMPLETED`  
4. Training completed (attested)  
5. Qualification submission valid and locked  
6. Scorer `passed=true` on frozen set/key/scorer versions  
7. No overlap/leakage incident open  
8. Attempt policy **adopted** (not draft)  
9. Qualification freeze **authorized** by human  
10. Human review completed  
11. Manifest fields updated honestly  
12. Target package still **SEALED** until explicit open step after READY  

**Scorer pass alone is never sufficient.**

## Calibration states

| Gate value | Requires |
|---|---|
| `BENCHMARK_CALIBRATION=IN_PROGRESS` | READY + target package opened |
| `BENCHMARK_CALIBRATION=COMPLETE` | Double coding locked; pre-adjudication reliability; BDD adjudicated; Phase-A recode decision documented; completion report |
