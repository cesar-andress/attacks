# Freeze-readiness register

**Status:** living audit (not a freeze declaration)  
**Machine-readable:** [`data/corpus/freeze_readiness_register.csv`](../../data/corpus/freeze_readiness_register.csv)  
**As of:** 2026-07-31

## Summary counts

| Class | Count (approx.) |
|---|---:|
| `freeze_blocker` | majority open (N, eligibility, provenance, local text, pilot) |
| `coding_blocker` | several (URLs for remaining docs; L1 pins) |
| `manuscript_blocker` | prereg ID; CMIST L1 citation |
| `resolved` | RQ2 denominator; reliability policy; Branch B formalization; CF-21 exclude recommendation |
| `nonblocking_editorial` | title/formatting; classical HRA citation |

## Hard freeze blockers (cannot GO)

1. Final corpus N unset (must follow eligibility, not a target number).
2. No authorized local source text (`local_file_status=none` for all L1; no `data/sources/`).
3. Pilot coding **not executed** (blocked by #2).
4. Multiple L0/L1 provenance and identity holds (PASS, CSTAG, CMIST ops, FEMA/HHS, PEEP, RAN, REMS annex).
5. Preregistration not registered (package readiness ≠ identifier).

## Resolved in this audit

- RQ2 denominator policy (primary + complementary).
- Reliability decision framework with α bands and contingencies.
- Branch B formal inactivation for current-paper aggregates.
- Official landing URLs captured for CF-03 (CISA) and CF-16 (GOV.UK).
- CF-20/CF-21 recommended **exclude** unless a dated citable document appears.

See CSV for full rows.
