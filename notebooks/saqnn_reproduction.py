import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # SAQNN universal approximation, explained from the evidence

    **Central result.** The upgraded clean-room reproduction verifies the
    exact `[0,1]`-valued Theorem 1 scope across dimensions 1–4 while
    retaining the four previously verified resource and basis claims.

    The chart below is embedded from the completed formal CPU run. Nothing
    expensive needs to be rerun to read this notebook.
    """)
    return


@app.cell
def _(np, plt):
    labels = np.array(
        ["smooth 1d", "jump 1d", "smooth 2d", "checker 2d", "smooth 3d", "smooth 4d"]
    )
    initial = np.array([0.129413, 0.187156, 0.134902, 0.296130, 0.069272, 0.059959])
    final = np.array([0.007863, 0.044232, 0.032173, 0.159703, 0.028401, 0.030591])
    positions = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar(positions - 0.18, initial, 0.36, label="first truncation", color="#718096")
    ax.bar(positions + 0.18, final, 0.36, label="largest truncation", color="#2F6BFF")
    ax.set_xticks(positions, labels, rotation=18, ha="right")
    ax.set_ylabel("held-out L2 error")
    ax.set_title("All six in-range targets improve")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why the range restriction matters

    SAQNN implements a finite complex spectrum and reads out its
    **magnitude**. For a nonnegative target \(f\),

    \[
    \left||g|-f\right| \leq |g-f|.
    \]

    The accepted theorem therefore states \(f:[-\pi,\pi]^d\to[0,1]\).
    A signed function such as \(\sin x\) is useful as a scope warning, but
    cannot falsify this theorem. The reproduction tests only targets that
    satisfy the stated range.
    """)
    return


@app.cell
def _(mo):
    dimension = mo.ui.slider(1, 4, value=2, label="dimension d")
    degree = mo.ui.slider(1, 8, value=3, label="truncation degree k")
    mo.hstack([dimension, degree], justify="start")
    return degree, dimension


@app.cell
def _(degree, dimension, mo):
    terms = (2 * degree.value + 1) ** dimension.value
    qubits = (terms - 1).bit_length() + 1
    mo.md(
        f"""
        A tensor Fourier box with **d={dimension.value}** and **k={degree.value}**
        contains **{terms:,} terms**. The compressed constructive address plus
        target uses **{qubits} qubits** in this finite count. The formal Claim 2
        checker exhausts integer boundaries instead of inferring the
        asymptotics from this toy control.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## What the formal run established

    | Claim | Result | Decisive evidence |
    |---|---|---|
    | 1 | VERIFIED | 131,072 exact cells; 118,784 holdouts; independent 10,280-cell checker |
    | 2 | VERIFIED | every integer n=2..8192 plus large boundaries |
    | 3 | VERIFIED | 36 parameter-rate cells; 27 high-d size cells |
    | 4 | VERIFIED | ten exact multiplexor unitaries; dropped-CNOT control |
    | 5 | VERIFIED | exact Fourier/Chebyshev statevector identities |

    The formal command was:

    ```text
    uv sync --frozen && uv run --frozen python repro/run_all.py
    ```

    It ran on local Apple arm64 CPU at zero hosted-compute cost. The
    notebook is explanatory; its slider is not formal evidence.
    """)
    return


if __name__ == "__main__":
    app.run()
