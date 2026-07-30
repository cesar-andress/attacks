# Corpus-freeze decision log

**Status:** recommendations only — **corpus is not frozen**.  
**Companion table:** [`data/corpus/candidate_disposition_recommendations.csv`](../../data/corpus/candidate_disposition_recommendations.csv)

## Rules applied

- Identity ≠ provenance ≠ screening ≠ inclusion.
- Purposive maximum-variation sampling; no representative claim; no forced N.
- OpenAlex never authorizes inclusion.
- Official institutional sources govern guidance identity/URLs.
- Do not silently finalize unresolved candidates.

## Disposition counts (recommendations, 2026-07-31)

| recommended_freeze_disposition | n |
|---|---:|
| include | 5 |
| comparator | 1 |
| hold | 14 |
| exclude | 2 |

### Recommended include (pending local authorized text + freeze checklist)

- **CF-03** CISA K-12 School Security Guide 3rd ed. (URL verified)
- **CF-13** France PPMS unified
- **CF-15** Spain NBA / RD 393/2007
- **CF-16** England Protective Security and Preparedness (URL verified)
- **CF-17** DfE Emergency Planning and Response for Education settings

### Recommended comparator (hold until L1 pin)

- **CF-02** CMIST / function-based pathway (2007 article confirmed; operational L1 open)

### Recommended exclude

- **CF-20** RAN / EU Knowledge Hub (no dated citable document)
- **CF-21** German Länder Amok/crisis guidance (never located)

### Hold (examples)

PASS edition, CSTAG manual, REMS annex, CPTED tool authorship, FEMA/HHS functional-needs, PEEP, SRP, Safe & Sound, Prevent, Plan Director eligibility for executability PEs, ACT-for-Education independence, CSSF URL capture, NTAC (BTAM domain; Branch B inactive for aggregates).

## Freeze declaration template (do not fill until blockers clear)

```
CORPUS_FREEZE_STATUS=not_frozen
FREEZE_DATE=
FREEZE_N_L0=
FREEZE_N_L1=
PREREGISTRATION_ID=
PILOT_STATUS=required_before_or_with_freeze
```

## Decision

**Corpus freeze: NOT DECLARED.**
