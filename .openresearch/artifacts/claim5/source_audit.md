# Claim 5 source audit

The accepted `docs/source/main.tex` has SHA-256
`6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2`.
Section 3.2 states that the implemented basis can shift from Fourier to
Chebyshev (lines 801–807). Appendix C, lines 1084–1134, defines the
multivariate Chebyshev construction, replaces spectral `Rz` rotations with
`Ry`, and restricts coefficient phases to signs.
