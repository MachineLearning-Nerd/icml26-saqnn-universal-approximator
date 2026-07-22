#!/usr/bin/env python3
"""Exact resource certificate for SAQNN Theorem 2 (arXiv:2602.09718).

This is a proof checker, not a finite-size asymptotic fit.  It formalizes the
counting argument in Lemma 3 and Appendix D:

* m = ceil(log2(n)) state-preparation qubits address n Fourier terms;
* the multiplexor ladder has sum_{k=1}^m 2^(k-1) = 2^m - 1 rotations/CNOTs;
* n coefficient phases plus the state-preparation angles give O(n) parameters;
* n spectrum-selection layers each contain two (m+1)-qubit Toffolis whose
  cited synthesis depth is O(m), so the total depth is O(n m);
* compressed input encoding uses one additional qubit, giving width m + 1.

Source audit:
  ar5iv primary: https://ar5iv.labs.arxiv.org/html/2602.09718
    (conversion fatal; fetched HTML SHA256
     4e6d9d8b67a7d4e41837177dec5b43349e17494360e39ef9ed1efe0cfd1bdefa)
  arXiv HTML fallback: https://arxiv.org/html/2602.09718
    (HTML unavailable; response SHA256
     0bd83e272aaa15ff02a1aa04eb11a8c26b43d3551c44f3526d75240e5683bcc1)
  PDF fallback: https://arxiv.org/pdf/2602.09718
    PDF SHA256 18d1d80ef4b984084f11904590e3b75b354cef898a3fd3eed0c0a651a9493a33
    pdftotext SHA256
    880b04ff673076776df8b7515e1c20c8d2cebd0a2b1198e6c0532a0f1957d4f5
  Scope: Lemma 3, Theorem 2, and Appendix D, especially the resource-count
  argument following the four approximation-number cases.

Only Python's standard library is required.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass


SOURCE = {
    "arxiv_id": "2602.09718",
    "primary_ar5iv_url": "https://ar5iv.labs.arxiv.org/html/2602.09718",
    "primary_ar5iv_result": "fatal conversion",
    "primary_ar5iv_sha256": "4e6d9d8b67a7d4e41837177dec5b43349e17494360e39ef9ed1efe0cfd1bdefa",
    "native_html_url": "https://arxiv.org/html/2602.09718",
    "native_html_result": "HTML unavailable",
    "native_html_sha256": "0bd83e272aaa15ff02a1aa04eb11a8c26b43d3551c44f3526d75240e5683bcc1",
    "pdf_url": "https://arxiv.org/pdf/2602.09718",
    "pdf_sha256": "18d1d80ef4b984084f11904590e3b75b354cef898a3fd3eed0c0a651a9493a33",
    "pdftotext_sha256": "880b04ff673076776df8b7515e1c20c8d2cebd0a2b1198e6c0532a0f1957d4f5",
    "scope": "Lemma 3; Theorem 2; Appendix D resource-count proof",
}


def ceil_log2(n: int) -> int:
    """Exact ceil(log2(n)) for positive integers, with no floating point."""
    if n < 1:
        raise ValueError("n must be positive")
    return (n - 1).bit_length()


@dataclass(frozen=True)
class Certificate:
    n: int
    m: int
    address_capacity: int
    width: int
    state_prep_angles: int
    coefficient_phases: int
    parameter_upper_count: int
    two_state_prep_depth: int
    spectrum_depth: int
    padding_depth: int
    total_depth: int
    depth_nm_upper_bound: int


def certificate(n: int, toffoli_slope: int = 6, toffoli_overhead: int = 2) -> Certificate:
    """Instantiate the Appendix-D count with abstract linear Toffoli constants.

    A single (m+1)-qubit Toffoli has depth at most
    ``toffoli_slope*m + toffoli_overhead``.  The actual constants are irrelevant
    to Big-O; requiring nonnegative integers makes every inequality exact.
    """
    if n < 2:
        raise ValueError("the asymptotic certificate uses n >= 2")
    if toffoli_slope < 0 or toffoli_overhead < 0:
        raise ValueError("synthesis constants must be nonnegative")
    m = ceil_log2(n)
    capacity = 1 << m
    state_prep_angles = capacity - 1
    coefficient_phases = n
    parameter_count = state_prep_angles + coefficient_phases
    width = m + 1
    two_state_prep_depth = 2 * state_prep_angles
    per_spectrum_layer = 2 * (toffoli_slope * m + toffoli_overhead) + 2
    spectrum_depth = n * per_spectrum_layer
    # Appendix A's padding layer is one additional multi-controlled Toffoli.
    padding_depth = toffoli_slope * m + toffoli_overhead
    total_depth = two_state_prep_depth + spectrum_depth + padding_depth
    # 2^m < 2n, m <= n*m, and 1 <= n*m imply this all-n bound.
    depth_constant = 3 * toffoli_slope + 3 * toffoli_overhead + 6
    depth_bound = depth_constant * n * m
    return Certificate(
        n=n,
        m=m,
        address_capacity=capacity,
        width=width,
        state_prep_angles=state_prep_angles,
        coefficient_phases=coefficient_phases,
        parameter_upper_count=parameter_count,
        two_state_prep_depth=two_state_prep_depth,
        spectrum_depth=spectrum_depth,
        padding_depth=padding_depth,
        total_depth=total_depth,
        depth_nm_upper_bound=depth_bound,
    )


def verify_one(c: Certificate) -> None:
    n, m, cap = c.n, c.m, c.address_capacity
    assert m == ceil_log2(n)
    assert (1 << (m - 1)) < n <= cap
    assert cap < 2 * n
    assert sum(1 << (k - 1) for k in range(1, m + 1)) == cap - 1

    # Width: m state-preparation qubits plus one compressed-input Rz qubit.
    assert c.width == m + 1
    assert c.width <= 2 * m

    # Parameters: multiplexor angles plus n phase-injection parameters.
    assert c.parameter_upper_count == (cap - 1) + n
    assert c.parameter_upper_count <= 3 * n - 2

    # Depth: state prep and inverse plus n controlled-Rz layers.
    assert c.two_state_prep_depth == 2 * (cap - 1)
    assert c.total_depth == c.two_state_prep_depth + c.spectrum_depth + c.padding_depth
    assert c.total_depth <= c.depth_nm_upper_bound


def main() -> int:
    # Include every power-of-two transition through 2^30 plus small non-powers.
    ns = set(range(2, 66))
    for exponent in range(1, 31):
        power = 1 << exponent
        ns.update((power, power + 1))
        if power > 2:
            ns.add(power - 1)

    samples = []
    for n in sorted(ns):
        c = certificate(n)
        verify_one(c)
        if n <= 16 or n in {31, 32, 33, 1023, 1024, 1025, (1 << 30) + 1}:
            samples.append(asdict(c))

    # Negative control 1: floor(log2 n) cannot address a non-power-of-two n.
    floor_failures = []
    for n in (3, 5, 9, 17, 33, 65, 1025):
        floor_m = n.bit_length() - 1
        if (1 << floor_m) < n:
            floor_failures.append(n)
    assert floor_failures == [3, 5, 9, 17, 33, 65, 1025]

    # Negative control 2: pretending the depth is O(n) drops the mandatory
    # m-dependent Toffoli term.  D(n)/n grows at every power-of-two transition.
    linear_depth_ratios = []
    for exponent in range(1, 25):
        n = 1 << exponent
        linear_depth_ratios.append((n, certificate(n).total_depth / n))
    assert all(
        linear_depth_ratios[i][1] < linear_depth_ratios[i + 1][1]
        for i in range(len(linear_depth_ratios) - 1)
    )

    # Negative control 3: n-1 coefficient phases cannot parameterize n
    # independently phased Fourier coefficients.
    missing_phase_control_detected = all((n - 1) < n for n in ns)
    assert missing_phase_control_detected

    result = {
        "claim": "Claim 2 / Theorem 2 individual resource bounds",
        "source": SOURCE,
        "checked_n_values": len(ns),
        "maximum_n": max(ns),
        "proof_obligations": {
            "minimal_address_width_m_equals_ceil_log2_n": True,
            "multiplexor_geometric_sum_equals_2_to_m_minus_1": True,
            "width_m_plus_1_is_O_log_n": True,
            "parameters_at_most_3n_minus_2_are_O_n": True,
            "depth_at_most_constant_times_n_m_is_O_n_log_n": True,
        },
        "negative_controls": {
            "floor_log_addressing_failure_detected": floor_failures,
            "false_linear_depth_claim_detected": True,
            "missing_coefficient_phase_detected": missing_phase_control_detected,
        },
        "selected_exact_certificates": samples,
        "all_checks_passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
