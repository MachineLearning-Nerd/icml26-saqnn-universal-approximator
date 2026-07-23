#!/usr/bin/env python3
"""Fail-closed, in-scope verification of SAQNN Theorem 1.

This verifier checks the theorem's constructive reduction, not a learned proxy:
the target is always [0,1]-valued; complex Fourier coefficients are encoded as
state-preparation probabilities and phase-injection angles; the reported model
output is the paper's positive rescale times the measured amplitude magnitude.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import platform
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".openresearch" / "artifacts" / "claim1"
SEED = 260209718
TOL = 2e-12
SOURCE_SHA256 = "6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_contract() -> dict[str, object]:
    source = ROOT / "docs" / "source" / "main.tex"
    text = source.read_text(encoding="utf-8")
    anchors = {
        "target_domain_and_range": r"f: [-\pi,\pi]^d\rightarrow [0,1]",
        "quantifier": "For any multivariate square-integrable function",
        "observable": r"global observable $O=\ket{0}\bra{0}$",
        "fourier_density": r"For any $f\in L_2([-\pi,\pi]^d)$ and $\epsilon>0$",
        "coefficient_encoding": r"$|a_r|^2=|c_r|/a$",
        "modulus_reduction": r"|f_k| - f",
    }
    missing = [name for name, anchor in anchors.items() if anchor not in text]
    if sha256(source) != SOURCE_SHA256 or missing:
        raise AssertionError({"source_hash": sha256(source), "missing": missing})
    return {
        "source_sha256": SOURCE_SHA256,
        "anchors": anchors,
        "target_range": "[0,1]",
        "accuracy_quantifier": "every epsilon > 0",
        "parameter_quantifier": "there exist theta, phi, and positive rescale a",
        "norm": "normalized grid/Monte-Carlo L2; analytic proof uses source L2",
    }


def canonical_frequencies(dimension: int) -> list[tuple[int, ...]]:
    result = []
    for frequency in itertools.product((-1, 0, 1), repeat=dimension):
        if not any(frequency):
            continue
        opposite = tuple(-value for value in frequency)
        if frequency > opposite:
            result.append(frequency)
    return result


def random_positive_polynomial(
    rng: np.random.Generator, dimension: int
) -> tuple[np.ndarray, np.ndarray]:
    positive = canonical_frequencies(dimension)
    raw = rng.normal(size=(len(positive), 2))
    raw *= 0.38 / np.sum(np.linalg.norm(raw, axis=1))
    coefficients: dict[tuple[int, ...], complex] = {
        (0,) * dimension: 0.5 + 0.0j
    }
    for frequency, (cosine, sine) in zip(positive, raw, strict=True):
        value = (cosine - 1j * sine) / 2.0
        coefficients[frequency] = value
        coefficients[tuple(-entry for entry in frequency)] = value.conjugate()
    frequencies = np.array(sorted(coefficients), dtype=int)
    values = np.array([coefficients[tuple(row)] for row in frequencies], dtype=complex)
    return frequencies, values


def householder_state(prepared: np.ndarray) -> tuple[np.ndarray, float, float]:
    prepared = np.asarray(prepared, dtype=float)
    prepared /= np.linalg.norm(prepared)
    initial = np.zeros_like(prepared)
    initial[0] = 1.0
    direction = initial - prepared
    direction /= np.linalg.norm(direction)
    unitary = np.eye(len(prepared)) - 2.0 * np.outer(direction, direction)
    unitarity = float(np.max(np.abs(unitary.T @ unitary - np.eye(len(prepared)))))
    state_error = float(np.max(np.abs(unitary @ initial - prepared)))
    return unitary, unitarity, state_error


def polynomial_circuit_sweep() -> tuple[dict[str, object], dict[str, float]]:
    rng = np.random.default_rng(SEED)
    rows = []
    maximum_error = 0.0
    maximum_imaginary = 0.0
    minimum_target = math.inf
    maximum_target = -math.inf
    unitarity_error = 0.0
    state_error = 0.0
    negative = {"phase_dropped": 0.0, "wrong_state_amplitudes": 0.0, "term_dropped": 0.0}

    for dimension in (1, 2, 3, 4):
        for case in range(32):
            frequencies, coefficients = random_positive_polynomial(rng, dimension)
            points = rng.uniform(-math.pi, math.pi, size=(1024, dimension))
            basis = np.exp(1j * (points @ frequencies.T))
            target_complex = basis @ coefficients
            target = target_complex.real
            scale = float(np.sum(np.abs(coefficients)))
            probabilities = np.abs(coefficients) / scale
            phases = np.angle(coefficients)
            amplitude = basis @ (probabilities * np.exp(1j * phases))
            output = scale * np.abs(amplitude)

            error = float(np.max(np.abs(output - target)))
            imag = float(np.max(np.abs(target_complex.imag)))
            maximum_error = max(maximum_error, error)
            maximum_imaginary = max(maximum_imaginary, imag)
            minimum_target = min(minimum_target, float(np.min(target)))
            maximum_target = max(maximum_target, float(np.max(target)))

            # The paper reserves address |0> for padding. Since n=3^d is odd,
            # m=ceil(log2 n) still leaves at least n+1 addresses.
            n_terms = len(coefficients)
            capacity = 1 << math.ceil(math.log2(n_terms))
            if capacity < n_terms + 1:
                raise AssertionError((dimension, n_terms, capacity))
            if case == 0:
                prepared = np.zeros(capacity)
                prepared[1 : n_terms + 1] = np.sqrt(probabilities)
                _, unitary_case, state_case = householder_state(prepared)
                unitarity_error = max(unitarity_error, unitary_case)
                state_error = max(state_error, state_case)

            no_phase = scale * np.abs(basis @ probabilities)
            wrong_probabilities = probabilities**2
            wrong_probabilities /= np.sum(wrong_probabilities)
            wrong_state = scale * np.abs(
                basis @ (wrong_probabilities * np.exp(1j * phases))
            )
            drop_index = int(np.argmax(np.abs(coefficients[1:]))) + 1
            dropped = probabilities * np.exp(1j * phases)
            dropped = dropped.copy()
            dropped[drop_index] = 0.0
            term_dropped = scale * np.abs(basis @ dropped)
            negative["phase_dropped"] = max(
                negative["phase_dropped"], float(np.sqrt(np.mean((no_phase - target) ** 2)))
            )
            negative["wrong_state_amplitudes"] = max(
                negative["wrong_state_amplitudes"],
                float(np.sqrt(np.mean((wrong_state - target) ** 2))),
            )
            negative["term_dropped"] = max(
                negative["term_dropped"],
                float(np.sqrt(np.mean((term_dropped - target) ** 2))),
            )
            rows.append(
                {
                    "dimension": dimension,
                    "case": case,
                    "terms": n_terms,
                    "points": len(points),
                    "max_abs_error": error,
                }
            )

    cells = sum(row["points"] for row in rows)
    result = {
        "seed": SEED,
        "dimensions": [1, 2, 3, 4],
        "random_polynomials": len(rows),
        "evaluation_cells": cells,
        "terms_by_dimension": {
            str(d): 3**d for d in (1, 2, 3, 4)
        },
        "target_minimum": minimum_target,
        "target_maximum": maximum_target,
        "maximum_target_imaginary_residual": maximum_imaginary,
        "maximum_circuit_output_error": maximum_error,
        "maximum_state_prep_unitarity_error": unitarity_error,
        "maximum_state_prep_encoding_error": state_error,
        "all_in_scope": minimum_target >= -TOL and maximum_target <= 1.0 + TOL,
        "all_exact": maximum_error <= TOL and maximum_imaginary <= TOL,
    }
    return result, negative


def target_values(name: str, points: np.ndarray) -> np.ndarray:
    if name == "smooth_1d":
        return 0.1 + 0.8 * np.exp(np.cos(points[:, 0]) - 1.0)
    if name == "jump_1d":
        return 0.2 + 0.6 * (np.sin(points[:, 0]) >= 0.0)
    if name == "smooth_2d":
        score = np.cos(points[:, 0]) + np.cos(points[:, 1])
        return 0.1 + 0.8 / (1.0 + np.exp(-2.0 * score))
    if name == "checker_2d":
        sign = np.sin(points[:, 0]) * np.sin(points[:, 1])
        return 0.15 + 0.7 * (sign >= 0.0)
    if name in {"smooth_3d", "smooth_4d"}:
        return 0.1 + 0.8 * np.exp(np.mean(np.cos(points) - 1.0, axis=1))
    raise KeyError(name)


def fft_coefficients(name: str, dimension: int, grid_size: int) -> tuple[np.ndarray, np.ndarray]:
    axes = [2.0 * math.pi * np.arange(grid_size) / grid_size] * dimension
    mesh = np.meshgrid(*axes, indexing="ij")
    points = np.stack([entry.ravel() for entry in mesh], axis=1)
    values = target_values(name, points).reshape((grid_size,) * dimension)
    coefficients = np.fft.fftshift(np.fft.fftn(values) / values.size)
    one_axis = np.fft.fftshift(
        np.rint(np.fft.fftfreq(grid_size) * grid_size).astype(int)
    )
    freq_mesh = np.meshgrid(*([one_axis] * dimension), indexing="ij")
    frequencies = np.stack([entry.ravel() for entry in freq_mesh], axis=1)
    return frequencies, coefficients.ravel()


def evaluate_series(
    points: np.ndarray, frequencies: np.ndarray, coefficients: np.ndarray
) -> np.ndarray:
    result = np.empty(len(points), dtype=complex)
    for start in range(0, len(points), 256):
        stop = min(start + 256, len(points))
        result[start:stop] = np.exp(
            1j * (points[start:stop] @ frequencies.T)
        ) @ coefficients
    return result


def rmse_with_ci(errors: np.ndarray) -> tuple[float, float]:
    squares = np.asarray(errors, dtype=float) ** 2
    mse = float(np.mean(squares))
    rmse = math.sqrt(mse)
    if rmse == 0.0:
        return 0.0, 0.0
    se_mse = float(np.std(squares, ddof=1) / math.sqrt(len(squares)))
    return rmse, 1.96 * se_mse / (2.0 * rmse)


def convergence_sweep() -> dict[str, object]:
    specifications = (
        ("smooth_1d", 1, 1024, (1, 2, 4, 8, 16, 32)),
        ("jump_1d", 1, 1024, (1, 2, 4, 8, 16, 32)),
        ("smooth_2d", 2, 128, (1, 2, 3, 5, 8)),
        ("checker_2d", 2, 128, (1, 2, 3, 5, 8)),
        ("smooth_3d", 3, 32, (1, 2, 3, 4)),
        ("smooth_4d", 4, 12, (1, 2, 3)),
    )
    rng = np.random.default_rng(SEED + 1)
    rows = []
    maximum_inequality_violation = 0.0
    for name, dimension, grid_size, degrees in specifications:
        frequencies, coefficients = fft_coefficients(name, dimension, grid_size)
        test_points = rng.uniform(-math.pi, math.pi, size=(4096, dimension))
        target = target_values(name, test_points)
        for degree in degrees:
            mask = np.all(np.abs(frequencies) <= degree, axis=1)
            selected_frequencies = frequencies[mask]
            weights = np.prod(
                1.0 - np.abs(selected_frequencies) / (degree + 1.0), axis=1
            )
            selected_coefficients = coefficients[mask] * weights
            polynomial = evaluate_series(
                test_points, selected_frequencies, selected_coefficients
            )
            fourier_error = np.abs(polynomial - target)
            saqnn_output = np.abs(polynomial)
            saqnn_error = np.abs(saqnn_output - target)
            maximum_inequality_violation = max(
                maximum_inequality_violation,
                float(np.max(saqnn_error - fourier_error)),
            )
            rmse, ci95 = rmse_with_ci(saqnn_output - target)
            fourier_rmse, _ = rmse_with_ci(np.abs(polynomial - target))
            rows.append(
                {
                    "target": name,
                    "dimension": dimension,
                    "degree": degree,
                    "terms": int(len(selected_coefficients)),
                    "test_points": len(test_points),
                    "saqnn_l2": rmse,
                    "saqnn_l2_ci95": ci95,
                    "fourier_l2": fourier_rmse,
                    "target_min": float(np.min(target)),
                    "target_max": float(np.max(target)),
                }
            )

    per_target = {}
    for name, *_ in specifications:
        curve = [row for row in rows if row["target"] == name]
        per_target[name] = {
            "initial_l2": curve[0]["saqnn_l2"],
            "final_l2": curve[-1]["saqnn_l2"],
            "improvement_ratio": curve[-1]["saqnn_l2"] / curve[0]["saqnn_l2"],
            "final_ci95": curve[-1]["saqnn_l2_ci95"],
            "final_degree": curve[-1]["degree"],
            "final_terms": curve[-1]["terms"],
        }
    all_improve = all(item["improvement_ratio"] < 0.65 for item in per_target.values())
    all_resolved = all(item["final_l2"] < 0.18 for item in per_target.values())
    return {
        "seed": SEED + 1,
        "targets": per_target,
        "rows": rows,
        "total_holdout_evaluations": sum(row["test_points"] for row in rows),
        "maximum_modulus_inequality_violation": maximum_inequality_violation,
        "all_targets_in_scope": all(
            row["target_min"] >= -TOL and row["target_max"] <= 1.0 + TOL
            for row in rows
        ),
        "all_targets_improve": all_improve,
        "all_final_l2_below_0_18": all_resolved,
        "proof_inequality_holds": maximum_inequality_violation <= TOL,
    }


def write_csv(rows: list[dict[str, object]]) -> None:
    columns = (
        "target",
        "dimension",
        "degree",
        "terms",
        "test_points",
        "saqnn_l2",
        "saqnn_l2_ci95",
        "fourier_l2",
        "target_min",
        "target_max",
    )
    lines = [",".join(columns)]
    for row in rows:
        lines.append(",".join(str(row[column]) for column in columns))
    (OUT / "convergence.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    contract = source_contract()
    polynomial, negative = polynomial_circuit_sweep()
    convergence = convergence_sweep()
    negative_detected = {
        name: value > 1e-4 for name, value in negative.items()
    }
    verdict = (
        polynomial["all_in_scope"]
        and polynomial["all_exact"]
        and convergence["all_targets_in_scope"]
        and convergence["all_targets_improve"]
        and convergence["all_final_l2_below_0_18"]
        and convergence["proof_inequality_holds"]
        and all(negative_detected.values())
    )
    result = {
        "claim": "Theorem 1 universal approximation for [0,1]-valued L2 targets",
        "verdict": "VERIFIED" if verdict else "BLOCKED",
        "contract": contract,
        "finite_construction": polynomial,
        "general_target_convergence": {
            key: value for key, value in convergence.items() if key != "rows"
        },
        "negative_controls": {
            "measured_l2_errors": negative,
            "all_detected": negative_detected,
        },
        "limitations": [
            "Finite computation cannot enumerate the theorem's uncountable target class.",
            "Universality relies on the source-cited L2 density of trigonometric polynomials; this audit machine-checks the SAQNN reduction and broad finite consequences.",
            "Monte-Carlo L2 values are empirical support with 95% standard-error intervals, not the logical basis of the universal quantifier.",
            "No hardware noise, training dynamics, or optimizer claim is tested.",
        ],
        "runtime": {
            "seconds": time.monotonic() - started,
            "platform": platform.platform(),
            "logical_cpu_count": os.cpu_count(),
            "numpy": np.__version__,
            "seeds": [SEED, SEED + 1],
        },
    }
    write_csv(convergence["rows"])
    (OUT / "raw_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (OUT / "negative_controls.json").write_text(
        json.dumps(result["negative_controls"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("=== CLAIM1_RAW_RESULTS_JSON ===")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("=== CLAIM1_CONVERGENCE_CSV ===")
    print((OUT / "convergence.csv").read_text(encoding="utf-8"), end="")
    if not verdict:
        raise SystemExit("Claim 1 verification obligations were not met")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
