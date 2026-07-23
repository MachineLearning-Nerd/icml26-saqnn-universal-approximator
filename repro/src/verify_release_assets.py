#!/usr/bin/env python3
"""Fail-closed integrity checks for claim packages and reader-facing assets."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
REPORT = ROOT / "reports" / "saqnn-reproduction" / "report.md"
NOTEBOOK = ROOT / "notebooks" / "saqnn_reproduction.py"
README = ROOT / "README.md"
EXACT_COMMAND = "uv sync --frozen && uv run --frozen python repro/run_all.py"
REQUIRED = {
    "claim1": {
        "claim_contract.json",
        "source_audit.md",
        "method.md",
        "expected_scientific_results.json",
        "expected_convergence.csv",
        "expected_independent_checker.json",
        "expected_negative_controls.json",
        "environment.json",
        "execution.json",
        "EVAL.md",
        "limitations.md",
    },
    "claim2": {
        "claim_contract.json",
        "source_audit.md",
        "method.md",
        "raw_results.json",
        "independent_checker.json",
        "negative_controls.json",
        "execution.json",
        "EVAL.md",
        "limitations.md",
    },
    "claim3": {
        "claim_contract.json",
        "source_audit.md",
        "method.md",
        "raw_results.json",
        "independent_checker.json",
        "negative_controls.json",
        "execution.json",
        "EVAL.md",
        "limitations.md",
    },
    "claim4": {
        "claim_contract.json",
        "source_audit.md",
        "method.md",
        "raw_results.json",
        "independent_checker.json",
        "negative_controls.json",
        "execution.json",
        "EVAL.md",
        "limitations.md",
    },
    "claim5": {
        "claim_contract.json",
        "source_audit.md",
        "method.md",
        "raw_results.json",
        "independent_checker.json",
        "negative_controls.json",
        "execution.json",
        "EVAL.md",
        "limitations.md",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    missing: list[str] = []
    for claim, filenames in REQUIRED.items():
        for filename in filenames:
            path = ARTIFACTS / claim / filename
            if not path.is_file():
                missing.append(str(path.relative_to(ROOT)))

    json_paths = sorted(ARTIFACTS.glob("claim*/*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))

    report_text = REPORT.read_text(encoding="utf-8")
    image_refs = re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", report_text)
    image_checks: dict[str, dict[str, object]] = {}
    for relative in image_refs:
        path = REPORT.parent / relative
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image_checks[relative] = {
                "width": image.width,
                "height": image.height,
                "sha256": sha256(path),
                "valid_size": image.width >= 1200 and image.height >= 700,
            }

    notebook_check = subprocess.run(
        ["marimo", "check", "--strict", str(NOTEBOOK)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    public_text = "\n".join(
        [
            README.read_text(encoding="utf-8"),
            report_text,
            NOTEBOOK.read_text(encoding="utf-8"),
            *[
                path.read_text(encoding="utf-8")
                for path in ARTIFACTS.glob("claim*/*")
                if path.suffix in {".json", ".md", ".csv"}
            ],
        ]
    )
    secret_patterns = {
        "private_key": r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----",
        "huggingface_token": r"\bhf_[A-Za-z0-9]{20,}\b",
        "github_token": r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",
    }
    secret_hits = {
        name: bool(re.search(pattern, public_text))
        for name, pattern in secret_patterns.items()
    }
    readme_text = README.read_text(encoding="utf-8")
    checks = {
        "no_missing_claim_files": not missing,
        "five_distinct_report_images": len(set(image_refs)) == 5,
        "all_report_images_valid": all(
            item["valid_size"] for item in image_checks.values()
        ),
        "strongest_figure_immediately_after_title": report_text.startswith(
            "# SAQNN universal approximation: a claim-by-claim reproduction\n\n!["
        ),
        "marimo_check_strict": notebook_check.returncode == 0,
        "readme_has_exact_command": EXACT_COMMAND in readme_text,
        "readme_accounts_for_main": "Not run as an experiment (publication surface)"
        in readme_text,
        "no_secret_patterns": not any(secret_hits.values()),
    }
    result = {
        "verdict": "VERIFIED" if all(checks.values()) else "BLOCKED",
        "checks": checks,
        "missing": missing,
        "image_checks": image_checks,
        "json_files_validated": len(json_paths),
        "marimo_stdout": notebook_check.stdout,
        "marimo_stderr": notebook_check.stderr,
        "secret_pattern_hits": secret_hits,
    }
    print("=== RELEASE_ASSET_INTEGRITY_JSON ===")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit("release asset integrity check failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
