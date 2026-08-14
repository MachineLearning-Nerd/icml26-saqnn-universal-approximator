# Evidence ledger

This ledger records how each paper claim is produced. `VERIFIED_SCOPED` means
the declared finite contract, source anchors, controls, and reproducibility
checks pass; it does not turn finite computation into a proof of every
universal statement.

## C1 — universal approximation

Producers: `repro/src/verify_claim1_full.py`,
`repro/src/check_claim1_independent.py`, and
`repro/src/verify_claim1_evidence_package.py`.

The primary verifier checks the coefficient-amplitude encoding, phase
injection, frequency selection, inverse state preparation, measured output,
and the modulus inequality for `[0,1]`-valued targets. It evaluates 128 seeded
random Fourier polynomials in dimensions 1–4 across 131,072 exact cells, then
checks six in-range targets with 118,784 held-out evaluations. The independent
checker covers 10,280 additional cells without importing the primary verifier.
Three broken constructions are required to fail. The result is
**VERIFIED_SCOPED**; the source-cited L2-density theorem remains the logical
universal step.

Artifacts: `.openresearch/artifacts/claim1/` and
`evidence/claim-1-full-scale/`.

## C2 — circuit resource bounds

Producers: `repro/src/verify_c2_resource_proof.py` and
`repro/src/audit_c2_resource_proof.py`.

The primary proof derives width, depth, parameter count, address width, and
multiplexor sums from the paper's constructive circuit. It checks every
integer `n=2..8192` and 136 boundary values through `2^30+1`. The independent
checker confirms the same `O(log n)`, `O(n log n)`, and `O(n)` bounds. This is a
gate-model audit, not a hardware-routing benchmark.

Artifact: `.openresearch/artifacts/claim2/`.

## C3 — asymptotic comparison and parameter rate

Producers: `repro/src/verify_c2_complexity.py`,
`repro/src/full_audit.py`, and `repro/tests/test_audit.py`.

The audit checks 36 fixed-dimension/high-accuracy parameter-rate cells against
the source Case-4 exponent `d/s`. It separately checks 27 fixed-accuracy,
sufficiently high-dimensional circuit-size cells. A fixed-dimension,
high-accuracy control rejects the unqualified all-regime circuit-advantage
interpretation. The maximum slope error is `2.22e-15`.

Artifacts: `.openresearch/artifacts/claim3/`, `outputs/full_audit.json`, and
`outputs/claim_verification.json`.

## C4 — multiplexor decomposition

Producers: `repro/src/verify_c4_lemma3.py` and
`repro/src/verify_c0c4_saqnn_circuit.py`.

The verifier independently builds the target `Ry`/`Rz` multiplexor and its
Gray-code decomposition. Ten cases at 2–6 qubits have exact dense-unitary
agreement and exactly `2^(n-1)` CNOTs. A dropped-CNOT control must be rejected.

Artifact: `.openresearch/artifacts/claim4/`.

## C5 — Fourier/Chebyshev basis switching

Producers: `repro/src/verify_c5_basis.py` and
`repro/src/verify_c0c4_saqnn_circuit.py`.

The checks combine exact statevector identities with periodic Fourier and
non-periodic Chebyshev convergence curves. Fourier identities reach
`2.48e-16` in one dimension and `2.12e-16` in two; Chebyshev modes through
`T_7` reach `4.44e-16`. Wrong-basis and distinct-basis controls remain in the
artifact package.

Artifact: `.openresearch/artifacts/claim5/`.

## Evidence path

```text
source archive + live contract
  → source/scope audit
  → exact claim producers
  → independent checks and negative controls
  → reproducibility and release-asset checks
  → SHA-256 evidence bundle
  → fail-closed publication gate
```
