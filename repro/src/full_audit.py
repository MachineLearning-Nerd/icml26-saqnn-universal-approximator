#!/usr/bin/env python3
"""Source-pinned, clean-room audit for the three QaHFVheV8X jury claims.

This implementation does not simulate a quantum device or import author code.
It independently evaluates the finite Fourier amplitude construction displayed
in the source and checks the source's own asymptotic resource expressions in
their stated regimes.  It is intentionally fail-closed about scope: a
nonnegative square-root observable cannot approximate arbitrary signed L2
targets with the source's positive rescaling convention.
"""

from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
from pathlib import Path


PRIMARY_TEX_SHA256 = "6ebdba9491251535fcd966fafe13ac735220a9aae9225e4f0391d558683d5ff2"
TOL = 2e-12


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_audit(source_dir: Path) -> dict:
    primary = source_dir / "main.tex"
    digest = sha256(primary)
    if digest != PRIMARY_TEX_SHA256:
        raise AssertionError((digest, PRIMARY_TEX_SHA256))
    text = primary.read_text(encoding="utf-8", errors="replace")
    anchors = {
        "theorem_1_range": r"f: [-\pi,\pi]^d\rightarrow [0,1]",
        "theorem_1_observable": r"global observable $O=\ket{0}\bra{0}$",
        "theorem_2_sobolev_range": r"Sobolev function $f\in H_u^s([-\pi,\pi]^d)$ with value range $[0,1]",
        "theorem_2_resource_formula": r"n=O((d+1/\epsilon)^{16(1/\epsilon)^{2/s}})",
        "fixed_accuracy_high_dimension_scope": r"we treat the target approximation error $\epsilon$ as a fixed constant",
        "fourier_nwidth_rate": r"n^{-s/d}",
        "case_4_rate": r"n \geq 4^d(1/\epsilon)^{d/s}d^{-d/2}",
        "positive_rescale_proof": r"Let the sum of the modulus of the coefficients of $f_k$ be",
    }
    missing = [name for name, anchor in anchors.items() if anchor not in text]
    if missing:
        raise AssertionError(("missing source anchors", missing))
    executable_suffixes = {".py", ".ipynb", ".sh", ".R", ".jl"}
    executables = sorted(
        str(path.relative_to(source_dir))
        for path in source_dir.rglob("*")
        if path.is_file() and path.suffix in executable_suffixes
    )
    if executables:
        raise AssertionError(("unexpected accepted-source executable", executables))
    return {
        "primary_tex_sha256": digest,
        "source_file_count": sum(path.is_file() for path in source_dir.rglob("*")),
        "arxiv_source_executable_files": executables,
        "source_anchors": sorted(anchors),
        "scope_disclosures": {
            "theorem_1_is_nonnegative_range_restricted": True,
            "circuit_advantage_fix_epsilon_high_d_only": True,
            "parameter_optimality_is_fixed_d_high_accuracy_fourier_rate": True,
            "uniform_resource_display_is_not_a_tight_fixed_d_accuracy_rate": True,
        },
        "pass": True,
    }


def evaluate_fourier(coefficients: dict[int, complex], x: float) -> complex:
    return sum(coefficient * cmath.exp(1j * frequency * x) for frequency, coefficient in coefficients.items())


def source_amplitude_observable(coefficients: dict[int, complex], x: float) -> float:
    """The source construction: a*|sum_r (|c_r|/a)e^iphi_r e^ij_rx|."""
    scale = sum(abs(value) for value in coefficients.values())
    if scale <= 0.0:
        raise ValueError("need a nonzero truncated Fourier polynomial")
    amplitude = sum(
        (abs(value) / scale)
        * cmath.exp(1j * cmath.phase(value))
        * cmath.exp(1j * frequency * x)
        for frequency, value in coefficients.items()
        if value != 0.0
    )
    return scale * abs(amplitude)


