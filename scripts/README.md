# Scripts

Thin CLI wrappers around the importable package `school_security_audit`.

```bash
# From repository root
PYTHONPATH=src python3 scripts/validate_metadata.py
PYTHONPATH=src python3 scripts/validate_coding.py
PYTHONPATH=src python3 -m school_security_audit.validate_pilot_phase
PYTHONPATH=src python3 -m school_security_audit.validate_research_program

# Or after editable install
pip install -e ".[dev]"
ssa-validate-metadata
ssa-validate-coding
ssa-validate-pilot-phase
ssa-validate-research-program
```

Phase A record regeneration (dev only; does not authorize Phase B):

```bash
PYTHONPATH=src python3 scripts/generate_phase_a_pilot_records.py
```

OpenAlex literature verification (optional; requires `OPEN_ALEX_KEY` in env):

```bash
source ~/.bashrc   # loads OPEN_ALEX_KEY; do not echo it
PYTHONPATH=src python3 scripts/verify_openalex.py --dry-run
PYTHONPATH=src python3 scripts/verify_openalex.py
```

See `docs/protocol/openalex_verification.md`.

Validation rules (selected):

- Required CSV headers for frameworks, documents, PEs, and coding records
- JSON Schema checks where applicable
- Executability rung ∈ {0…5}; locus ∈ {individual, subgroup, setting, multiple, not_specified}
- `ambiguous_memo` demand sources cannot be stored as demand presence (`1`)
- Entailed demands require trigger evidence
- Orphan `framework_id` / `document_id` / `pe_id` references are rejected
- Codebook versions on coding rows must exist in the codebook YAML
- Combined E+F composite score fields are rejected
