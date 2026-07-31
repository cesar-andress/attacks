# v1.0.0 tag regeneration log

| Date (UTC) | Previous commit | New commit | Reason | Validation | Zenodo DOI | Archive match note | Operator |
|---|---|---|---|---|---|---|---|
| 2026-07-31 | (prior) | dea6344482a21b843744493d0c91112b0d7dc817 | Authors/dash cleanup before ops consolidation | release-check OK at time | 10.5281/zenodo.21711588 | Zenodo snapshot may predate later tag moves; DOI unchanged; no new Zenodo version | agent |
| 2026-07-31 | dea6344482a21b843744493d0c91112b0d7dc817 | 90d9a5f646a29d2150e2573eb9e9e708cbe6650f | Execution-readiness ops pack (public templates, validators, synthetic reliability pipeline) | release-check OK (129 tests) | 10.5281/zenodo.21711588 | GitHub annotated tag v1.0.0 force-updated to branch HEAD including this log; Zenodo DOI unchanged (no new version) | agent |

Policy: regenerate annotated `v1.0.0` after public commits; never mint Zenodo v1.0.1 for ordinary updates.

Exact tag object is recorded by `git rev-parse v1.0.0` after push (branch HEAD).
