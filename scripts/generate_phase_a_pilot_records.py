#!/usr/bin/env python3
"""Generate Phase A operational pilot PE/coding/adjudication artefacts.

Copyright-safe: public CSVs use reference locations + short redacted stems.
Full short excerpts go only under gitignored local_sources/pilot_coding/.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "data/pilot"
LOCAL = ROOT / "local_sources/pilot_coding"
LOCAL.mkdir(parents=True, exist_ok=True)

FLAGS = {
    "pilot_flag": "PILOT",
    "inference_flag": "NOT_FOR_SUBSTANTIVE_INFERENCE",
    "benchmark_flag": "NOT_FOR_BENCHMARK_COMPARISON",
    "protocol_flag": "PROTOCOL_DEVELOPMENT_ONLY",
    "pilot_phase": "A_operational",
    "sample_role": "operational_pilot_sample",
    "analysis_scope": "branch_a_executability",
}

PE_HEADERS = [
    "pe_id",
    "document_id",
    "candidate_id",
    "pilot_id",
    "acquisition_id",
    "source_location",
    "page_number",
    "section_heading",
    "verbatim_trigger_text",
    "excerpt_policy",
    "local_excerpt_ref",
    "coder_segmentation_notes",
    "measure_present",
    "measure_type",
    "prescriptive_force",
    "unitization_ambiguity",
    "setting_differentiation_surface",
    "pilot_phase",
    "sample_role",
    "pilot_flag",
    "inference_flag",
    "benchmark_flag",
    "protocol_flag",
]

CODING_HEADERS = [
    "coder_id",
    "coding_round",
    "codebook_version",
    "pe_id",
    "measure_type",
    "prescriptive_force",
    "demand_alert_perception",
    "demand_alert_perception_source",
    "demand_alert_perception_trigger",
    "demand_instruction_comprehension",
    "demand_instruction_comprehension_source",
    "demand_instruction_comprehension_trigger",
    "demand_decision_making",
    "demand_decision_making_source",
    "demand_decision_making_trigger",
    "demand_emergency_communication",
    "demand_emergency_communication_source",
    "demand_emergency_communication_trigger",
    "demand_inhibitory_acoustic",
    "demand_inhibitory_acoustic_source",
    "demand_inhibitory_acoustic_trigger",
    "demand_inhibitory_movement",
    "demand_inhibitory_movement_source",
    "demand_inhibitory_movement_trigger",
    "demand_behavioural_sensory_regulation",
    "demand_behavioural_sensory_regulation_source",
    "demand_behavioural_sensory_regulation_trigger",
    "demand_physical_execution",
    "demand_physical_execution_source",
    "demand_physical_execution_trigger",
    "demand_temporal_endurance",
    "demand_temporal_endurance_source",
    "demand_temporal_endurance_trigger",
    "demand_responder_interaction",
    "demand_responder_interaction_source",
    "demand_responder_interaction_trigger",
    "support_present",
    "support_demand_link",
    "executability_rung",
    "executability_locus",
    "detection_mechanism_present",
    "baseline_interpretation_addressed",
    "specialist_participation",
    "false_positive_safeguard",
    "conflict_acknowledged",
    "conflict_resolution_offered",
    "qualitative_memo",
    "adjudication_status",
    "adjudicated_value",
    "pilot_phase",
    "sample_role",
    "pilot_flag",
    "inference_flag",
    "benchmark_flag",
    "protocol_flag",
    "analysis_scope",
    "coder_pass_type",
]


def blank_demands() -> dict[str, str]:
    out: dict[str, str] = {}
    for d in [
        "demand_alert_perception",
        "demand_instruction_comprehension",
        "demand_decision_making",
        "demand_emergency_communication",
        "demand_inhibitory_acoustic",
        "demand_inhibitory_movement",
        "demand_behavioural_sensory_regulation",
        "demand_physical_execution",
        "demand_temporal_endurance",
        "demand_responder_interaction",
    ]:
        out[d] = "0"
        out[f"{d}_source"] = ""
        out[f"{d}_trigger"] = ""
    return out


def demand(
    field: str, source: str, trigger: str = ""
) -> dict[str, str]:
    return {
        field: "1",
        f"{field}_source": source,
        f"{field}_trigger": trigger,
    }


def coding_row(
    *,
    coder_id: str,
    pe_id: str,
    measure_type: str,
    force: str,
    rung: str,
    locus: str,
    support: str = "0",
    support_link: str = "not_applicable",
    demands: dict[str, str] | None = None,
    memo: str = "",
    branch_b: str = "inactive",
    conflict_ack: str = "0",
    conflict_res: str = "0",
    pass_type: str = "primary_human",
    adj_status: str = "none",
    adj_value: str = "",
    analysis_scope: str | None = None,
) -> dict[str, str]:
    row = {h: "" for h in CODING_HEADERS}
    row.update(blank_demands())
    if demands:
        row.update(demands)
    row.update(
        {
            "coder_id": coder_id,
            "coding_round": "phase_a_operational",
            "codebook_version": "0.1.0",
            "pe_id": pe_id,
            "measure_type": measure_type,
            "prescriptive_force": force,
            "support_present": support,
            "support_demand_link": support_link if support == "1" else ("not_applicable" if support == "0" else support_link),
            "executability_rung": rung,
            "executability_locus": locus,
            "detection_mechanism_present": "" if branch_b == "inactive" else "0",
            "baseline_interpretation_addressed": "" if branch_b == "inactive" else "0",
            "specialist_participation": "" if branch_b == "inactive" else "absent",
            "false_positive_safeguard": "" if branch_b == "inactive" else "0",
            "conflict_acknowledged": conflict_ack,
            "conflict_resolution_offered": conflict_res,
            "qualitative_memo": memo,
            "adjudication_status": adj_status,
            "adjudicated_value": adj_value,
            "coder_pass_type": pass_type,
            **FLAGS,
        }
    )
    if analysis_scope:
        row["analysis_scope"] = analysis_scope
    if branch_b == "out_of_scope_mark":
        row["analysis_scope"] = "out_of_scope_branch_b_material_noted"
        row["detection_mechanism_present"] = ""
        row["qualitative_memo"] = (
            (memo + " | ").lstrip(" |")
            + "Threat-assessment language present; Family F inactive; not coded as Branch B presence."
        )
    return row


# --- Unitization catalogue (selection rule applied) ---
# Public verbatim_trigger_text: short redacted stem only (<=12 words) or empty.
# Full excerpts stored locally under EXCERPTS.

UNITS: list[dict] = [
    # P1 CF-16
    {
        "pe_id": "PE-OPA-CF16-01",
        "document_id": "DOC-CF16-01",
        "candidate_id": "CF-16",
        "pilot_id": "P1",
        "acquisition_id": "ACQ-P1-CF16-01",
        "page_number": "4",
        "section_heading": "Overview",
        "source_location": "PDF p.4 Overview bullet: security lead",
        "stem": "a ‘security’ lead should be appointed…",
        "excerpt": "a ‘security’ lead should be appointed to develop and maintain policies and plans which promote a good security culture",
        "notes": "Planning/role prescription; actor=settings; variation=planning requirement",
        "measure_type": "other",
        "force": "recommended",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(rung="1", locus="not_specified", support="0", memo="Role appointment; executability of protective actions not engaged beyond prescription."),
        "Bdiff": {"executability_rung": "1"},  # agreement on main
    },
    {
        "pe_id": "PE-OPA-CF16-02",
        "document_id": "DOC-CF16-01",
        "candidate_id": "CF-16",
        "pilot_id": "P1",
        "acquisition_id": "ACQ-P1-CF16-01",
        "page_number": "4",
        "section_heading": "Overview",
        "source_location": "PDF p.4 Overview bullet: SEND inclusive/accessible",
        "stem": "settings should consider what works best… SEND…",
        "excerpt": "settings should consider what works best for learners and staff with special educational needs and disabilities (SEND) to ensure that policies, plans and procedures are inclusive and accessible",
        "notes": "Generic consider/inclusive language — stress test support_present vs rung 2",
        "measure_type": "procedural_response",
        "force": "recommended",
        "unitization_ambiguity": "medium",
        "setting_diff": "1_subgroup_mention",
        "A": dict(
            rung="1",
            locus="subgroup",
            support="0",
            support_link="not_applicable",
            memo="Generic 'consider…inclusive and accessible' without named support → support_present=0; rung<=1 per codebook negative example pattern.",
        ),
        "Bdiff": {"support_present": "1", "executability_rung": "2", "executability_locus": "subgroup"},
    },
    {
        "pe_id": "PE-OPA-CF16-03",
        "document_id": "DOC-CF16-01",
        "candidate_id": "CF-16",
        "pilot_id": "P1",
        "acquisition_id": "ACQ-P1-CF16-01",
        "page_number": "4",
        "section_heading": "Overview",
        "source_location": "PDF p.4 Overview bullet: RUN HIDE TELL familiarisation",
        "stem": "all staff should familiarise themselves with RUN HIDE TELL…",
        "excerpt": "all staff should familiarise themselves with RUN HIDE TELL to ensure they can [respond]",
        "notes": "Multi-action protocol name; demands largely entailed from named protocol; cross-ref to later section",
        "measure_type": "procedural_response",
        "force": "recommended",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            demands={
                **demand("demand_decision_making", "entailed", "RUN HIDE TELL implies option choice"),
                **demand("demand_physical_execution", "entailed", "RUN/HIDE motor actions entailed by protocol name"),
                **demand("demand_instruction_comprehension", "entailed", "familiarise with multi-step protocol"),
            },
            memo="Overview-level citation of RUN HIDE TELL; inhibitory silence not explicit here → not coded without later explicit text in this PE.",
        ),
        "Bdiff": {
            "demand_inhibitory_acoustic": "1",
            "demand_inhibitory_acoustic_source": "entailed",
            "demand_inhibitory_acoustic_trigger": "HIDE often entails silence",
        },
    },
    {
        "pe_id": "PE-OPA-CF16-04",
        "document_id": "DOC-CF16-01",
        "candidate_id": "CF-16",
        "pilot_id": "P1",
        "acquisition_id": "ACQ-P1-CF16-01",
        "page_number": "4",
        "section_heading": "Overview",
        "source_location": "PDF p.4 Overview bullet: Lockdown Invacuation Evacuation",
        "stem": "educational settings should consider three response options…",
        "excerpt": "educational settings should consider three response options to a live incident: Lockdown, Invacuation and Evacuation",
        "notes": "Multi-option decision prescription; actor=settings",
        "measure_type": "procedural_response",
        "force": "recommended",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="setting",
            support="0",
            demands={
                **demand("demand_decision_making", "explicit", "three response options"),
                **demand("demand_instruction_comprehension", "entailed", "must distinguish lockdown/invacuation/evacuation"),
            },
            memo="Decision among named options; locus=setting because settings consider options.",
        ),
        "Bdiff": {"executability_locus": "not_specified"},
    },
    {
        "pe_id": "PE-OPA-CF16-05",
        "document_id": "DOC-CF16-01",
        "candidate_id": "CF-16",
        "pilot_id": "P1",
        "acquisition_id": "ACQ-P1-CF16-01",
        "page_number": "4",
        "section_heading": "Overview",
        "source_location": "PDF p.4 Overview bullet: PEEPs",
        "stem": "Personal Emergency Evacuation Plans (PEEPs) should be in place…",
        "excerpt": "Personal Emergency Evacuation Plans (PEEPs) should be in place for those required. These plans should also be adjusted to consider the impact of alternative [procedures]",
        "notes": "Named support (PEEP); individual locus candidate; higher rung candidate",
        "measure_type": "procedural_response",
        "force": "recommended",
        "unitization_ambiguity": "low",
        "setting_diff": "1_individual_plans",
        "A": dict(
            rung="2",
            locus="individual",
            support="1",
            support_link="1",
            demands={**demand("demand_physical_execution", "entailed", "evacuation plan implies motor egress")},
            memo="Named PEEP support → rung 2; not assessment of executability → not rung 3.",
        ),
        "Bdiff": {"executability_rung": "3"},
    },
    {
        "pe_id": "PE-OPA-CF16-06",
        "document_id": "DOC-CF16-01",
        "candidate_id": "CF-16",
        "pilot_id": "P1",
        "acquisition_id": "ACQ-P1-CF16-01",
        "page_number": "5",
        "section_heading": "Introduction / testing plans",
        "source_location": "PDF p.5 Settings should test their plans…",
        "stem": "Settings should test their plans to make sure they are suitable…",
        "excerpt": "Settings should test their plans to make sure they are suitable and effective, for any live testing such as practice drills, consideration must be taken around individual trauma",
        "notes": "Testing + trauma consideration; ladder ambiguity: plan testing vs executability testing",
        "measure_type": "training_drill",
        "force": "recommended",
        "unitization_ambiguity": "high",
        "setting_diff": "0",
        "A": dict(
            rung="4",
            locus="not_specified",
            support="0",
            memo="PROVISIONAL: 'test their plans…practice drills' coded rung 4 as realistic-condition testing of protective plans; trauma 'consideration' not named support. Benchmark-sensitive: whether AFN comparator would force narrower rung-4 rule.",
        ),
        "Bdiff": {"executability_rung": "1", "support_present": "0"},
    },
    {
        "pe_id": "PE-OPA-CF16-07",
        "document_id": "DOC-CF16-01",
        "candidate_id": "CF-16",
        "pilot_id": "P1",
        "acquisition_id": "ACQ-P1-CF16-01",
        "page_number": "8",
        "section_heading": "For Special schools and learners/staff with SEND",
        "source_location": "PDF p.8 Special schools SEND buddies/marshals",
        "stem": "settings should therefore consider having specific buddies/marshals…",
        "excerpt": "settings should therefore consider having specific buddies/marshals to assist [learners with SEND]",
        "notes": "Named support role; subgroup/setting differentiation surface",
        "measure_type": "procedural_response",
        "force": "recommended",
        "unitization_ambiguity": "low",
        "setting_diff": "1_special_schools_section",
        "A": dict(
            rung="2",
            locus="subgroup",
            support="1",
            support_link="1",
            demands={**demand("demand_physical_execution", "entailed", "assist implies supported motor action")},
            memo="Named buddy/marshal support in SEND/special-schools section.",
        ),
        "Bdiff": {"executability_locus": "multiple"},
    },
    {
        "pe_id": "PE-OPA-CF16-08",
        "document_id": "DOC-CF16-01",
        "candidate_id": "CF-16",
        "pilot_id": "P1",
        "acquisition_id": "ACQ-P1-CF16-01",
        "page_number": "11",
        "section_heading": "Case illustration: practice lockdown accessibility",
        "source_location": "PDF p.11 College A amends plan after inaccessible egress",
        "stem": "College A then amends their plan to make reasonable adjustments…",
        "excerpt": "College A then amends their plan to make reasonable adjustments for learners with [mobility needs following practice lockdown]",
        "notes": "Exercise evidence used to revise — candidate rung 5; illustrative case not binding shall",
        "measure_type": "training_drill",
        "force": "unspecified",
        "unitization_ambiguity": "high",
        "setting_diff": "1_mobility",
        "A": dict(
            rung="5",
            locus="subgroup",
            support="1",
            support_link="1",
            demands={**demand("demand_physical_execution", "explicit", "wheelchair egress during drill")},
            memo="Illustrative case of drill revealing inaccessibility then amending plan → rung 5 candidate; force=unspecified (example). PROVISIONAL until comparator calibration of whether examples count.",
        ),
        "Bdiff": {"executability_rung": "4", "prescriptive_force": "optional"},
    },
    # P2 CF-03
    {
        "pe_id": "PE-OPA-CF03-01",
        "document_id": "DOC-CF03-01",
        "candidate_id": "CF-03",
        "pilot_id": "P2",
        "acquisition_id": "ACQ-P2-CF03-01",
        "page_number": "6",
        "section_heading": "Planning team",
        "source_location": "PDF p.6 multi-disciplinary team",
        "stem": "Schools should build a multi-disciplinary team…",
        "excerpt": "Schools should build a multi-disciplinary team that will lead the physical security planning process",
        "notes": "Planning requirement; low protective-action demand",
        "measure_type": "other",
        "force": "recommended",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(rung="1", locus="not_specified", support="0", memo="Planning-team prescription; no occupant protective-action executability content."),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF03-02",
        "document_id": "DOC-CF03-01",
        "candidate_id": "CF-03",
        "pilot_id": "P2",
        "acquisition_id": "ACQ-P2-CF03-01",
        "page_number": "12",
        "section_heading": "Prevention / threat assessment mention",
        "source_location": "PDF p.12 threat assessment and reporting process",
        "stem": "a school’s robust threat assessment and reporting process…",
        "excerpt": "a school’s robust threat assessment and reporting process (falling under prevention) depends on a functioning [system]",
        "notes": "Branch B surface — out of scope for demand-capability model; Family F inactive",
        "measure_type": "behavioural_threat_assessment",
        "force": "unspecified",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="0",
            locus="not_specified",
            support="0",
            memo="Descriptive dependency statement; Branch B material noted; executability engagement not addressed → rung 0.",
            branch_b="out_of_scope_mark",
        ),
        "Bdiff": {"executability_rung": "1"},
    },
    {
        "pe_id": "PE-OPA-CF03-03",
        "document_id": "DOC-CF03-01",
        "candidate_id": "CF-03",
        "pilot_id": "P2",
        "acquisition_id": "ACQ-P2-CF03-01",
        "page_number": "25",
        "section_heading": "Building perimeter / lockdown PA",
        "source_location": "PDF p.25 PA lockdown message prompts close/lock/move",
        "stem": "A PA message announcing a lockdown emergency…",
        "excerpt": "A PA message announcing a lockdown emergency, for instance, should prompt students and staff to close and lock doors that remain open, and move to certain “safe” areas",
        "notes": "Direct action + alert perception explicit; multi-action sentence",
        "measure_type": "procedural_response",
        "force": "recommended",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            demands={
                **demand("demand_alert_perception", "explicit", "PA message announcing lockdown"),
                **demand("demand_instruction_comprehension", "entailed", "map announcement to actions"),
                **demand("demand_physical_execution", "explicit", "close and lock doors; move to safe areas"),
                **demand("demand_inhibitory_movement", "entailed", "remain in safe area implied by lockdown"),
            },
            memo="Unit kept as one PE (prompted action chain). Inhibitory acoustic not explicit.",
        ),
        "Bdiff": {
            "demand_inhibitory_acoustic": "1",
            "demand_inhibitory_acoustic_source": "ambiguous_memo",
            "demand_inhibitory_acoustic_trigger": "",
        },
    },
    {
        "pe_id": "PE-OPA-CF03-04",
        "document_id": "DOC-CF03-01",
        "candidate_id": "CF-03",
        "pilot_id": "P2",
        "acquisition_id": "ACQ-P2-CF03-01",
        "page_number": "25",
        "section_heading": "Building perimeter / drills",
        "source_location": "PDF p.25 Regular drills can help… practice these actions",
        "stem": "Regular drills can help members of the school community practice…",
        "excerpt": "Regular drills can help members of the school community practice these actions, and training programs should be imple[mented]",
        "notes": "Drill language; ladder ambiguity vs CF-16 testing",
        "measure_type": "training_drill",
        "force": "recommended",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            memo="Practice/familiarisation drills without assessment of executability for diverse needs → rung 1 (contrast CF16-06). Ladder consistency stress.",
        ),
        "Bdiff": {"executability_rung": "4"},
    },
    {
        "pe_id": "PE-OPA-CF03-05",
        "document_id": "DOC-CF03-01",
        "candidate_id": "CF-03",
        "pilot_id": "P2",
        "acquisition_id": "ACQ-P2-CF03-01",
        "page_number": "23",
        "section_heading": "School grounds / emergency call boxes",
        "source_location": "PDF p.23 emergency call boxes awareness",
        "stem": "If emergency call boxes are put in place, schools should ensure…",
        "excerpt": "If emergency call boxes are put in place, schools should ensure that members of the school community are aware of [how to use them]",
        "notes": "Conditional physical + communication demand",
        "measure_type": "communication_alerting",
        "force": "recommended",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            demands={
                **demand("demand_emergency_communication", "entailed", "call-box use implies transmitting emergency info"),
                **demand("demand_physical_execution", "entailed", "locate/activate call box"),
            },
            memo="Awareness requirement; no accessibility support specified.",
        ),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF03-06",
        "document_id": "DOC-CF03-01",
        "candidate_id": "CF-03",
        "pilot_id": "P2",
        "acquisition_id": "ACQ-P2-CF03-01",
        "page_number": "7",
        "section_heading": "School Security Assessment Tool",
        "source_location": "PDF p.7 SSAT companion assessment tool",
        "stem": "School Security Assessment Tool (SSAT)… further guidance…",
        "excerpt": "School Security Assessment Tool (SSAT), a web-based tool that provides further guidance on school physical security planning and imple[mentation]",
        "notes": "Assessment tool for physical security — not executability assessment (rung 3 trap)",
        "measure_type": "other",
        "force": "optional",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            memo="SSAT assesses physical security posture, not protective-action executability → do not code rung 3.",
        ),
        "Bdiff": {"executability_rung": "3"},
    },
    {
        "pe_id": "PE-OPA-CF03-07",
        "document_id": "DOC-CF03-01",
        "candidate_id": "CF-03",
        "pilot_id": "P2",
        "acquisition_id": "ACQ-P2-CF03-01",
        "page_number": "22",
        "section_heading": "Unintended consequences",
        "source_location": "PDF p.22 unintended consequences of security measures",
        "stem": "School personnel should also consider the potential for various security measures to have unintended consequences…",
        "excerpt": "School personnel should also consider the potential for various security measures to have unintended consequences; tall [barriers example context]",
        "notes": "Conflict acknowledgement surface (Family I)",
        "measure_type": "other",
        "force": "recommended",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            conflict_ack="1",
            conflict_res="0",
            memo="Acknowledges unintended consequences; no specific accessibility resolution offered in-unit.",
        ),
        "Bdiff": {"conflict_resolution_offered": "1"},
    },
    # P3 CF-15
    {
        "pe_id": "PE-OPA-CF15-01",
        "document_id": "DOC-CF15-01",
        "candidate_id": "CF-15",
        "pilot_id": "P3",
        "acquisition_id": "ACQ-P3-CF15-01",
        "page_number": "12842",
        "section_heading": "Artículo 4 / elaboración planes",
        "source_location": "BOE PDF Art.4.1.a elaboración/implantación/mantenimiento/revisión",
        "stem": "elaboración, implantación, mantenimiento y revisión es responsabilidad…",
        "excerpt": "Su elaboración, implantación, mantenimiento y revisión es responsabilidad del titular de la actividad.",
        "notes": "Multi-action planning obligation; actor=titular; Spanish unitization",
        "measure_type": "other",
        "force": "required",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(rung="1", locus="not_specified", support="0", memo="Bundle of plan lifecycle duties kept as one PE; could split — unitization stress."),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF15-02",
        "document_id": "DOC-CF15-01",
        "candidate_id": "CF-15",
        "pilot_id": "P3",
        "acquisition_id": "ACQ-P3-CF15-01",
        "page_number": "12844",
        "section_heading": "1.4 Obligaciones titulares",
        "source_location": "BOE PDF 1.4.c implantación y mantenimiento eficacia",
        "stem": "Desarrollar las actuaciones para la implantación y el mantenimiento de la eficacia…",
        "excerpt": "Desarrollar las actuaciones para la implantación y el mantenimiento de la eficacia del Plan de Autoprotección",
        "notes": "Efficacy maintenance — cross-ref Annex II",
        "measure_type": "other",
        "force": "required",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(rung="1", locus="not_specified", support="0", memo="Cross-referenced efficacy maintenance; not yet drill detail."),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF15-03",
        "document_id": "DOC-CF15-01",
        "candidate_id": "CF-15",
        "pilot_id": "P3",
        "acquisition_id": "ACQ-P3-CF15-01",
        "page_number": "12846",
        "section_heading": "3.6 Mantenimiento eficacia / simulacros",
        "source_location": "BOE PDF 3.6 simulacros al menos una vez al año",
        "stem": "se realizarán simulacros de emergencia… al menos una vez al año…",
        "excerpt": "se realizarán simulacros de emergencia, con la periodicidad mínima que fije el propio plan, y en todo caso, al menos una vez al año evaluando sus resultados",
        "notes": "Annual drills + evaluate results — rung 4 vs 5 ambiguity",
        "measure_type": "training_drill",
        "force": "required",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="4",
            locus="not_specified",
            support="0",
            memo="Annual simulacros with evaluation of results → rung 4; revision-from-findings not explicit in-unit → not rung 5. PROVISIONAL/benchmark-dependent for AFN specificity.",
        ),
        "Bdiff": {"executability_rung": "5"},
    },
    {
        "pe_id": "PE-OPA-CF15-04",
        "document_id": "DOC-CF15-01",
        "candidate_id": "CF-15",
        "pilot_id": "P3",
        "acquisition_id": "ACQ-P3-CF15-01",
        "page_number": "12847",
        "section_heading": "ANEXO I e) Actividades docentes",
        "source_location": "BOE PDF Annex I docente disability / other thresholds",
        "stem": "Establecimientos de uso docente especialmente destinados a personas discapacitadas…",
        "excerpt": "Establecimientos de uso docente especialmente destinados a personas discapacitadas físicas o psíquicas o a otras personas que no puedan realizar una evacuación por sus propios medios. Cualquier otro establecimiento de uso docente siempre que disponga una altura de evacuación igual o superior a 28 m, o de una ocupación igual o superior a 2.000 personas.",
        "notes": "Setting differentiation: special/disability education settings vs size/height thresholds — G1 stress; not protective-action support",
        "measure_type": "other",
        "force": "required",
        "unitization_ambiguity": "high",
        "setting_diff": "1_annex_I_docente_split",
        "A": dict(
            rung="1",
            locus="setting",
            support="0",
            memo="Catalog threshold differentiates disability-destined teaching establishments (no size threshold) vs other teaching establishments (height/occupancy). Setting differentiation present; no PE-level support for evacuation executability.",
        ),
        "Bdiff": {"executability_rung": "2", "support_present": "1"},
    },
    {
        "pe_id": "PE-OPA-CF15-05",
        "document_id": "DOC-CF15-01",
        "candidate_id": "CF-15",
        "pilot_id": "P3",
        "acquisition_id": "ACQ-P3-CF15-01",
        "page_number": "12846",
        "section_heading": "3.7 Vigencia / revisión",
        "source_location": "BOE PDF 3.7 plan revisión",
        "stem": "se revisará, al menos, con una periodicidad no superior a tres años…",
        "excerpt": "El Plan de Autoprotección tendrá vigencia indeterminada; se mantendrá adecuadamente actualizado, y se revisará, al menos, con una periodicidad no superior a tres años.",
        "notes": "Revision requirement; source-format: consolidado HTML marks Norma derogated 2023 — provenance condition",
        "measure_type": "other",
        "force": "required",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            memo="Revision obligation without requiring evidence-from-executability-tests → rung 1 not 5. SOURCE NOTE: consolidado HTML states Norma derogada efectiva 11 Jul 2023 (RD 524/2023); Phase A uses original BOE PDF identity already registered — freeze must revisit supersession.",
        ),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF15-06",
        "document_id": "DOC-CF15-01",
        "candidate_id": "CF-15",
        "pilot_id": "P3",
        "acquisition_id": "ACQ-P3-CF15-01",
        "page_number": "12845",
        "section_heading": "1.4 e) Informar y formar",
        "source_location": "BOE PDF 1.4.e informar y formar al personal",
        "stem": "Informar y formar al personal a su servicio…",
        "excerpt": "Informar y formar al personal a su servicio en los contenidos del Plan de Autoprotección.",
        "notes": "Training prescription",
        "measure_type": "training_drill",
        "force": "required",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(rung="1", locus="not_specified", support="0", memo="Staff training on plan content; not occupant drill executability test."),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF15-07",
        "document_id": "DOC-CF15-01",
        "candidate_id": "CF-15",
        "pilot_id": "P3",
        "acquisition_id": "ACQ-P3-CF15-01",
        "page_number": "12845",
        "section_heading": "1.5 Obligaciones del personal",
        "source_location": "BOE PDF 1.5 participar en la medida de sus capacidades",
        "stem": "obligación de participar, en la medida de sus capacidades…",
        "excerpt": "El personal al servicio de las actividades reseñadas en el Anexo I tendrá la obligación de participar, en la medida de sus capacidades, en el Plan de Autoprotección",
        "notes": "Capability language — ambiguous_memo risk; not AFN support",
        "measure_type": "procedural_response",
        "force": "required",
        "unitization_ambiguity": "high",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            memo="'en la medida de sus capacidades' is not a named support; do not inflate to rung 2. Capability phrase logged as codebook ambiguity (staff capacity ≠ functional-diversity supports).",
        ),
        "Bdiff": {"support_present": "1", "executability_rung": "2"},
    },
    # P4 CF-13
    {
        "pe_id": "PE-OPA-CF13-01",
        "document_id": "DOC-CF13-01",
        "candidate_id": "CF-13",
        "pilot_id": "P4",
        "acquisition_id": "ACQ-P4-CF13-01",
        "page_number": "",
        "section_heading": "Introduction / obligation PPMS",
        "source_location": "Wayback HTML §intro: doit préparer organisation / PPMS",
        "stem": "Chaque école… doit… préparer… organisation… PPMS…",
        "excerpt": "Chaque école ou établissement d’enseignement public du second degré doit à ce titre préparer « sa propre organisation de gestion de l’événement ». Les autorités académiques s’assurent qu’ils soient dotés d’un plan particulier de mise en sûreté (PPMS)",
        "notes": "P4 archive HTML; planning obligation; French",
        "measure_type": "other",
        "force": "required",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(rung="1", locus="setting", support="0", memo="PPMS possession/organisation obligation; archive HTML location by heading."),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF13-02",
        "document_id": "DOC-CF13-01",
        "candidate_id": "CF-13",
        "pilot_id": "P4",
        "acquisition_id": "ACQ-P4-CF13-01",
        "page_number": "",
        "section_heading": "5 – Exercices et retours d’expérience",
        "source_location": "Wayback HTML §5: au moins deux exercices PPMS",
        "stem": "réalise au moins deux exercices PPMS… chaque année…",
        "excerpt": "Le directeur d’école ou le chef d’établissement réalise au moins deux exercices PPMS distincts des exercices incendie chaque année",
        "notes": "Two annual exercises — testing language",
        "measure_type": "training_drill",
        "force": "required",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(
            rung="4",
            locus="setting",
            support="0",
            memo="Required biannual PPMS exercises → rung 4 candidate (realistic practice). Inclusivity sentence is separate PE.",
        ),
        "Bdiff": {"executability_rung": "1"},
    },
    {
        "pe_id": "PE-OPA-CF13-03",
        "document_id": "DOC-CF13-01",
        "candidate_id": "CF-13",
        "pilot_id": "P4",
        "acquisition_id": "ACQ-P4-CF13-01",
        "page_number": "",
        "section_heading": "5 – Exercices",
        "source_location": "Wayback HTML §5: élèves en situation de handicap / PAI",
        "stem": "attention particulière… élèves en situation de handicap…",
        "excerpt": "Une attention particulière est portée aux élèves en situation de handicap et aux élèves fragiles, notamment aux titulaires d’un projet d’accueil personnalisé.",
        "notes": "Attention particulière — generic vs named PAI support; benchmark-relevant",
        "measure_type": "training_drill",
        "force": "recommended",
        "unitization_ambiguity": "high",
        "setting_diff": "1_handicap_PAI",
        "A": dict(
            rung="2",
            locus="subgroup",
            support="1",
            support_link="unlinked",
            memo="PROVISIONAL: PAI mention treated as named individual plan support during exercises → support=1 but unlinked to a specific demand; rung 2. Generic 'attention particulière' alone would be 0 — here PAI anchors. Benchmark calibration needed vs CF-02 function-based language.",
        ),
        "Bdiff": {"support_present": "0", "executability_rung": "1"},
    },
    {
        "pe_id": "PE-OPA-CF13-04",
        "document_id": "DOC-CF13-01",
        "candidate_id": "CF-13",
        "pilot_id": "P4",
        "acquisition_id": "ACQ-P4-CF13-01",
        "page_number": "",
        "section_heading": "5 – Exercices",
        "source_location": "Wayback HTML §5: sans effet de surprise / arme factice proscrite",
        "stem": "L’exercice doit se dérouler sans effet de surprise…",
        "excerpt": "L’exercice doit se dérouler sans effet de surprise et sans mise en scène exagérément réaliste. L’utilisation d’arme factice est proscrite, notamment lors des exercices « menaces ».",
        "notes": "Exercise condition/exception constraints",
        "measure_type": "training_drill",
        "force": "required",
        "unitization_ambiguity": "low",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            memo="Constraints on exercise realism; not itself a protective-action support for diverse needs.",
        ),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF13-05",
        "document_id": "DOC-CF13-01",
        "candidate_id": "CF-13",
        "pilot_id": "P4",
        "acquisition_id": "ACQ-P4-CF13-01",
        "page_number": "",
        "section_heading": "5 – Retours d’expérience",
        "source_location": "Wayback HTML §5: REX peuvent alimenter actualisation",
        "stem": "Les retours d’expérience… peuvent alimenter son actualisation…",
        "excerpt": "Les retours d’expérience organisés à la suite de l’activation du PPMS dans le cadre d’exercices ou d’événements majeurs peuvent alimenter son actualisation.",
        "notes": "Optional ('peuvent') evidence-informed revision — rung 5 force weak",
        "measure_type": "other",
        "force": "optional",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="5",
            locus="not_specified",
            support="0",
            memo="PROVISIONAL: REX may feed updates → rung 5 with optional force. Alternative coding: rung 1 because not required. Benchmark-dependent whether optional learning loops count as rung 5.",
        ),
        "Bdiff": {"executability_rung": "1"},
    },
    {
        "pe_id": "PE-OPA-CF13-06",
        "document_id": "DOC-CF13-01",
        "candidate_id": "CF-13",
        "pilot_id": "P4",
        "acquisition_id": "ACQ-P4-CF13-01",
        "page_number": "",
        "section_heading": "2 – Élaboration / multi-site",
        "source_location": "Wayback HTML §2: chaque site… PPMS… deux exercices",
        "stem": "chaque site réalisera son propre PPMS… ainsi que les deux exercices annuels…",
        "excerpt": "Si la structure scolaire est répartie sur différents sites éloignés géographiquement … chaque site réalisera son propre PPMS au regard de ses spécificités ainsi que les deux exercices annuels.",
        "notes": "Setting/site differentiation + cross-ref exercises",
        "measure_type": "other",
        "force": "required",
        "unitization_ambiguity": "medium",
        "setting_diff": "1_multi_site",
        "A": dict(
            rung="1",
            locus="setting",
            support="0",
            memo="Per-site PPMS/exercises; differentiation by site not by functional need.",
        ),
        "Bdiff": {},
    },
    {
        "pe_id": "PE-OPA-CF13-07",
        "document_id": "DOC-CF13-01",
        "candidate_id": "CF-13",
        "pilot_id": "P4",
        "acquisition_id": "ACQ-P4-CF13-01",
        "page_number": "",
        "section_heading": "2 – Élaboration / procédures communes",
        "source_location": "Wayback HTML §2: signal d’alarme / cheminements / lieux de mise en sécurité",
        "stem": "déclenchement du signal d’alarme… cheminements… lieux de mise en sécurité…",
        "excerpt": "Des procédures communes (déclenchement du signal d’alarme, identification des cheminements et des lieux de mise en sécurité, contrôle des personnes extérieures à l’école …) peuvent être identifiées.",
        "notes": "Alert + movement routes; force=optional ('peuvent'); entailed demands",
        "measure_type": "communication_alerting",
        "force": "optional",
        "unitization_ambiguity": "medium",
        "setting_diff": "0",
        "A": dict(
            rung="1",
            locus="not_specified",
            support="0",
            demands={
                **demand("demand_alert_perception", "entailed", "signal d’alarme"),
                **demand("demand_physical_execution", "entailed", "cheminements / mise en sécurité"),
                **demand("demand_instruction_comprehension", "entailed", "follow common procedures"),
            },
            memo="Optional identification of common procedures; demands entailed if procedures used.",
        ),
        "Bdiff": {},
    },
]


def pe_row(u: dict) -> dict[str, str]:
    return {
        "pe_id": u["pe_id"],
        "document_id": u["document_id"],
        "candidate_id": u["candidate_id"],
        "pilot_id": u["pilot_id"],
        "acquisition_id": u["acquisition_id"],
        "source_location": u["source_location"],
        "page_number": u.get("page_number", ""),
        "section_heading": u["section_heading"],
        "verbatim_trigger_text": u["stem"],
        "excerpt_policy": "public_short_stem_only; full_excerpt_gitignored",
        "local_excerpt_ref": f"local_sources/pilot_coding/phase_a_excerpts.json#{u['pe_id']}",
        "coder_segmentation_notes": u["notes"],
        "measure_present": "1",
        "measure_type": u["measure_type"],
        "prescriptive_force": u["force"],
        "unitization_ambiguity": u["unitization_ambiguity"],
        "setting_differentiation_surface": u["setting_diff"],
        **FLAGS,
    }


def build_A(u: dict) -> dict[str, str]:
    a = u["A"]
    return coding_row(
        coder_id="coder_A",
        pe_id=u["pe_id"],
        measure_type=u["measure_type"],
        force=u["force"],
        rung=a["rung"],
        locus=a["locus"],
        support=a.get("support", "0"),
        support_link=a.get("support_link", "not_applicable"),
        demands=a.get("demands"),
        memo=a.get("memo", ""),
        branch_b=a.get("branch_b", "inactive"),
        conflict_ack=a.get("conflict_ack", "0"),
        conflict_res=a.get("conflict_res", "0"),
        pass_type="primary_human",
    )


def build_B(u: dict, a_row: dict[str, str]) -> dict[str, str]:
    """Simulated procedural second pass: copy A then apply intentional Bdiff disagreements."""
    row = dict(a_row)
    row["coder_id"] = "procedural_second_pass"
    row["coder_pass_type"] = "simulated_procedural_second_pass"
    row["coding_round"] = "phase_a_operational_procedural"
    for k, v in u.get("Bdiff", {}).items():
        row[k] = v
    # Special case: if B sets demand present with ambiguous_memo, force value rules
    for d in [
        "demand_alert_perception",
        "demand_instruction_comprehension",
        "demand_decision_making",
        "demand_emergency_communication",
        "demand_inhibitory_acoustic",
        "demand_inhibitory_movement",
        "demand_behavioural_sensory_regulation",
        "demand_physical_execution",
        "demand_temporal_endurance",
        "demand_responder_interaction",
    ]:
        if row.get(f"{d}_source") == "ambiguous_memo" and row.get(d) == "1":
            # Invalid for confirmatory; procedural pass records confusion then corrected in adjudication
            # Keep as intentional disagreement artifact: set value 0 with memo in adjudication
            row[d] = "0"
            row["qualitative_memo"] = (
                row.get("qualitative_memo", "")
                + " | procedural_pass: considered inhibitory acoustic as ambiguous_memo (not counted as presence)."
            )
    return row


DISAGREE_TYPES = {
    "PE-OPA-CF16-02": ("codebook_gap", "support_present/rung", "Generic inclusive language vs named support"),
    "PE-OPA-CF16-03": ("explicit-versus-entailed confusion", "demand_inhibitory_acoustic", "Entailing silence from HIDE"),
    "PE-OPA-CF16-04": ("locus ambiguity", "executability_locus", "setting vs not_specified"),
    "PE-OPA-CF16-05": ("ladder ambiguity", "executability_rung", "PEEP as support (2) vs assessment (3)"),
    "PE-OPA-CF16-06": ("ladder ambiguity", "executability_rung", "Plan testing vs executability testing"),
    "PE-OPA-CF16-07": ("locus ambiguity", "executability_locus", "subgroup vs multiple"),
    "PE-OPA-CF16-08": ("ladder ambiguity", "executability_rung", "Illustrative case as rung 5"),
    "PE-OPA-CF03-02": ("document-level versus PE-level confusion", "executability_rung", "BTAM descriptive text"),
    "PE-OPA-CF03-03": ("explicit-versus-entailed confusion", "demand_inhibitory_acoustic", "Lockdown silence assumption"),
    "PE-OPA-CF03-04": ("ladder ambiguity", "executability_rung", "Practice drills as rung 1 vs 4"),
    "PE-OPA-CF03-06": ("ladder ambiguity", "executability_rung", "SSAT as security assessment not executability assessment"),
    "PE-OPA-CF03-07": ("variable overlap", "conflict_resolution_offered", "Acknowledge vs resolve"),
    "PE-OPA-CF15-03": ("ladder ambiguity", "executability_rung", "Evaluate results as rung 4 vs 5"),
    "PE-OPA-CF15-04": ("codebook_gap", "support_present", "Catalog threshold vs support"),
    "PE-OPA-CF15-07": ("codebook_gap", "support_present", "Capacidades language"),
    "PE-OPA-CF13-02": ("ladder ambiguity", "executability_rung", "Required exercises as rung 4 vs 1"),
    "PE-OPA-CF13-03": ("benchmark-dependent", "support_present", "Attention/PAI as support"),
    "PE-OPA-CF13-05": ("ladder ambiguity", "executability_rung", "Optional REX as rung 5"),
}


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in headers})


def main() -> None:
    assert len(UNITS) >= 20 and len(UNITS) <= 32, len(UNITS)
    assert not any(u["pilot_id"] == "P5" or u["candidate_id"] == "CF-02" for u in UNITS)

    excerpts = {
        u["pe_id"]: {
            "pe_id": u["pe_id"],
            "document_id": u["document_id"],
            "source_location": u["source_location"],
            "excerpt": u["excerpt"],
            "NOT_FOR_SUBSTANTIVE_INFERENCE": True,
            "NOT_FOR_BENCHMARK_COMPARISON": True,
            "PROTOCOL_DEVELOPMENT_ONLY": True,
            "do_not_commit": True,
        }
        for u in UNITS
    }
    (LOCAL / "phase_a_excerpts.json").write_text(
        json.dumps(excerpts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (LOCAL / "README.md").write_text(
        "# Gitignored Phase A excerpts\n\nDo not commit. Public records use short stems + locations only.\n",
        encoding="utf-8",
    )

    pe_rows = [pe_row(u) for u in UNITS]
    a_rows = [build_A(u) for u in UNITS]
    b_rows = [build_B(u, a) for u, a in zip(UNITS, a_rows)]

    # Adjudication: start from A; resolve disagreements without maximizing agreement
    adj_rows: list[dict[str, str]] = []
    disagree_rows: list[dict[str, str]] = []
    for u, a, b in zip(UNITS, a_rows, b_rows):
        adj = dict(a)
        adj["coder_id"] = "adjudicator"
        adj["coder_pass_type"] = "adjudication"
        adj["coding_round"] = "phase_a_adjudicated"
        diffs = []
        for key in CODING_HEADERS:
            if key in {
                "coder_id",
                "coding_round",
                "qualitative_memo",
                "adjudication_status",
                "adjudicated_value",
                "coder_pass_type",
            }:
                continue
            if a.get(key, "") != b.get(key, ""):
                diffs.append(key)
        if diffs:
            adj["adjudication_status"] = "resolved"
            # Keep A's values as adjudicated defaults except document procedural uncertainty
            adj["adjudicated_value"] = "retained_coder_A_with_provisional_flags_where_noted"
            adj["qualitative_memo"] = (
                a.get("qualitative_memo", "")
                + f" | ADJUDICATION: disagreed on {','.join(diffs)}; retained A; see disagreement_log."
            )
            dtype, var, detail = DISAGREE_TYPES.get(
                u["pe_id"], ("variable overlap", diffs[0], "procedural disagreement")
            )
            disagree_rows.append(
                {
                    "pilot_unit_id": u["pe_id"],
                    "variable": var if var in diffs or var == diffs[0] else diffs[0],
                    "coder_A_value": a.get(var if var in a else diffs[0], a.get(diffs[0], "")),
                    "coder_B_or_procedural_value": b.get(var if var in b else diffs[0], b.get(diffs[0], "")),
                    "disagreement_type": dtype,
                    "adjudicated_resolution": "retain_A_provisional; do_not_change_rule_to_maximize_agreement",
                    "codebook_implication": detail,
                    "protocol_amendment_required": "yes_if_benchmark_or_ladder_rule" if "ladder" in dtype or "benchmark" in dtype else "review",
                    "benchmark_calibration_needed": "yes" if ("benchmark" in dtype or u["pe_id"] in {"PE-OPA-CF16-06", "PE-OPA-CF16-08", "PE-OPA-CF13-03", "PE-OPA-CF13-05", "PE-OPA-CF15-03"}) else "no",
                    "inference_flag": "NOT_FOR_SUBSTANTIVE_INFERENCE",
                    "benchmark_flag": "NOT_FOR_BENCHMARK_COMPARISON",
                    "protocol_flag": "PROTOCOL_DEVELOPMENT_ONLY",
                    "pilot_phase": "A_operational",
                }
            )
        else:
            adj["adjudication_status"] = "none"
            adj["adjudicated_value"] = "no_disagreement"
        adj_rows.append(adj)

    write_csv(PILOT / "prescriptive_elements.csv", PE_HEADERS, pe_rows)
    write_csv(PILOT / "coding_coder_A.csv", CODING_HEADERS, a_rows)
    write_csv(PILOT / "coding_coder_B_procedural.csv", CODING_HEADERS, b_rows)
    write_csv(PILOT / "coding_adjudicated.csv", CODING_HEADERS, adj_rows)

    d_headers = [
        "pilot_unit_id",
        "variable",
        "coder_A_value",
        "coder_B_or_procedural_value",
        "disagreement_type",
        "adjudicated_resolution",
        "codebook_implication",
        "protocol_amendment_required",
        "benchmark_calibration_needed",
        "inference_flag",
        "benchmark_flag",
        "protocol_flag",
        "pilot_phase",
    ]
    write_csv(PILOT / "disagreement_log.csv", d_headers, disagree_rows)

    print(f"Wrote {len(pe_rows)} PEs; disagreements={len(disagree_rows)}")


if __name__ == "__main__":
    main()
