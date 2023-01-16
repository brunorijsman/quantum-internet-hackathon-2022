"""
Check whether two different implementations of D(QFT) produce the same result (in terms of the
density matrix describing the final state).
"""

import sys


def read_density_matrix(file_name):
    """
    Read a density matrix file.

    Parameters
    ----------
    file_name: The name of the file to read.

    Returns
    -------
    A dictionary with the following keys:
    input_size: The number of input qubits for the (D)QFT
    input_value: The input value for the (D)QFT
    density_matrix: The density matrix describing the final state of the data qubits for the (D)QFT
    """
    print(f"Reading density matrix from {file_name}")
    # TODO: Determine dir_name automatically
    dir_name = "/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022"
    with open(f"{dir_name}/{file_name}", "r", encoding="utf-8") as file:
        producer = file.readline().strip()
        print(f"  Producer: {producer}")
        production_time = file.readline().strip()
        print(f"  Production time: {production_time}")
        input_size = int(file.readline().strip())
        print(f"  Input size: {input_size}")
        input_value = int(file.readline().strip())
        print(f"  Input value: {input_value}")
        density_matrix = []
        for _ in range(input_size):
            row = []
            for _ in range(input_size):
                value = complex(file.readline().strip())
                row.append(value)
            density_matrix.append(row)
        print(f"  Read {input_size}x{input_size} density matrix")
        return {
            "input_size": input_size,
            "input_value": input_value,
            "density_matrix": density_matrix,
        }


def compare_density_matrices(density_matrix_1, density_matrix_2):
    """
    Compute the difference between two density matrices.

    Parameters
    ----------
    density_matrix_1: The first density matrix to be compared.
    density_matrix_2: The second density matrix to be compared.

    Returns
    -------
    The difference matrix, which is density_matrix_1 - density_matrix_2
    """
    size = len(density_matrix_1)
    assert size == len(density_matrix_2), "The density matrices must be the same size"
    difference_matrix = []
    for row_nr in range(size):
        row = []
        for col_nr in range(size):
            difference_value = density_matrix_1[row_nr][col_nr] - density_matrix_2[row_nr][col_nr]
            row.append(difference_value)
        difference_matrix.append(row)
    return difference_matrix


def transpose_density_matrix(density_matrix):
    """
    Transpose a density matrix.

    Parameters
    ----------
    density_matrix: The density matrix to be transposed.
    """
    size = len(density_matrix)
    transposed_density_matrix = []
    for row_nr in range(size):
        row = []
        for col_nr in range(size):
            row.append(density_matrix[col_nr][row_nr])
        transposed_density_matrix.append(row)
    return transposed_density_matrix


def pretty_print_density_matrix(name, density_matrix):
    """
    Pretty print a density matrix

    Parameters
    ----------
    name: The name of the density matrix.
    density_matrix: The density matrix to be printed.
    """
    print(f"\n{name}\n")
    for row in density_matrix:
        for value in row:
            print(f"{value.real:>6.3f} {value.imag:>6.3f}j   ", end="")
        print("")


def compare_qiskit_with_qne():
    """
    Compare the result of a qiskit (D)QFT run to the result of a QNE-ADK (D)QFT run.
    """

    qiskit = read_density_matrix("qiskit_dm.txt")
    qne = read_density_matrix("qne_dm.txt")

    if qiskit["input_size"] != qne["input_size"]:
        print("ERROR: Inconsistent input size")
        sys.exit(1)

    if qiskit["input_value"] != qne["input_value"]:
        print("WARNING: Inconsistent input value")

    qiskit_density_matrix = qiskit["density_matrix"]
    transposed_qiskit_dm = transpose_density_matrix(qiskit_density_matrix)

    qne_density_matrix = qne["density_matrix"]

    pretty_print_density_matrix("Qiskit Density Matrix", qiskit_density_matrix)

    pretty_print_density_matrix("QNE Density Matrix", qne_density_matrix)

    difference_matrix = compare_density_matrices(qiskit_density_matrix, qne_density_matrix)
    pretty_print_density_matrix("Difference Density Matrix: Qiskit vs QNE", difference_matrix)

    difference_matrix = compare_density_matrices(transposed_qiskit_dm, qne_density_matrix)
    pretty_print_density_matrix(
        "Difference Density Matrix: transposed Qiskit vs QNE", difference_matrix
    )


if __name__ == "__main__":
    compare_qiskit_with_qne()
