# Validation contract

Passing `make release-check` means:

1. Metadata/coding/pilot/research-programme validators succeed.  
2. Phase-B / coder-workflow validators succeed (including freeze integrity and sealed target).  
3. Experimental pack validators succeed.  
4. Full pytest suite passes.  
5. Synthetic experiment analyses run and refuse prohibited claims (α from procedural pass; total SLAPA score; human-executed status).

For tag **v1.0.0**, passing `make release-check` is required before release publication.

It does **not** mean:

- human experiments were executed;  
- SLAPA is validated;  
- documentary corpus is frozen;  
- complete pilot is finished;  
- an independent coder is READY;  
- Phase-B target coding has begun;  
- empirical Results exist.
