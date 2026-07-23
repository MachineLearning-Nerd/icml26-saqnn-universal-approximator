# Source audit: arXiv 2602.09718

- Retrieval URL: `https://ar5iv.labs.arxiv.org/html/2602.09718`
- Retrieval time: 2026-07-23 08:30:52 UTC
- Request policy: HTTP GET with explicit
  `OpenResearch-Reproduction/1.0 (paper audit; contact via repository)`
  User-Agent.
- Retrieved HTML SHA-256:
  `4e6d9d8b67a7d4e41837177dec5b43349e17494360e39ef9ed1efe0cfd1bdefa`
- Result: ar5iv fatal-conversion page, so the pinned arXiv source archive and
  `docs/source/main.tex` are the auditable primary fallback.
- Pinned source archive SHA-256:
  `0909b548f500f6a09dbade8b9caba91ff5f8525d0e6f3bb7ebde866f74b1e3bd`
- Primary TeX SHA-256:
  `6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2`
- PDF SHA-256:
  `18d1d80ef4b984084f11904590e3b75b354cef898a3fd3eed0c0a651a9493a33`

## Claim anchors and quantifiers

- Theorem 1, Section 3.2, `docs/source/main.tex:368`: for every multivariate
  square-integrable `f : [-π,π]^d -> [0,1]` and every accuracy `epsilon`,
  there exist `theta`, `phi`, and a rescale coefficient `a` whose measured
  output has L2 error at most `epsilon`.
- Theorem 2, Section 3.3, `docs/source/main.tex:383`: for every
  `[0,1]`-valued Sobolev target and every positive `epsilon`, the construction
  has width `O(log n)`, depth `O(n log n)`, and `O(n)` parameters, with the
  displayed sufficient term count at `docs/source/main.tex:399`.
- Lemma 3, Section 2.3, `docs/source/main.tex:485-518`: multiplexor rotations
  admit the stated CNOT upper bound; Appendix D applies this to state
  preparation and controlled spectrum selection.
- High-dimensional comparison, `docs/source/main.tex:831`: accuracy is fixed
  and dimension is the demanding asymptotic variable.
- Chebyshev modification, Appendix C, `docs/source/main.tex:1084-1132`:
  the basis switch changes spectrum rotations/input encoding and restricts
  coefficient phases to signs.

## Assumptions that matter for Claim 1

The target range `[0,1]` is part of the quantified theorem. The measured
construction is nonnegative because it is a positive rescale times the
magnitude of a complex amplitude. Therefore a signed target is not an
in-scope counterexample. A faithful verifier must instead check the
construction and convergence for nonnegative targets, across genuinely
multivariate and non-polynomial cases, or find a counterexample satisfying
all of the theorem assumptions.
