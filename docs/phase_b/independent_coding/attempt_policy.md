# Qualification attempt and retraining policy (adopted)

**Policy ID:** `QUAL-ATTEMPT-v1`  
**Status:** **ADOPTED**  
**Adopted:** 2026-07-31  
**Authority:** Protocol steward / repository change-control (methodological governance)  
**Linked amendment / freeze:** `PA-2026-07-31-002` · `QUAL-FREEZE-v1`  
**Supersedes:** `QUAL-ATTEMPT-DRAFT-v1` (`attempt_policy_DRAFT.md`, retained as history)

This policy is frozen with the qualification materials. Changes require a formal protocol amendment and a new freeze version.

## Rules

| Topic | Adopted rule |
|---|---|
| Maximum attempts | **2** (attempt 1 + at most one retrain attempt) |
| Attempt 2 set | Must use a **different** qualification-set version (e.g. `QUAL-SET-v2`); reuse of `QUAL-SET-v1` is prohibited |
| Answer-key release | Answer keys are **never** released case-by-case to the coder |
| Retraining content | May explain coding **principles** and process feedback; must **not** reveal qualification or Phase-B target answers |
| Answer-key exposure | Any demonstrated exposure to the answer key **invalidates** that qualification set for the exposed person; a new set version is required |
| Technical failures | Demonstrated technical failures (malformed delivery, corrupted file, identity/system mismatch not caused by coder gaming) yield `QUALIFICATION_INVALID` and **do not count** as a failed attempt |
| Failure of attempt 2 | `QUALIFICATION_FAIL_FINAL` — no further attempt under this policy without a new amendment |
| Withdrawal | Coder may withdraw anytime; locked submissions remain archived under opaque ID |
| Material COI / idle | Material COI change or >90 days idle → new COI/confidentiality before a further attempt |

## States

See `qualification_decision_rules.md`. Scorer pass alone never sets `INDEPENDENT_CODER=READY`.
