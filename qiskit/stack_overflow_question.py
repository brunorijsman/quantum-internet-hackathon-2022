"""
See StackOverflow question:
https://quantumcomputing.stackexchange.com/questions/29405/how-to-do-a-partial-trace-over-registers-rather-than-individual-qubits-in-qisk
"""
from qiskit import Aer, QuantumCircuit, QuantumRegister, transpile
from qiskit.providers.aer.library import save_statevector
from qiskit.quantum_info import partial_trace


qc = QuantumCircuit()

reg1 = QuantumRegister(2)
qc.add_register(reg1)

reg2 = QuantumRegister(2)
qc.add_register(reg2)

reg3 = QuantumRegister(2)
qc.add_register(reg3)

reg4 = QuantumRegister(2)
qc.add_register(reg4)

# It's not relevant to the question what exactly is done in the circuit
qc.h(reg1[0])
qc.cnot(reg1[0], reg2[0])
qc.h(reg3[0])
qc.x(reg4[0])
qc.cnot(reg3[0], reg4[0])

simulator = Aer.get_backend("aer_simulator")
qc.save_statevector()
transpiled_qc = transpile(qc, simulator)
result = simulator.run(transpiled_qc).result()
traced_over_registers = [reg2, reg4]
traced_over_qubits = []
for reg in traced_over_registers:
    traced_over_qubits += [qc.qubits.index(qubit) for qubit in reg[:]]
density_matrix = partial_trace(result.get_statevector(), traced_over_qubits)
statevector = density_matrix.to_statevector()
print(f"{statevector.data=}")
