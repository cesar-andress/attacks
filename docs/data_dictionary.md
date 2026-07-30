# Data dictionary

Stable identifiers use opaque string IDs (`CF-…`, `DOC-…`, `pe_…`).  
Dates use ISO-8601 (`YYYY-MM-DD`) when known.

## Candidate-frame status (v0.1 — not frozen)

This repository currently holds a **provisional candidate framework register (v0.1)**.

- It is **not** a frozen corpus.
- **Identity verification** is distinct from **eligibility screening**.
- **Surface indications** in sampling/counterexample fields are **not** audit findings.
- Final sampling decisions require provenance checks and full-text screening.

Forbidden in this provisional register: `included`, `excluded`, `frozen`, `final`, `corpus_frozen`, and the geography label `EU/UK`.

## L0 — Framework (`data/corpus/candidate_frameworks.csv`)

| Field | Type | Description |
|---|---|---|
| framework_id | string | Provisional ID (e.g. `CF-01`) |
| framework_name | string | Provisional official name |
| issuing_body | string | Issuer if known; may be `unresolved` |
| authority_type | enum | `government`, `professional_association`, `peer_reviewed`, `research_centre`, `non_profit`, `standards_organisation`, `supranational`, `other`, `unresolved` |
| primary_domain | enum | See domain list |
| secondary_domains | string | Pipe-separated domain tags |
| jurisdiction | string | Country / region as stated |
| geographic_region | enum | `US`, `Europe`, `other`, `multi`, `unspecified` |
| eu_member_state | enum | `yes`, `no`, `not_applicable` (England/UK → `no`) |
| intended_setting_scope | string | Document’s own terminology |
| comparator_status | enum | `frame_candidate`, `benchmark_comparator_candidate`, `not_comparator` |
| version_date_text | string | Free-text version/date claims (may be unresolved) |
| source_domain_text | string | Domain/host text; exact URLs optional |
| identity_status | enum | `candidate_verified_identity`, `candidate_partly_verified`, `candidate_unverified`, `excluded_before_full_text` |
| screening_status | enum | `not_screened`, `uncertain_pending_full_text`, `likely_eligible`, `likely_ineligible` |
| provenance_confidence | enum | `verified_official_source`, `partly_verified`, `known_not_reverified`, `provisional_to_locate` |
| sampling_relevance_note | string | Why the candidate is in the frame |
| potential_counterexample_surface_indication | string | Pre-coding surface note only — **not** a coded finding |
| exclusion_or_uncertainty_concern | string | Eligibility/provenance concern |
| unresolved_verification_action | string | Required for unverified identity statuses |
| framework_notes | string | Free text |
| register_status | enum | Only `provisional_v0.1` |

**Domains:** `physical_security`, `btam`, `eop`, `active_assailant_response`, `cpted`, `accessibility_afn`, `comprehensive_school_safety`, `prevention_radicalisation`, `other`.

## L1 — Document (`data/corpus/document_registry.csv`)

| Field | Type | Description |
|---|---|---|
| document_id | string | Provisional document ID |
| framework_id | string | FK → L0 |
| title | string | Provisional title (or placeholder) |
| version | string | Edition/version text |
| publication_date | string | If known |
| retrieval_date | string | Optional |
| source_url | string | Only if known; do not invent |
| source_domain_text | string | Host/domain text |
| language | string | BCP-47 preferred |
| document_type | enum | `guideline`, `assessment_tool`, `standard`, `regulatory_instrument`, `annex`, `other`, `placeholder` |
| relationship_type | enum | `primary_document`, `companion_assessment_tool`, `implementation_guide`, `appendix_or_annex`, `regulatory_instrument`, `related_but_independent_framework`, `placeholder_unverified` |
| is_primary_document | enum | `yes` / `no` |
| redistribution_status | enum | `unknown`, `prohibited`, `permitted`, `public_domain`, `fair_use_excerpts_only` |
| local_file_status | enum | `none`, `local_ignored`, `tracked_open` |
| identity_status / screening_status / provenance_confidence | enums | Same as framework |
| unresolved_verification_action | string | Required when unverified |
| exclusion_or_uncertainty_concern | string | |
| document_notes | string | |

Local PDFs are **not required**. Public repo may store metadata without URLs.

## Counterexample commitments (`data/corpus/counterexample_commitments.csv`)

Pre-coding commitments only. **Not** findings.

| Field | Description |
|---|---|
| candidate_id | FK → framework |
| reason_selected_as_possible_disconfirming_case | Sampling reason |
| date_committed | ISO date |
| status | `committed_pre_coding` / `withdrawn` / `superseded` |
| surface_indication | Surface note only |
| warning_not_coded_finding | Must state `NOT_A_CODED_FINDING` |

Must not contain codebook tokens such as `executability_rung` or claim audit findings.

## L2 — Prescriptive element / coding

Unchanged templates under `data/coding/`. Do not populate with real framework text in this task.

## OpenAlex literature verifications (`data/corpus/openalex_literature_verifications.csv`)

Optional scholarly-identity checks via OpenAlex. See [`docs/protocol/openalex_verification.md`](protocol/openalex_verification.md).

Required retained fields: OpenAlex work ID, DOI (if any), title, authors, year, source/journal, retrieval date, verification status.

`does_not_authorize_corpus_inclusion` must be `true`. OpenAlex hits never auto-add candidates to the corpus.

Not authoritative for current government guidance versions, official URLs, supersession, legal status, adoption, or copyright.

## Pilot source acquisition (full text gitignored)

| File | Role |
|---|---|
| `data/source_registry/pilot_source_acquisitions.csv` | Per-source acquisition/provenance/authorization records |
| `data/source_checksums/pilot_source_checksums.csv` | SHA-256 for acquired local files |
| `data/source_registry/pilot_source_readiness.csv` | P1–P5 disposition summary |
| `data/pilot/PILOT_SOURCE_GATE.txt` | Complete-pilot `PILOT_SOURCE_*` gate |
| `data/gates/gate_register.csv` | Separate gates (complete / operational / benchmark / freeze / full coding) |
| `local_sources/` | Local full text + Phase A excerpts (**gitignored**; not redistributed) |

## Freeze-readiness and dispositions (not inclusion)

| File | Role |
|---|---|
| `data/corpus/freeze_readiness_register.csv` | Blocking/status register for freeze |
| `data/corpus/candidate_disposition_recommendations.csv` | Recommended `include`/`exclude`/`hold`/`comparator`/`background_only` — **not** frozen inclusion |
| `data/pilot/*` | Pilot artefacts; triple labels (`NOT_FOR_SUBSTANTIVE_INFERENCE`, `NOT_FOR_BENCHMARK_COMPARISON`, `PROTOCOL_DEVELOPMENT_ONLY`); Phase A may be completed while complete pilot remains incomplete |

Disposition values must not be written into `screening_status` or `register_status`.

## Inclusion log (`data/corpus/inclusion_log.csv`)

Tracks later screening decisions (still empty for v0.1).
