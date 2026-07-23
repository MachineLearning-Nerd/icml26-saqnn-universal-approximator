# Method

The primary verifier constructs real, range-controlled Fourier polynomials in
dimensions one through four; explicitly builds the coefficient state,
Householder preparation, phase injection, and spectral readout; and compares
the circuit result with the intended polynomial magnitude. Fejer means test
six additional smooth or discontinuous in-range targets on fixed-seed
holdouts with 95% standard-error intervals.

The independent checker imports no primary implementation. It reconstructs
the direct sum from fresh seeded coefficients, checks the source hash and the
nonnegative-target modulus inequality, and requires all three negative
controls to be detected. Every verifier exits nonzero on an unmet obligation.
