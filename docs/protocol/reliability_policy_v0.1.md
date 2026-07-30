# Reliability policy v0.1

**Status:** adopted for preregistration planning (2026-07-31; small-corpus threshold clarified 2026-07-31)  
**Does not invent observed α values.**  
**Citation:** Krippendorff, K. (2018). *Content Analysis: An Introduction to Its Methodology* (4th ed.). SAGE. DOI: [10.4135/9781071878781](https://doi.org/10.4135/9781071878781). Interpretive bands below follow that methodological tradition (commonly α ≥ 0.800 confirmatory; 0.667 usable with caution).

## Scope

Applies to unitization and classification for L2 PE coding and L0 differentiation codes used in confirmatory analyses.

## Coefficients

| Object | Preferred coefficient | Percent agreement |
|---|---|---|
| Unitization (PE boundary) | Unitizing agreement / percent of identically bounded units; report disagreement types | Supplementary |
| Nominal codes (locus, demand presence, sources, binary supports) | Krippendorff’s α (nominal) | Supplementary only |
| Ordinal ladder (`executability_rung`) | Krippendorff’s α (ordinal) | Supplementary only |
| Sparse categories | α with prevalence/bias diagnostics; do not hide sparsity by aggregation | Supplementary |

## Minimum sample and double-coding fraction

- Pilot: full double-coding of all pilot PEs (target 20–40 PEs when text available).
- **Small corpus (protocol definition):** frozen corpus with **≤ 15 included L1 documents** and **≤ 250 eligible PEs**.
- Main study default for a small corpus: **100% independent double-coding**.
- If either L1 count or PE count exceeds the small-corpus ceiling, preregister a random double-coded subsample fraction **before** coding begins (recommended floor: ≥ 30% of eligible PEs or ≥ 50 PEs, whichever is larger, unless a power/stability justification is preregistered).
- Training-set PEs used only for coder calibration are **excluded** from confirmatory α.
- Do not compute α on tiny cells as confirmatory without noting instability.
- Coder independence: second coder must not see first-coder values or adjudication notes before independent coding.
- Raw coder files are retained immutably; **pre-consensus** α is reported; adjudicated values may form the analysis dataset.

## Threshold categories (preregistered floors)

| Band | α (approx.) | Analysis status |
|---|---|---|
| Acceptable for confirmatory use | α ≥ 0.80 | Confirmatory |
| Usable with caution | 0.67 ≤ α < 0.80 | Confirmatory only with explicit caution + sensitivity |
| Exploratory only | 0.40 ≤ α < 0.67 | Exploratory; not main claims |
| Not interpretable | α < 0.40 or undefined | Do not interpret; repair codebook or drop |

Exact numeric floors may be adjusted **only** by preregistered amendment before main coding, with citation support.

## Variable-class contingencies

1. **Manifest codes** (prescription, support, assessment/testing/revision cues, rung, locus, G1/G2): carry confirmatory analyses when within band.
2. **`explicit` vs `entailed`:** report separately; never pool to inflate presence.
3. **`ambiguous_memo`:** never positive evidence.
4. **Entailed-demand / inhibitory-demand / responder-interaction:** if α falls below confirmatory floor, demote to exploratory; paper remains viable on manifest engagement.
5. **Family F (Branch B):** inactive for current-paper confirmatory aggregates (see Branch B decision).

## Adjudication

- Train → pilot → freeze codebook → independent double-coding → compute **pre-consensus** agreement → adjudicate.
- Adjudicated values may form the analysis dataset.
- **Adjudicated data must not replace raw reliability inputs:** archive coder_A and coder_B (or procedural second-pass) files immutably; report pre-consensus α.
- Simulated procedural second passes are **not** independent coding and must not be reported as empirical intercoder α.

## Low-reliability response

- Report α transparently.
- Demote variables below floor.
- Do not build composite scores to mask disagreement.
- Amend codebook only for genuine under-specification (changelog required).
