# Phase-A recoding decision rule (formalized; not executed)

**Trigger window:** After Phase-B double coding, pre-adjudication reliability, and BDD adjudication.

| Outcome | When | Actions |
|---|---|---|
| `no_action` | BDD clarifies wording only; Phase-A codes remain valid | Document decision; preserve values |
| `clarification_no_code_change` | Memo/definition clarified; codes unchanged | Amendment note optional |
| `local_phase_a_recode` | Few units affected by a rule change | Preserve pre-change values; recode listed units; log |
| `systematic_recode` | Rule change affects a class of units | Preserve pre-change archive; recode systematically; amendment |
| `codebook_amendment` | Instrument change required | Protocol amendment ID; then recode as required |

## Required record fields

See `data/phase_b/phase_a_recoding_decision_template.csv`.

## Prohibitions

- No Phase-A recode during this infrastructure task.  
- No recode without documented trigger.  
- CF-02 must not be used as primary operational evidence for BDD adjudication under OPT-B.
