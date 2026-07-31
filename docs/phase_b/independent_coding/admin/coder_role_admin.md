# Independent coder — admin-only role notes

**Access:** ADMIN_ONLY — do not include in coder-facing packages.

Operational decisions (channel, compensation, timing, eligibility exclusions) are recorded in:

`docs/operations/UCW-003_decision_record.md`

| Field | Value |
|---|---|
| Compensation | Decision pending (UCW-003) |
| Recruitment channel | Decision pending (UCW-003) |
| Human contact | Decision pending (UCW-003) |
| Local PII store | `private/coder_admin/` (gitignored; never commit) |
| Public ID scheme | `CODER_B`, `CODER_C`, … (opaque) |
| CODER_A convention | May be PI for dual coding; second coder must be independent |

Machine-readable UCW-003 status remains `open_human` with `resolution_condition=TO_BE_SET_BY_HUMAN` in `data/phase_b/unresolved_coder_workflow_items.csv` until a human closes the decision record.

Do not invent employment, payment rates, affiliations, or candidate identities.
