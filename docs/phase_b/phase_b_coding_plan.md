# Phase-B coding plan (not executed)

## Sources required

**Primary path (current recommendation):** ALT-FNSS-001 after adoption of PA-DRAFT-002.  
**Alternate/dual:** DOC-CF02-01 if `CF02_ACCESS_GO`.  
**Forbidden:** silent DSIL/CMIST training PDFs; pirate copies.

## Procedure

1. Confirm amendment status and authorized checksum.  
2. Assign ≥2 independent qualified human coders (`CODER_A` may be PI; second must be independent).  
3. Independent unitization → PE table with source locations (page/section).  
4. Blinded raw coding into separate files:  
   `data/pilot/phase_b/coding_<coder_id>_raw.csv` (create at execution; not pre-populated).  
5. Compute pre-consensus reliability.  
6. Adjudicate disagreements; archive raw immutably.  
7. Resolve BDD-001…005 with evidence notes.  
8. Codebook amendments if needed; Phase-A recode only if required.  
9. Update pilot completion report; run validators.

## File naming

- `prescriptive_elements_phase_b.csv`  
- `coding_phase_b_<CODER_ID>_raw.csv`  
- `coding_phase_b_adjudicated.csv`  
- `disagreement_log_phase_b.csv`

## Exclusions

- Training and qualification cases never enter Phase-B α.  
- Simulated procedural second pass never counted as independent coding.  
- `data/phase_b/phase_b_target_codes.csv` must remain empty until execution.

## Restricted excerpts

Short stems only in public CSVs; full text stays in `local_sources/` (gitignored).
