"""
A distributed implementation of the Quantum Fourier Transformation (QFT).
"""

from quantum_computer import ClusteredQuantumComputer


class DistributedQFT(ClusteredQuantumComputer):
    """
    A distributed implementation of the Quantum Fourier Transformation (QFT).
    """

    def __init__(self, nr_processors, total_nr_qubits, method, final_swaps=True):
        ClusteredQuantumComputer.__init__(self, nr_processors, total_nr_qubits, method)
        self.make_qft_circuit(final_swaps)
