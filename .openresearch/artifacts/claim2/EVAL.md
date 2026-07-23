# Claim 2 evaluation

Verdict: **VERIFIED**

Every integer `n=2..8192` and 136 boundary-heavy values through `2^30+1`
satisfied width `O(log n)`, parameters `O(n)`, and depth `O(n log n)`.
An independent implementation checked 8,191 values. Three weakened
constructions were detected. The cumulative release-candidate run uses the
same fixed command recorded in `execution.json`.
