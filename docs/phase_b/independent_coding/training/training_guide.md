# Coder training guide (rules only)

**Version:** `TRAIN-v1`  
**Access:** PRE_QUALIFICATION_SAFE  
**Comparator roles (OPT-B):** CF-02 = conceptual; FEMA FNSS = operational L1 to be coded after qualification. Comparator ≠ gold standard.

This guide teaches **coding rules**. It does not state expected study findings, hypotheses, or how any document “should” score.

## 1. Documentary focus

The study audits **text**. Codes describe documentary engagement with executability, not whether people can perform actions in the field and not whether measures are effective.

## 2. Prescription vs executability engagement

A text may prescribe an action without engaging supports, assessment, testing, or revision. Engagement depth is coded on the ladder (0–5) as the highest ordinal depth evidenced in the document for that PE.

## 3. PE unit definition (L2)

A PE is a segmentable statement that prescribes an action, mandates a control, or poses an assessment question such that a planner/operator could comply or not. Narrative rationale and bare definitions are not PEs.

## 4. Unitization

- Split separable actions when each can be complied with independently.  
- Do not merge unrelated prescriptions to inflate depth.  
- Record source location (section/page) for every PE.  
- Unitizing is itself a coding decision.

## 5. L0 / L1 / L2

- L0 = framework/package candidate.  
- L1 = versioned document artefact.  
- L2 = PE (primary coding unit).

## 6. Demand source

| Value | Meaning |
|---|---|
| `explicit` | Named in text |
| `entailed` | Logically necessary under entailment rules, with trigger evidence |
| `ambiguous_memo` | Uncertain; memo only — **never** counts as presence |

## 7. Ladder (documentary depth)

0 not addressed · 1 prescription only · 2 support/accommodation · 3 assessed · 4 tested under realistic conditions (as directed) · 5 revised using evidence (as directed).  
Support ≠ assessment ≠ testing ≠ revision.

## 8. Locus (orthogonal)

`individual` | `subgroup` | `setting` | `multiple` | `not_specified`  
Locus situates engagement in the document; it does not diagnose occupants.

## 9. Comparator role

Function-based / AFN operational doctrine is coded with the **same** rules as school-security texts. It is a contrastive benchmark, not a positive control and not a gold standard.

## 10. Uncertainty and notes

Use `ambiguous_memo` and procedural notes when evidence is insufficient. Default under ambiguity: do not code presence.

## 11. What not to infer

- Occupant incapacity from silence.  
- Real-world execution from documentary testing language without the named activity.  
- Support from setting catalogs alone.  
- Branch B / threat-detectability material into confirmatory executability aggregates (Paper 1).

## 12. Practice materials

- Synthetic stimuli in `data/phase_b/qualification_cases.csv` (coder-facing stimuli only).  
- Public experiments `EXP-01` / `EXP-02` for additional practice.  
- Answer keys are **admin-only** and are not part of this guide.

## 13. After training

Complete the qualification exercise under timed/independent conditions as instructed. Do not seek answer keys.
