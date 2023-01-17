"""
Common functions shared by all QNE-ADK applications.
"""

from datetime import datetime


def write_density_matrix_to_log(app_logger, density_matrix):
    """
    Pretty print a density matrix to the application log.

    Parameters
    ----------
    app_logger: The application logger.
    density_matrix: The density matrix to pretty print.
    """
    for row in density_matrix:
        log_msg = ""
        for value in row:
            real_value = value.real
            imaginary_value = value.imag
            if imaginary_value < 0.0:
                sign = "-"
                imaginary_value = -imaginary_value
            else:
                sign = "+"
            log_msg += f"{real_value:>5.3f} {sign} {imaginary_value:<5.3f}i    "
        log_msg = log_msg.strip()
        app_logger.log(log_msg)


def write_density_matrix_to_file(app_logger, density_matrix, input_size, input_value):
    """
    Write the density matrix for the qubits to a file, including some metadata.

    Parameters
    ----------
    app_logger: The application logger.
    density_matrix: The density matrix to write to a file.
    input_size: The number of qubits in the input value for the QFT.
    input_value: The input value for the QFT.
    """
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