def mean_square(values: list[float]) -> float:
    return sum(value * value for value in values) / len(values)


def audit_universal_approximation() -> dict:
    """Check the finite construction and falsify the broader live wording."""
    # Each target is real and strictly inside [0, 1], so its exact finite
    # Fourier polynomial is nonnegative and the source square-root observable
    # should recover it exactly.
    cases = {
        "cosine": {0: 0.5, 1: 0.1, -1: 0.1},
        "sine_and_cosine": {0: 0.5, 1: 0.075, -1: 0.075, 2: 0.05j, -2: -0.05j},
        "three_harmonic": {0: 0.5, 1: 0.05, -1: 0.05, 2: 0.05, -2: 0.05, 3: 0.05, -3: 0.05},
    }
    points = [(-math.pi + 2.0 * math.pi * index / 2048.0) for index in range(2048)]
    finite_cells = 0
    max_amplitude_error = 0.0
    minimum_target_value = math.inf
    for coefficients in cases.values():
        for x in points:
            target = evaluate_fourier(coefficients, x)
            if abs(target.imag) > TOL:
                raise AssertionError(target)
            output = source_amplitude_observable(coefficients, x)
            minimum_target_value = min(minimum_target_value, target.real)
            max_amplitude_error = max(max_amplitude_error, abs(output - target.real))
            finite_cells += 1

    # Under the source proof's a=sum|c_r|>0 convention, every model output is
    # nonnegative.  For f(x)=sin(x), every nonnegative candidate has normalized
    # L2 error at least ||min(sin(x),0)||_2 = 1/2.  The discrete calculation is
    # independent of a circuit simulator and rejects the live "any L2" wording.
    signed_target = [math.sin(x) for x in points]
    nonnegative_output_lower_bound = math.sqrt(
        mean_square([min(value, 0.0) for value in signed_target])
    )
    negative_constant = [-0.25 for _ in points]
    negative_constant_lower_bound = math.sqrt(mean_square(negative_constant))

    if minimum_target_value < 0.19 or max_amplitude_error > TOL:
        raise AssertionError((minimum_target_value, max_amplitude_error))
    if abs(nonnegative_output_lower_bound - 0.5) > 1e-10:
        raise AssertionError(nonnegative_output_lower_bound)
    if abs(negative_constant_lower_bound - 0.25) > TOL:
        raise AssertionError(negative_constant_lower_bound)

    return {
        "restricted_nonnegative_finite_fourier_cells": finite_cells,
        "minimum_restricted_target_value": minimum_target_value,
        "maximum_source_amplitude_construction_error": max_amplitude_error,
        "signed_l2_counterexample": "sin(x)",
        "signed_l2_counterexample_nonnegative_output_lower_bound": nonnegative_output_lower_bound,
        "negative_constant_counterexample_nonnegative_output_lower_bound": negative_constant_lower_bound,
        "source_theorem_scope": "[0,1]-valued L2 targets with positive a=sum_r |c_r|",
        "live_claim_outcome": "falsified_as_written_range_omitted",
        "pass": True,
    }


def log_source_quantum_circuit_size(dimension: int, epsilon: float, smoothness: float) -> float:
    """log(n log(n)^2) for the source's uniform sufficient n expression."""
    exponent = 16.0 * (1.0 / epsilon) ** (2.0 / smoothness)
    log_n = exponent * math.log(dimension + 1.0 / epsilon)
    return log_n + 2.0 * math.log(log_n)


def log_source_classical_circuit_size(dimension: int, epsilon: float, smoothness: float) -> float:
    """The ReLU-FNN comparison displayed at source line 831, in log scale."""
    return (
        (3.0 * dimension * dimension / (4.0 * smoothness)) * math.log(2.0 * math.pi)
        + (dimension / (2.0 * smoothness)) * math.log(1.0 / epsilon)
    )


