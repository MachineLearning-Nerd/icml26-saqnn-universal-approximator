# Branch audit

The final branch names describe the experiment lineage and remove the
automation-specific `orx/` prefix. All final branches are retained on GitHub;
the former names are documented for traceability.

| Final branch | Former branch | Purpose |
| --- | --- | --- |
| `main` | `main` | Canonical publication surface and release metadata |
| `baseline/judged-9-10` | `orx/judged-9-10-baseline` | Frozen environment and judged baseline |
| `audit/restored-five-claim-regression` | `orx/restore-judged-five-claim-regression` | Restored Claim 2–5 regression checks |
| `audit/claim-1-multivariate` | `orx/claim-1-multivariate-theorem-audit` | In-scope multivariate Claim 1 audit |
| `release/claim-1-evidence-package` | `orx/package-full-claim-evidence` | Deterministic Claim 1 package |
| `release/candidate-evidence-and-report` | `orx/release-candidate-evidence-and-report` | Release report and asset validation |

The default branch is `main`. The final remote namespace contains exactly
these six branches; the old `orx/*` refs are deleted after the renamed refs
are published. Reachable commits are normalized to:

```text
MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
```
