# CF-02 / AFN access route log

**Date of agent checks:** 2026-07-31  
**Machine table:** `data/phase_b/access_routes.csv`  
**Rule:** Do not claim access until the full article/PDF has been opened and verified.

## Summary

| Target | Result |
|---|---|
| Kailes & Enders 2007 (CF-02) | **CF02_ACCESS_NO_GO** — closed OA (Unpaywall + OpenAlex); SAGE PDF not opened |
| FEMA FNSS 2010 (ALT-FNSS-001) | **Authorized full text verified locally** (state EMA redistribution of FEMA guidance); checksum recorded |
| ASPR CMIST web explainers | Citation/background only |

## Forbidden routes

Pirate repositories, credential sharing, access-control bypass, unauthorized mirrors — **not used** (AR-CF02-009).

## Human actions still required for CF-02

1. UCJC library discovery / SAGE subscription (AR-CF02-005).  
2. Interlibrary loan using prepared request (AR-CF02-006).  
3. Author-authorized manuscript request if lawful (AR-CF02-007).  
4. Publisher permissions portal using `PERM-CF02-001` pack (AR-CF02-008).

Agent environment cannot complete institutional login or send email.
