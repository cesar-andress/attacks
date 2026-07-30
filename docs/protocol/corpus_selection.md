# Corpus selection (draft procedure)

**Status:** draft — **candidate-frame version 0.1 (not frozen).**  
A provisional register of CF-01–CF-22 lives in `data/corpus/candidate_frameworks.csv`.

Important distinctions:

- Identity verification ≠ eligibility screening ≠ audit coding.
- Surface indications / counterexample commitments are **not** findings.
- Final sampling decisions require provenance checks and full-text screening.
- Do not describe this register as an 8-framework final corpus.

## Inclusion criteria (all required)

A document qualifies as a framework artifact if it:

1. Is **prescriptive or assessment-oriented** (recommendations, standards, controls, checklists, or assessment questions).
2. Addresses at least one in-scope domain:
   - school physical security
   - behavioural threat assessment / BTAM
   - emergency operations planning
   - active-assailant / lone-actor response
   - CPTED applied to schools/education settings
   - accessibility / access-and-functional-needs emergency planning
3. Is **attributable and citable** (issuing body, date, version).
4. Is **general** (intended for adoption across schools or a jurisdiction), not a single school’s internal procedure.

## Exclusion criteria

- Vendor/marketing material and product documentation.
- Opinion/advocacy pieces and news without prescriptive content.
- Isolated single-institution procedures (unless a labelled bounded comparator set).
- Pure empirical papers that study frameworks but do not prescribe.
- Documents without a stable version/date.

## Sampling strategy

Purposive, criterion-based, **maximum-variation** sampling with a documented frame — not convenience sampling, and not a claim of statistical representativeness.

Stratify along:

1. Authority type (government/agency, professional association, peer-reviewed).
2. Domain (cover each in-scope domain that exists).
3. Geography (US and European sources; record each jurisdiction’s own setting labels).
4. Recency (current version as primary).
5. **Benchmark comparators** — accessibility/AFN frameworks included as a documentary falsification route (not experimental positive controls).

## Anti-confirmation safeguards

- Freeze the frame before deep coding; log dates and search paths.
- Preregister the expected direction **and** the disconfirming pattern.
- Include strongest candidates *against* the gap hypothesis, named before coding.
- Record every excluded candidate and reason in `data/corpus/inclusion_log.csv`.

## Public repository vs local PDFs

- Public data: metadata, URLs, inclusion status, open derived tables.
- Local PDFs: optional, ignored by git (`data/sources/`), only if redistribution is permitted or fair-use excerpts are used under local legal responsibility.
- `redistribution_status` and `local_file_status` on document records track this explicitly.
