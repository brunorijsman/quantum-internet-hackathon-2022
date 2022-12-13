"""
A non-distributed implementation of the Quantum Fourier Transformation (QFT).
"""

from circuit_base import CircuitBase
from make_qft_circuit import make_qft_circuit


class QFT(CircuitBase):
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
        CircuitBase.__init__(self, total_nr_qubits)
        make_qft_circuit(self, total_nr_qubits, final_swaps)
