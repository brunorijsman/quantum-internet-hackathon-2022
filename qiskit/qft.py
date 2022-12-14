"""
A non-distributed implementation of the Quantum Fourier Transformation (QFT).
"""

from numpy import pi
from quantum_computer import ClusteredQuantumComputer, MonolithicQuantumComputer


def _add_qft_circuit(processor, final_swaps):
    _add_qft_circuit_rotations(processor, processor.total_nr_qubits)
    if final_swaps:
        _add_qft_circuit_final_swaps(processor)


def _add_qft_circuit_rotations(processor, remaining_nr_qubits):
    if remaining_nr_qubits == 0:
        return
    remaining_nr_qubits -= 1
    processor.hadamard(remaining_nr_qubits)
    for qubit in range(remaining_nr_qubits):
        processor.controlled_phase(
            pi / 2 ** (remaining_nr_qubits - qubit), qubit, remaining_nr_qubits
        )
    _add_qft_circuit_rotations(processor, remaining_nr_qubits)


def _add_qft_circuit_final_swaps(processor):
    for qubit in range(processor.total_nr_qubits // 2):
        processor.swap(qubit, processor.total_nr_qubits - qubit - 1)


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
        _add_qft_circuit(self, final_swaps)


class DistributedQFT(ClusteredQuantumComputer):
    """
    A distributed implementation of the Quantum Fourier Transformation (QFT).
    """

    def __init__(self, nr_processors, total_nr_qubits, method, final_swaps=True):
        ClusteredQuantumComputer.__init__(self, nr_processors, total_nr_qubits, method)
        _add_qft_circuit(self, final_swaps)
