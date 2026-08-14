# Publication gate

## Decision

`evidence_release_gate = PASSED`

`overall_status = VERIFIED_SCOPED`

`strict_paper_gate = NOT_READY`

Five claim contracts pass within their declared source scopes. The strict gate
stays open because finite exact witnesses and convergence studies cannot prove
the paper's universal quantifier or all asymptotic statements on their own.

## Machine-readable records

- `publication_gate.json` — canonical root copy
- `outputs/publication_gate.json` — output copy
- `outputs/PUBLICATION_GATE_PASSED.json` — compatibility copy
- `outputs/evidence_bundle.json` — SHA-256 inventory of the release surface
- `outputs/claim_verification.json` — official three-claim live-contract result

## Reproduction command

```bash
uv sync --frozen && uv run --frozen python repro/run_all.py
```

The command must finish with the release-asset integrity check and the
hash-addressed bundle. The external challenge score is intentionally not
rewritten by this local gate.
