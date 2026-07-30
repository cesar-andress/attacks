# Protocol amendment PA-2026-07-31-003 — Reliability sparsity and estimability

**Amendment ID:** `PA-2026-07-31-003`  
**Date:** 2026-07-31  
**Status:** **adopted** (pre-coding methodological clarification)  
**Parent policies:** `reliability_policy_v0.1.md`; Phase-B reliability operationalization  
**Does not amend:** OPT-B / `PA-2026-07-31-002`; qualification freeze `QUAL-FREEZE-v1`; PE definition; ladder; locus; BDD definitions  

## Reason

The prior reliability policy treated undefined α as “not interpretable” in the same band as failed reliability, risking conflation of invariant/sparse categories with coder failure. High rungs may be rare by design. This amendment distinguishes estimability states and protects the confirmatory core before target coding.

## Amended rules

1. Report **exact agreement** and **category marginal frequencies** alongside α for every confirmatory variable.  
2. When α is undefined or unstable because of no variation, a single observed category, or insufficient units, record an explicit state:  
   `NOT_ESTIMABLE_NO_VARIATION` | `NOT_ESTIMABLE_INSUFFICIENT_CATEGORIES` | `NOT_ESTIMABLE_INSUFFICIENT_UNITS`  
   These states are **not** automatic coder failure and do **not** by themselves demote manifest engagement.  
3. When α is estimable but below threshold, use existing bands (`ESTIMABLE_BELOW_THRESHOLD` / exploratory demotion rules).  
4. Empty high rungs are substantive distributional findings, not reliability failures.  
5. **No post-hoc category collapse** after observing target outcomes.  
6. Optional **secondary** pre-specified sensitivity: binary collapsed bands  
   - `no_engagement` (rung 0) vs `any_engagement` (rung ≥ 1);  
   - and/or `prescription_only` (rung 1) vs `support_or_higher` (rung ≥ 2).  
   Primary ladder remains uncollapsed.  
7. Qualification scoring and materials remain unchanged (`QUAL-FREEZE-v1`).  
8. OPT-B / FNSS comparator roles unchanged; RQ4 remains a secondary document-specific contrast.

## Timing

Adopted before independent target coding; not outcome-dependent.
