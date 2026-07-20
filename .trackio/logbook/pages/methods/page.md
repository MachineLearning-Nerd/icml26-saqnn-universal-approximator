# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_6eb1ccb4d0a1", "created_at": "2026-07-20T10:12:29+00:00", "title": "Source and method"}
-->
Clean-room deterministic audit of the accepted arXiv 2602.09718 source. No executable author code exists in the archive. The audit reimplements the finite Fourier amplitude identity, evaluates resource formulas in log scale, pins every source hash, and uses the official 2026-07-20 three-claim website contract.


---
<!-- trackio-cell
{"type": "code", "id": "cell_1ca222d333dd", "created_at": "2026-07-20T10:12:39+00:00", "title": "Regression suite", "command": ["python", "repro/src/run_tests.py"], "exit_code": 0, "duration_s": 0.133}
-->
````bash
$ python repro/src/run_tests.py
````

exit 0 · 0.1s


````python title=run_tests.py
"""Run the full standard-library test suite and retain a machine-readable result."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    payload = {
        "tests_passed": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    (ROOT / "outputs" / "test_results.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(completed.stdout, end="")
    print(completed.stderr, file=sys.stderr, end="")
    if completed.returncode:
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()

````


````output
test_claim_2_conditional_circuit_advantage (test_audit.AuditTests.test_claim_2_conditional_circuit_advantage) ... ok
test_claim_3_fixed_dimension_parameter_rate (test_audit.AuditTests.test_claim_3_fixed_dimension_parameter_rate) ... ok
test_source_and_claim_1_range_counterexample (test_audit.AuditTests.test_source_and_claim_1_range_counterexample) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.039s

OK

````
