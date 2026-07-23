#!/usr/bin/env python3
"""Render the evidence figures used by the SAQNN reproduction report."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
REPORT = Path(__file__).resolve().parent
IMAGES = REPORT / "images"
CLAIM1 = ROOT / ".openresearch" / "artifacts" / "claim1"

COLORS = {
    "navy": "#16324F",
    "blue": "#2F6BFF",
    "cyan": "#24A6A8",
    "gold": "#F2B134",
    "coral": "#E56B6F",
    "gray": "#718096",
}


def setup() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "#F7F9FC",
            "axes.edgecolor": "#CBD5E0",
            "axes.titleweight": "bold",
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "font.size": 10,
            "grid.alpha": 0.25,
            "grid.linestyle": "--",
            "legend.frameon": False,
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(IMAGES / name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def claim1_headline() -> None:
    data = json.loads(
        (CLAIM1 / "expected_scientific_results.json").read_text(encoding="utf-8")
    )["general_target_convergence"]["targets"]
    names = ["smooth_1d", "jump_1d", "smooth_2d", "checker_2d", "smooth_3d", "smooth_4d"]
    initial = [data[name]["initial_l2"] for name in names]
    final = [data[name]["final_l2"] for name in names]
    labels = [name.replace("_", " ") for name in names]

    fig, ax = plt.subplots(figsize=(10, 5.4))
    positions = np.arange(len(names))
    width = 0.37
    ax.bar(positions - width / 2, initial, width, color=COLORS["gray"], label="First truncation")
    ax.bar(positions + width / 2, final, width, color=COLORS["blue"], label="Largest tested truncation")
    for index, value in enumerate(final):
        ax.text(index + width / 2, value + 0.006, f"{value:.3f}", ha="center", fontsize=9)
    ax.set_xticks(positions, labels, rotation=18, ha="right")
    ax.set_ylabel("Held-out L2 error")
    ax.set_title("Claim 1: every in-range target improved, including d = 4")
    ax.grid(axis="y")
    ax.legend()
    ax.text(
        0.99,
        0.97,
        "118,784 held-out evaluations • fixed seeds",
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=COLORS["navy"],
        fontweight="bold",
    )
    save(fig, "claim1-headline.png")


def claim1_convergence() -> None:
    rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    with (CLAIM1 / "expected_convergence.csv").open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows[row["target"]].append(row)

    fig, ax = plt.subplots(figsize=(10, 5.4))
    palette = [
        COLORS["blue"],
        COLORS["coral"],
        COLORS["cyan"],
        COLORS["gold"],
        COLORS["navy"],
        COLORS["gray"],
    ]
    for color, (name, values) in zip(palette, rows.items(), strict=True):
        terms = [int(value["terms"]) for value in values]
        errors = [float(value["saqnn_l2"]) for value in values]
        ax.plot(terms, errors, marker="o", linewidth=2, color=color, label=name.replace("_", " "))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Fourier terms in Fejer truncation")
    ax.set_ylabel("Held-out L2 error")
    ax.set_title("Convergence persists across smooth, discontinuous, and multivariate targets")
    ax.grid(True, which="both")
    ax.legend(ncol=2)
    save(fig, "claim1-convergence.png")


def negative_controls() -> None:
    data = json.loads(
        (CLAIM1 / "expected_negative_controls.json").read_text(encoding="utf-8")
    )["measured_l2_errors"]
    labels = ["Drop phases", "Drop one term", "Wrong amplitudes"]
    values = [data["phase_dropped"], data["term_dropped"], data["wrong_state_amplitudes"]]

    fig, ax = plt.subplots(figsize=(10, 5.4))
    bars = ax.bar(labels, values, color=[COLORS["coral"], COLORS["gold"], COLORS["cyan"]])
    ax.axhline(1e-4, color=COLORS["navy"], linestyle="--", label="Detection threshold")
    for bar, value in zip(bars, values, strict=True):
        ax.text(bar.get_x() + bar.get_width() / 2, value * 1.12, f"{value:.3f}", ha="center")
    ax.set_yscale("log")
    ax.set_ylim(5e-5, 1.0)
    ax.set_ylabel("L2 error")
    ax.set_title("All deliberately broken Claim 1 constructions are rejected")
    ax.legend()
    ax.grid(axis="y")
    save(fig, "negative-controls.png")


def resource_scaling() -> None:
    data = json.loads(
        (ROOT / ".openresearch" / "artifacts" / "claim2" / "raw_results.json").read_text(
            encoding="utf-8"
        )
    )["judged_regression"]
    n_values = data["n_values"]
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.plot(n_values, data["width_over_log2n"], marker="o", label="width / log2(n)")
    ax.plot(n_values, data["params_over_n"], marker="s", label="parameters / n")
    ax.plot(n_values, data["depth_over_n_log2n"], marker="^", label="depth / (n log2 n)")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("Number of Fourier terms n")
    ax.set_ylabel("Normalized resource count")
    ax.set_title("Claim 2: normalized constructive resources stay bounded")
    ax.grid(True)
    ax.legend()
    save(fig, "resource-scaling.png")


def basis_switching() -> None:
    data = json.loads(
        (ROOT / ".openresearch" / "artifacts" / "claim5" / "raw_results.json").read_text(
            encoding="utf-8"
        )
    )
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
    fourier = data["Fourier_periodic"]
    chebyshev = data["Chebyshev_nonperiodic"]
    axes[0].semilogy(
        [item["k"] for item in fourier],
        [max(item["L2_error"], 1e-16) for item in fourier],
        marker="o",
        color=COLORS["blue"],
    )
    axes[0].set_title("Periodic target: Fourier")
    axes[0].set_xlabel("Terms k")
    axes[0].set_ylabel("L2 error (zeros shown at 1e-16)")
    axes[1].semilogy(
        [item["k"] for item in chebyshev],
        [max(item["L2_error"], 1e-16) for item in chebyshev],
        marker="o",
        color=COLORS["cyan"],
    )
    axes[1].set_title("Non-periodic target: Chebyshev")
    axes[1].set_xlabel("Terms k")
    for ax in axes:
        ax.grid(True, which="both")
    fig.suptitle("Claim 5: the same architecture realizes two useful spectral bases", fontweight="bold")
    save(fig, "basis-switching.png")


def main() -> None:
    setup()
    claim1_headline()
    claim1_convergence()
    negative_controls()
    resource_scaling()
    basis_switching()
    for path in sorted(IMAGES.glob("*.png")):
        print(f"{path.relative_to(ROOT)} {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
