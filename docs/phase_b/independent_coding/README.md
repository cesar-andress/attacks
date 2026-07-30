# Independent-coder package (infrastructure)

**Status:** workflow implemented — **no real coder recruited or qualified**  
**Amendment:** `PA-2026-07-31-002` (OPT-B)  
**Gates:** `INDEPENDENT_CODER=NOT_READY` · `BENCHMARK_CALIBRATION=NO_GO` · target package **SEALED**

## Directory map

| Path | Access class | Purpose |
|---|---|---|
| [`coder_role.md`](coder_role.md) | RECRUITMENT_SAFE | Public-safe role description |
| [`admin/coder_role_admin.md`](admin/coder_role_admin.md) | ADMIN_ONLY | Admin fields (compensation TBD by human) |
| [`forms/independence_coi_form.md`](forms/independence_coi_form.md) | PRE_QUALIFICATION_SAFE | Independence + COI (blank) |
| [`forms/confidentiality_agreement.md`](forms/confidentiality_agreement.md) | PRE_QUALIFICATION_SAFE | Confidentiality / data handling |
| [`training/`](training/) | PRE_QUALIFICATION_SAFE | Rules-focused training (no expected outcomes) |
| [`qualification/`](qualification/) | QUALIFICATION_ONLY | Coder-facing qualification instructions |
| [`recruitment/`](recruitment/) | ADMIN_ONLY | Checklist + communication templates |
| [`operator_runbook.md`](operator_runbook.md) | ADMIN_ONLY | PI execution runbook |
| [`information_access_matrix.md`](information_access_matrix.md) | ADMIN_ONLY | Blinding matrix |
| [`procedural_query_protocol.md`](procedural_query_protocol.md) | POST_QUALIFICATION_SAFE | Neutral Q&A rules during coding |
| [`qualification_decision_rules.md`](qualification_decision_rules.md) | ADMIN_ONLY | State machine + READY criteria |
| [`attempt_policy_DRAFT.md`](attempt_policy_DRAFT.md) | ADMIN_ONLY | **Draft** — readiness blocked until human adopts |
| [`phase_a_recoding_rule.md`](phase_a_recoding_rule.md) | ADMIN_ONLY | Recode decision rule (not executed) |
| [`integrity_red_team.md`](integrity_red_team.md) | ADMIN_ONLY | Integrity risks / mitigations |
| [`coi_confidentiality.md`](coi_confidentiality.md) | SUPERSEDED_POINTER | Points to new forms |
| [`recruitment.md`](recruitment.md) | SUPERSEDED_POINTER | Points to recruitment/ |

## Machine-readable registers

Under `data/phase_b/`: package manifest, admin template, qualification freeze, overlap report, target seal, execution manifest, unresolved items.

## Commands

```bash
python -m school_security_audit.validate_coder_workflow
python -m school_security_audit.check_training_overlap
python -m school_security_audit.generate_coder_package --type recruitment --dry-run
python -m school_security_audit.phase_b_qualification data/phase_b/synthetic_qualification_pass.csv
```

## Forbidden in this package

- Real coder names, signatures, scores, or pass decisions  
- Prefill of Phase-B target codes  
- Opening the target package before READY  
- Directional RQ4 / “FNSS should score higher” cues  