def audit_circuit_size_comparison() -> dict:
    """Reproduce the source's conditional comparison and reject scope expansion."""
    fixed_accuracy_cells = 0
    min_log_classical_minus_quantum = math.inf
    for smoothness in (2.0, 4.0, 8.0):
        for epsilon in (0.5, 0.2, 0.1):
            for dimension in (1_000, 10_000, 100_000):
                log_quantum = log_source_quantum_circuit_size(dimension, epsilon, smoothness)
                log_classical = log_source_classical_circuit_size(dimension, epsilon, smoothness)
                min_log_classical_minus_quantum = min(
                    min_log_classical_minus_quantum, log_classical - log_quantum
                )
                fixed_accuracy_cells += 1

    # The advertised comparison is not uniform in epsilon.  At fixed d with
    # epsilon -> 0 the source's uniform sufficient expression grows faster
    # than its displayed classical comparator; that control prevents a false
    # all-regime reading of the live metadata sentence.
    high_accuracy_dimension = 2
    high_accuracy_epsilon = 1e-3
    high_accuracy_smoothness = 2.0
    high_accuracy_log_quantum = log_source_quantum_circuit_size(
        high_accuracy_dimension, high_accuracy_epsilon, high_accuracy_smoothness
    )
    high_accuracy_log_classical = log_source_classical_circuit_size(
        high_accuracy_dimension, high_accuracy_epsilon, high_accuracy_smoothness
    )
    high_accuracy_control_rejected = high_accuracy_log_quantum > high_accuracy_log_classical

    if min_log_classical_minus_quantum <= 0.0:
        raise AssertionError(min_log_classical_minus_quantum)
    if not high_accuracy_control_rejected:
        raise AssertionError((high_accuracy_log_quantum, high_accuracy_log_classical))

    return {
        "fixed_accuracy_high_dimension_cells": fixed_accuracy_cells,
        "minimum_log_classical_size_minus_log_saqnn_size": min_log_classical_minus_quantum,
        "source_resource_model": "SAQNN n log(n)^2 versus displayed ReLU-FNN circuit-size expression",
        "high_accuracy_fixed_dimension_control": {
            "dimension": high_accuracy_dimension,
            "epsilon": high_accuracy_epsilon,
            "smoothness": high_accuracy_smoothness,
            "log_saqnn_size": high_accuracy_log_quantum,
            "log_classical_size": high_accuracy_log_classical,
            "rejected_unqualified_all_regime_advantage": high_accuracy_control_rejected,
        },
        "scope": "Fixed epsilon and sufficiently large dimension; the source comparison is not uniform in accuracy.",
        "verdict": "verified_for_source_fixed_accuracy_high_dimension_comparison",
        "pass": True,
    }


def source_case_four_log_parameter_count(dimension: int, epsilon: float, smoothness: float) -> float:
    """The source Case-4 Fourier construction: 4^d eps^(-d/s) d^(-d/2)."""
    return (
        dimension * math.log(4.0)
        + (dimension / smoothness) * math.log(1.0 / epsilon)
        - (dimension / 2.0) * math.log(dimension)
    )


def uniform_display_log_parameter_count(dimension: int, epsilon: float, smoothness: float) -> float:
    return 16.0 * (1.0 / epsilon) ** (2.0 / smoothness) * math.log(dimension + 1.0 / epsilon)


def least_squares_slope(xs: list[float], ys: list[float]) -> float:
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    return sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator


