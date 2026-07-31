# Analytical data lineage

## Pipeline layers

1. Raw source inventory (checksums; gitignored PDFs)  
2. Coder-A output (immutable)  
3. Coder-B output (immutable)  
4. Reliability input extract  
5. Disagreement register  
6. Adjudication layer  
7. Final analytical dataset  
8. Analysis tables  
9. Manuscript outputs  

Each derived file should carry or inherit: source version; script version; timestamp; checksum; responsible role; transformation description.

Manual untracked edits to analytical outputs are forbidden; regenerate via scripts.

Fixture/synthetic outputs must be marked `SYNTHETIC_NOT_FOR_MANUSCRIPT`.
