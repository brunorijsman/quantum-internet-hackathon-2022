"""
A non-distributed implementation of the Quantum Fourier Transformation (QFT).
"""

from quantum_computer import MonolithicQuantumComputer


class QFT(MonolithicQuantumComputer):
    """
    A non-distributed implementation of the Quantum Fourier Transformation (QFT).
    """

    def __init__(self, total_nr_qubits, final_swaps=True):
        """
        Constructor.

        Parameters
        ----------
        nr_qubits: The number of qubits in the quantum Fourier transform circuit.
        final_swaps: Should the final qubit reordering swaps be performed at the end of the quantum
            Fourier transform.
        """
        MonolithicQuantumComputer.__init__(self, total_nr_qubits)
        self.make_qft_circuit(final_swaps)
