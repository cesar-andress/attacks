# Codebook v0.1 (human-readable)

**Status:** draft  
**Machine-readable source:** [`codebook_v0.1.yaml`](codebook_v0.1.yaml)

> **Examples disclaimer.** Every example below is a **constructed illustration** for coder calibration. None is a quotation from a real framework.

## Conventions

- **Levels:** L0 framework · L1 document · L2 prescriptive element (PE)
- **Branches:** E (executability) and F (detectability) stay separate — no combined inclusive-security score
- **Family C sources:** for each demand, store `demand_source ∈ {explicit, entailed, ambiguous_memo}`; only `explicit` and `entailed` count in confirmatory analyses
- **Executability:** rung (0–5) × locus (`individual` | `subgroup` | `setting` | `multiple` | `not_specified`) are orthogonal

## Family A — Framework metadata and scope

| Code | Label | Level | Values |
|---|---|---|---|
| A1 | authority_type | L0 | government · professional_association · peer_reviewed · other |
| A2 | primary_domain | L0 | physical_security · btam · eop · active_assailant_response · cpted · accessibility_afn · other |
| A3 | intended_setting_scope | L0 | free text; use `unspecified` if silent |

## Family B — Security measures prescribed

| Code | Label | Level | Values |
|---|---|---|---|
| B1 | measure_present | L2 | 0 / 1 |
| B2 | measure_type | L2 | physical_target_hardening · procedural_response · behavioural_threat_assessment · environmental_cpted · communication_alerting · training_drill · other |
| B3 | prescriptive_force | L2 | required · recommended · optional · unspecified |

## Family C — Procedural demands (draft taxonomy)

These are **not** final validated constructs.

| Code | Label | Confirmatory? |
|---|---|---|
| C1 | demand_alert_perception | confirmatory |
| C2 | demand_instruction_comprehension | confirmatory |
| C3 | demand_decision_making | exploratory |
| C4 | demand_emergency_communication | confirmatory |
| C5 | demand_inhibitory_acoustic | confirmatory |
| C6 | demand_inhibitory_movement | confirmatory |
| C7 | demand_behavioural_sensory_regulation | exploratory |
| C8 | demand_physical_execution | confirmatory |
| C9 | demand_temporal_endurance | confirmatory |
| C10 | demand_responder_interaction | confirmatory |

For each `C*` demand present (`1`), also record:

- `demand_*_source`
- `demand_*_trigger` (required when source = `entailed`)

## Family D — Contextual supports

| Code | Label | Values |
|---|---|---|
| D1 | support_present | 0 / 1 |
| D2 | support_demand_link | 0 / 1 / unlinked / not_applicable |

## Family E — Protective-action executability

| Rung | Meaning |
|---|---|
| 0 | Not addressed |
| 1 | Prescription only |
| 2 | Support or accommodation specified |
| 3 | Executability explicitly assessed |
| 4 | Executability tested under realistic conditions |
| 5 | Test findings used to revise or adapt the measure |

| Code | Label | Values |
|---|---|---|
| E1 | executability_rung | 0–5 |
| E2 | executability_locus | individual · subgroup · setting · multiple · not_specified |

Report the joint rung × locus distribution; do not collapse to a single mean.

## Family F — Threat detectability

| Code | Label | Values |
|---|---|---|
| F1 | detection_mechanism_present | 0 / 1 |
| F2 | baseline_interpretation_addressed | 0 / 1 |
| F3 | specialist_participation | absent · optional · required |
| F4 | false_positive_safeguard | 0 / 1 |

Directional-harm rule: absence of F4 is coded `0`, never inferred as endorsement of over-referral.

## Family G — Population and setting differentiation

| Code | Label | Values |
|---|---|---|
| G1 | setting_differentiation | none · mentions_difference · differentiated_guidance |
| G2 | population_capability_variance_acknowledged | 0 / 1 |

## Family H — Evidence, testing, and validation

| Code | Label | Values |
|---|---|---|
| H1 | evidence_basis | none_or_expert_opinion · cites_research · reports_own_validation |
| H2 | executability_evidence | 0 / 1 |

## Family I — Security–accessibility conflicts

| Code | Label | Values |
|---|---|---|
| I1 | conflict_acknowledged | 0 / 1 |
| I2 | conflict_resolution_offered | 0 / 1 |

## Full field definitions

See [`codebook_v0.1.yaml`](codebook_v0.1.yaml) for definition, inclusion/exclusion rules, and constructed examples for every code.
