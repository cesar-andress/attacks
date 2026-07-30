# Data dictionary

Stable identifiers use opaque string IDs (`fw_…`, `doc_…`, `pe_…`).  
Dates use ISO-8601 (`YYYY-MM-DD`) when known.

## L0 — Framework (`data/corpus/candidate_frameworks.csv`)

| Field | Type | Description |
|---|---|---|
| framework_id | string | Stable ID |
| framework_name | string | Short display name |
| issuing_body | string | Author / agency |
| authority_type | enum | `government`, `professional_association`, `peer_reviewed`, `other` |
| primary_domain | enum | See domain list below |
| secondary_domains | string | Pipe-separated domain tags |
| jurisdiction | string | Country / region as stated |
| geographic_group | enum | `US`, `Europe`, `other`, `multi`, `unspecified` |
| intended_setting_scope | string | As stated by document; `unspecified` if silent |
| comparator_status | enum | `main_corpus`, `benchmark_comparator`, `excluded_candidate` |
| current_version | string | Version label |
| framework_notes | string | Free text |

**Domains:** `physical_security`, `btam`, `eop`, `active_assailant_response`, `cpted`, `accessibility_afn`, `other`.

## L1 — Document (`data/corpus/document_registry.csv`)

| Field | Type | Description |
|---|---|---|
| document_id | string | Stable ID |
| framework_id | string | FK → framework |
| title | string | Document title |
| version | string | Edition / version |
| publication_date | date | Publication date if known |
| retrieval_date | date | When metadata/URL was recorded |
| source_url | string | Canonical URL (no local path required) |
| language | string | BCP-47 preferred (`en`, `es`, …) |
| document_type | enum | `guideline`, `assessment_tool`, `standard`, `other` |
| redistribution_status | enum | `unknown`, `prohibited`, `permitted`, `public_domain`, `fair_use_excerpts_only` |
| local_file_status | enum | `none`, `local_ignored`, `tracked_open` |
| checksum_sha256 | string | Optional; empty if no local file |
| page_count | integer | Optional |
| word_count | integer | Optional (sensitivity analyses only) |
| inclusion_status | enum | `included`, `excluded`, `candidate`, `deferred` |
| exclusion_reason | string | Required when excluded |

Local PDFs are **not required**. Public repo may store metadata + URL only.

## L2 — Prescriptive element (`data/coding/prescriptive_elements.csv`)

| Field | Type | Description |
|---|---|---|
| pe_id | string | Stable ID |
| document_id | string | FK → document |
| source_location | string | Locator string (section/PDF page range) |
| page_number | string | Page if applicable |
| section_heading | string | Nearest heading |
| verbatim_trigger_text | string | Short excerpt; copyright limits apply — leave empty until reviewed |
| coder_segmentation_notes | string | Unitizing notes |
| measure_present | enum | `0`, `1` |
| measure_type | enum | See codebook B2 |
| prescriptive_force | enum | `required`, `recommended`, `optional`, `unspecified` |

## Coding records (`data/coding/coding_template.csv`)

Key fields:

| Field | Notes |
|---|---|
| coder_id | Coder identifier (non-personal preferred) |
| coding_round | e.g. `pilot`, `main`, `adjudication` |
| codebook_version | Must match a published codebook version |
| pe_id | FK → PE |
| Family B–I codes | See codebook |
| `demand_*_source` | `explicit` / `entailed` / `ambiguous_memo` / empty |
| `demand_*_trigger` | Required for `entailed` |
| executability_rung | 0–5 |
| executability_locus | `individual` / `subgroup` / `setting` / `multiple` / `not_specified` |
| qualitative_memo | Free text |
| adjudication_status | `none` / `pending` / `resolved` |
| adjudicated_value | Optional resolved JSON/string |

**Forbidden:** any field named like `inclusive_security_score` or combined E+F composites.

## Inclusion log (`data/corpus/inclusion_log.csv`)

Tracks screening decisions for auditability (PRISMA-style documentation flow adapted for frameworks).
