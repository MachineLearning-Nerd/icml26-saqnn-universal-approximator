# 2026-07-23 release candidate

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_release_20260723", "created_at": "2026-07-23T09:07:58+00:00", "title": "Cumulative gate", "pinned": true, "pinned_at": "2026-07-23T09:07:58+00:00"}
-->

All five judge claims are **VERIFIED** under their exact source scopes in the
local release-candidate run. This does not claim a score increase; the
published revision must still be evaluated by the live judge.

| Claim | Result | Decisive evidence |
| --- | --- | --- |
| 1 | VERIFIED | 131,072 exact multivariate cells, six convergence studies, independent 10,280-cell checker |
| 2 | VERIFIED | all integers `n=2..8192` plus 136 large boundaries |
| 3 | VERIFIED | 36 parameter-rate cells, 27 high-d size cells, opposite-regime control |
| 4 | VERIFIED | ten exact multiplexor unitaries and dropped-CNOT control |
| 5 | VERIFIED | exact Fourier/Chebyshev statevector identities and convergence |

The cumulative run used the frozen `uv.lock`, fixed command, and local CPU.
Every prior full-credit Claim 2–5 check passed. The protected judged revision
`57218a49b75b419e3947e836a449696177740498` remains in this Space's Git
history, and every judged path remains present in the candidate.

The illustrated report and tutorial notebook are prepared on the winning
GitHub branch:

- [illustrated report](https://github.com/MachineLearning-Nerd/icml26-saqnn-universal-approximator/blob/30ce1193b25e094a364cb5b2b8c676206290f86b/reports/saqnn-reproduction/report.md)
- [tutorial marimo notebook](https://github.com/MachineLearning-Nerd/icml26-saqnn-universal-approximator/blob/30ce1193b25e094a364cb5b2b8c676206290f86b/notebooks/saqnn_reproduction.py)

Publication was explicitly approved. This evidence update is awaiting
evaluation by the live judge; the official score remains 9/10 until that
evaluation produces a new verdict.
