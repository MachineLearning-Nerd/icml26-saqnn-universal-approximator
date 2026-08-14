# Audit report

## Decision

The evidence-release gate **PASSED**. Five repository claim contracts are
**VERIFIED_SCOPED**. The strict paper-level gate is **NOT_READY** because the
finite checks cannot establish every universal target or asymptotic conclusion
by enumeration. The official live score remains `9/10`; no score change is
claimed.

## What the audit establishes

- C1: the source's positive-rescaling and measured-amplitude construction is
  reproduced for in-range multivariate finite Fourier targets, with independent
  checks and negative controls.
- C2: the constructive resource identities hold across the exhaustive and
  boundary ranges declared by the claim contract.
- C3: the source's two asymptotic regimes are reproduced separately, including
  the fixed-dimension parameter rate and fixed-accuracy/high-dimensional
  circuit comparison.
- C4: both multiplexor rotation families decompose exactly at the claimed
  CNOT count in the tested finite range.
- C5: the circuit forward map supports both Fourier and Chebyshev basis
  constructions in the tested finite range.

## What it does not establish

Finite cells do not enumerate all L2 functions, do not replace the paper's
density argument, and do not constitute a hardware or training benchmark. The
source-scope conditions and the live-contract mismatch are retained in the
README, `docs/SOURCE_AUDIT.md`, and the machine-readable gate files.

## Reproduction command

```bash
uv sync --frozen && uv run --frozen python repro/run_all.py
```

The runner performs the source audit, tests, claim producers, independent
checkers, release-asset validation, and final evidence bundle creation.
