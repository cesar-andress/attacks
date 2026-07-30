# Skipped-test / validation-debt audit

**Date:** 2026-07-31  
**Search:** `pytest.mark.skip`, `xfail`, `unittest.skip`, commented tests, disabled CI steps.

| Finding | Status |
|---|---|
| `pytest.mark.skip` / `xfail` in suite | **None found** |
| Commented-out tests | None material |
| Disabled validators | None — `validate_todos` added to `make validate` |
| Empty “allow any” schemas | Coding validators enforce enums; no change this sprint |
| Manual-only checks remaining | Clean-checkout / manuscript PDF still manual; submission-ready LaTeX mode documented |

No difficult tests were deleted to green the suite.
