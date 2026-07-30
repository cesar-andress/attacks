# Next human actions — Phase B coder readiness

## CURRENT BLOCKER

**No independent coder has been recruited and qualified.**

Infrastructure is ready; human decisions and attestations are not.

Also open:

- `UCW-001` — adopt qualification attempt policy (`docs/phase_b/independent_coding/attempt_policy_DRAFT.md`)  
- `UCW-002` — authorize qualification freeze (`data/phase_b/qualification_freeze_record.csv`)  
- `UCW-003` — set compensation and recruitment channel (`TO_BE_SET_BY_HUMAN`)

## NEXT HUMAN ACTIONS

1. **Choose compensation and recruitment route** — edit admin notes only: `docs/phase_b/independent_coding/admin/coder_role_admin.md`  
2. **Identify candidate** — store identity only in gitignored `private/coder_admin/`  
3. **Assign provisional opaque coder ID** — do not invent a pass result  
4. **Complete eligibility screening** — `docs/phase_b/independent_coding/forms/independence_coi_form.md`  
5. **Complete COI** — signed copy → `private/coder_admin/` only  
6. **Complete confidentiality agreement** — `docs/phase_b/independent_coding/forms/confidentiality_agreement.md`  
7. **Approve or reject candidate** — human review fields; keep public manifest honest  
8. **Adopt attempt policy + authorize freeze** — close UCW-001/UCW-002; set `human_authorized=true` only when true  
9. **Deliver training** — `python -m school_security_audit.generate_coder_package --type pre_qualification`  
10. **Record training completion** — admin manifest (private or controlled)  
11. **Deliver qualification** — `--type qualification` (blocked until freeze auth + adopted policy)  
12. **Receive and lock submission** — hash; set attempt number; store outside public git if PII  
13. **Run scorer** — `python -m school_security_audit.phase_b_qualification SUBMISSION.csv --json --coder-id CODER_X --attempt 1`  
14. **Review result** — scorer pass ≠ READY  
15. **Mark coder READY only if all controls pass** — see `qualification_decision_rules.md`  
16. **Open target package** — set seal OPEN in execution manifest only after READY  
17. **Begin independent unitization/coding** — blank templates in `data/phase_b/unitization_template.csv` / coding schema; no prefilled codes  

## Commands (infrastructure)

```bash
python -m school_security_audit.validate_coder_workflow
python -m school_security_audit.check_training_overlap
make release-check
```

## Do not

- Fabricate coder names, scores, or READY  
- Prefill `phase_b_target_codes.csv`  
- Open corpus freeze or full coding  
- Treat FNSS as gold-standard validation
- Use CF-02 as operational L1  
