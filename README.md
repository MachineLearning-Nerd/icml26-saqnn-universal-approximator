# SAQNN universal-approximation reproduction

Clean-room, source-pinned reproduction of *SAQNN: Spectral Adaptive Quantum
Neural Network as a Universal Approximator* (ICML 2026; OpenReview
`QaHFVheV8X`; arXiv `2602.09718`).

The current challenge contract has three claims (six possible points):

1. Constructive universal approximation for square-integrable functions.
2. An asymptotic circuit-size advantage over classical feed-forward networks.
3. Optimal parameter complexity for Sobolev approximation under L2.

The accepted source contains no author executable. This reproduction will use
independent finite Fourier/circuit calculations and will distinguish the live
claim wording from the source theorem's explicit `[0,1]`, fixed-accuracy, and
Sobolev-domain conditions.
