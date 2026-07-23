# Claim 1 method

The primary verifier has three layers.

First, it checks the source hash and exact theorem/proof anchors. Second, it
constructs 128 seeded, real, strictly `[0,1]`-valued Fourier polynomials in
dimensions 1 through 4. It maps every complex coefficient into the paper's
state-preparation probability and phase, verifies a real Householder state
preparation, evaluates 131,072 points, and compares the measured SAQNN output
with the target. Third, it computes tensor Fejer approximants for six smooth
and discontinuous non-polynomial targets in dimensions 1 through 4. Each
curve is evaluated on 4,096 independently seeded holdout points with a 95%
standard-error interval.

Three negative controls deliberately drop coefficient phases, use amplitudes
instead of square-root probabilities, or delete a spectrum term. Each must
produce a measurable error. A separate checker imports none of the primary
verifier and independently tests 10,280 construction cells plus 100,000
instances of the key modulus inequality.

The fixed command is:

```text
uv sync --frozen && uv run --frozen python repro/run_all.py
```

The environment is Python 3.12 with `uv.lock` SHA-256
`ca90fb40e1c1b24c8b84e8dd3f6809d1c5e91ca6833e9d2e72e1dc1b12e85f32`.
Seeds are `260209718`, `260209719`, and `718092062`.
