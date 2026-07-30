# School-security framework audit (public infrastructure)

Public, reproducible research software and metadata templates for a **structured documentary content analysis** of school-security and emergency-preparedness frameworks.

This repository supports **methods, schemas, codebook drafts, empty data templates, and validation tooling**. It does **not** contain the private manuscript, and it does **not** redistribute copyrighted framework PDFs unless redistribution is explicitly permitted and documented.

## Scientific purpose

The study asks whether recognized school-security and preparedness frameworks address, in their own prescriptive text:

1. **Protective-action executability** — whether measures are assessed/tested as executable by intended occupants under realistic conditions (Branch E).
2. **Threat detectability** — whether detection/assessment processes address high capability-variance populations and false-positive safeguards (Branch F).

These are **two separate analytical branches**. The repository deliberately does **not** define or accept a single combined “inclusive security score.”

## What this study is (and is not)

| This study **is** | This study **is not** |
|---|---|
| A documentary audit of frameworks | An effectiveness / outcome evaluation |
| A content analysis of what documents prescribe and assess | A claim that measures work (or fail) in real incidents |
| A methods-preregistrable coding design | A replacement for field validation of school practice |

Allowed and disallowed claim types are bindingly stated in [`docs/protocol/claims_policy.md`](docs/protocol/claims_policy.md).

## Units of analysis (L0 / L1 / L2)

| Level | Unit | Role |
|---|---|---|
| **L0** | Framework | Doctrine issued by an authority (may span multiple documents) |
| **L1** | Document | Versioned artifact (PDF/edition/tool) |
| **L2** | Prescriptive element (PE) | Atomic coding unit: one discrete prescription, control, or assessment question |

Aggregate upward from PE codes; do not impute framework-level judgements downward onto PEs.

**Default normalization denominator:** counts and rates are expressed **per PE** (or as PE proportions). Word-count density may be added later as a sensitivity analysis only.

## Coding families

| Family | Name |
|---|---|
| A | Framework metadata and scope |
| B | Security measures prescribed |
| C | Procedural demands |
| D | Contextual supports and accommodations |
| E | Protective-action executability |
| F | Threat detectability |
| G | Population and setting differentiation |
| H | Evidence, testing, and validation |
| I | Security–accessibility conflicts and trade-offs |

Executability **depth (rung 0–5)** and **locus** (individual / subgroup / setting / multiple / not specified) are **orthogonal** fields. See the codebook.

For Family C, every coded demand stores a separate `demand_source`:

- `explicit` — stated in text
- `entailed` — necessarily entailed by a prescribed action (entailment table)
- `ambiguous_memo` — uncertain; **must not** count as demand presence in confirmatory analyses

## OpenAlex literature checks

Scholarly identity for selected literature-linked candidates may be verified with the OpenAlex API (`scripts/verify_openalex.py`). Policy and limits: [`docs/protocol/openalex_verification.md`](docs/protocol/openalex_verification.md).

- Load `OPEN_ALEX_KEY` from the environment; never commit or print it.
- OpenAlex does **not** authorize corpus inclusion and is not authoritative for current government guidance versions or official URLs.

## Candidate frame v0.1 (current data status)

`data/corpus/candidate_frameworks.csv` holds a **provisional candidate register** assembled for later screening.

- It is **not** a frozen or final corpus.
- Do not treat candidate counts as a definitive “8 frameworks / 10–12 documents” study corpus.
- **Identity status** (is the doctrine identifiable?) is distinct from **screening status** (likely eligibility).
- **Surface indications** and `counterexample_commitments.csv` are sampling commitments, **not** audit findings or codebook values.
- England/UK use `geographic_region=Europe` and `eu_member_state=no` — never `EU/UK`.

## Freeze rules and falsification

Before main coding:

1. Complete provenance checks and full-text screening; then freeze the **corpus inclusion list**.
2. Freeze the **codebook** and **demand-entailment table** versions.
3. Preregister directional expectations **and** the disconfirming pattern.

**Benchmark comparator candidates** (accessibility / AFN) provide a falsification route once eligibility is confirmed: if general frameworks reach comparator scores on executability/support codes, the gap hypothesis is weakened or retired. They are **not** experimental “positive controls.”

## Copyright and local sources

- The public repo stores **metadata, URLs, schemas, templates, and derived open data**.
- Local PDFs (if any) belong under ignored paths such as `data/sources/` and are **not** tracked.
- `verbatim_trigger_text` fields may hold short excerpts for coding auditability; researchers remain responsible for fair-dealing / fair-use and copyright limits. **Do not populate PE tables with real framework text until legally reviewed.**
- The manuscript is maintained **privately outside this repository**.

## Repository layout

```text
attacks/
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── docs/                 # protocol, codebook, data dictionary
├── schemas/              # JSON Schemas for L0/L1/L2/coding
├── data/                 # CSV templates (empty / constructed only)
├── src/school_security_audit/   # validation library (importable)
├── scripts/              # CLI wrappers
└── tests/                # constructed fixtures only
```

## Quick start

```bash
cd ~/papers/attacks/attacks
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Validate empty/template corpus metadata
python3 scripts/validate_metadata.py

# Validate coding templates / fixtures
python3 scripts/validate_coding.py

# Run tests
python3 -m pytest -q
```

Without installing the package:

```bash
PYTHONPATH=src python3 scripts/validate_metadata.py
PYTHONPATH=src python3 -m pytest -q
```

## Citation

See [`CITATION.cff`](CITATION.cff).

## Licence

MIT — see [`LICENSE`](LICENSE). Framework source documents retain their own copyright terms and are not covered by this licence.
