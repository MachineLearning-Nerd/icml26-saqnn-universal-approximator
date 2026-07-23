# Claim 1 source audit

The audited source is `docs/source/main.tex`, SHA-256
`6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2`.
Theorem 1 is anchored at line 368 and its proof at Appendix A, line 924.

The quantifiers are: every positive integer dimension, every
`[0,1]`-valued square-integrable target on the torus, and every positive
accuracy. The conclusion is existential in the state-preparation angles,
phase-injection angles, and rescale coefficient.

The judge correctly rejected the earlier `sin(x)` counterexample: it violates
the theorem's target-range assumption. This audit does not use that argument.
It checks the actual in-scope reduction:

1. choose a finite Fourier polynomial close to the target in L2;
2. encode coefficient magnitudes as squared state amplitudes and coefficient
   arguments as phase-injection angles;
3. spectrum selection realizes each multivariate exponential;
4. the square-root measurement returns the polynomial magnitude;
5. nonnegativity of the target gives the pointwise modulus inequality that
   transfers the Fourier approximation error to the SAQNN output.

The source's displayed indexing alternates between `1..n` and `0..n-1`.
The verifier uses addresses `1..n`, reserves address zero for the padding
flip, and checks that the theorem's `n=(2k+1)^d` leaves enough capacity under
`m=ceil(log2 n)`.
