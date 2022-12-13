"""
A non-distributed implementation of the Quantum Fourier Transformation (QFT).
"""

from numpy import pi
from qiskit_textbook.tools import array_to_latex
from qiskit import Aer, QuantumCircuit, transpile
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_bloch_multivector, plot_state_city


class QFT:
    """
    A non-distributed implementation of the Quantum Fourier Transformation (QFT).
    """

    def __init__(self, nr_qubits, swaps=True):
        self.nr_qubits = nr_qubits
        self.swaps = swaps
        self.qc = QuantumCircuit(nr_qubits)
        self.qc_with_input = None
        self.simulator = None
        self.result = None
        self._make_qft()

    def _make_qft(self):
        self._add_qft_rotations(self.nr_qubits)
        if self.swaps:
            self._add_qft_swaps()

    def _add_qft_rotations(self, remaining_nr_qubits):
        if remaining_nr_qubits == 0:
            return
        remaining_nr_qubits -= 1
        self.qc.h(remaining_nr_qubits)
        for qubit in range(remaining_nr_qubits):
            self.qc.cp(pi / 2 ** (remaining_nr_qubits - qubit), qubit, remaining_nr_qubits)
        self._add_qft_rotations(remaining_nr_qubits)

    def _add_qft_swaps(self):
        for qubit in range(self.nr_qubits // 2):
            self.qc.swap(qubit, self.nr_qubits - qubit - 1)

    def circuit_diagram(self, with_input=False):
        if with_input:
            if self.qc_with_input is None:
                return None
            return self.qc_with_input.draw(fold=False, output="mpl")
        return self.qc.draw(fold=False, output="mpl")

    def statevector(self):
        if self.result is None:
            return None
        return self.result.get_statevector().data

    def statevector_latex(self):
        if self.result is None:
            return None
        return array_to_latex(self.result.get_statevector())

    def bloch_multivector(self):
        if self.result is None:
            return None
        return plot_bloch_multivector(self.result.get_statevector())

    def density_matrix(self):
        if self.result is None:
            return None
        return DensityMatrix(self.result.get_statevector())

    def density_matrix_city(self):
        if self.result is None:
            return None
        return plot_state_city(self.result.get_statevector())

    def run(self, input_value, shots=10000):
        self.qc_with_input = QuantumCircuit(self.nr_qubits)
        bin_value = bin(input_value)[2:].zfill(self.nr_qubits)
        self.qc_with_input.initialize(bin_value, self.qc_with_input.qubits)
        self.qc_with_input = self.qc_with_input.compose(self.qc)
        self.simulator = Aer.get_backend("aer_simulator")
        self.qc_with_input.save_statevector()
        self.qc_with_input = transpile(self.qc_with_input, self.simulator)
        self.result = self.simulator.run(self.qc_with_input, shots=shots).result()
