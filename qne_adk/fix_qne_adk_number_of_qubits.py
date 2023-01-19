#!/usr/bin/env python3
"""
Increase the number of qubits per node in QNE-ADK from 3 to 32.
"""

import argparse
from common import read_json_file, write_json_file


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
