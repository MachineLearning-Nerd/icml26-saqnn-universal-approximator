#!/usr/bin/env python3
"""Fixed entrypoint for the cumulative SAQNN reproduction suite.

The OpenResearch run command never changes. Experiment branches vary this
committed runner and add claim verifiers while retaining every accepted check.
"""

from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / ".openresearch" / "artifacts" / "runtime.json"

BASELINE_STEPS = (
    (
        "source-pinned three-claim audit",
        "repro/src/full_audit.py",
        "--source-dir",
        "docs/source",
        "--output",
        "outputs/full_audit.json",
    ),
    ("independent regression tests", "repro/src/run_tests.py"),
    ("fail-closed baseline verifier", "repro/src/verify_claims.py"),
    ("Claim 2 exact resource proof", "repro/src/verify_c2_resource_proof.py"),
    ("Claim 2 independent resource audit", "repro/src/audit_c2_resource_proof.py"),
    (
        "judged SAQNN circuit and basis regression",
        "repro/src/verify_c0c4_saqnn_circuit.py",
    ),
    ("judged Claim 2 complexity regression", "repro/src/verify_c2_complexity.py"),
    ("judged Claim 4 multiplexor regression", "repro/src/verify_c4_lemma3.py"),
    ("judged Claim 5 basis regression", "repro/src/verify_c5_basis.py"),
    ("Claim 1 full multivariate verifier", "repro/src/verify_claim1_full.py"),
    ("Claim 1 independent checker", "repro/src/check_claim1_independent.py"),
    (
        "Claim 1 frozen evidence package",
        "repro/src/verify_claim1_evidence_package.py",
    ),
    ("baseline evidence hash bundle", "repro/src/build_evidence_bundle.py"),
)


def git_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def installed_versions() -> dict[str, str]:
    return {
        distribution.metadata["Name"]: distribution.version
        for distribution in sorted(
            importlib.metadata.distributions(),
            key=lambda item: (item.metadata["Name"] or "").lower(),
        )
        if distribution.metadata["Name"]
    }


def run_step(step: tuple[str, ...]) -> None:
    label, *arguments = step
    print(f"\n=== {label} ===", flush=True)
    completed = subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        check=False,
    )
    if completed.returncode:
        raise SystemExit(
            f"{label} failed with exit code {completed.returncode}"
        )


def main() -> int:
    started = time.monotonic()
    runtime = {
        "schema_version": 1,
        "git_sha": git_sha(),
        "python": sys.version,
        "python_executable": str(Path(sys.executable).resolve()),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "logical_cpu_count": os.cpu_count(),
        "environment_manager": "uv",
        "uv_lock_sha256": __import__("hashlib").sha256(
            (ROOT / "uv.lock").read_bytes()
        ).hexdigest(),
        "deterministic_seed_policy": "baseline checks are deterministic and seed-free",
        "installed_distributions": installed_versions(),
    }
    RUNTIME_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_PATH.write_text(
        json.dumps(runtime, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("=== runtime contract ===")
    print(json.dumps(runtime, indent=2, sort_keys=True), flush=True)

    for step in BASELINE_STEPS:
        run_step(step)

    summary = {
        "campaign": "SAQNN claim-by-claim reproduction",
        "status": "PASS",
        "git_sha": runtime["git_sha"],
        "checks_completed": [step[0] for step in BASELINE_STEPS],
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }
    print("\n=== ORX_EVAL_SUMMARY ===")
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
