"""
A distributed implementation of the Quantum Fourier Transformation (QFT).
"""

from cluster import Cluster
from make_qft_circuit import make_qft_circuit


class DistributedQFT(Cluster):
    """
    A distributed implementation of the Quantum Fourier Transformation (QFT).
    """

    def __init__(self, nr_processors, total_nr_qubits, method):
        Cluster.__init__(self, nr_processors, total_nr_qubits, method)
        final_swaps = True  # TODO
        make_qft_circuit(self, total_nr_qubits, final_swaps)
