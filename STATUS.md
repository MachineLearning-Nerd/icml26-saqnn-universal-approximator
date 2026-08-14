# Status

- Paper: `QaHFVheV8X` — *SAQNN: Spectral Adaptive Quantum Neural Network as a Universal Approximator*
- Authors: Jialiang Tang, Jialin Zhang, and Xiaoming Sun
- Repository: `MachineLearning-Nerd/icml26-saqnn-universal-approximator`
- State: `verified_scoped`
- Evidence-release gate: `PASSED`
- Overall status: `VERIFIED_SCOPED`
- Strict paper-level gate: `NOT_READY`
- Official live challenge score: `9/10` (not changed or rejudged here)
- Official author executable: none found in the accepted source

## Claim status

The repository retains five claim contracts. C1–C5 are verified within their
declared source scopes. The official live contract contains three claims and
six possible points; `outputs/claim_verification.json` records all three live
claims complete for `6/6`. C1 explicitly narrows the paper construction to
`[0,1]`-valued L2 targets, and C3 separates fixed-accuracy/high-dimensional
circuit comparison from fixed-dimension/high-accuracy parameter rates.

## Evidence boundary

The source archive, PDF, and TeX are pinned under `docs/`. The formal run uses
the frozen `uv.lock` environment and local Apple arm64 CPU. The exact command
is:

```bash
uv sync --frozen && uv run --frozen python repro/run_all.py
```

The finite constructions, independent checkers, negative controls, and
release-asset checks are retained under `.openresearch/artifacts/` and
`evidence/`. They support the paper's mechanisms but do not replace the cited
L2-density theorem or prove a universal asymptotic claim by enumeration.

## Next review point

If the external challenge judge publishes a new verdict, update the score and
live-contract readback separately from this clean-room evidence gate. Until
then, keep the `9/10` score unchanged and treat the repository as a public
reproduction handoff.