def audit_parameter_optimality() -> dict:
    """Check the fixed-d high-accuracy Fourier rate against n-width scaling."""
    cells = 0
    max_slope_error = 0.0
    minimum_case_four_log_count = math.inf
    epsilon_grid = (0.04, 0.02, 0.01, 0.005)
    for dimension in (2, 4, 8):
        for smoothness in (1.0, 2.0, 4.0):
            xs = [math.log(1.0 / epsilon) for epsilon in epsilon_grid]
            ys = [
                source_case_four_log_parameter_count(dimension, epsilon, smoothness)
                for epsilon in epsilon_grid
            ]
            slope = least_squares_slope(xs, ys)
            max_slope_error = max(max_slope_error, abs(slope - dimension / smoothness))
            minimum_case_four_log_count = min(minimum_case_four_log_count, min(ys))
            cells += len(epsilon_grid)

    # The convenient all-regime display in Theorem 2 has a very different,
    # non-optimal fixed-d dependence.  This negative control makes clear that
    # optimality follows from the tighter Fourier Case-4 construction, not the
    # displayed uniform sufficient formula alone.
    control_dimension = 2
    control_smoothness = 2.0
    control_epsilons = (0.25, 0.125, 0.0625)
    lower_logs = [
        (control_dimension / control_smoothness) * math.log(1.0 / epsilon)
        for epsilon in control_epsilons
    ]
    uniform_logs = [
        uniform_display_log_parameter_count(control_dimension, epsilon, control_smoothness)
        for epsilon in control_epsilons
    ]
    uniform_to_nwidth_log_gaps = [u - lower for u, lower in zip(uniform_logs, lower_logs)]
    nonoptimal_uniform_display_control = all(
        right > left
        for left, right in zip(uniform_to_nwidth_log_gaps, uniform_to_nwidth_log_gaps[1:])
    )

    if max_slope_error > TOL or not math.isfinite(minimum_case_four_log_count):
        raise AssertionError((max_slope_error, minimum_case_four_log_count))
    if not nonoptimal_uniform_display_control:
        raise AssertionError(uniform_to_nwidth_log_gaps)

    return {
        "fixed_dimension_high_accuracy_rate_cells": cells,
        "maximum_case_four_log_parameter_slope_error": max_slope_error,
        "case_four_parameter_exponent": "d/s in log N versus log(1/epsilon)",
        "nwidth_lower_bound_exponent": "d/s",
        "uniform_display_nonoptimality_control_log_gaps": uniform_to_nwidth_log_gaps,
        "uniform_display_control_rejected_as_optimal_fixed_d_rate": nonoptimal_uniform_display_control,
        "scope": "Fixed d and epsilon -> 0, where the source Case-4 Fourier construction has the n-width exponent d/s.",
        "verdict": "verified_for_source_fixed_dimension_high_accuracy_parameter_rate",
        "pass": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    result = {
        "candidate": {
            "openreview_id": "QaHFVheV8X",
            "arxiv": "2602.09718",
            "title": "SAQNN: Spectral Adaptive Quantum Neural Network as a Universal Approximator",
            "official_jury_claim_count": 3,
            "points_possible": 6,
        },
        "methodology": {
            "uses_competitor_code_or_results": False,
            "network_access": False,
            "compute": "deterministic CPU finite Fourier and logarithmic resource arithmetic",
        },
        "source": source_audit(arguments.source_dir),
        "claims": {
            "claim_1_universal_approximation": audit_universal_approximation(),
            "claim_2_circuit_size_advantage": audit_circuit_size_comparison(),
            "claim_3_parameter_optimality": audit_parameter_optimality(),
        },
    }
    result["candidate_decision"] = {
        "recommended_for_future_claim": True,
        "required_disclosures": [
            "The live universal-approximation wording omits the source theorem's [0,1] range restriction and is false for general signed L2 targets under the source positive-rescaling construction.",
            "The circuit-size comparison is fixed-accuracy/high-dimension only; it is not uniform as epsilon tends to zero at fixed d.",
            "The parameter-optimality result follows from the source Case-4 Fourier/n-width rate at fixed d and high accuracy, not from treating its uniform sufficient n display as a tight rate.",
            "The accepted source includes no executable author implementation; all calculations are clean-room.",
        ],
    }
    result["pass"] = result["source"]["pass"] and all(
        claim["pass"] for claim in result["claims"].values()
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
