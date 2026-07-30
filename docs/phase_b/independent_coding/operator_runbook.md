# Operator runbook — independent coder → Phase-B readiness

**Audience:** PI / protocol steward  
**Do not** mark a real coder as passed without locked evidence.

---

### Step 0 — Validate infrastructure

- **Prerequisite:** OPT-B adopted; source READY  
- **Command:** `make release-check` and `python -m school_security_audit.validate_coder_workflow`  
- **Expected:** OK; `INDEPENDENT_CODER=NOT_READY`; target SEALED  
- **Failure:** fix validators; do not recruit on red build  
- **Next:** Step 1  

### Step 1 — Adopt attempt policy

- **Human action:** Adopt or revise `attempt_policy_DRAFT.md`; close UCW-001  
- **Evidence:** freeze record + unresolved items CSV  
- **Failure:** leave DRAFT → READY remains false  

### Step 2 — Authorize qualification freeze

- **Human action:** Confirm QUAL-SET-v1 cases, reference, scorer version, thresholds unchanged  
- **Command:** record authorization in `data/phase_b/qualification_freeze_record.csv` (`human_authorized=true` only when true)  
- **Failure:** do not deliver qualification pack  

### Step 3 — Recruit

- **Human action:** checklist steps 1–9  
- **Evidence:** signed forms in `private/coder_admin/` only  

### Step 4 — Generate pre-qualification package

- **Command:** `python -m school_security_audit.generate_coder_package --type pre_qualification --out data/phase_b/generated_packages`  
- **Expected:** manifest + checksums; forbidden-file scan clean  
- **Failure:** overlap or answer-key detection → do not send  

### Step 5 — Training completion

- **Human action:** attest training completed in admin manifest  
- **Next state:** `TRAINING_COMPLETED`  

### Step 6 — Generate qualification package

- **Prerequisite:** freeze authorized; attempt policy adopted  
- **Command:** `--type qualification`  
- **Failure:** generator refuses if freeze not authorized  

### Step 7 — Ingest submission

- **Human action:** receive CSV; copy to controlled path; compute sha256; set attempt number  
- **Command:** `python -m school_security_audit.phase_b_qualification path/to/submission.csv`  
- **Expected:** JSON-like dict with versions; pass/fail  
- **Do not** edit submission after lock  

### Step 8 — Human review

- **Human action:** confirm COI/confidentiality/training/scorer; set review status  
- **READY only if** all criteria in `qualification_decision_rules.md`  

### Step 9 — Open target package (after READY)

- **Command / action:** set `target_package_seal_status=OPEN` in execution manifest only after READY  
- **Validator:** fails if OPEN while coder not ready  

### Step 10 — Independent unitization + coding

- Follow `phase_b_coding_plan.md` (amended OPT-B).  
- Separate files per coder; lock both before reliability.  

### Step 11 — Reliability (pre-adjudication)

- Synthetic pipeline checks only until real locks exist.  
- **Forbidden:** reliability on adjudicated values.  

### Step 12 — BDD adjudication → Phase-A recode decision → completion report

- Blank BDD records until then.  

### Rollback

If leakage or COI failure discovered: set coder REJECTED; reseal target; open incident; do not delete locked evidence.
