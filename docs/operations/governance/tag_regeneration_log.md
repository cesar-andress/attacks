# v1.0.0 tag regeneration log

| Date (UTC) | Previous commit | New commit | Reason | Validation | Zenodo DOI | Archive match note | Operator |
|---|---|---|---|---|---|---|---|
| 2026-07-31 | (prior) | dea6344482a21b843744493d0c91112b0d7dc817 | Authors/dash cleanup before ops consolidation | release-check OK at time | 10.5281/zenodo.21711588 | Zenodo snapshot may predate later tag moves; DOI unchanged; no new Zenodo version | agent |
| 2026-07-31 | dea6344482a21b843744493d0c91112b0d7dc817 | 90d9a5f646a29d2150e2573eb9e9e708cbe6650f | Execution-readiness ops pack (templates, validators, synthetic reliability pipeline) | release-check OK (129 tests) | 10.5281/zenodo.21711588 | Annotated tag v1.0.0 regenerated on branch HEAD after follow-up log commits; Zenodo DOI unchanged (no new version); archive file set may lag | agent |

Policy: regenerate annotated `v1.0.0` after public commits; never mint Zenodo v1.0.1 for ordinary updates.

Exact current tag: run `git rev-parse v1.0.0^{}` (must equal `git rev-parse HEAD` on release tip).
