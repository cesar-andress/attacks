# Adjudication runbook (after reliability)

## Rules

- Begin only after pre-consensus reliability is computed and archived.  
- Never overwrite coder_A / coder_B raw files.  
- Store adjudicated values in a separate layer.  
- Reliability remains pre-adjudication.  
- Link BDD-001…005 resolutions transparently when triggered.

## Record fields

disagreement_id; unit_id; coder_a; coder_b; adjudicator; rationale; evidence_location; final_value; unresolved; codebook_ambiguity; protocol_deviation; bdd_link; timestamp; version.

Templates: `data/operations/disagreement_register_template.csv`, `data/phase_b/bdd_adjudication_blank.csv`.
