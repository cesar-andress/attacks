# Next human actions — Phase B coder readiness

## CURRENT BLOCKER

**No independent coder has been recruited and qualified.**

Methodological governance is complete:

- Attempt policy **ADOPTED** (`QUAL-ATTEMPT-v1`)  
- Qualification freeze **AUTHORIZED** (`QUAL-FREEZE-v1`)  
- OV-05 **PASS** (UCW-004 closed)  
- Target package **SEALED**

Principal open human/administrative item:

- `UCW-003` — compensation and recruitment channel (**Decision pending**)  
  Record: `docs/operations/UCW-003_decision_record.md`  
  Machine status remains `open_human` / `TO_BE_SET_BY_HUMAN` until the human closes that record.

Editorial/reliability work (`PA-2026-07-31-003`) does **not** block recruitment: qualification materials remain frozen; coder instructions unchanged; target remains SEALED.

Execution index: `docs/operations/README.md`  
Dashboard: `data/operations/execution_dashboard.csv`

## NEXT HUMAN ACTIONS

1. **Complete UCW-003 decision fields** — channel, compensation model/amount/timing, eligibility notes, withdrawal/replacement.  
2. **Recruit** using `docs/operations/recruitment/` (do not invent a candidate).  
3. **Screen + COI** — `forms/independence_coi_form.md` + `coi_decision_guide.md`; signed copy → `private/coder_admin/` only.  
4. **Confidentiality** — `IC-CONF-v1` + secure-handling instructions.  
5. **Onboard** — follow `docs/operations/onboarding/onboarding_checklist.md` gates in order.  
6. **Train** — release training package; complete `training_completion_record.md`.  
7. **Qualify** — authorize attempt; deliver frozen qualification package; score; apply `QUAL-ATTEMPT-v1` (max two valid attempts; no answer-key disclosure).  
8. **Activate READY only if controls pass** — `qualification_decision_rules.md` + activation checklist.  
9. **Calibration** — `docs/operations/calibration/runbook.md` (gate remains NO_GO until done).  
10. **Corpus freeze** — only after authorized path; `corpus_freeze/runbook.md`.  
11. **Independent coding → reliability → adjudication → analysis** — use coding/reliability/adjudication/analysis runbooks.  
12. **Write Results/Discussion/Conclusion** only after analytical outputs exist.

## Commands

```bash
python -m school_security_audit.validate_coder_workflow
python -m school_security_audit.validate_operations
python -m school_security_audit.check_training_overlap
make release-check
```

## Do not

- Fabricate coder names, scores, or READY  
- Prefill `phase_b_target_codes.csv`  
- Change frozen qualification artifacts without a formal amendment  
- Open corpus freeze or full coding prematurely  
- Treat FNSS as gold-standard validation  
- Use CF-02 as operational L1  
- Invent empirical Results or α  
