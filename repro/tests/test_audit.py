"""Independent regression tests for the source-bound QaHFVheV8X audit."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "repro" / "src" / "full_audit.py"
SPEC = importlib.util.spec_from_file_location("full_audit", MODULE_PATH)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class AuditTests(unittest.TestCase):
    def test_source_and_claim_1_range_counterexample(self) -> None:
        source = AUDIT.source_audit(ROOT / "docs" / "source")
        claim = AUDIT.audit_universal_approximation()
        self.assertTrue(source["pass"])
        self.assertTrue(claim["pass"])
        self.assertEqual(claim["restricted_nonnegative_finite_fourier_cells"], 6144)
        self.assertLessEqual(claim["maximum_source_amplitude_construction_error"], AUDIT.TOL)
        self.assertEqual(claim["live_claim_outcome"], "falsified_as_written_range_omitted")
        self.assertAlmostEqual(claim["signed_l2_counterexample_nonnegative_output_lower_bound"], 0.5)

    def test_claim_2_conditional_circuit_advantage(self) -> None:
        claim = AUDIT.audit_circuit_size_comparison()
        self.assertTrue(claim["pass"])
        self.assertEqual(claim["fixed_accuracy_high_dimension_cells"], 27)
        self.assertGreater(claim["minimum_log_classical_size_minus_log_saqnn_size"], 0.0)
        self.assertTrue(
            claim["high_accuracy_fixed_dimension_control"]["rejected_unqualified_all_regime_advantage"]
        )

    def test_claim_3_fixed_dimension_parameter_rate(self) -> None:
        claim = AUDIT.audit_parameter_optimality()
        self.assertTrue(claim["pass"])
        self.assertEqual(claim["fixed_dimension_high_accuracy_rate_cells"], 36)
        self.assertLessEqual(claim["maximum_case_four_log_parameter_slope_error"], AUDIT.TOL)
        self.assertTrue(claim["uniform_display_control_rejected_as_optimal_fixed_d_rate"])


if __name__ == "__main__":
    unittest.main()
