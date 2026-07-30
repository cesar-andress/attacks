# Scripts

Thin CLI wrappers around the importable package `school_security_audit`.

```bash
# From repository root
PYTHONPATH=src python3 scripts/validate_metadata.py
PYTHONPATH=src python3 scripts/validate_coding.py

# Or after editable install
pip install -e ".[dev]"
ssa-validate-metadata
ssa-validate-coding
```

Validation rules (selected):

- Required CSV headers for frameworks, documents, PEs, and coding records
- JSON Schema checks where applicable
- Executability rung ∈ {0…5}; locus ∈ {individual, subgroup, setting, multiple, not_specified}
- `ambiguous_memo` demand sources cannot be stored as demand presence (`1`)
- Entailed demands require trigger evidence
- Orphan `framework_id` / `document_id` / `pe_id` references are rejected
- Codebook versions on coding rows must exist in the codebook YAML
- Combined E+F composite score fields are rejected
