# Corpus-freeze runbook (do not freeze prematurely)

**Current gate:** corpus_freeze_gate = NO_GO.

## Pre-freeze checks

- Source eligibility vs protocol  
- Inclusion/exclusion decisions logged  
- Duplicate detection  
- Document version + retrieval date + provenance  
- Filename policy + normalization  
- Checksums for each L1 file  
- Copyright classification + redistribution status  
- Restricted-storage path (`local_sources/`, gitignored)  
- Corpus index + freeze manifest draft  

## Freeze action (when authorized)

1. Write freeze manifest with file list, checksums, versions, dates.  
2. Tag codebook/protocol versions used.  
3. Set corpus_freeze_gate only when exit criteria truly met.  
4. Announce freeze; disable silent file swaps.

## Post-freeze change control

Any change requires: reason; affected files; old checksum; new checksum; impact assessment; authorization; deviation/amendment status.  
No silent edits.
