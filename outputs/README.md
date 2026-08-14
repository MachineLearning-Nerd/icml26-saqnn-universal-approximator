# Output directory

These files are retained evidence rather than scratch output.

- `full_audit.json`: source-pinned audit of the official three-claim live contract.
- `claim_verification.json`: fail-closed live-contract result and `6/6` local points.
- `test_results.json`: reproducibility test result.
- `evidence_bundle.json`: SHA-256 inventory of the evidence surface.
- `publication_gate.json`: normalized five-claim release decision.
- `PUBLICATION_GATE_PASSED.json`: compatibility filename for the same decision.
- `reproduction_bundle.zip` and its manifest: portable source/evidence bundle.

The paper-level evidence for C1–C5 is organized under
`.openresearch/artifacts/` and the reader-facing report under
`reports/saqnn-reproduction/`.
