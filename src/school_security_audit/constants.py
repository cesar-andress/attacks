"""Shared constants for validation."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

FRAMEWORK_HEADERS = [
    "framework_id",
    "framework_name",
    "issuing_body",
    "authority_type",
    "primary_domain",
    "secondary_domains",
    "jurisdiction",
    "geographic_region",
    "eu_member_state",
    "intended_setting_scope",
    "comparator_status",
    "version_date_text",
    "source_domain_text",
    "identity_status",
    "screening_status",
    "provenance_confidence",
    "sampling_relevance_note",
    "potential_counterexample_surface_indication",
    "exclusion_or_uncertainty_concern",
    "unresolved_verification_action",
    "framework_notes",
    "register_status",
]

DOCUMENT_HEADERS = [
    "document_id",
    "framework_id",
    "title",
    "version",
    "publication_date",
    "retrieval_date",
    "source_url",
    "source_domain_text",
    "language",
    "document_type",
    "relationship_type",
    "is_primary_document",
    "redistribution_status",
    "local_file_status",
    "checksum_sha256",
    "page_count",
    "word_count",
    "identity_status",
    "screening_status",
    "provenance_confidence",
    "unresolved_verification_action",
    "exclusion_or_uncertainty_concern",
    "document_notes",
]

PE_HEADERS = [
    "pe_id",
    "document_id",
    "source_location",
    "page_number",
    "section_heading",
    "verbatim_trigger_text",
    "coder_segmentation_notes",
    "measure_present",
    "measure_type",
    "prescriptive_force",
]

COUNTEREXAMPLE_HEADERS = [
    "candidate_id",
    "reason_selected_as_possible_disconfirming_case",
    "date_committed",
    "status",
    "surface_indication",
    "warning_not_coded_finding",
]

OPENALEX_HEADERS = [
    "verification_id",
    "candidate_id",
    "document_id",
    "openalex_work_id",
    "doi",
    "title",
    "authors",
    "publication_year",
    "source_or_journal",
    "openalex_type",
    "retrieval_date",
    "verification_status",
    "relation_to_candidate",
    "peer_reviewed_indication",
    "prescriptive_or_assessment_bearing",
    "notes",
    "does_not_authorize_corpus_inclusion",
]

OPENALEX_VERIFICATION_STATUSES = {
    "confirmed_via_openalex",
    "ambiguous_match",
    "not_found",
    "related_literature_only",
    "not_applicable_non_indexed_guidance",
}

DEMAND_FIELDS = [
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
]

CODING_REQUIRED_HEADERS = [
    "coder_id",
    "coding_round",
    "codebook_version",
    "pe_id",
    "executability_rung",
    "executability_locus",
]

EXECUTABILITY_RUNGS = {"0", "1", "2", "3", "4", "5"}
EXECUTABILITY_LOCI = {
    "individual",
    "subgroup",
    "setting",
    "multiple",
    "not_specified",
}
DEMAND_SOURCES = {"explicit", "entailed", "ambiguous_memo"}
CONFIRMATORY_DEMAND_SOURCES = {"explicit", "entailed"}

FORBIDDEN_COMPOSITE_FIELDS = {
    "inclusive_security_score",
    "combined_executability_detectability_score",
    "inclusive_security_index",
}

# Branch B / Family F is retained in schemas but inactive for current-paper aggregates.
BRANCH_B_FAMILY_F_FIELDS = {
    "detection_mechanism_present",
    "baseline_interpretation_addressed",
    "specialist_participation",
    "false_positive_safeguard",
}
BRANCH_B_STATUS = "inactive_for_current_study"

# Pilot records must carry these markers and must not silently enter final analysis.
PILOT_REQUIRED_FLAGS = {
    "pilot_flag": "PILOT",
    "inference_flag": "NOT_FOR_SUBSTANTIVE_INFERENCE",
}

FREEZE_DISPOSITION_VALUES = {
    "include",
    "exclude",
    "hold",
    "comparator",
    "background_only",
}

# RQ2 primary denominator: locus among PEs with executability_rung >= 1
RQ2_PRIMARY_MIN_RUNG = 1
RQ2_COMPLEMENTARY_DENOMINATOR = "all_eligible_pes"

IDENTITY_STATUSES = {
    "candidate_verified_identity",
    "candidate_partly_verified",
    "candidate_unverified",
    "excluded_before_full_text",
}

SCREENING_STATUSES = {
    "not_screened",
    "uncertain_pending_full_text",
    "likely_eligible",
    "likely_ineligible",
}

FORBIDDEN_SCREENING_OR_INCLUSION_VALUES = {
    "included",
    "excluded",
    "frozen",
    "final",
    "corpus_frozen",
    "main_corpus",
}

PROVENANCE_CONFIDENCE = {
    "verified_official_source",
    "partly_verified",
    "known_not_reverified",
    "provisional_to_locate",
}

GEOGRAPHIC_REGIONS = {"US", "Europe", "other", "multi", "unspecified"}
EU_MEMBER_STATE_VALUES = {"yes", "no", "not_applicable"}
FORBIDDEN_GEOGRAPHY_LABELS = {"EU/UK", "eu/uk", "UK/EU", "uk/eu"}

COMPARATOR_STATUSES = {
    "frame_candidate",
    "benchmark_comparator_candidate",
    "not_comparator",
}

RELATIONSHIP_TYPES = {
    "primary_document",
    "companion_assessment_tool",
    "implementation_guide",
    "appendix_or_annex",
    "regulatory_instrument",
    "related_but_independent_framework",
    "placeholder_unverified",
}

REGISTER_STATUSES = {"provisional_v0.1"}
FORBIDDEN_REGISTER_STATUSES = {"frozen", "final", "corpus_frozen"}

# Codebook / audit finding tokens that must not appear in counterexample surface fields
FORBIDDEN_COUNTEREXAMPLE_TOKENS = {
    "executability_rung",
    "executability_locus",
    "demand_alert_perception",
    "false_positive_safeguard",
    "coded_finding",
    "audit_finding",
    "rung>=3",
    "rung >= 3",
}

UNVERIFIED_IDENTITY_STATUSES = {
    "candidate_unverified",
    "excluded_before_full_text",
}

# Specific hard rules from the librarian corrections
CF22_ID = "CF-22"
