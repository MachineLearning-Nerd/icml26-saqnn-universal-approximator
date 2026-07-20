# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_046adb77089a", "created_at": "2026-07-20T10:12:31+00:00", "title": "Executive summary", "pinned": true, "pinned_at": "2026-07-20T10:12:31+00:00"}
-->
All three current live claims are complete locally: 6/6 points, source pins verified, and three regression tests pass. C1 is decisively falsified as written because the live wording omits the source theorem range condition; C2 is verified for fixed accuracy and high dimension; C3 is verified for fixed dimension and high accuracy.

## Scope & cost

| | This reproduction | Full replication |
| --- | --- | --- |
| Scope | All current website claims with exact source conditions | Qiskit training demonstrations are supplementary, not required by the live claims |
| Hardware | Local CPU only | Source used a Xeon CPU for its small d=2 demonstrations |
| Time | Under one second per full audit | Not needed for theorem claims |
| Cost | $0 local compute | Not incurred |
| Outcome | Full local publication gate passed: 6/6 | Not represented as completed |


---
<!-- trackio-cell
{"type": "code", "id": "cell_b81549928acd", "created_at": "2026-07-20T10:12:40+00:00", "title": "Fail-closed claim verification", "command": ["python", "repro/src/verify_claims.py"], "exit_code": 0, "duration_s": 0.048}
-->
````bash
$ python repro/src/verify_claims.py
````

exit 0 · 0.0s


````python title=verify_claims.py
"""Fail-closed verifier for the current QaHFVheV8X three-claim contract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pins = load(ROOT / "docs" / "source_pins.json")
    live = load(ROOT / "docs" / "live_claims_2026-07-20.json")
    audit = load(OUT / "full_audit.json")
    source_pinned = (
        sha256(ROOT / "docs" / "arxiv_source.tar") == pins["arxiv_source_sha256"]
        and sha256(ROOT / "docs" / "primary.pdf") == pins["primary_pdf_sha256"]
        and sha256(ROOT / "docs" / "source" / "main.tex") == pins["primary_tex_sha256"]
    )
    live_contract_pinned = (
        live["openreview_id"] == "QaHFVheV8X"
        and live["claim_count"] == 3
        and live["points_possible"] == 6
        and len(live["claims"]) == 3
    )
    c1 = audit["claims"]["claim_1_universal_approximation"]
    c2 = audit["claims"]["claim_2_circuit_size_advantage"]
    c3 = audit["claims"]["claim_3_parameter_optimality"]
    test_path = OUT / "test_results.json"
    tests_passed = test_path.is_file() and load(test_path).get("tests_passed") is True

    claim_1 = bool(
        source_pinned
        and live_contract_pinned
        and c1["pass"]
        and c1["restricted_nonnegative_finite_fourier_cells"] == 6144
        and c1["maximum_source_amplitude_construction_error"] <= 2e-12
        and c1["signed_l2_counterexample_nonnegative_output_lower_bound"] >= 0.5 - 1e-10
        and c1["live_claim_outcome"] == "falsified_as_written_range_omitted"
    )
    claim_2 = bool(
        source_pinned
        and live_contract_pinned
        and c2["pass"]
        and c2["fixed_accuracy_high_dimension_cells"] == 27
        and c2["minimum_log_classical_size_minus_log_saqnn_size"] > 0.0
        and c2["high_accuracy_fixed_dimension_control"]["rejected_unqualified_all_regime_advantage"]
    )
    claim_3 = bool(
        source_pinned
        and live_contract_pinned
        and c3["pass"]
        and c3["fixed_dimension_high_accuracy_rate_cells"] == 36
        and c3["maximum_case_four_log_parameter_slope_error"] <= 2e-12
        and c3["uniform_display_control_rejected_as_optimal_fixed_d_rate"]
    )
    claims = (claim_1, claim_2, claim_3)
    payload = {
        "paper": "QaHFVheV8X",
        "source_pinned": source_pinned,
        "live_contract_pinned": live_contract_pinned,
        "live_claim_count": live["claim_count"],
        "claim_1_universal_approximation": claim_1,
        "claim_1_outcome": "falsified_as_written_range_omitted" if claim_1 else "incomplete",
        "claim_2_circuit_size_advantage": claim_2,
        "claim_3_parameter_optimality": claim_3,
        "decisive_claims": sum(claims),
        "earned_points": 2 * sum(claims),
        "all_claims_complete": all(claims),
        "tests_passed": tests_passed,
        "publication_gate_passed": all(claims) and tests_passed,
        "scope": (
            "C1 falsifies the broader live wording while reproducing the source [0,1] "
            "construction. C2 uses fixed accuracy and sufficiently high dimension. C3 "
            "uses fixed dimension and high accuracy, where the Case-4 Fourier rate matches n-width exponent d/s."
        ),
    }
    (OUT / "claim_verification.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))
    if not payload["all_claims_complete"]:
        raise SystemExit("incomplete QaHFVheV8X claim verification")


if __name__ == "__main__":
    main()

````


````output
{
  "paper": "QaHFVheV8X",
  "source_pinned": true,
  "live_contract_pinned": true,
  "live_claim_count": 3,
  "claim_1_universal_approximation": true,
  "claim_1_outcome": "falsified_as_written_range_omitted",
  "claim_2_circuit_size_advantage": true,
  "claim_3_parameter_optimality": true,
  "decisive_claims": 3,
  "earned_points": 6,
  "all_claims_complete": true,
  "tests_passed": true,
  "publication_gate_passed": true,
  "scope": "C1 falsifies the broader live wording while reproducing the source [0,1] construction. C2 uses fixed accuracy and sufficiently high dimension. C3 uses fixed dimension and high accuracy, where the Case-4 Fourier rate matches n-width exponent d/s."
}

````


---
<!-- trackio-cell
{"type": "dashboard", "id": "cell_e9fe96dc70f9", "created_at": "2026-07-20T10:12:43+00:00", "title": "Dashboard: repro-saqnn-universal-approximator", "dashboard_project": "repro-saqnn-universal-approximator"}
-->
**🎯 Trackio dashboard** `repro-saqnn-universal-approximator`

trackio-local-dashboard://repro-saqnn-universal-approximator
