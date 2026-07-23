#!/usr/bin/env python3
"""Fail closed if regenerated Claim 1 evidence differs from the frozen evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".openresearch" / "artifacts" / "claim1"
EXPECTED_COMMAND = "uv sync --frozen && uv run --frozen python repro/run_all.py"


def load_json(name: str) -> dict[str, object]:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def main() -> int:
    actual = load_json("raw_results.json")
    independent = load_json("independent_checker.json")
    expected = load_json("expected_scientific_results.json")
    expected_independent = load_json("expected_independent_checker.json")

    actual_scientific = {
        key: value for key, value in actual.items() if key != "runtime"
    }
    convergence = (OUT / "convergence.csv").read_bytes()
    expected_convergence = (OUT / "expected_convergence.csv").read_bytes()
    negative = load_json("negative_controls.json")
    expected_negative = load_json("expected_negative_controls.json")

    checks = {
        "scientific_json_exact": actual_scientific == expected,
        "convergence_csv_exact": convergence == expected_convergence,
        "negative_control_json_exact": negative == expected_negative,
        "independent_checker_json_exact": independent == expected_independent,
        "source_hash_exact": actual["contract"]["source_sha256"]
        == "6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2",
        "uv_lock_hash_exact": hashlib.sha256(
            (ROOT / "uv.lock").read_bytes()
        ).hexdigest()
        == "ca90fb40e1c1b24c8b84e8dd3f6809d1c5e91ca6833e9d2e72e1dc1b12e85f32",
        "python_pin_exact": (ROOT / ".python-version").read_text(
            encoding="utf-8"
        ).strip()
        == "3.12",
    }
    result = {
        "verdict": "VERIFIED" if all(checks.values()) else "BLOCKED",
        "checks": checks,
        "exact_run_command": EXPECTED_COMMAND,
        "convergence_sha256": hashlib.sha256(convergence).hexdigest(),
        "expected_files": [
            "expected_scientific_results.json",
            "expected_convergence.csv",
            "expected_negative_controls.json",
            "expected_independent_checker.json",
        ],
    }
    print("=== CLAIM1_EVIDENCE_PACKAGE_JSON ===")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit("Claim 1 evidence package differs from regenerated outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
