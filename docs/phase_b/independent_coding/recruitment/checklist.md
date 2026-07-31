# Recruitment checklist (human-executable)

**Current blocker:** No independent coder has been recruited and qualified.

| Step | Action | Evidence path / command |
|---|---|---|
| 1 | Confirm UCW-003 terms | RESOLVED — direct contact; voluntary unpaid (`docs/operations/UCW-003_decision_record.md`) |
| 2 | Confirm eligibility criteria | `coder_role.md` |
| 3 | Identify candidate | Private notes only (`private/coder_admin/`) |
| 4 | Send role description | Template `recruitment/communication_templates.md` §invite |
| 5 | Screen prior involvement | Form `forms/independence_coi_form.md` |
| 6 | Assign candidate opaque ID (provisional) | `data/phase_b/coder_admin_manifest.csv` (after TEMPLATE row replaced carefully — still NOT_READY) |
| 7 | Complete COI | Signed copy → `private/coder_admin/` only |
| 8 | Complete confidentiality | Signed copy → `private/coder_admin/` |
| 9 | Approve or reject | Update machine status fields; never invent APPROVE in git without human |
| 10 | Freeze qualification materials | Human authorize freeze record; adopt attempt policy |
| 11 | Deliver pre-qualification / training pack | `python -m school_security_audit.generate_coder_package --type pre_qualification` |
| 12 | Record training completion | Admin manifest — human date |
| 13 | Deliver qualification pack | `--type qualification` (only after freeze auth) |
| 14 | Receive submission | Store under `data/phase_b/coder_submissions/` locally; prefer gitignored |
| 15 | Lock submission | Hash file; set attempt number |
| 16 | Run scorer | `python -m school_security_audit.phase_b_qualification <submission.csv>` |
| 17 | Review result | Human review field |
| 18 | Seal or open target | Target remains SEALED until READY; then explicit open |

Do not mark READY in `PILOT_STATUS.txt` until every readiness criterion in `qualification_decision_rules.md` is met.
