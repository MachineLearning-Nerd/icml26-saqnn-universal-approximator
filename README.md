# ICML 2026 — SAQNN: Spectral Adaptive Quantum Neural Network as a Universal Approximator

This repository contains a clean-room, source-pinned reproduction audit of
[*SAQNN: Spectral Adaptive Quantum Neural Network as a Universal
Approximator*](https://arxiv.org/abs/2602.09718) by Jialiang Tang, Jialin
Zhang, and Xiaoming Sun.

The paper proposes a constructive quantum neural network that represents
Fourier or Chebyshev expansions, proves a universal-approximation result, and
derives circuit-resource and parameter-complexity claims. The audit tests the
five claim contracts retained in this repository with exact finite arithmetic,
independent checks, negative controls, and a reproducible CPU entrypoint.

## Release status

The evidence-release gate **PASSED**: all five repository claim contracts are
**VERIFIED_SCOPED**. The strict paper-level gate remains **NOT_READY** because
finite computation cannot enumerate every L2 target or establish every
universal asymptotic statement by itself. The official live challenge score
remains **9/10**; this repository does not claim that a judge score changed.

The official live contract contains three claims and six possible points. Its
fail-closed verifier passes all three for `6/6`, while Claims 4–5 below are
additional paper-level contracts retained by the release branch. Claim 1 is
verified for the paper theorem's explicit `[0,1]`-valued L2 scope; the broader
live wording omits that range restriction and must not be read as a claim about
all signed L2 functions.

No author executable was found in the accepted source. All checks are
independent, clean-room implementations against the pinned paper source.

| Claim | Paper statement | Status | Claim producer and evidence |
| --- | --- | --- | --- |
| C1 | The constructive SAQNN has universal approximation for `[0,1]`-valued L2 targets | **VERIFIED_SCOPED** | `repro/src/verify_claim1_full.py`, `check_claim1_independent.py`, and `verify_claim1_evidence_package.py`; 128 seeded Fourier polynomials in dimensions 1–4, 131,072 exact circuit cells, six in-range convergence targets, 118,784 held-out evaluations, and an independent 10,280-cell checker |
| C2 | Width `O(log n)`, depth `O(n log n)`, and parameter count `O(n)` | **VERIFIED_SCOPED** | `repro/src/verify_c2_resource_proof.py` and `audit_c2_resource_proof.py`; every integer `n=2..8192`, 136 large boundary values, exact resource identities, and negative controls |
| C3 | The claimed high-dimensional circuit-size comparison and Sobolev parameter rate hold in their stated asymptotic regimes | **VERIFIED_SCOPED** | `repro/src/verify_c2_complexity.py`, `full_audit.py`, and `repro/tests/test_audit.py`; 27 fixed-accuracy/high-dimensional comparison cells, 36 fixed-dimension rate cells, and an opposite-regime control |
| C4 | Multiplexor rotations meet the `2^(n-1)` CNOT bound and contribute the claimed depth term | **VERIFIED_SCOPED** | `repro/src/verify_c4_lemma3.py` and `verify_c0c4_saqnn_circuit.py`; exact dense-unitary checks for `Ry` and `Rz` at 2–6 qubits plus a dropped-CNOT control |
| C5 | The same architecture can switch between Fourier and Chebyshev bases | **VERIFIED_SCOPED** | `repro/src/verify_c5_basis.py` and `verify_c0c4_saqnn_circuit.py`; exact statevector identities, periodic Fourier convergence, non-periodic Chebyshev convergence, and wrong-basis controls |

## How each claim is produced

```text
Pinned arXiv source + live claim contract
  → source-anchor and scope audit
  → exact finite construction / resource / circuit check
  → independent checker and negative controls
  → reproducibility tests and release-asset validation
  → hash-addressed evidence bundle and fail-closed gate
```

### C1 — constructive universal approximation

`verify_claim1_full.py` constructs the paper's coefficient state, input
dependent frequency phases, inverse state preparation, and measured amplitude.
It checks the exact identity for 128 random positive trigonometric polynomials
across dimensions 1–4. The largest circuit-output error is `5.55e-16`.

Six smooth or discontinuous targets provide finite convergence support: every
target is in `[0,1]`, all curves improve, and the largest final Monte Carlo L2
estimate is below `0.18`. `check_claim1_independent.py` reimplements the
identity without importing the primary verifier and checks another 10,280
cells to `8.88e-16`. Three deliberately broken constructions must be detected.
The universal quantifier still rests on the paper's cited L2-density theorem;
finite tests do not replace that theorem.

### C2 — constructive resource bounds

`verify_c2_resource_proof.py` derives the address width, multiplexor count,
depth, and parameter count directly from the circuit construction. It checks
every integer `n` from 2 through 8,192 and 136 large boundary values through
`2^30+1`. `audit_c2_resource_proof.py` independently checks the same bounds
without importing the primary resource verifier. The accepted scope is the
paper's constructive gate model, not a claim about a particular hardware
layout.

### C3 — separated asymptotic regimes

`verify_c2_complexity.py` and `full_audit.py` keep two comparisons separate.
For the Sobolev parameter rate, 36 fixed-dimension/high-accuracy cells match
the source Case-4 Fourier exponent `d/s` to `2.22e-15`. For circuit size, 27
fixed-accuracy/high-dimensional cells favor the displayed SAQNN comparison;
the fixed-dimension high-accuracy control correctly rejects an unqualified
all-regime advantage. This separation is why the README does not overstate the
paper's asymptotics.

### C4 — multiplexor synthesis

`verify_c4_lemma3.py` independently assembles the target multiplexor unitary
and its Gray-code decomposition for both `Ry` and `Rz`. Ten cases at 2–6
qubits have zero dense-matrix error and exactly `2^(n-1)` CNOTs. Removing one
CNOT must be detected. The controlled-rotation cost is retained in the C2
depth accounting.

### C5 — basis switching

`verify_c5_basis.py` evaluates periodic Fourier and non-periodic Chebyshev
approximations, while `verify_c0c4_saqnn_circuit.py` checks the corresponding
statevector forward map. Fourier identities reach `2.48e-16` in one dimension
and `2.12e-16` in two; Chebyshev modes through `T_7` reach `4.44e-16`.
Convergence curves and a wrong-basis control document why the switch matters.

## Branch map

The final repository keeps the experiment lineage visible with descriptive
branch names. `main` is the canonical publication surface and was not itself
run as an experiment.

| Final branch | Former branch | Purpose |
| --- | --- | --- |
| `main` | `main` | README, report, notebook, source pins, and release metadata; Not run as an experiment (publication surface) |
| `baseline/judged-9-10` | `orx/judged-9-10-baseline` | Frozen environment and the original judged 9/10 cumulative baseline |
| `audit/restored-five-claim-regression` | `orx/restore-judged-five-claim-regression` | Restored Claim 2–5 regression suite and accepted checks |
| `audit/claim-1-multivariate` | `orx/claim-1-multivariate-theorem-audit` | In-scope multivariate Claim 1 audit replacing toy-only evidence |
| `release/claim-1-evidence-package` | `orx/package-full-claim-evidence` | Deterministic Claim 1 evidence package and frozen outputs |
| `release/candidate-evidence-and-report` | `orx/release-candidate-evidence-and-report` | Reader-facing report, figures, claim packages, and release-asset checks |

See [BRANCH_AUDIT.md](BRANCH_AUDIT.md) for final branch tips and the remote
ref audit.

## Pinned inputs and provenance

- Paper: [arXiv:2602.09718](https://arxiv.org/abs/2602.09718); OpenReview identifier `QaHFVheV8X`.
- Authors: Jialiang Tang, Jialin Zhang, and Xiaoming Sun.
- Source archive: `docs/arxiv_source.tar`, SHA-256 `0909b548f500f6a09dbade8b9caba91ff5f8525d0e6f3bb7ebde866f74b1e3bd`.
- Primary PDF: `docs/primary.pdf`, SHA-256 `18d1d80ef4b984084f11904590e3b75b354cef898a3fd3eed0c0a651a9493a33`.
- Primary TeX: `docs/source/main.tex`, SHA-256 `6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2`.
- Official author executable: none found in the accepted source; this is a clean-room audit.

## Reproduce the audit

```bash
git clone https://github.com/MachineLearning-Nerd/icml26-saqnn-universal-approximator.git
cd icml26-saqnn-universal-approximator
uv sync --frozen && uv run --frozen python repro/run_all.py
```

The command is fail-closed: it checks the source pins, all claim packages,
negative controls, report assets, notebook syntax, tests, and the evidence
bundle. To inspect the tutorial notebook locally:

```bash
uv run marimo edit notebooks/saqnn_reproduction.py
uv run marimo run notebooks/saqnn_reproduction.py
```

## Documentation

- [Evidence ledger](docs/EVIDENCE.md)
- [Source audit and scope limits](docs/SOURCE_AUDIT.md)
- [Source manifest and citation](SOURCE_MANIFEST.md)
- [Audit report](AUDIT_REPORT.md)
- [Branch audit](BRANCH_AUDIT.md)
- [Publication gate](docs/PUBLICATION_GATE.md)
- [Output guide](outputs/README.md)
- [Illustrated technical report](reports/saqnn-reproduction/report.md)
- [Tutorial notebook](notebooks/saqnn_reproduction.py)

## Citation

```bibtex
@article{tang2026saqnn,
  title={SAQNN: Spectral Adaptive Quantum Neural Network as a Universal Approximator},
  author={Tang, Jialiang and Zhang, Jialin and Sun, Xiaoming},
  journal={arXiv preprint arXiv:2602.09718},
  year={2026},
  note={ICML 2026}
}
```

Paper page: [arXiv:2602.09718](https://arxiv.org/abs/2602.09718).

## Thank you

Thank you to Jialiang Tang, Jialin Zhang, and Xiaoming Sun for presenting a
constructive route to quantum neural-network approximation and for making the
source available for careful, scope-aware reproduction. The paper's explicit
range, resource, and basis assumptions make it possible to test the mechanism
directly while preserving the distinction between finite evidence and a
universal theorem.

Maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
