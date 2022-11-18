Application: qft

Nodes: qc1

Description: Perform a (non-distributed) quantum fourier transformation

Procedure:
1. Create a quantum fourier transformation circuit of size n
2. Apply the qft circuit to input i
3. Print the resulting state vector

We compare the state vector produced by QNE with the state vector produced by Qiskit Aer
to make sure the circuit is implemented correctly.