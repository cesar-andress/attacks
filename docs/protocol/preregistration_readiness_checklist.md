# Preregistration-readiness checklist

**As of:** 2026-07-31  
**Preregistration identifier:** *not issued* (do not invent)  
**Package status:** draft-ready components exist; **not submission-ready** until complete pilot + freeze blockers clear.

| Item | Status | Notes |
|---|---|---|
| Research questions | Ready | RQ1–RQ4 + falsification |
| Sampling strategy | Ready | Purposive max-variation |
| Eligibility criteria | Ready (draft) | corpus_selection.md |
| Corpus-freeze procedure | Partial | Decision log exists; freeze not declared |
| Units L0/L1/L2 | Ready | |
| Codebook | Ready (v0.1 draft) | Freeze codebook before main coding; benchmark-dependent items open |
| Ladder | Ready | Protocol-aligned labels; Phase A provisional drill/rung rules |
| Locus | Ready | `not_specified` token |
| Demand-source rules | Ready | explicit/entailed/ambiguous_memo |
| Benchmark comparator logic | Partial | Logic ready; P5 text missing |
| Counterexample commitments | Ready | Pre-coding only |
| Confirmatory vs exploratory | Ready | Reliability contingencies |
| Reliability policy | Ready | reliability_policy_v0.1.md (Krippendorff 2018; small-corpus ≤15 L1 / ≤250 PE); empirical α after independent coding |
| Fallback rules | Ready | Manifest carries paper if entailed fails |
| Denominators | Ready | RQ2 primary B + complementary A |
| Exclusions | Partial | Disposition recommendations; not final |
| Claims policy | Ready | |
| Amendment policy | Ready | PA-2026-07-31-001 + pilot amendment log |
| Two-phase pilot | Ready | Phase A completed; Phase B blocked |
| Pilot-data treatment | Ready | Triple labels; no silent merge |
| Branch B inactive | Ready | branch_b_scope_decision.md |
| Local source availability (complete) | **Not ready** | P5/CF-02 |
| Phase A operational sources | Ready | P1–P4 |
| Registry ID | **Not ready** | |

## Static package manifest (local only; not submitted)

When freeze blockers clear, zip or tag:

- `docs/protocol/*.md` (frozen versions) + amendments/
- `docs/codebook/codebook_v0.1.yaml` (+ human-readable)
- `data/corpus/candidate_frameworks.csv` + `document_registry.csv` + disposition + freeze register
- `data/corpus/counterexample_commitments.csv`
- `docs/protocol/reliability_policy_v0.1.md`
- `docs/protocol/rq2_denominator_decision.md`
- `docs/protocol/claims_policy.md`
- `docs/pilot/*` + `data/gates/gate_register.csv` + pilot status

**Do not submit** until complete pilot (A+B) executed and corpus freeze declared.
