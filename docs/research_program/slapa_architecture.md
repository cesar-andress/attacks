# SLAPA architecture (programme-level)

**Working name:** School Lone-Actor Preparedness Assessment  
**Acronym:** SLAPA  
**Status:** `planned_unvalidated` architecture — **not** an implemented or validated instrument  
**Machine-readable domains:** `slapa_domains.csv`

## Purpose

Provide a multidimensional **organisational** assessment architecture for educational centres facing lone-actor and related acute threats, sensitive to diverse functional needs, without a single total preparedness rank.

## Non-goals

- No questionnaire items in this document.  
- No scoring algorithm.  
- No psychometric validity claims.  
- No combined inclusive-security score.  
- No pupil-level dangerousness assessment.

## Domain structure

| ID | Domain |
|---|---|
| A | Governance and doctrine adoption |
| B | Organisational sensing and threat detectability |
| C | Decision authority and interagency coordination |
| D | Protective-action executability |
| E | Inclusive access and functional supports |
| F | Security-by-design and environmental conditions |
| G | Training, exercises, and organisational learning |
| H | Evidence use and revision |

Domains produce **profiles**, not a single rank. Domain B is theoretically independent of D (see `branch_b_detectability.md`).

## Evidence levels (must not be collapsed)

| Level | Meaning | Primary papers |
|---|---|---|
| Document content | What doctrine/local text says | RP-P1 (authoritative); local docs in later papers |
| Organisational adoption | Whether provisions are taken up locally | RP-P2/P3 |
| Organisational capability | People, supports, authority, resources available | RP-P2/P3 |
| Individual perception | Staff/occupant beliefs (optional later module) | Not core SLAPA v1 |
| Observed performance | Drills/exercises (Layer 4) | RP-P3 |

See `evidence_layers.md`.

## Relationship to RP-P1

RP-P1 informs especially Domains **D, E, G, H** (and partially F) via documentary under-specification. RP-P1 does **not** populate SLAPA scores for any centre.

## Relationship to RP-P4

RP-P4 develops Domain **B** (and related safeguards). Domain B must never be averaged with Domain D into one index.
