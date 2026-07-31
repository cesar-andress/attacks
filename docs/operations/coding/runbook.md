# Independent coding runbook

## Principles

- Independence until reliability is calculated.  
- Raw coder files are immutable after lock.  
- Clarifications are procedural, logged, and symmetrically shared when relevant.

## Operations

1. Assignment release with coder-specific paths  
2. Write permissions only to assigned drop folders  
3. Naming: `CODERID_DOCID_attempt.csv`  
4. Version control via checksums + timestamps  
5. Deadlines recorded in dashboard  
6. Backup policy: PI retains hashed submissions  
7. Allowed clarifications: unitization procedure, schema fields, file format  
8. Prohibited: case-level answer leading; sharing other coder values  
9. Submission validation then lock  
10. Audit trail in attempt/coding logs  
11. Incidents → confidentiality incident form  
12. Late submissions: document; do not silently alter others' files  
13. Withdrawal/replacement: revoke access; do not reopen sealed materials to failed candidates

## Clarification log

Use `data/operations/clarification_log_template.csv`.
