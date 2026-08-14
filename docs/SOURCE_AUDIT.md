# Source audit

## Pinned paper

- Title: *SAQNN: Spectral Adaptive Quantum Neural Network as a Universal Approximator*
- Authors: Jialiang Tang, Jialin Zhang, and Xiaoming Sun
- arXiv: [2602.09718](https://arxiv.org/abs/2602.09718)
- OpenReview: `QaHFVheV8X`
- Source archive SHA-256: `0909b548f500f6a09dbade8b9caba91ff5f8525d0e6f3bb7ebde866f74b1e3bd`
- Primary PDF SHA-256: `18d1d80ef4b984084f11904590e3b75b354cef898a3fd3eed0c0a651a9493a33`
- Primary TeX SHA-256: `6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2`

The accepted source contains no executable author implementation. The audit
therefore uses clean-room Python/NumPy and standard-library code. No external
quantum SDK, GPU, hosted compute, or competitor result is required.

## Scope disclosures

1. Theorem 1's constructive reduction is tested for `[0,1]`-valued L2 targets.
   The finite evidence does not prove the universal quantifier by itself.
2. Dense circuit matrices are checked through six qubits; this is a deliberate
   finite substitution for the paper's general construction.
3. C3's circuit-size comparison is fixed-accuracy and sufficiently high
   dimensional. It is not uniform as `epsilon` tends to zero at fixed `d`.
4. C3's parameter-rate check uses the source Case-4 Fourier/n-width rate at
   fixed dimension and high accuracy, not the loose uniform sufficient-`n`
   display as a tight rate.
5. Monte Carlo L2 curves are empirical support with confidence intervals, not
   the logical basis of the theorem.
6. No training dynamics, optimizer behavior, noisy hardware, or hardware
   routing claim is tested.

## Live-contract distinction

The live challenge snapshot contains three claims and six possible points. Its
original universal-approximation wording is broader than the source theorem's
explicit range restriction. `outputs/full_audit.json` preserves that audit
finding, while the five repository claim contracts use the narrower source
scopes shown in `docs/EVIDENCE.md`.
