# Branch B scope decision (formal)

**Decision date:** 2026-07-31  
**Current paper spine:** Branch A — Protective-Action Executability / executability engagement only.

## Decision

| Item | Status |
|---|---|
| Threat detectability (Family F) | `inactive_for_current_study` |
| Future short module | `reserved_for_secondary_module` (option open) |
| Separate paper | `reserved_for_separate_study` (option open) |
| Demand–capability characterization of detectability | **Forbidden** — detectability is not demand–capability fit |

## Operationalization

1. Family F fields may remain in schemas/templates for reuse.
2. Current-paper analysis scripts and claims must ignore Family F for aggregates.
3. Coding rows for the current study should set `analysis_scope=branch_a_executability` and leave Family F empty **or** mark them out-of-scope in memos; they must not enter confirmatory tables.
4. No combined inclusive-security score (already forbidden in constants).
5. Sampling may still include BTAM-domain frameworks for any protective-action PEs they contain; that is not Branch B analysis.

## Classification of existing Family F artifacts

| Artifact | Classification |
|---|---|
| Codebook Family F definitions | `reserved_for_secondary_module` / reusable |
| Coding template F columns | `inactive_for_current_study` |
| Reviewer notes discussing Branch B | `background_only` |
