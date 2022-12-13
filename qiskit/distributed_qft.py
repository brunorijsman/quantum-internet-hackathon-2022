from cluster import Cluster
from numpy import pi


class DistributedQFT(Cluster):

    def __init__(self, nr_processors, total_nr_qubits, method):
        Cluster.__init__(self, nr_processors, total_nr_qubits, method)
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
            self.controlled_phase(pi/2 ** (n - qubit), qubit, n)
        self.add_qft_rotations(n)

    def add_qft_swaps(self):
        for qubit in range(self.total_nr_qubits // 2):
            self.swap(qubit, self.total_nr_qubits - qubit - 1)
