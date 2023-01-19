"""
Common functions shared by all platforms (Qiskit, QNE-ADK, ...)
"""

import datetime
import json
import os
import sys


def fatal_error(message):
    """
    Print a fatal error message and exit the program.

    Parameters
    ----------
    message: The fatal error message
    """
    print(message, file=sys.stderr)
    sys.exit(1)


def read_json_file(file_name, description):
    """
    Read data from a JSON file.

    Parameters
    ----------
    file_name: The file name of the experiment JSON file.
    description: A human-readable description of what is in the JSON file.

    Returns
    -------
    A data structure containing the deserialized JSON file.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, IOError) as exception:
        fatal_error(f"Could not open {description} file {file_name}: {exception}")
    return data


def write_json_file(data, file_name, description):
    """
    Write data to a JSON file.

    Parameters
    ----------
    data: The data to be written to the JSON file.
    file_name: The file name of the experiment JSON file.
    description: A human-readable description of what is in the JSON file.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    except (OSError, IOError) as exception:
        fatal_error(f"Could not open {description} file {file_name}: {exception}")


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


def write_density_matrix_to_file(
    platform, flavor, input_size, input_value, density_matrix, results_dir=None
):
    """
    Write the density matrix for the qubits to a file, including some metadata.

    Parameters
    ----------
    platform: The platform on which the experiment was run (qiskit or qne)
    flavor: The flavor of quantum fourier transformation (distributed or monolithic)
    input_size: The number of qubits in the input value for the QFT.
    input_value: The input value for the QFT.
    density_matrix: The density matrix to write to a file.
    results_dir: The results directory.

    Returns
    -------
    The name of the file the density matrix was written to
    """
    assert platform in ["qiskit", "qne"]
    assert flavor in ["distributed", "monolithic"]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    serializable_matrix = []
    for row in density_matrix:
        serializable_matrix_row = []
        for value in row:
            serializable_value = {"real": value.real, "imag": value.imag}
            serializable_matrix_row.append(serializable_value)
        serializable_matrix.append(serializable_matrix_row)
    file_name = f"dm_{platform}_{flavor}_size_{input_size}_value_{input_value}.json"
    if results_dir is not None:
        dir_name = results_dir
    else:
        dir_name = os.getenv("QIH_RESULTS_DIR")
    if dir_name:
        file_name = f"{dir_name}/{file_name}"
    data = {
        "platform": platform,
        "flavor": flavor,
        "datetime": now,
        "input_size": input_size,
        "input_value": input_value,
        "density_matrix": serializable_matrix,
    }
    write_json_file(data, file_name, "density_matrix")
    return file_name
