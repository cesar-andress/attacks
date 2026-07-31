# Next human actions — Phase B coder readiness

## CURRENT BLOCKER

**No independent coder has been recruited and qualified.**

UCW-003 is **RESOLVED** (direct contact; voluntary unpaid; eligibility by protocol completion).  
Record: `docs/operations/UCW-003_decision_record.md`

Methodological governance remains complete:

- Attempt policy **ADOPTED** (`QUAL-ATTEMPT-v1`)  
- Qualification freeze **AUTHORIZED** (`QUAL-FREEZE-v1`)  
- OV-05 **PASS** (UCW-004 closed)  
- Target package **SEALED**  
- Independent coder **NOT_READY**  
- Calibration / corpus freeze / full coding **NO_GO**

Execution index: `docs/operations/README.md`  
Dashboard: `data/operations/execution_dashboard.csv`

## NEXT HUMAN ACTIONS

1. **Recruit by direct contact** using `docs/operations/recruitment/` (do not invent a candidate in the public repo).  
2. **Screen + COI** — `forms/independence_coi_form.md` + `coi_decision_guide.md`; signed copy → `private/coder_admin/` only.  
3. **Confidentiality** — `IC-CONF-v1` + secure-handling instructions.  
4. **Onboard** — follow `docs/operations/onboarding/onboarding_checklist.md` gates in order.  
5. **Train** — release training package; complete `training_completion_record.md`.  
6. **Qualify** — authorize attempt; deliver frozen qualification package; score; apply `QUAL-ATTEMPT-v1`.  
7. **Activate READY only if controls pass** — `qualification_decision_rules.md` + activation checklist.  
8. **Calibration** — `docs/operations/calibration/runbook.md` (gate remains NO_GO until done).  
9. **Corpus freeze → independent coding → reliability → adjudication → analysis** as authorized.  
10. **Write Results/Discussion/Conclusion** only after analytical outputs exist.

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
