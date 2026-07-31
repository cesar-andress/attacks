# UCW-003 decision record: compensation and recruitment channel

| Field | Value |
|---|---|
| Issue identifier | UCW-003 |
| Topic | Compensation model and recruitment channel for the independent coder |
| Date opened | 2026-07-31 |
| Decision owner | Project owner / PI (human) |
| Status | **UNRESOLVED** (Decision pending) |
| Blocks | Active recruitment packaging with concrete pay/channel; coder READY remains blocked |

This record enables a human decision. It does **not** select financial terms.

## Decision fields (to be completed before recruitment)

| Decision | Selected option | Notes |
|---|---|---|
| Recruitment channel | Not yet selected | e.g. university list, professional network, open call |
| Compensation model | Not yet selected | e.g. honorarium, hourly, unpaid voluntary |
| Compensation amount or range | Not yet selected | Currency and gross amount |
| Payment timing | Not yet selected | e.g. after qualification; after Phase-B coding; milestone |
| Expected workload statement | Not yet selected | Align with role description (training 4-8 h; Phase B 1-3 days) |
| Candidate eligibility notes | Not yet selected | Beyond independence/COI rules |
| COI exclusions (local extras) | Not yet selected | Optional additions to standard COI form |
| Confidentiality extras | Not yet selected | Optional institutional clauses |
| Withdrawal / replacement procedure | Not yet selected | Confirm or amend default in onboarding docs |
| Implementation date | Not yet selected | |
| Rationale | Not yet selected | |
| Downstream files affected when closed | `coder_role_admin.md`; recruitment announcement; candidate info sheet; dashboard | |

## Options considered (illustrative; not selected)

### A. Institutional / university channel with honorarium
- Advantages: clearer contracting path; easier eligibility screening.  
- Risks: procurement delay; tax/employment classification review.

### B. Professional network direct invitation with fixed honorarium
- Advantages: faster; known skill fit.  
- Risks: independence optics; smaller pool.

### C. Open call (association list / research board) with posted range
- Advantages: broader pool; transparent terms.  
- Risks: screening volume; confidentiality hygiene.

### D. Unpaid voluntary research assistance
- Advantages: no payment logistics.  
- Risks: retention; institutional volunteer rules; fairness.

## Non-contingent compensation principle

Compensation must **not** depend on qualification pass/fail or on producing a preferred reliability outcome. Payment may depend only on completed authorized work stages.

## Closure rule

When the owner completes the decision fields above:

1. set this Status to `RESOLVED`;  
2. update `data/phase_b/unresolved_coder_workflow_items.csv` UCW-003 to `closed` with the chosen resolution text;  
3. update recruitment materials with concrete channel/pay wording;  
4. update `data/operations/execution_dashboard.csv`;  
5. re-run `make release-check`.

Until then, validators must keep UCW-003 as `open_human`.
