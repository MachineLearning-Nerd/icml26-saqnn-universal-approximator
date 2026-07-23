# SAQNN claim-by-claim reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-QaHFVheV8X-saqnn-universal-approximator/blob/main/notebooks/saqnn_reproduction.py)

This clean-room campaign tests all five judged claims from
[*SAQNN: Spectral Adaptive Quantum Neural Network as a Universal
Approximator*](https://arxiv.org/abs/2602.09718), with special attention to
Theorem 1. The existing judge gave Claim 1 only toy credit because it covered
three one-dimensional functions and used an out-of-scope signed
counterexample.

The upgraded evidence is **VERIFIED for the theorem's exact `[0,1]`-valued L2
scope**: 128 seeded random Fourier polynomials across dimensions 1–4 produced
131,072 exact circuit-evaluation cells with maximum error `5.55e-16`; six
in-range targets added 118,784 held-out convergence evaluations; and an
independent implementation checked another 10,280 cells to `8.88e-16`.
Claims 2–5 also pass their cumulative regressions. This is a reproduction
assessment, not a promise of a perfect score or a claim that the live judge
has increased it. The additive logbook evidence is published at Hugging Face
revision
[`11a72785b6e8bea73457081a7ddb9d13f6913d8e`](https://huggingface.co/spaces/DineshAI/QaHFVheV8X/commit/11a72785b6e8bea73457081a7ddb9d13f6913d8e);
the official score remains **9/10** while that revision awaits live judging.

- [Illustrated technical report](reports/saqnn-reproduction/report.md) —
  implementation, five evidence figures, limitations, and claim-level results.
- [Tutorial marimo notebook](notebooks/saqnn_reproduction.py) — opens with
  embedded completed-run evidence and includes only a bounded explanatory
  slider.
- [Claim contracts and raw evidence](.openresearch/artifacts/) — source audits,
  machine-readable outputs, controls, environments, and evaluations.

The paper's analytical construction is tested directly rather than trained.
The only scale substitutions are finite dimensions `d=1..4`, dense unitaries
through six qubits, and Monte Carlo L2 estimates for supporting convergence
curves. The universal quantifier still relies on the paper's cited L2-density
theorem; finite sweeps do not replace it. All formal runs used local Apple
arm64 CPU with Python 3.12 and a frozen `uv.lock`. No GPU or Hugging Face
upgrade was needed; hosted-compute cost was `$0`.

## Claim results

| Claim | Paper result | Observed result | Assessment |
|---|---|---|---|
| 1 | Universal approximation of `[0,1]`-valued L2 targets | `5.55e-16` maximum circuit identity error; six multivariate/smooth/discontinuous convergence studies | **VERIFIED** |
| 2 | Width `O(log n)`, depth `O(n log n)`, parameters `O(n)` | Every integer `n=2..8192` plus 136 large boundary cases | **VERIFIED** |
| 3 | Optimal parameter order and fixed-accuracy/high-d circuit-size advantage | 36 slope cells and 27 high-d cells, with opposite-regime controls | **VERIFIED** |
| 4 | Multiplexor CNOT bound and controlled-rotation depth contribution | Ten exact `Ry`/`Rz` unitaries; dropped-CNOT control | **VERIFIED** |
| 5 | Fourier/Chebyshev basis switching | Exact statevector identities and convergence in both modes | **VERIFIED** |

## Experiment log

The table includes only lineage needed to understand the result. Every formal
node inherited the command verbatim. `main` is presentation-only.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | README, report, and notebook | Not run as an experiment (publication surface) | Presentation only | — |
| [Judged 9/10 baseline](https://github.com/MachineLearning-Nerd/icml26-repro-QaHFVheV8X-saqnn-universal-approximator/tree/orx/judged-9-10-baseline) | Pin the environment and freeze the control | `uv sync --frozen && uv run --frozen python repro/run_all.py` | PASS | Local Apple arm64 CPU, 10 s, `$0` |
| [Restore judged five-claim regression](https://github.com/MachineLearning-Nerd/icml26-repro-QaHFVheV8X-saqnn-universal-approximator/tree/orx/restore-judged-five-claim-regression) | Restore the exact full-credit Claim 2–5 scripts | `uv sync --frozen && uv run --frozen python repro/run_all.py` | PASS | Local Apple arm64 CPU, 10 s, `$0` |
| [Claim 1 multivariate theorem audit](https://github.com/MachineLearning-Nerd/icml26-repro-QaHFVheV8X-saqnn-universal-approximator/tree/orx/claim-1-multivariate-theorem-audit) | Replace toy evidence with in-scope multivariate verification | `uv sync --frozen && uv run --frozen python repro/run_all.py` | VERIFIED; cumulative PASS | Local Apple arm64 CPU, 15 s, `$0` |
| [Package full claim evidence](https://github.com/MachineLearning-Nerd/icml26-repro-QaHFVheV8X-saqnn-universal-approximator/tree/orx/package-full-claim-evidence) | Freeze and regenerate deterministic Claim 1 evidence | `uv sync --frozen && uv run --frozen python repro/run_all.py` | VERIFIED; package exact | Local Apple arm64 CPU, 15 s, `$0` |
| [Release candidate evidence and report](https://github.com/MachineLearning-Nerd/icml26-repro-QaHFVheV8X-saqnn-universal-approximator/tree/orx/release-candidate-evidence-and-report) | Validate all claim packages and publication assets | `uv sync --frozen && uv run --frozen python repro/run_all.py` | PASS; all five claims and release assets verified | Local Apple arm64 CPU, 20 s, `$0` |

## Reproduce

```bash
uv sync --frozen
uv run --frozen python repro/run_all.py
```

The two commands above are the fixed formal run command when joined with
`&&`. To explore the evidence locally:

```bash
uv run marimo edit notebooks/saqnn_reproduction.py
uv run marimo run notebooks/saqnn_reproduction.py
```

The accepted source contains no author executable. All checks here are
clean-room implementations, pinned to arXiv `2602.09718` and OpenReview
`QaHFVheV8X`.
