"""
Functions for creating a quantum Fourier circuit, which are common for both the non-distributed and
distributed implementation
"""

from numpy import pi


def make_qft_circuit(logical_processor, total_nr_qubits, final_swaps):
    """
    Make a quantum Fourier transform circuit.
    """
    _add_rotations_to_qft_circuit(logical_processor, total_nr_qubits)
    if final_swaps:
        _add_final_swaps_to_qft_circuit(logical_processor, total_nr_qubits)
    # TODO move this to run self.measure_main()


def _add_rotations_to_qft_circuit(logical_processor, remaining_nr_qubits):
    if remaining_nr_qubits == 0:
        return
    remaining_nr_qubits -= 1
    logical_processor.hadamard(remaining_nr_qubits)
    for qubit in range(remaining_nr_qubits):
        logical_processor.controlled_phase(
            pi / 2 ** (remaining_nr_qubits - qubit), qubit, remaining_nr_qubits
        )
    _add_rotations_to_qft_circuit(logical_processor, remaining_nr_qubits)


def _add_final_swaps_to_qft_circuit(logical_processor, total_nr_qubits):
    for qubit in range(total_nr_qubits // 2):
        logical_processor.swap(qubit, total_nr_qubits - qubit - 1)
