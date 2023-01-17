"""
Common functions shared by all QNE-ADK applications.
"""

from datetime import datetime
from netqasm.sdk.external import get_qubit_state


def write_density_matrix_to_file(app_logger, qubits, input_size, input_value):
    """
    Write the density matrix for the qubits to a file, including some metadata.

    Parameters
    ----------
    app_logger: The application logger.
    qubits: A map of Qubit objects, indexed by qubit index number, for which to write the density
        matrix.
    input_size: The number of qubits in the input value for the QFT.
    input_value: Assume that all input values for qubits are |0> or |1>, treat these qubits
        as the binary encoding of the input value as a number.
    """
    density_matrix = get_qubit_state(qubits[0], reduced_dm=False)
    app_logger.log(f"density matrix is {density_matrix}")
    app_logger.log("writing density matrix to qne_dm.txt")
    # TODO: Determine dir in a better way
    dir_name = "/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022"
    with open(f"{dir_name}/qne_dm.txt", "w", encoding="utf-8") as file:
        print("QNE-ADM density matrix", file=file)
        print(f"{datetime.now()}", file=file)
        print(f"{input_size}", file=file)
        print(f"{input_value}", file=file)
        for row_index in range(input_size):
            for column_index in range(input_size):
                print(density_matrix[row_index][column_index], file=file)
