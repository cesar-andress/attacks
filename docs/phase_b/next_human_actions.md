# Next human actions — Phase B coder readiness

## CURRENT BLOCKER

**No independent coder has been recruited and qualified.**

Methodological governance is complete:

- Attempt policy **ADOPTED** (`QUAL-ATTEMPT-v1`)  
- Qualification freeze **AUTHORIZED** (`QUAL-FREEZE-v1`)  
- OV-05 **PASS** (UCW-004 closed)  
- Target package **SEALED**

Remaining open item that is genuinely human/administrative:

- `UCW-003` — compensation and recruitment channel (`TO_BE_SET_BY_HUMAN`)

## NEXT HUMAN ACTIONS

1. **Choose compensation and recruitment route** — `docs/phase_b/independent_coding/admin/coder_role_admin.md` (`TO_BE_SET_BY_HUMAN`)  
2. **Identify candidate** — identity only in gitignored `private/coder_admin/`  
3. **Assign provisional opaque coder ID** — do not invent a pass result  
4. **Complete eligibility screening** — `forms/independence_coi_form.md`  
5. **Complete COI** — signed copy → `private/coder_admin/` only  
6. **Complete confidentiality agreement** — `forms/confidentiality_agreement.md`  
7. **Approve or reject candidate** — human review; keep public manifest honest  
8. **Deliver training** — `python -m school_security_audit.generate_coder_package --type pre_qualification`  
9. **Record training completion**  
10. **Deliver qualification** — `--type qualification` (freeze authorized; policy adopted)  
11. **Receive and lock submission** — hash; attempt number  
12. **Run scorer** — `python -m school_security_audit.phase_b_qualification SUBMISSION.csv --json --coder-id CODER_X --attempt 1`  
13. **Review result** — scorer pass ≠ READY  
14. **Mark coder READY only if all controls pass** — `qualification_decision_rules.md`  
15. **Open target package** — seal → OPEN only after READY  
16. **Begin independent unitization/coding**

## Commands

```bash
python -m school_security_audit.validate_coder_workflow
python -m school_security_audit.check_training_overlap
make release-check
```

## Do not

- Fabricate coder names, scores, or READY  
- Prefill `phase_b_target_codes.csv`  
- Change frozen qualification artifacts without a formal amendment  
- Open corpus freeze or full coding  
- Treat FNSS as gold-standard validation  
- Use CF-02 as operational L1  
