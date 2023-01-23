"""
QNE-ADK application distributed quantum Fourier transformation on two processors.
This is the program for the first of two processors.
"""

import processor
import numpy


def main(app_config=None):
    """
    Main function for the QNE-ADK quantum Fourier transformation running on the first of two
    processors.
    """
    total_nr_qubits = 4
    controller_processor = processor.Processor(
        app_config=app_config, nr_processors=2, total_nr_qubits=total_nr_qubits, processor_index=0
    )
    quantum_fourier_transform(controller_processor, total_nr_qubits)


def quantum_fourier_transform(controller_processor, total_nr_qubits):
    """
    Perform a (distributed) quantum Fourier transformation.

    Parameters
    ----------
    controller_processor: The controller processor in the cluster.
    total_nr_qubits: The total number of qubits for the QFT.
    """
    add_qft_rotations(controller_processor, total_nr_qubits)


def add_qft_rotations(controller_processor, remaining_nr_qubits):
    """
    Perform the controlled rotations part of the distributed quantum Fourier transformation.

    Parameters
    ----------
    controller_processor: The controller processor in the cluster.
    remaining_nr_qubits: The remaining number of qubits for which controlled rotations need
        to be performed.
    """
    if remaining_nr_qubits == 0:
        return
    remaining_nr_qubits -= 1
    controller_processor.hadamard(remaining_nr_qubits)
    for qubit in range(remaining_nr_qubits):
        controller_processor.controlled_phase(
            numpy.pi / 2 ** (remaining_nr_qubits - qubit), qubit, remaining_nr_qubits
        )
    add_qft_rotations(controller_processor, remaining_nr_qubits)


# TODO: Add swaps
