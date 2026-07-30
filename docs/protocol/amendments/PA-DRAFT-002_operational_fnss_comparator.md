# DRAFT protocol amendment PA-DRAFT-002 — Operational FNSS comparator (OPT-B)

**Amendment ID:** `PA-DRAFT-002`  
**Date drafted:** 2026-07-31  
**Status:** **DRAFT_NOT_ADOPTED** — recommendation only  
**Parent:** PA-2026-07-31-001 (two-phase pilot)

## 1. Purpose

Authorize Phase-B benchmark calibration to use **ALT-FNSS-001** (FEMA FNSS November 2010) as the operational coded comparator L1, while retaining **CF-02** (Kailes & Enders 2007) as the conceptual / bibliographic function-based source.

## 2. Why not silent substitution

CF-02 remains the original sole comparator. This draft changes the **coding** comparator only if adopted, with explicit limitations.

## 3. Proposed Phase-B sample

| Role | Source |
|---|---|
| Conceptual AFN / anti-deficit citation | CF-02 (bibliographic; code only if authorized full text later obtained) |
| Operational coded comparator | ALT-FNSS-001 / proposed `DOC-ALT-FNSS-001` |
| Checksum | `ab21f61b8ee451adb5cb6ca79dabf3305cdaea4a742ed7478b42ef6becf464a7` |

## 4. Declared limitations

- FNSS targets general-population **shelters**, not schools.  
- RQ4 contrasts are bounded to function-based emergency-planning doctrine, not school-specific AFN manuals.  
- CMIST label is not required for function-based orientation.

## 5. Effects if adopted

- `benchmark_calibration_gate` may move toward GO only after independent coder qualification + coding execution criteria in `complete_pilot_exit_criteria.csv`.  
- BDD-001…005 to be resolved against FNSS (and CF-02 if later coded).  
- No change to Phase-A labels; recode Phase A only if BDD resolutions require it.  
- RP-P2 / SLAPA unchanged.

## 6. Adoption checklist (human)

- [ ] PI approves OPT-B (or OPT-C if CF-02 arrives)  
- [ ] Rename to `PA-YYYY-MM-DD-00N` and set status `adopted`  
- [ ] Update `document_registry.csv` with DOC-ALT-FNSS-001  
- [ ] Update `pilot_source_readiness.csv` / gates only when coding-ready  
- [ ] Log in `amendment_log.csv`

**Until adoption: BENCHMARK_CALIBRATION = NO_GO.**
