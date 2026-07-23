# Claim 3 source audit

The accepted `docs/source/main.tex` has SHA-256
`6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2`.
Section 3.3 explicitly fixes non-tiny accuracy before taking dimension large
for the circuit-size comparison (lines 831–833). Appendix E gives
Kolmogorov/manifold width scaling `n^(-s/d)`, hence parameter exponent `d/s`,
for fixed dimension and increasing accuracy (lines 1342–1378). Those are two
different asymptotic regimes and are audited separately.
