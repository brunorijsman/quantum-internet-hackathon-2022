from cluster import Cluster
from numpy import pi
from qiskit import Aer, QuantumCircuit, transpile
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_bloch_multivector, plot_state_city
from qiskit_textbook.tools import array_to_latex


class TeleportDQFT(Cluster):

    def __init__(self, nr_processors, total_nr_qubits):
        Cluster.__init__(self, nr_processors, total_nr_qubits,flag="teleport")
        self.swaps = True  # TODO Add this as a constructor parameter
        self.make_qft()

    def make_qft(self):
        self.add_qft_rotations(self.total_nr_qubits)
        if self.swaps:
            self.add_qft_swaps()
        self.clear_ancillary()
        # TODO self.final_measure()

    def add_qft_rotations(self, n):
        if n == 0:
            return
        n -= 1
        self.hadamard(n)
        for qubit in range(n):
            self.controlled_phase(pi/2 ** (n - qubit), qubit, n,flag="teleport")
        self.add_qft_rotations(n)

    def add_qft_swaps(self):
        for qubit in range(self.total_nr_qubits // 2):
            self.swap(qubit, self.total_nr_qubits - qubit - 1)
