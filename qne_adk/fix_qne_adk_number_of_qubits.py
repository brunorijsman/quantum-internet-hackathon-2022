#!/usr/bin/env python3
"""
Increase the number of qubits per node in QNE-ADK from 3 to 32.
"""

import argparse
import json
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


def parse_command_line_arguments():
    """
    Parse the command line arguments.

    Returns
    -------
    The parsed arguments in the form of a dictionary.
    """
    parser = argparse.ArgumentParser(
        description="Increase the number of qubits per node in " "QNE-ADK from 3 to 32."
    )
    parser.add_argument("venv_dir", help="Python virtual environment directory")
    args = parser.parse_args()
    return args


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


def set_number_of_qubits_per_node(data, new_number_of_qubits):
    """
    Set the the number of qubits per node to a new value.

    Parameters
    ----------
    data: The data in the QNE-ADK nodes.json file.
    new_number_of_qubits: The new number of qubits per node.
    """
    nodes = data["nodes"]
    for node in nodes:
        node["number_of_qubits"] = new_number_of_qubits


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


def main():
    """
    The main function.
    """
    args = parse_command_line_arguments()
    nodes_file = f"{args.venv_dir}/lib/python3.8/site-packages/adk/networks/nodes.json"
    data = read_json_file(nodes_file, "nodes file")
    set_number_of_qubits_per_node(data, 32)
    write_json_file(data, nodes_file, "nodes file")


if __name__ == "__main__":
    main()
