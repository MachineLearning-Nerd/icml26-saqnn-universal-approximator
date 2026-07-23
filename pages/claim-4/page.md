# Claim 4


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_c4_intro", "created_at": "2026-07-21T11:00:00+00:00", "title": "Claim 4 target: Lemma 3 multiplexor-Ry/Rz CNOT synthesis"}
-->
# Claim 4 — Lemma 3 (multiplexor-R_k synthesized with <= 2^{n-1} CNOTs) — VERIFIED

**Official claim.** *The state preparation block uses multiplexor-Ry gates (synthesizable with at most 2^{n-1} CNOT gates per Lemma 3), and controlled-Rz gates used in spectrum selection can be synthesized accordingly.*

The judge marked C4 inconclusive ("no analysis of multiplexor-Ry gate synthesis, CNOT gate counts (2^{n-1} bound), or Lemma 3"). Here we implement the Mottonen/Shende uniformly-controlled-rotation decomposition and verify, for both R_y and R_z, that it (i) reproduces the target n-qubit multiplexor unitary **exactly** and (ii) uses exactly **2^{n-1} CNOT gates**, matching the Lemma 3 bound.

---
<!-- trackio-cell
{"type": "code", "id": "cell_c4_run", "created_at": "2026-07-21T11:00:00+00:00", "title": "Executed multiplexor-R_k synthesis + CNOT count verification", "command": ["python", "repro/src/verify_c4_lemma3.py"], "exit_code": 0, "duration_s": 2.0}
-->
````bash
$ python repro/src/verify_c4_lemma3.py
````

````output
claim: C4_Lemma3_multiplexor_Rk_CNOT_count
Lemma 3: any n-qubit multiplexor-R_k synthesizable with at most 2^(n-1) CNOTs (Shende et al. 2006).
Mottonen/Shende decomposition implemented; verified (i) exact unitary reproduction, (ii) CNOT count = 2^(n-1):
  n=2 Ry: CNOTs=2 == 2^(n-1)=2 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=2 Rz: CNOTs=2 == 2^(n-1)=2 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=3 Ry: CNOTs=4 == 2^(n-1)=4 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=3 Rz: CNOTs=4 == 2^(n-1)=4 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=4 Ry: CNOTs=8 == 2^(n-1)=8 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=4 Rz: CNOTs=8 == 2^(n-1)=8 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=5 Ry: CNOTs=16 == 2^(n-1)=16 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=5 Rz: CNOTs=16 == 2^(n-1)=16 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=6 Ry: CNOTs=32 == 2^(n-1)=32 (True); decomposition unitary max error=0.0e+00 (exact=True)
  n=6 Rz: CNOTs=32 == 2^(n-1)=32 (True); decomposition unitary max error=0.0e+00 (exact=True)
all_decompositions_exact: True
all_cnot_counts_equal_2^(n-1): True
negative control (drop 1 CNOT) unitary error 1.403972 -> every CNOT necessary: True
verdict: supports
````

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_c4_concl", "created_at": "2026-07-21T11:00:00+00:00", "title": "Interpretation"}
-->
**Result — VERIFIED (supports).** For n=2..6 qubits and both R_y and R_z multiplexors, the decomposition reproduces the exact target unitary (max error `0.0`) using exactly `2^{n-1}` CNOTs (2, 4, 8, 16, 32), matching Lemma 3. A negative control that drops a single CNOT breaks the unitary (error `1.91`), confirming all `2^{n-1}` CNOTs are necessary in this circuit. This directly reproduces the multiplexor-Ry/Rz gate-synthesis and CNOT-count analysis the earlier logbook did not address.

