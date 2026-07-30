#!/usr/bin/env python3
"""Generate synthetic/public experiment-pack case files (no restricted text)."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments"


def wcsv(path: Path, headers: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        wr.writeheader()
        for r in rows:
            wr.writerow({h: r.get(h, "") for h in headers})


# --- EXP-01 Unitization cases (synthetic constructed text) ---
U01 = [
    ("U01-01", "simple_one_action", "Schools must appoint a security lead.", "1", "single PE: appoint security lead"),
    ("U01-02", "multi_action_sentence", "Staff must lock classroom doors and move students to the safe corner.", "2", "split lock vs move OR keep as one chained PE — reference keeps 2"),
    ("U01-03", "conditional", "If a lockdown is announced, occupants shall remain in place until released.", "1", "conditional protective action"),
    ("U01-04", "exception", "Evacuate using the nearest exit, except when the exit is blocked by smoke.", "1", "exception within one PE"),
    ("U01-05", "cross_reference", "Follow the response options in Annex B when an intruder is reported.", "1", "cross-ref still one PE"),
    ("U01-06", "actor_ambiguity", "Appropriate personnel should secure the perimeter.", "1", "actor unspecified"),
    ("U01-07", "passive_voice", "Doors are to be locked from the inside during a lockdown.", "1", "passive prescription"),
    ("U01-08", "planning_requirement", "Each centre shall maintain a written emergency response plan.", "1", "planning PE"),
    ("U01-09", "support_provision", "Provide a visual alert equivalent for occupants who cannot hear the siren.", "1", "named support"),
    ("U01-10", "assessment_provision", "Verify whether all occupants can reach the secure room within three minutes.", "1", "assessment of executability"),
    ("U01-11", "exercise_provision", "Conduct at least two lockdown drills each school year.", "1", "exercise requirement"),
    ("U01-12", "revision_provision", "Revise the lockdown procedure using findings from the annual drill review.", "1", "evidence-based revision"),
    ("U01-13", "setting_specific", "Special education classrooms must have an assigned buddy for each evacuation route.", "1", "setting/subgroup clause"),
    ("U01-14", "multi_option", "Settings should consider lockdown, invacuation, or evacuation as response options.", "1", "options as one decision PE"),
    ("U01-15", "generic_inclusive", "Plans should be inclusive and accessible for learners with special educational needs.", "1", "generic inclusivity — support_present later may be 0"),
    ("U01-16", "named_plan_support", "Personal emergency evacuation plans must be in place for identified individuals.", "1", "named individual plan"),
    ("U01-17", "communication_demand", "If safe, call emergency services and report your location.", "1", "transmission demand"),
    ("U01-18", "inhibitory", "Remain silent and still until an all-clear is given.", "1", "inhibitory acoustic+movement"),
    ("U01-19", "responder_interaction", "Keep hands visible and empty when officers enter the room.", "1", "responder interaction"),
    ("U01-20", "bundle_lifecycle", "The titular shall elaborate, implement, maintain, and review the self-protection plan.", "1", "multi-verb lifecycle; reference=1 unit with note that split is plausible"),
    ("U01-21", "threat_assessment_oos", "Staff should report concerning behaviour to the threat-assessment team.", "1", "Branch B surface; still a PE for unitization"),
    ("U01-22", "non_prescription", "School violence is a serious societal concern requiring attention.", "0", "no PE — rationale/statement only"),
    ("U01-23", "drill_with_constraint", "Exercises must proceed without surprise effects and without replica weapons.", "1", "exercise condition"),
    ("U01-24", "multi_site", "If the school spans distant sites, each site shall prepare its own plan and two annual exercises.", "2", "plan PE + exercises PE"),
    ("U01-25", "ambiguous_unit_boundary", "On hearing the alarm, close and lock doors, then move to the safe area and await instructions.", "3", "reference prefers 3 action units; 1 chained PE is plausible alternative"),
    ("U01-26", "support_unlinked", "Consider individual needs. Provide strobe alarms in hallways.", "2", "generic consider + named support as separate units"),
]

u_cases = []
u_ref = []
for cid, ctype, text, n_units, rationale in U01:
    u_cases.append({
        "case_id": cid,
        "case_type": ctype,
        "stimulus_text": text,
        "language": "en",
        "source_status": "synthetic_constructed",
        "copyright_status": "original_for_calibration",
        "difficulty": "high" if "multi" in ctype or "ambiguous" in ctype or "bundle" in ctype else "medium" if "ambigu" in ctype or "passive" in ctype or "actor" in ctype else "low",
        "experiment_id": "EXP-01",
        "NOT_EXECUTED": "true",
    })
    u_ref.append({
        "case_id": cid,
        "reference_unit_count": n_units,
        "reference_label": "REFERENCE_ADJUDICATION",
        "not_true_answer": "true",
        "segmentation_notes": rationale,
        "plausible_alternative": "yes" if cid in {"U01-02", "U01-20", "U01-25"} else "no",
        "experiment_id": "EXP-01",
    })

wcsv(
    EXP / "EXP-01_unitization/materials/cases.csv",
    ["case_id", "case_type", "stimulus_text", "language", "source_status", "copyright_status", "difficulty", "experiment_id", "NOT_EXECUTED"],
    u_cases,
)
wcsv(
    EXP / "EXP-01_unitization/reference/reference_adjudication.csv",
    ["case_id", "reference_unit_count", "reference_label", "not_true_answer", "segmentation_notes", "plausible_alternative", "experiment_id"],
    u_ref,
)

# blank + synthetic responses EXP-01
blank_u = [{"participant_id": "", "case_id": c["case_id"], "units_identified": "", "unit_boundaries_notes": "", "confidence_1_to_5": "", "pass_type": "independent_human", "experiment_id": "EXP-01"} for c in u_cases]
wcsv(EXP / "EXP-01_unitization/responses/response_template.csv", list(blank_u[0].keys()), blank_u)

synth_a = []
synth_b = []
for c, r in zip(u_cases, u_ref):
    n = int(r["reference_unit_count"])
    synth_a.append({"participant_id": "SYN-CODER-A", "case_id": c["case_id"], "units_identified": str(n), "unit_boundaries_notes": "synthetic match", "confidence_1_to_5": "4", "pass_type": "independent_human", "experiment_id": "EXP-01", "dataset_role": "synthetic_demonstration"})
    # B systematically over-segments multi cases
    nb = n + 1 if c["case_type"] in {"multi_action_sentence", "ambiguous_unit_boundary", "bundle_lifecycle"} else n
    if c["case_id"] == "U01-22":
        nb = 1  # false positive unit
    synth_b.append({"participant_id": "SYN-CODER-B", "case_id": c["case_id"], "units_identified": str(nb), "unit_boundaries_notes": "synthetic disagreement pattern", "confidence_1_to_5": "3", "pass_type": "independent_human", "experiment_id": "EXP-01", "dataset_role": "synthetic_demonstration"})
wcsv(EXP / "EXP-01_unitization/responses/synthetic_coder_A.csv", list(synth_a[0].keys()), synth_a)
wcsv(EXP / "EXP-01_unitization/responses/synthetic_coder_B.csv", list(synth_b[0].keys()), synth_b)

# --- EXP-02 Coding decision cases ---
C02 = [
    ("C02-01", "Appoint a security lead.", "other", "recommended", "0", "", "1", "not_specified", "0", "not_applicable", "0", "planning only", "rule_application"),
    ("C02-02", "Plans should be inclusive and accessible for learners with SEND.", "procedural_response", "recommended", "1", "", "1", "subgroup", "0", "not_applicable", "0", "generic inclusivity → support 0", "codebook_ambiguity"),
    ("C02-03", "Provide strobe alarms for occupants who cannot hear audible alerts.", "communication_alerting", "required", "1", "demand_alert_perception:explicit", "2", "subgroup", "1", "1", "0", "named support → rung 2", "rule_application"),
    ("C02-04", "On hearing the alarm, evacuate via the nearest exit.", "procedural_response", "required", "1", "demand_alert_perception:explicit;demand_physical_execution:explicit;demand_instruction_comprehension:entailed", "1", "not_specified", "0", "not_applicable", "0", "explicit alert+motor", "rule_application"),
    ("C02-05", "If escape is possible, run; otherwise hide.", "procedural_response", "recommended", "1", "demand_decision_making:explicit;demand_physical_execution:entailed", "1", "not_specified", "0", "not_applicable", "0", "decision demand", "rule_application"),
    ("C02-06", "Remain silent until released.", "procedural_response", "required", "1", "demand_inhibitory_acoustic:explicit;demand_temporal_endurance:entailed", "1", "not_specified", "0", "not_applicable", "0", "explicit silence", "rule_application"),
    ("C02-07", "Follow RUN HIDE TELL.", "procedural_response", "recommended", "1", "demand_physical_execution:entailed;demand_decision_making:entailed", "1", "not_specified", "0", "not_applicable", "0", "do not entail silence from name alone", "plausible_alternative"),
    ("C02-08", "Personal emergency evacuation plans should be in place for those who need them.", "procedural_response", "recommended", "1", "demand_physical_execution:entailed", "2", "individual", "1", "1", "0", "PEEP named support", "rule_application"),
    ("C02-09", "Verify by drill that occupants with mobility limitations can reach the secure area within the target time.", "training_drill", "required", "1", "demand_physical_execution:explicit", "4", "subgroup", "1", "1", "0", "realistic testing of executability", "rule_application"),
    ("C02-10", "Conduct familiarisation drills so staff know the lockdown announcement.", "training_drill", "recommended", "1", "demand_alert_perception:entailed", "1", "not_specified", "0", "not_applicable", "0", "familiarisation ≠ rung 4", "codebook_ambiguity"),
    ("C02-11", "Revise the procedure using findings from the annual drill review.", "other", "required", "1", "", "5", "not_specified", "0", "not_applicable", "0", "evidence-based revision", "rule_application"),
    ("C02-12", "Exercise findings may inform plan updates.", "other", "optional", "1", "", "5", "not_specified", "0", "not_applicable", "0", "optional REX → provisional rung 5", "benchmark_dependent"),
    ("C02-13", "Use the physical security assessment tool to review campus layers.", "other", "optional", "1", "", "1", "not_specified", "0", "not_applicable", "0", "not executability assessment", "coder_mistake_trap"),
    ("C02-14", "Teaching establishments especially destined for persons who cannot self-evacuate are in scope regardless of size.", "other", "required", "1", "", "1", "setting", "0", "not_applicable", "0", "setting differentiation not support", "rule_application"),
    ("C02-15", "Staff shall participate in the plan according to their capacities.", "procedural_response", "required", "1", "", "1", "not_specified", "0", "not_applicable", "0", "capacity clause ≠ AFN support", "codebook_ambiguity"),
    ("C02-16", "Call emergency services and report your location if safe.", "communication_alerting", "recommended", "1", "demand_emergency_communication:explicit;demand_decision_making:entailed", "1", "not_specified", "0", "not_applicable", "0", "transmission", "rule_application"),
    ("C02-17", "Keep hands visible and empty; do not run toward officers.", "procedural_response", "required", "1", "demand_responder_interaction:explicit;demand_inhibitory_movement:entailed", "1", "not_specified", "0", "not_applicable", "0", "responder interaction", "rule_application"),
    ("C02-18", "Try to stay calm.", "procedural_response", "optional", "1", "", "1", "not_specified", "0", "not_applicable", "0", "boilerplate; sensory demand not coded", "ambiguous_memo_case"),
    ("C02-19", "Staff should report concerning behaviour to the threat-assessment team.", "behavioural_threat_assessment", "recommended", "0", "", "0", "not_specified", "0", "not_applicable", "1", "Branch B out of scope for Branch A model", "out_of_scope_branch_b"),
    ("C02-20", "Consider individual needs during drills.", "training_drill", "recommended", "1", "", "1", "not_specified", "0", "not_applicable", "0", "generic consider", "rule_application"),
    ("C02-21", "Assign buddies/marshals to assist learners who need support during evacuation.", "procedural_response", "recommended", "1", "demand_physical_execution:entailed", "2", "subgroup", "1", "1", "0", "named support role", "rule_application"),
    ("C02-22", "A PA lockdown message should prompt students to close and lock doors and move to safe areas.", "procedural_response", "recommended", "1", "demand_alert_perception:explicit;demand_physical_execution:explicit;demand_instruction_comprehension:entailed", "1", "not_specified", "0", "not_applicable", "0", "multi-action chain one PE", "rule_application"),
    ("C02-23", "After a drill revealed an inaccessible egress route, the college amended its plan with reasonable adjustments.", "training_drill", "unspecified", "1", "demand_physical_execution:explicit", "5", "subgroup", "1", "1", "0", "illustrative revision case", "plausible_alternative"),
    ("C02-24", "School violence is a serious concern.", "other", "unspecified", "0", "", "0", "not_specified", "0", "not_applicable", "0", "no measure", "rule_application"),
    ("C02-25", "Remain secured until released by law enforcement, which may be prolonged.", "procedural_response", "required", "1", "demand_inhibitory_movement:entailed;demand_temporal_endurance:explicit", "1", "not_specified", "0", "not_applicable", "0", "endurance", "rule_application"),
    ("C02-26", "Attention should be paid to pupils with disabilities and those with personalised reception plans during exercises.", "training_drill", "recommended", "1", "", "2", "subgroup", "1", "unlinked", "0", "PAI mention provisional support", "benchmark_dependent"),
    ("C02-27", "Identify alarm signals, routes, and secure locations as common procedures.", "communication_alerting", "optional", "1", "demand_alert_perception:entailed;demand_physical_execution:entailed", "1", "not_specified", "0", "not_applicable", "0", "optional procedures", "rule_application"),
    ("C02-28", "Distinguish threat behaviour from disability-related behaviour known for the student.", "behavioural_threat_assessment", "recommended", "0", "", "0", "not_specified", "0", "not_applicable", "1", "Branch B baseline — out of Branch A", "out_of_scope_branch_b"),
    ("C02-29", "The planning team should include a special-education professional when assessing threat referrals.", "behavioural_threat_assessment", "recommended", "0", "", "0", "not_specified", "0", "not_applicable", "1", "specialist participation Branch B", "out_of_scope_branch_b"),
    ("C02-30", "Settings should test their protective plans using practice drills, taking individual trauma into account.", "training_drill", "recommended", "1", "", "4", "not_specified", "0", "not_applicable", "0", "provisional rung 4; trauma consideration not named support", "benchmark_dependent"),
    ("C02-31", "Keep noise down during the drill.", "training_drill", "recommended", "1", "", "1", "not_specified", "0", "not_applicable", "0", "vague quiet → no inhibitory=1; memo only", "ambiguous_memo_case"),
    ("C02-32", "Barricade the door with heavy furniture.", "procedural_response", "recommended", "1", "demand_physical_execution:explicit", "1", "not_specified", "0", "not_applicable", "0", "motor demand", "rule_application"),
]

c_headers_case = ["case_id", "stimulus_text", "case_focus", "disagreement_interest", "source_status", "experiment_id", "NOT_EXECUTED"]
c_cases = []
c_ref = []
for row in C02:
    cid, text, mtype, force, measure, demands, rung, locus, support, slink, branch_b, rationale, interest = row
    c_cases.append({
        "case_id": cid,
        "stimulus_text": text,
        "case_focus": interest,
        "disagreement_interest": interest,
        "source_status": "synthetic_constructed",
        "experiment_id": "EXP-02",
        "NOT_EXECUTED": "true",
    })
    # parse demands into fields
    dmap = {k: "0" for k in [
        "demand_alert_perception", "demand_instruction_comprehension", "demand_decision_making",
        "demand_emergency_communication", "demand_inhibitory_acoustic", "demand_inhibitory_movement",
        "demand_behavioural_sensory_regulation", "demand_physical_execution", "demand_temporal_endurance",
        "demand_responder_interaction",
    ]}
    smap = {f"{k}_source": "" for k in dmap}
    if demands:
        for part in demands.split(";"):
            name, src = part.split(":")
            dmap[name] = "1"
            smap[f"{name}_source"] = src
    c_ref.append({
        "case_id": cid,
        "reference_label": "REFERENCE_ADJUDICATION",
        "not_true_answer": "true",
        "measure_present": measure,
        "measure_type": mtype if measure == "1" else "",
        "prescriptive_force": force if measure == "1" else "",
        **dmap,
        **smap,
        "support_present": support,
        "support_demand_link": slink,
        "executability_rung": rung,
        "executability_locus": locus,
        "branch_b_out_of_scope": branch_b,
        "analysis_scope": "out_of_scope_branch_b_material_noted" if branch_b == "1" else "branch_a_executability",
        "rationale": rationale,
        "disagreement_interest": interest,
        "experiment_id": "EXP-02",
    })

wcsv(EXP / "EXP-02_coding_decisions/materials/cases.csv", c_headers_case, c_cases)
ref_headers = list(c_ref[0].keys())
wcsv(EXP / "EXP-02_coding_decisions/reference/reference_adjudication.csv", ref_headers, c_ref)

# response template EXP-02
resp_fields = [
    "participant_id", "case_id", "measure_present", "measure_type", "prescriptive_force",
    "demand_alert_perception", "demand_alert_perception_source",
    "demand_instruction_comprehension", "demand_instruction_comprehension_source",
    "demand_decision_making", "demand_decision_making_source",
    "demand_emergency_communication", "demand_emergency_communication_source",
    "demand_inhibitory_acoustic", "demand_inhibitory_acoustic_source",
    "demand_inhibitory_movement", "demand_inhibitory_movement_source",
    "demand_behavioural_sensory_regulation", "demand_behavioural_sensory_regulation_source",
    "demand_physical_execution", "demand_physical_execution_source",
    "demand_temporal_endurance", "demand_temporal_endurance_source",
    "demand_responder_interaction", "demand_responder_interaction_source",
    "support_present", "support_demand_link", "executability_rung", "executability_locus",
    "branch_b_out_of_scope", "confidence_1_to_5", "perceived_difficulty_1_to_5",
    "pass_type", "experiment_id",
]
blank2 = []
for c in c_cases:
    blank2.append({k: ("" if k not in {"case_id", "experiment_id", "pass_type"} else {"case_id": c["case_id"], "experiment_id": "EXP-02", "pass_type": "independent_human"}[k]) for k in resp_fields})
wcsv(EXP / "EXP-02_coding_decisions/responses/response_template.csv", resp_fields, blank2)

# synthetic A = reference; B = common errors
syn2a = []
syn2b = []
for r in c_ref:
    a = {k: r.get(k, "") for k in resp_fields if k in r or k in resp_fields}
    a.update({"participant_id": "SYN-CODER-A", "confidence_1_to_5": "4", "perceived_difficulty_1_to_5": "2", "pass_type": "independent_human", "experiment_id": "EXP-02", "dataset_role": "synthetic_demonstration"})
    for k in resp_fields:
        a.setdefault(k, r.get(k, ""))
    syn2a.append(a)
    b = dict(a)
    b["participant_id"] = "SYN-CODER-B"
    b["dataset_role"] = "synthetic_demonstration"
    # inject errors
    if r["case_id"] == "C02-02":
        b["support_present"] = "1"
        b["executability_rung"] = "2"
    if r["case_id"] == "C02-07":
        b["demand_inhibitory_acoustic"] = "1"
        b["demand_inhibitory_acoustic_source"] = "entailed"
    if r["case_id"] == "C02-10":
        b["executability_rung"] = "4"
    if r["case_id"] == "C02-13":
        b["executability_rung"] = "3"
    if r["case_id"] == "C02-19":
        b["executability_rung"] = "1"
        b["branch_b_out_of_scope"] = "0"
    syn2b.append(b)

wcsv(EXP / "EXP-02_coding_decisions/responses/synthetic_coder_A.csv", resp_fields + ["dataset_role"], syn2a)
wcsv(EXP / "EXP-02_coding_decisions/responses/synthetic_coder_B.csv", resp_fields + ["dataset_role"], syn2b)

# procedural non-independent metadata file for negative reliability test
proc = [dict(x, pass_type="simulated_procedural_second_pass", participant_id="SYN-PROC") for x in syn2b]
wcsv(EXP / "EXP-02_coding_decisions/responses/synthetic_procedural_second_pass.csv", resp_fields + ["dataset_role"], proc)

# --- EXP-03 usability items ---
items = [
    ("US-01", "likert_1_5", "The codebook definitions were clear.", "definition_clarity"),
    ("US-02", "likert_1_5", "The constructed examples were sufficient.", "example_sufficiency"),
    ("US-03", "likert_1_5", "Decision rules were clear enough to apply.", "decision_rule_clarity"),
    ("US-04", "confidence_1_5", "Overall confidence in my coding decisions.", "confidence"),
    ("US-05", "likert_1_5", "Cognitive workload while coding was manageable.", "cognitive_workload"),
    ("US-06", "likert_1_5", "Variables overlapped in confusing ways.", "variable_overlap"),
    ("US-07", "likert_1_5", "It was difficult to locate evidence in the stimulus text.", "evidence_location_difficulty"),
    ("US-08", "likert_1_5", "Separating explicit from entailed demands was difficult.", "explicit_entailed_difficulty"),
    ("US-09", "likert_1_5", "The executability ladder was usable.", "ladder_usability"),
    ("US-10", "likert_1_5", "The locus categories were usable.", "locus_usability"),
    ("US-11", "likert_1_5", "The demand categories were usable.", "demand_category_usability"),
    ("US-12", "likert_1_5", "I needed additional examples.", "need_additional_examples"),
    ("US-13", "likert_1_5", "Overall, the coding instrument was usable.", "overall_usability"),
    ("US-14", "minutes", "Estimated minutes to code 10 PEs with this codebook.", "coding_burden_estimate"),
    ("US-15", "open_text", "Which rule was most ambiguous?", "open_ambiguity"),
    ("US-16", "open_text", "What one change would most improve usability?", "open_improvement"),
]
wcsv(
    EXP / "EXP-03_codebook_usability/materials/item_register.csv",
    ["item_id", "response_type", "item_text", "construct", "experiment_id", "instrument_status", "psychometric_claim"],
    [{
        "item_id": i, "response_type": t, "item_text": txt, "construct": c,
        "experiment_id": "EXP-03", "instrument_status": "designed_not_validated",
        "psychometric_claim": "none",
    } for i, t, txt, c in items],
)
wcsv(
    EXP / "EXP-03_codebook_usability/responses/response_template.csv",
    ["participant_id", "item_id", "response_value", "experiment_id", "pass_type"],
    [{"participant_id": "", "item_id": i, "response_value": "", "experiment_id": "EXP-03", "pass_type": "independent_human"} for i, *_ in items],
)
# synthetic usability responses
syn_u = []
for pid, bias in [("SYN-RATER-1", 4), ("SYN-RATER-2", 3)]:
    for i, t, txt, c in items:
        if t == "open_text":
            val = "Ladder rung 4 vs familiarisation drills" if "ambiguous" in txt.lower() or i == "US-15" else "Add more rung examples"
        elif t == "minutes":
            val = "45"
        else:
            val = str(bias if i != "US-06" else 2)
        syn_u.append({"participant_id": pid, "item_id": i, "response_value": val, "experiment_id": "EXP-03", "pass_type": "independent_human", "dataset_role": "synthetic_demonstration"})
wcsv(EXP / "EXP-03_codebook_usability/responses/synthetic_responses.csv", ["participant_id", "item_id", "response_value", "experiment_id", "pass_type", "dataset_role"], syn_u)

# --- EXP-04 evidence layers ---
L04 = [
    ("L04-01", "A national guidance document requires schools to maintain lockdown procedures.", "1", "doctrine text"),
    ("L04-02", "The school board approved a local lockdown policy last term.", "2", "local adoption"),
    ("L04-03", "Two trained marshals and a working PA system are available during school hours.", "3", "capability/resources"),
    ("L04-04", "Observers timed a drill: all classes reached secure rooms in under four minutes.", "4", "exercised performance"),
    ("L04-05", "After a real incident, after-action review found delayed lockdown initiation.", "5", "real-world outcome"),
    ("L04-06", "The school has a written PEEP template on file.", "2", "adoption of document, not capability"),
    ("L04-07", "A named buddy is rostered and present for Student X during the school day.", "3", "actual availability"),
    ("L04-08", "The calendar lists two lockdown drills for the year.", "2", "scheduled ≠ performed"),
    ("L04-09", "Video of yesterday's drill shows students misunderstanding the PA message.", "4", "observed drill performance"),
    ("L04-10", "The drill went smoothly, so the school claims the plan would work in a real attack.", "4", "performance ≠ Layer 5 effectiveness — classify statement's evidenced layer as 4; overclaim flagged"),
    ("L04-11", "Accessible exit signage is installed throughout the building.", "3", "environmental capability/support"),
    ("L04-12", "A comprehension check during drill showed three students could not interpret the signs under noise.", "4", "demonstrated comprehension issue"),
    ("L04-13", "A memorandum of understanding with local police is signed.", "2", "agreement adopted"),
    ("L04-14", "During a tabletop, police liaison and school leads completed the escalation decision tree in 8 minutes.", "4", "exercised coordination"),
    ("L04-15", "National doctrine says plans should be inclusive.", "1", "doctrine"),
    ("L04-16", "Staff report that inclusive adaptations are rarely staffed on drill day.", "3", "capability gap report"),
    ("L04-17", "Incident statistics show fewer injuries after a new plan — attributed causally without design.", "5", "outcome claim; weak causal warrant"),
    ("L04-18", "The centre downloaded the national template but never completed local fields.", "2", "partial adoption"),
]
wcsv(
    EXP / "EXP-04_evidence_layers/materials/cases.csv",
    ["case_id", "stimulus_text", "source_status", "experiment_id", "NOT_EXECUTED"],
    [{"case_id": i, "stimulus_text": t, "source_status": "synthetic_constructed", "experiment_id": "EXP-04", "NOT_EXECUTED": "true"} for i, t, *_ in L04],
)
wcsv(
    EXP / "EXP-04_evidence_layers/reference/reference_adjudication.csv",
    ["case_id", "reference_layer", "reference_label", "not_true_answer", "explanation", "overclaim_flag", "experiment_id"],
    [{
        "case_id": i, "reference_layer": layer, "reference_label": "REFERENCE_ADJUDICATION",
        "not_true_answer": "true", "explanation": exp,
        "overclaim_flag": "yes" if i in {"L04-10", "L04-17"} else "no",
        "experiment_id": "EXP-04",
    } for i, t, layer, exp in L04],
)
wcsv(
    EXP / "EXP-04_evidence_layers/responses/response_template.csv",
    ["participant_id", "case_id", "assigned_layer", "confidence_1_to_5", "notes", "experiment_id", "pass_type"],
    [{"participant_id": "", "case_id": i, "assigned_layer": "", "confidence_1_to_5": "", "notes": "", "experiment_id": "EXP-04", "pass_type": "independent_human"} for i, *_ in L04],
)
syn_l = []
for i, t, layer, exp in L04:
    syn_l.append({"participant_id": "SYN-RATER-1", "case_id": i, "assigned_layer": layer, "confidence_1_to_5": "4", "notes": "synthetic", "experiment_id": "EXP-04", "pass_type": "independent_human", "dataset_role": "synthetic_demonstration"})
    wrong = "3" if layer != "3" else "2"
    if i == "L04-10":
        wrong = "5"  # common overclaim
    syn_l.append({"participant_id": "SYN-RATER-2", "case_id": i, "assigned_layer": wrong if i in {"L04-06", "L04-08", "L04-10", "L04-13"} else layer, "confidence_1_to_5": "3", "notes": "synthetic errors on adoption/performance confusions", "experiment_id": "EXP-04", "pass_type": "independent_human", "dataset_role": "synthetic_demonstration"})
wcsv(EXP / "EXP-04_evidence_layers/responses/synthetic_responses.csv", ["participant_id", "case_id", "assigned_layer", "confidence_1_to_5", "notes", "experiment_id", "pass_type", "dataset_role"], syn_l)

# --- EXP-05 domain ratings ---
domains = [
    ("A", "Governance and doctrine adoption"),
    ("B", "Organisational sensing and threat detectability"),
    ("C", "Decision authority and interagency coordination"),
    ("D", "Protective-action executability"),
    ("E", "Inclusive access and functional supports"),
    ("F", "Security-by-design and environmental conditions"),
    ("G", "Training, exercises, and organisational learning"),
    ("H", "Evidence use and revision"),
]
rating_fields = [
    "relevance_1_to_4", "clarity_1_to_4", "necessity_1_to_4", "observability_1_to_4",
    "applicability_across_settings_1_to_4", "functional_diversity_sensitivity_1_to_4",
    "misuse_risk_1_to_4", "belongs_in_slapa_yes_no", "primary_evidence_mode",
    "qualitative_comment",
]
rows5 = []
for d, label in domains:
    rows5.append({
        "domain_id": d, "domain_label": label, "experiment_id": "EXP-05",
        "validation_status": "planned_unvalidated",
    })
wcsv(EXP / "EXP-05_slapa_content_mapping/materials/domains.csv", ["domain_id", "domain_label", "experiment_id", "validation_status"], rows5)

blank5 = []
for d, label in domains:
    blank5.append({
        "participant_id": "", "expertise_profile_id": "", "conflict_of_interest": "",
        "domain_id": d, **{f: "" for f in rating_fields}, "experiment_id": "EXP-05",
    })
wcsv(EXP / "EXP-05_slapa_content_mapping/responses/response_template.csv", list(blank5[0].keys()), blank5)

syn5 = []
for pid, exp_id in [("SYN-EXPERT-1", "EPROF-01"), ("SYN-EXPERT-2", "EPROF-02"), ("SYN-EXPERT-3", "EPROF-03")]:
    for d, label in domains:
        # relevance mostly 3-4; B has higher misuse risk
        syn5.append({
            "participant_id": pid, "expertise_profile_id": exp_id, "conflict_of_interest": "none_declared",
            "domain_id": d,
            "relevance_1_to_4": "4" if d in {"D", "E", "G"} else "3",
            "clarity_1_to_4": "3",
            "necessity_1_to_4": "4" if d != "F" else "3",
            "observability_1_to_4": "2" if d == "B" else "3",
            "applicability_across_settings_1_to_4": "3",
            "functional_diversity_sensitivity_1_to_4": "4" if d in {"D", "E"} else "2",
            "misuse_risk_1_to_4": "4" if d == "B" else "2",
            "belongs_in_slapa_yes_no": "yes",
            "primary_evidence_mode": "observation" if d == "F" else "interview" if d == "C" else "document" if d == "A" else "mixed",
            "qualitative_comment": "synthetic comment — Domain B must stay separate from D" if d == "B" else "synthetic",
            "experiment_id": "EXP-05",
            "dataset_role": "synthetic_demonstration",
        })
wcsv(EXP / "EXP-05_slapa_content_mapping/responses/synthetic_responses.csv", list(syn5[0].keys()), syn5)
wcsv(
    EXP / "EXP-05_slapa_content_mapping/materials/expertise_profile_template.csv",
    ["expertise_profile_id", "role_category", "years_experience_band", "setting_familiarity", "btam_familiarity", "afn_familiarity", "notes"],
    [
        {"expertise_profile_id": "EPROF-01", "role_category": "school_leadership", "years_experience_band": "10-19", "setting_familiarity": "inclusive_mainstream", "btam_familiarity": "low", "afn_familiarity": "medium", "notes": "synthetic"},
        {"expertise_profile_id": "EPROF-02", "role_category": "special_education", "years_experience_band": "5-9", "setting_familiarity": "special_education", "btam_familiarity": "low", "afn_familiarity": "high", "notes": "synthetic"},
        {"expertise_profile_id": "EPROF-03", "role_category": "emergency_police", "years_experience_band": "10-19", "setting_familiarity": "multi", "btam_familiarity": "high", "afn_familiarity": "low", "notes": "synthetic"},
    ],
)

# --- EXP-06 synthetic schools ---
schools = [
    {
        "case_id": "CASE-A",
        "setting_type": "mainstream_inclusive",
        "fictional_name": "Northbridge Community School",
        "fictional_location": "Municipality of Rivermark (fictional)",
        "pupil_roll": "620",
        "profile": "Inclusive mainstream primary/secondary; ~12% pupils with identified additional support needs; mixed building ages.",
        "building": "Two connected blocks; one lift; rear playground exit with step; PA in classrooms; visual beacons in new block only.",
        "plan_extract": "SYNTHETIC: Local plan adopts national lockdown/evac options; PEEP list mentioned but incomplete; revision dated last year without linked drill findings.",
        "staffing": "Security lead (teacher+TLR); SENCO 0.6 FTE; fire marshals present; no dedicated drill inclusion marshal.",
        "comms": "PA + staff phones; no guaranteed multimodal alert in old block.",
        "supports": "Some PEEPs drafted; buddy system informal; sensory room exists but not linked to lockdown plan.",
        "coordination": "Signed municipal emergency contact sheet; no recent joint tabletop.",
        "drill_records": "Two drills scheduled; one completed; notes say 'went well' without timing or access checks.",
        "reporting": "Staff concern form exists; unclear specialist participation rules.",
        "revision_history": "Plan updated after inspection; not after drills.",
    },
    {
        "case_id": "CASE-B",
        "setting_type": "special_education",
        "fictional_name": "Cedar Hollow Specialist Centre",
        "fictional_location": "Borough of Eastmere (fictional)",
        "pupil_roll": "140",
        "profile": "Special education centre; high staff-to-pupil ratios; many pupils need assisted movement; internal and external threat planning required without deficit framing.",
        "building": "Single-storey; wide corridors; secure entrance lobby; some classrooms with secondary exits; garden fencing.",
        "plan_extract": "SYNTHETIC: Site-specific PPMS-like plan; assisted evacuation routes documented; silence-based lockdown alternatives described for some classes; annual exercises required.",
        "staffing": "Always ≥2 adults per class; on-call nurse; transport staff midday; night residual occupancy rare.",
        "comms": "Visual+auditory alerts; staff radios; learner AAC devices variable by class.",
        "supports": "Individual emergency plans for most pupils; sensory regulation kits; mobility aids checked weekly.",
        "coordination": "Quarterly liaison with local police disability liaison officer (fictional role).",
        "drill_records": "Two exercises completed; one adapted scenario; REX notes led to route change for Class 4.",
        "reporting": "Concern pathways include baseline-aware guidance draft; FP safeguards under development.",
        "revision_history": "Route change after exercise REX — Layer 4→H link present.",
    },
    {
        "case_id": "CASE-C",
        "setting_type": "further_education_campus",
        "fictional_name": "Harbourview Sixth Form College",
        "fictional_location": "City of Porthaven (fictional)",
        "pupil_roll": "1100",
        "profile": "Post-16 campus; open daytime access; mixed adult learners; shared municipal sports hall.",
        "building": "Multi-building campus; public footpath crossing; complex lock regimes.",
        "plan_extract": "SYNTHETIC: Invacuation preferred; limited lockdown hardware in older halls; grab kits listed.",
        "staffing": "Estates security officers daytime; teaching staff variable evening classes.",
        "comms": "Campus SMS + PA inconsistent across buildings.",
        "supports": "Accessibility services office; PEEPs for registered students only.",
        "coordination": "City emergency planning liaison annual meeting.",
        "drill_records": "One staff-only drill; learners often not included.",
        "reporting": "Online tip form; out-of-hours unclear.",
        "revision_history": "Hardware upgrade proposal pending budget.",
    },
]
wcsv(EXP / "EXP-06_synthetic_school_assessment/materials/synthetic_cases.csv", list(schools[0].keys()) + ["experiment_id", "fictional_disclaimer"], [{**s, "experiment_id": "EXP-06", "fictional_disclaimer": "All names locations and persons are fictional. No real school is depicted. Disability is never a threat proxy."} for s in schools])

# assessor response template
doms = ["A", "B", "C", "D", "E", "F", "G", "H"]
blank6 = []
for s in schools:
    for d in doms:
        blank6.append({
            "participant_id": "",
            "case_id": s["case_id"],
            "domain_id": d,
            "can_assess_yes_no_partial": "",
            "evidence_cited": "",
            "evidence_layer": "",
            "information_missing": "",
            "unjustified_if_scored": "",
            "additional_evidence_to_request": "",
            "notes": "",
            "experiment_id": "EXP-06",
            "total_readiness_score": "",  # must remain empty — forbidden
        })
wcsv(EXP / "EXP-06_synthetic_school_assessment/responses/response_template.csv", list(blank6[0].keys()), blank6)

# reference analysis (provisional)
ref6 = []
for s in schools:
    for d in doms:
        layer = "2" if d == "A" else "3" if d in {"E", "F"} else "4" if d in {"G", "H"} and s["case_id"] == "CASE-B" else "2"
        can = "yes" if s["case_id"] == "CASE-B" and d in {"D", "E", "G", "H"} else "partial"
        ref6.append({
            "case_id": s["case_id"],
            "domain_id": d,
            "reference_can_assess": can,
            "reference_layer_emphasis": layer,
            "reference_label": "REFERENCE_ADJUDICATION",
            "not_true_answer": "true",
            "notes": "Provisional synthetic reference; domain profiles only; no total score.",
            "experiment_id": "EXP-06",
        })
wcsv(EXP / "EXP-06_synthetic_school_assessment/reference/reference_adjudication.csv", list(ref6[0].keys()), ref6)

syn6 = []
for pid in ["SYN-ASSESSOR-1", "SYN-ASSESSOR-2"]:
    for row in blank6:
        r = dict(row)
        r["participant_id"] = pid
        r["can_assess_yes_no_partial"] = "partial"
        r["evidence_layer"] = "2"
        r["evidence_cited"] = "synthetic packet fields"
        r["information_missing"] = "direct observation"
        r["unjustified_if_scored"] = "any Layer-5 effectiveness claim"
        r["additional_evidence_to_request"] = "timed inclusive drill observation"
        r["dataset_role"] = "synthetic_demonstration"
        r["total_readiness_score"] = ""  # keep empty
        syn6.append(r)
wcsv(EXP / "EXP-06_synthetic_school_assessment/responses/synthetic_responses.csv", list(syn6[0].keys()), syn6)

print("Generated experiment materials under", EXP)


if __name__ == "__main__":
    main = None
    # executed at import/run
