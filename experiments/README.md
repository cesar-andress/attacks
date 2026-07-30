# Experimental Development Pack

**Status:** experimental materials designed for future methodological and content-validity studies  
**Maturity (current):** `internally_tested_synthetic` only  
**Human experiments executed:** **no**  
**SLAPA validated:** **no**

## Purpose

Support controlled methodological experiments on:

1. PE unitization reproducibility (EXP-01)  
2. Coding-decision reproducibility (EXP-02)  
3. Codebook usability (EXP-03)  
4. Evidence-layer comprehension (EXP-04)  
5. Preliminary SLAPA domain content mapping (EXP-05)  
6. Synthetic organisational-assessment feasibility (EXP-06)

## What this pack does **not** test

- Real school preparedness  
- Attack prediction or prevention  
- Validated field questionnaires  
- Empirical intercoder reliability from `simulated_procedural_second_pass`  
- Layer-5 incident effectiveness  

## Who may use it

Additional coders; expert reviewers; educational researchers; school-safety and special-education experts; emergency/police practitioners — **after** ethics/institutional conditions are met for human data collection.

## Maturity table

| State | Meaning | Current pack |
|---|---|---|
| designed | Materials drafted | yes (prior) |
| internally_tested_synthetic | Schemas/scripts/synthetic demos pass | **yes** |
| piloted | Human feasibility sample | **no** |
| independently_replicated | Independent human coder study | **no** |
| content_validated | Expert CVI on real panel | **no** |
| field_validated | SLAPA field study | **no** |

## Quick synthetic demonstration

```bash
cd ~/papers/attacks/attacks
make validate
make test
make experiment-demo
# reports: experiments/_generated/synthetic_demonstration_report.md
```

## Preparing real studies

1. Complete `ethics_readiness_checklist.md`.  
2. Do **not** store consent/identifiers in this public repo.  
3. Keep stimuli synthetic or legally redistributable.  
4. Label study type in response metadata (`independent_human`, etc.).  
5. Run validators before analysis.  
6. Follow `analysis_plans.md` and `future_claims_policy` in `docs/research_program/`.

## Claims boundaries

Permitted now: “synthetic demonstration / internally tested materials.”  
Prohibited: “validated SLAPA survey,” “human experiment completed,” “empirical α from procedural second pass,” total readiness scores.

See `experiment_register.csv` and per-experiment folders.
