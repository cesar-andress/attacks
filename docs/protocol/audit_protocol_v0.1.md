# Structured content-analysis audit — methodology protocol (v0.1)

**Status:** draft for preregistration / supplementary material  
**Scope:** methods design only. This document does not perform the audit, select confirming evidence, or report findings.

## Governing principle

A security protocol cannot be treated as operationally implemented solely because it formally exists. Its implicit demands must also be executable by the intended occupants under realistic conditions, given the contextual supports the framework itself specifies.

## Study type

Documentary content analysis of school-security and emergency-preparedness frameworks.  
**Not** an effectiveness study of real-world protective actions.

## Units of analysis

| Level | Unit | Codes |
|---|---|---|
| L0 | Framework | Families A (partial), G, H |
| L1 | Document | Provenance, version, length, inclusion status |
| L2 | Prescriptive element (PE) | Families B, C, D, E, F, I |

A PE is a single statement that prescribes an action, mandates a control, or poses an assessment question such that a school could in principle comply or not comply. Narrative rationale and definitions are not PEs.

Segmenting text into PEs is a coding decision; report **unitizing reliability** as well as classification reliability.

## Analytical branches (do not collapse)

1. **Branch E — Protective-action executability**  
   Depth ladder (0–5) × orthogonal locus (individual / subgroup / setting / multiple / not specified).

2. **Branch F — Threat detectability**  
   Detection mechanisms, baseline interpretation, specialist participation, false-positive safeguards.

Do **not** average Branch E and Branch F into one “inclusive security” score. Their normative implications can point in opposite directions (more executability testing vs. stronger anti-overflagging safeguards).

## Executability ladder (Branch E)

| Rung | Label |
|---|---|
| 0 | Not addressed |
| 1 | Prescription only |
| 2 | Support or accommodation specified |
| 3 | Executability explicitly assessed |
| 4 | Executability tested under realistic conditions |
| 5 | Test findings used to revise or adapt the measure |

## Procedural demands (Family C)

Demands are coded only when `demand_source` is `explicit` or `entailed`.  
`ambiguous_memo` is qualitative only and **must not** count as presence in confirmatory analyses.

Entailed demands require pasted trigger evidence and must satisfy the **necessity threshold** in the entailment table (logical necessity, not contingent association). Default on ambiguity: do not code the demand.

## Corpus and freeze rules

- Purposive, criterion-based, maximum-variation sampling with a documented frame.
- Stratify by authority type, domain, geography, and recency.
- Include **benchmark comparators** (accessibility / AFN frameworks) as a falsification route.
- Freeze inclusion list and codebook **before** main coding.
- Preregister directional expectations **and** the disconfirming pattern.

## Normalization

Primary denominator: **prescriptive elements**.  
Word-count density is optional sensitivity analysis only.

## Reliability (planned)

- ≥2 coders; training + pilot; freeze codebook; double-coding (100% for small corpora).
- Report Krippendorff’s α per variable, unitizing reliability, and pre-consensus agreement.
- Pre-commit floors; demote below-floor variables to exploratory-only.

## Claims

See [`claims_policy.md`](claims_policy.md). Bind every Discussion claim to a code that licenses it.

## Smallest viable audit (guidance)

6–8 frameworks spanning core domains plus ≥2 accessibility benchmark comparators; US and ≥1 European source; full double-coding; coverage matrix; rung × locus distribution; main-vs-comparator contrast; reliability table; claims-bound narrative.

---

*Protocol v0.1 — draft. Designed to remain valid under a negative result (frameworks scoring as inclusive as, or more than, expected).*
