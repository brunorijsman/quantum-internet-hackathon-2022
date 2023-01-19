#!/usr/bin/env python3
"""
Run a QFT experiment using Qiskit and write the results to a file for verification.
"""

import argparse
import common
import qft


def parse_command_line_arguments():
    """
    Parse the command line arguments.

    Returns
    -------
    The parsed arguments in the form of a dictionary.
    """
    parser = argparse.ArgumentParser(description="Run a QFT experiment using Qiskit")
    parser.add_argument("flavor", help="Flavor", choices=["monolithic", "distributed"])
    parser.add_argument("input_size", type=int, help="Number of input qubits")
    parser.add_argument("input_value", type=int, help="Input value, as a number")
    parser.add_argument("results_dir", help="Results directory")
    args = parser.parse_args()
    return args


def run_experiment(flavor, input_size, input_value, results_dir):
    """
    Run an experiment.
    """
    if flavor == "monolithic":
        algorithm = qft.QFT(input_size)
    elif flavor == "distributed":
        algorithm = qft.DistributedQFT(input_size)
    else:
        assert False, "Unknown flavor"
    print(f"Running {flavor} QFT, input_size {input_size}, input_value {input_value}")
    algorithm.run(input_value)
    density_matrix = algorithm.main_density_matrix().data
    file_name = common.write_density_matrix_to_file(
        "qiskit", flavor, input_size, input_value, density_matrix, results_dir
    )
    print(f"Wrote density_matrix to {file_name}")


def main():
    """
    The main function.
    """
    args = parse_command_line_arguments()
    run_experiment(args.flavor, args.input_size, args.input_value, args.results_dir)


if __name__ == "__main__":
    main()
