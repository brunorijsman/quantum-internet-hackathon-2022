"""
General utilities for QFTs in Qiskit.
"""

from datetime import datetime
from qiskit.quantum_info import DensityMatrix


def reverse_bit_order(nr_bits, value):
    """
    Reverse the bits in a value.

    Parameters
    ----------
    nr_bits: The number of bits for the value (we need to specify this because the value might have
        leading zeroes).
    value: The value to be reversed.

    Returns
    -------
    The value of the reversed bit order.
    """
    reversed_value = 0
    for _ in range(nr_bits):
        bit = value & 1
        value >>= 1
        reversed_value <<= 1
        reversed_value |= bit
    return reversed_value


def density_matrix_reverse_bit_order(density_matrix):
    """
    Convert a density matrix into the corresponding density bit matrix where the bit order of the
    states is reversed. This is needed to convert density matrices as computed by Qiskit into
    density matrices as computed by Quantum Network Explorer, and vice versa.

    Parameters
    ----------
    density_matrix: A density matrix.

    Returns
    -------
    The corresponding density matrix with the bit order of the states reversed.
    """
    nr_qubits = len(density_matrix.dims())
    dm_size = nr_qubits**2
    reversed_dm = []
    for row_index in range(dm_size):
        row = []
        for column_index in range(dm_size):
            reversed_row_index = reverse_bit_order(nr_qubits, row_index)
            reversed_column_index = reverse_bit_order(nr_qubits, column_index)
            value = density_matrix.data[reversed_row_index][reversed_column_index]
            row.append(value)
        reversed_dm.append(row)
    return DensityMatrix(reversed_dm)


def density_matrix_pretty_print(density_matrix):
    """
    Pretty print a density matrix.

    Parameters
    ----------
    density_matrix: The density matrix to be printed.
    """
    nr_qubits = len(density_matrix.dims())
    for dimension in density_matrix.dims():
        assert dimension == 2, "dimension of each subsystem must be 2"
    dm_size = 2**nr_qubits
    for row in range(dm_size):
        for column in range(dm_size):
            value = density_matrix.data[row][column]
            real_value = value.real
            imaginary_value = value.imag
            print(f"{real_value:>6.3f} {imaginary_value:>6.3f}j    ", end="")
        print()


def density_matrix_print_to_file(
    file_name, producer_name, nr_qubits, density_matrix, input_value, final_swaps
):
    """
    Print a density matrix to a file. This is used to compare one density matrix with another
    density matrix.

    Parameters
    ----------
    file_name: The name of the file that the density matrix should be printed to.
    producer_name: The name of the algorithm that produced the density matrix.
    nr_qubits: The number of qubits that the density matrix describes.
    density_matrix: The density matrix to be printed.
    input_value: The input value to the algorithm that produced the density matrix.
    final_swap: Whether the QFT algorithm that produced the density matrix did final swaps.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        print(producer_name, file=file)
        print(f"{datetime.now()}", file=file)
        print(f"{nr_qubits}", file=file)
        print(f"{input_value}", file=file)
        print(f"{final_swaps}", file=file)
        for row in range(nr_qubits):
            for column in range(nr_qubits):
                print(density_matrix[row][column], file=file)
