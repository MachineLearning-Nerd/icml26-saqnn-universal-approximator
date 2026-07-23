#!/usr/bin/env python3
"""Independent Claim 1 checker; intentionally imports no primary verifier code."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".openresearch" / "artifacts" / "claim1"
SEED = 718092062
SOURCE_SHA256 = "6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2"


def main() -> int:
    source_hash = hashlib.sha256(
        (ROOT / "docs" / "source" / "main.tex").read_bytes()
    ).hexdigest()
    primary = json.loads((OUT / "raw_results.json").read_text(encoding="utf-8"))
    rng = np.random.default_rng(SEED)

    # Independent pointwise proof obligation:
    # for real f>=0 and complex z, ||z|-f| <= |z-f|.
    values = rng.uniform(0.0, 1.0, size=100_000)
    complex_values = rng.normal(size=100_000) + 1j * rng.normal(size=100_000)
    inequality_violation = float(
        np.max(
            np.abs(np.abs(complex_values) - values)
            - np.abs(complex_values - values)
        )
    )

    maximum_identity_error = 0.0
    minimum_target = math.inf
    maximum_target = -math.inf
    cells = 0
    for dimension in (1, 2, 3, 4):
        all_frequencies = list(itertools.product((-1, 0, 1), repeat=dimension))
        frequency_array = np.array(all_frequencies, dtype=int)
        for _ in range(10):
            coefficients = np.zeros(len(all_frequencies), dtype=complex)
            zero_index = all_frequencies.index((0,) * dimension)
            coefficients[zero_index] = 0.5
            representatives = [
                frequency
                for frequency in all_frequencies
                if any(frequency)
                and frequency > tuple(-entry for entry in frequency)
            ]
            raw = rng.normal(size=(len(representatives), 2))
            raw *= 0.35 / np.sum(np.linalg.norm(raw, axis=1))
            for frequency, (cosine, sine) in zip(representatives, raw, strict=True):
                positive_index = all_frequencies.index(frequency)
                negative = tuple(-entry for entry in frequency)
                negative_index = all_frequencies.index(negative)
                value = (cosine - 1j * sine) / 2.0
                coefficients[positive_index] = value
                coefficients[negative_index] = value.conjugate()
            scale = float(sum(abs(value) for value in coefficients))
            points = rng.uniform(-math.pi, math.pi, size=(257, dimension))
            for point in points:
                polynomial = sum(
                    coefficient
                    * np.exp(1j * float(np.dot(frequency, point)))
                    for frequency, coefficient in zip(
                        frequency_array, coefficients, strict=True
                    )
                )
                amplitude = sum(
                    (abs(coefficient) / scale)
                    * np.exp(1j * np.angle(coefficient))
                    * np.exp(1j * float(np.dot(frequency, point)))
                    for frequency, coefficient in zip(
                        frequency_array, coefficients, strict=True
                    )
                    if coefficient != 0.0
                )
                target = float(polynomial.real)
                output = scale * abs(amplitude)
                maximum_identity_error = max(
                    maximum_identity_error, abs(output - target)
                )
                minimum_target = min(minimum_target, target)
                maximum_target = max(maximum_target, target)
                cells += 1

    obligations = {
        "source_hash_matches": source_hash == SOURCE_SHA256,
        "primary_verdict_verified": primary["verdict"] == "VERIFIED",
        "modulus_inequality_holds": inequality_violation <= 2e-15,
        "independent_identity_exact": maximum_identity_error <= 2e-12,
        "independent_targets_in_scope": minimum_target >= 0.0 and maximum_target <= 1.0,
        "primary_negative_controls_detected": all(
            primary["negative_controls"]["all_detected"].values()
        ),
        "primary_multivariate_coverage": (
            primary["finite_construction"]["dimensions"] == [1, 2, 3, 4]
        ),
    }
    passed = all(obligations.values())
    result = {
        "checker": "independent direct-sum Claim 1 audit",
        "implementation_independence": "does not import verify_claim1_full",
        "seed": SEED,
        "cells": cells,
        "maximum_modulus_inequality_violation": inequality_violation,
        "maximum_circuit_identity_error": maximum_identity_error,
        "target_minimum": minimum_target,
        "target_maximum": maximum_target,
        "obligations": obligations,
        "verdict": "VERIFIED" if passed else "BLOCKED",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "independent_checker.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("=== CLAIM1_INDEPENDENT_CHECKER_JSON ===")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit("independent Claim 1 checker failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
