# Unresolved-item (TODO) register

**Purpose:** Track every unresolved scientific, editorial, source, release, and experiment item without fabricating empirical values or silently deleting blockers.

**Machine-readable register:** [`unresolved_item_register.csv`](unresolved_item_register.csv)  
**Human-readable report:** [`unresolved_item_report.md`](unresolved_item_report.md)  
**Allowlist for scanner:** [`todo_allowlist.yaml`](todo_allowlist.yaml)  
**Sprint plan:** [`resolution_sprint_plan.md`](resolution_sprint_plan.md)  
**Citation audit:** [`citation_completion_audit.md`](citation_completion_audit.md)  
**Preregistration readiness matrix:** [`preregistration_readiness_matrix.md`](preregistration_readiness_matrix.md)  
**Release implications:** [`release_implications.md`](release_implications.md)

## Categories (primary)

1. `RESOLVABLE_NOW_EDITORIAL` … `RESOLVABLE_NOW_VALIDATION`  
2. `BLOCKED_BY_*` gates (source, freeze, prereg, coding, results, ethics, external)  
3. `INTENTIONAL_PLACEHOLDER` / `OBSOLETE_MARKER` / `DUPLICATE` / `INVALID_OR_UNSUPPORTED_REQUEST`

## Priorities

| Priority | Meaning |
|---|---|
| P0 | Repository validity, release safety, or scientific integrity |
| P1 | Blocks preregistration, corpus freeze, or main coding |
| P2 | Blocks manuscript submission |
| P3 | Future research-programme development |
| P4 | Optional improvement |

## Validator

```bash
python -m school_security_audit.validate_todos
# or
make validate
```

Unregistered TODO/FIXME/CITATION-NEEDED markers in release-critical tracked files fail validation. Registered intentional/blocked markers listed in the allowlist are permitted with diagnostics.

## Gate status (do not weaken without evidence)

| Gate | Status |
|---|---|
| OPERATIONAL_PILOT | COMPLETED |
| BENCHMARK_CALIBRATION | NO_GO |
| COMPLETE_PILOT | INCOMPLETE |
| CORPUS_FREEZE | NO_GO |
| FULL_CODING | NO_GO |
| PILOT_SOURCE_NO_GO (P5/CF-02) | active |

No empirical intercoder α. Results/Discussion/Conclusion remain blocked.
