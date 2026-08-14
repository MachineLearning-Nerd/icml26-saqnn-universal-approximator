# Claim 1 full-scale update

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_claim1_full_20260723", "created_at": "2026-07-23T09:07:58+00:00", "title": "Verified in the exact theorem scope", "pinned": true, "pinned_at": "2026-07-23T09:07:58+00:00"}
-->

## Verdict: VERIFIED

This additive page supersedes the interpretation on the preserved historical
Claim 1 page. The live judge's claim includes the source theorem's explicit
range `f: [-π,π]^d → [0,1]`; therefore the old signed `sin(x)` example is
outside the assumptions and is **not** a falsification of Claim 1.

The upgraded clean-room evidence tests the actual contract:

- 128 fixed-seed, `[0,1]`-valued random Fourier polynomials across
  `d = 1, 2, 3, 4`;
- 131,072 exact circuit-evaluation cells;
- maximum circuit-output error `5.551115123125783e-16`;
- six smooth or discontinuous in-range Fejer convergence studies with 118,784
  held-out evaluations and 95% Monte Carlo intervals;
- an independent implementation covering another 10,280 direct-sum cells,
  with maximum error `8.881784197001252e-16`;
- 100,000 independent checks of the key nonnegative-target modulus inequality;
- three detected negative controls: dropped phases (`0.539877` L2), one
  dropped spectral term (`0.469938`), and wrong state amplitudes (`0.377648`).

The universal quantifier is not inferred from a finite sweep. It combines the
paper's cited L2 density of trigonometric polynomials with a source-audited,
machine-checked SAQNN reduction: coefficient magnitudes are squared state
amplitudes, phases are injected explicitly, spectrum selection realizes each
multivariate exponential, and nonnegativity gives
`|| |g| - f ||₂ ≤ ||g - f||₂`.

The fixed formal command was:

```text
uv sync --frozen && uv run --frozen python repro/run_all.py
```

The release-candidate run passed on local Apple arm64 CPU at Git SHA
`30ce1193b25e094a364cb5b2b8c676206290f86b` in 14.126704 seconds. Hosted
compute cost was `$0`; no GPU or Hugging Face CPU upgrade was used.

Evidence:

- `evidence/claim-1-full-scale/claim_contract.json`
- `evidence/claim-1-full-scale/raw_results.json`
- `evidence/claim-1-full-scale/convergence.csv`
- `evidence/claim-1-full-scale/independent_checker.json`
- `evidence/claim-1-full-scale/negative_controls.json`
- `evidence/claim-1-full-scale/EVAL.md`
- [exact verifier source at the winning Git SHA](https://github.com/MachineLearning-Nerd/icml26-saqnn-universal-approximator/blob/30ce1193b25e094a364cb5b2b8c676206290f86b/repro/src/verify_claim1_full.py)
- [independent checker at the winning Git SHA](https://github.com/MachineLearning-Nerd/icml26-saqnn-universal-approximator/blob/30ce1193b25e094a364cb5b2b8c676206290f86b/repro/src/check_claim1_independent.py)

Limitations: finite computation cannot enumerate an uncountable L2 class.
Monte Carlo curves support the construction but do not replace the cited
density theorem. No noisy hardware or optimizer claim is made.
