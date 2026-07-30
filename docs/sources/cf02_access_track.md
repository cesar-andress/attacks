# CF-02 access track (active)

**Status:** OPEN — blocks `benchmark_calibration_gate` and complete pilot  
**Design recommendation (not enactment):** see `docs/phase_b/` — `OPERATIONAL_L1_AMENDMENT_RECOMMENDED` (OPT-B)  
**Do not replace silently**  
**Do not use pirated repositories**

## Target identity

- **Candidate:** CF-02  
- **Document:** DOC-CF02-01 — Kailes & Enders (2007), *Moving Beyond “Special Needs”*  
- **Role:** original sole pilot **benchmark comparator** (`benchmark_calibration_sample`)  
- **DOI:** 10.1177/10442073070170040601

## Legitimate access routes (checked 2026-07-31)

Full machine log: `data/phase_b/access_routes.csv`.

| Route ID | Route | Status |
|---|---|---|
| AR-CF02-001 | Unpaywall | closed (`is_oa=false`) |
| AR-CF02-002 | OpenAlex | closed; no repository fulltext |
| AR-CF02-003 | SAGE PDF via DOI | not opened (403 / no institutional session) |
| AR-CF02-004 | CiteSeerX location | rejected — uncertain rights |
| AR-CF02-005 | UCJC library discovery | **pending human** |
| AR-CF02-006 | Interlibrary loan | template ready — **not sent** |
| AR-CF02-007 | Author manuscript | not identified; request template ready |
| AR-CF02-008 | Publisher permissions | `PERM-CF02-001` ready — **not sent** |
| AR-CF02-009 | Pirate mirrors | **forbidden** |

## Parallel operational L1 (not a silent substitute)

| Route ID | Source | Status |
|---|---|---|
| AR-FNSS-001 | FEMA FNSS Nov 2010 via Missouri SEMA public PDF | **Authorized full text verified locally**; sha256 in `authorized_source_status.csv` |

Coding FNSS as Phase-B comparator requires adoption of `PA-DRAFT-002` (OPT-B/C). Until then calibration remains **NO_GO**.

## Forbidden

- Sci-Hub / pirate mirrors  
- Unauthorized PDFs  
- Silent substitution with DSIL/CMIST training PDFs without protocol amendment

## Ready-to-send requests

- `docs/phase_b/access_requests/PERM-CF02-001_publisher.md`  
- `docs/phase_b/access_requests/ILL-CF02-001_library.md`  
- `docs/phase_b/access_requests/AUTH-CF02-001_author.md`  
