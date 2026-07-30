# Reliability policy v0.1

**Status:** adopted for preregistration planning (2026-07-31)  
**Does not invent observed α values.**  
**Citation:** \todo{CITATION NEEDED: Krippendorff content-analysis reliability standards (primary source)} — bands below follow common content-analysis practice and must be confirmed against the cited primary source before preregistration submission.

## Scope

Applies to unitization and classification for L2 PE coding and L0 differentiation codes used in confirmatory analyses.

## Coefficients

| Object | Preferred coefficient | Percent agreement |
|---|---|---|
| Unitization (PE boundary) | Unitizing agreement / percent of identically bounded units; report disagreement types | Supplementary |
| Nominal codes (locus, demand presence, sources, binary supports) | Krippendorff’s α (nominal) | Supplementary only |
| Ordinal ladder (`executability_rung`) | Krippendorff’s α (ordinal) | Supplementary only |
| Sparse categories | α with prevalence/bias diagnostics; do not hide sparsity by aggregation | Supplementary |

## Minimum sample

- Pilot: full double-coding of all pilot PEs (target 20–40 PEs when text available).
- Main study: protocol default **100% double-coding for small corpora**; if corpus grows large, preregister a random double-coded subsample **before** coding begins.
- Do not compute α on tiny cells as confirmatory without noting instability.

## Threshold categories (preregistered floors)

Pending confirmation against the Krippendorff primary source:

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

## Low-reliability response

- Report α transparently.
- Demote variables below floor.
- Do not build composite scores to mask disagreement.
- Amend codebook only for genuine under-specification (changelog required).
