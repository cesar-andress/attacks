# RP-P1 execution operations index

**Purpose:** operational readiness for independent coding without changing methodology.  
**Canonical protocol:** `docs/protocol/`, `docs/phase_b/`, amendments PA-2026-07-31-001/002/003.  
**Zenodo DOI:** [10.5281/zenodo.21711588](https://doi.org/10.5281/zenodo.21711588)  
**Tag policy:** regenerate GitHub `v1.0.0` after public commits; do not mint a new Zenodo version.

## Authoritative gate snapshot (do not invent changes)

| Gate | Status |
|---|---|
| OPT-B / PA-2026-07-31-002 | adopted |
| PA-2026-07-31-003 | adopted |
| QUAL-ATTEMPT-v1 | ADOPTED |
| QUAL-FREEZE-v1 | AUTHORIZED |
| Target package | SEALED |
| Independent coder | NOT_READY |
| Benchmark calibration | NO_GO |
| Corpus freeze | NO_GO |
| Full coding | NO_GO |
| UCW-003 | RESOLVED (direct contact; voluntary unpaid) |

## Document map

| Stage | Authoritative docs |
|---|---|
| Compensation / channel | [`UCW-003_decision_record.md`](UCW-003_decision_record.md) |
| Recruitment | [`recruitment/`](recruitment/) (+ legacy `docs/phase_b/independent_coding/recruitment/`) |
| COI / independence | [`recruitment/coi_decision_guide.md`](recruitment/coi_decision_guide.md); form in `docs/phase_b/independent_coding/forms/` |
| Confidentiality | [`onboarding/secure_handling_instructions.md`](onboarding/secure_handling_instructions.md); agreement form in Phase-B forms |
| Onboarding | [`onboarding/`](onboarding/) |
| Training | Phase-B `training/`; completion record here |
| Qualification execution | [`qualification/`](qualification/); freeze materials unchanged |
| Calibration | [`calibration/runbook.md`](calibration/runbook.md) |
| Corpus freeze | [`corpus_freeze/runbook.md`](corpus_freeze/runbook.md) |
| Independent coding | [`coding/runbook.md`](coding/runbook.md) |
| Reliability | [`reliability/pipeline_readiness.md`](reliability/pipeline_readiness.md); PA-003 |
| Adjudication | [`adjudication/runbook.md`](adjudication/runbook.md) |
| Analysis provenance | [`analysis/data_lineage.md`](analysis/data_lineage.md) |
| Governance / privacy | [`governance/`](governance/) |
| Checklists | [`checklists/`](checklists/) |
| Dashboard | [`../../data/operations/execution_dashboard.csv`](../../data/operations/execution_dashboard.csv) |

## Public vs private

Public: templates, blank logs, role descriptions, runbooks, validators, synthetic fixtures.  
Private (`private/coder_admin/`, gitignored): identities, signed forms, compensation, submissions, sealed sources.
