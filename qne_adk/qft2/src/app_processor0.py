"""
QNE-ADK application distributed quantum Fourier transformation on two processors.
This is the program for the first of two processors.
"""

import processor

# import numpy


def main(app_config=None):
    """
    Main function for the QNE-ADK quantum Fourier transformation running on the first of two
    processors.
    """
    total_nr_qubits = 4
    controller_processor = processor.Processor(
        app_config=app_config, nr_processors=2, total_nr_qubits=total_nr_qubits, processor_index=0
    )
    _quantum_fourier_transform(controller_processor, total_nr_qubits)


def _quantum_fourier_transform(controller_processor, total_nr_qubits):
    _add_qft_rotations(controller_processor, total_nr_qubits)


def _add_qft_rotations(controller_processor, remaining_nr_qubits):
    if remaining_nr_qubits == 0:
        return
    remaining_nr_qubits -= 1
    controller_processor.hadamard(remaining_nr_qubits)
    # TODO
    # for qubit in range(remaining_nr_qubits):
    #     controller_processor.controlled_phase(
    #         numpy.pi / 2 ** (remaining_nr_qubits - qubit), qubit, remaining_nr_qubits
    #     )
    _add_qft_rotations(controller_processor, remaining_nr_qubits)


# TODO: Add swaps
