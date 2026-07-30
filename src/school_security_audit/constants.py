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
    "geographic_group",
    "intended_setting_scope",
    "comparator_status",
    "current_version",
    "framework_notes",
    "inclusion_status",
]

DOCUMENT_HEADERS = [
    "document_id",
    "framework_id",
    "title",
    "version",
    "publication_date",
    "retrieval_date",
    "source_url",
    "language",
    "document_type",
    "redistribution_status",
    "local_file_status",
    "checksum_sha256",
    "page_count",
    "word_count",
    "inclusion_status",
    "exclusion_reason",
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

COMPARATOR_STATUSES = {"main_corpus", "benchmark_comparator", "excluded_candidate"}
