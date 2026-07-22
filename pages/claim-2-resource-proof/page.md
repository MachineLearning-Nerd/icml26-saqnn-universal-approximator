# Claim 2: exact Theorem 2 resource-bound certificate

## Outcome

The source-derived counting proof independently certifies each resource bound
that the last judge found missing:

- width: `m + 1`, where `m = ceil(log2(n))`, hence `O(log n)`;
- parameters: `(2^m - 1) + n <= 3n - 2`, hence `O(n)`;
- depth: two multiplexor ladders, the padding Toffoli, and `n`
  controlled-`Rz` layers, bounded by `C n m` for a constant `C`, hence
  `O(n log n)`.

This is an exact integer/symbolic certificate, not a regression over a few
resource points. The primary verifier checks 136 boundary-heavy values through
`n = 2^30 + 1`; the independent implementation exhaustively checks every
integer `n` from 2 through 8192 without importing the primary verifier.

## Exact source scope

The HTML-first retrieval policy was followed:

1. `https://ar5iv.labs.arxiv.org/html/2602.09718` returned ar5iv's fatal
   conversion page (SHA-256
   `4e6d9d8b67a7d4e41837177dec5b43349e17494360e39ef9ed1efe0cfd1bdefa`).
2. `https://arxiv.org/html/2602.09718` reported that native HTML is unavailable
   (SHA-256
   `0bd83e272aaa15ff02a1aa04eb11a8c26b43d3551c44f3526d75240e5683bcc1`).
3. The required fallback was `https://arxiv.org/pdf/2602.09718` (PDF SHA-256
   `18d1d80ef4b984084f11904590e3b75b354cef898a3fd3eed0c0a651a9493a33`;
   layout-preserving `pdftotext` SHA-256
   `880b04ff673076776df8b7515e1c20c8d2cebd0a2b1198e6c0532a0f1957d4f5`).

Audited scope: Lemma 3, Theorem 2, and Appendix D's resource-count argument.
Appendix D uses `m = ceil(log n)`, sums the multiplexor depths as a geometric
series, counts `O(n)` phase/amplitude parameters, compresses the input to one
additional `Rz` qubit, and uses the cited `O(m)` synthesis of each multi-qubit
Toffoli in each of the `n` spectrum-selection layers.

## Reproduction

From the Space root:

```bash
python repro/src/verify_c2_resource_proof.py
python repro/src/audit_c2_resource_proof.py
```

The primary result ends with `"all_checks_passed": true`; the independent
result ends with `"audit_passed": true`.

## Negative controls

The checks deliberately reject three weakened constructions:

- using `floor(log2(n))` cannot address non-power-of-two term counts;
- deleting a spectrum-selection layer leaves only `n - 1` selected terms;
- dropping the mandatory `m` factor from multi-controlled-Toffoli synthesis
  falsely changes the depth from `O(n log n)` to `O(n)`.

## Scope boundary

This evidence certifies only Claim 2's three individual circuit-resource
bounds. It does not alter Claims 1, 3, 4, or 5, and it does not treat a finite
numerical fit as a proof of asymptotic behavior.
