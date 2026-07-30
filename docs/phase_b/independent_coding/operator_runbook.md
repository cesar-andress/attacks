# Operator runbook — independent coder → Phase-B readiness

**Audience:** PI / protocol steward  
**Do not** mark a real coder as passed without locked evidence.

**Governance status:** attempt policy **ADOPTED**; qualification freeze **AUTHORIZED** (`QUAL-FREEZE-v1`).

---

### Step 0 — Validate infrastructure

- **Prerequisite:** OPT-B adopted; source READY; freeze AUTHORIZED  
- **Command:** `make release-check` and `python -m school_security_audit.validate_coder_workflow`  
- **Expected:** OK; `INDEPENDENT_CODER=NOT_READY`; target SEALED; freeze checksums match  
- **Failure:** fix validators; do not recruit on red build  
- **Next:** Step 1  

### Step 1 — Set human admin fields

- **Human action:** compensation + recruitment channel (`TO_BE_SET_BY_HUMAN` in admin role notes); close process aspects of UCW-003 when set  
- **Evidence:** private admin notes only  

### Step 2 — Recruit

- **Human action:** checklist steps (identity, COI, confidentiality, approve/reject)  
- **Evidence:** signed forms in `private/coder_admin/` only  

### Step 3 — Generate pre-qualification package

- **Command:** `python -m school_security_audit.generate_coder_package --type pre_qualification --out data/phase_b/generated_packages`  
- **Expected:** manifest + checksums; forbidden-file scan clean  
- **Failure:** overlap or answer-key detection → do not send  

### Step 4 — Training completion

- **Human action:** attest training completed  
- **Next state:** `TRAINING_COMPLETED`  

### Step 5 — Generate qualification package

- **Prerequisite:** freeze AUTHORIZED; attempt policy ADOPTED (both true)  
- **Command:** `--type qualification`  
- **Failure:** generator refuses if freeze/policy regress  

### Step 6 — Ingest submission

- **Human action:** receive CSV; copy to controlled path; compute sha256; set attempt number  
- **Command:** `python -m school_security_audit.phase_b_qualification path/to/submission.csv --json`  
- **Expected:** result dict with frozen versions; pass/fail  
- **Do not** edit submission after lock  
- **Attempt 2:** requires `QUAL-SET-v2` (new freeze/amendment) — not the same set  

### Step 7 — Human review

- **Human action:** confirm COI/confidentiality/training/scorer; set review status  
- **READY only if** all criteria in `qualification_decision_rules.md`  

### Step 8 — Open target package (after READY)

- **Action:** set `target_package_seal_status=OPEN` in execution manifest only after READY  
- **Validator:** fails if OPEN while coder not ready  

### Step 9 — Independent unitization + coding

- Follow `phase_b_coding_plan.md` (OPT-B). Separate files per coder; lock both before reliability.  

### Step 10 — Reliability → BDD → Phase-A recode decision → completion

- Pre-adjudication reliability only. Blank BDD until then.  

### Rollback

If leakage or COI failure: set coder REJECTED; reseal target; open incident; do not delete locked evidence.  
If frozen artifacts must change: formal amendment + new freeze version — never silent edit.
