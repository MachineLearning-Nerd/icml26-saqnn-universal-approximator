# Claim 4 method

The clean-room verifier builds the target block-diagonal rotation unitary and
the Gray-code/Mottonen-Shende gate product along separate code paths. It
compares dense unitaries for both rotation axes at two through six qubits and
counts CNOTs exactly. A dropped-CNOT circuit is the negative control.
