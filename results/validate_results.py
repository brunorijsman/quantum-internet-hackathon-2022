#!/usr/bin/env python3
"""
Validate whether the result files are consistent with each other.
"""

import argparse
import math
import os
import common


def parse_command_line_arguments():
    """
    Parse the command line arguments.

    Returns
    -------
    The parsed arguments in the form of a dictionary.
    """
    parser = argparse.ArgumentParser(description="Validate the results")
    parser.add_argument("results_dir", help="Results directory")
    args = parser.parse_args()
    return args


def read_all_experiment_results(results_dir):
    """
    Read the results for all experiments.

    Parameters
    ----------
    results_dir: The directory that contains the result files.
    """
    all_experiment_results = []
    for file_name in os.listdir(results_dir):
        if file_name.endswith(".json"):
            data = common.read_json_file(file_name, "experiment results")
            experiment_results = {"file_name": file_name, "data": data}
            all_experiment_results.append(experiment_results)
    return all_experiment_results


def validate_all_experiment_results(all_experiment_results):
    """
    Validate all experiment results.

    Parameters
    ----------
    all_experiment_results: The results of all experiments.

    Returns
    -------
    True if all experiment results are consistent with each other, False if not.
    """
    all_consistent = True
    for experiment_results in all_experiment_results:
        consistent = validate_one_experiment_results(experiment_results, all_experiment_results)
        all_consistent = all_consistent and consistent
    return all_consistent


def validate_one_experiment_results(experiment_results, all_experiment_results):
    """
    Validate one experiment results against the other experiment results for consistency.

    Parameters
    ----------
    experiment_results: The results of the experiment that is to be compared against all other
        experiment results.
    all_experiment_results: The results of all experiments to compare against.

    Returns
    -------
    True if all experiment results are consistent with each other, False if not.
    """
    file_name = experiment_results["file_name"]
    data = experiment_results["data"]
    # DEBUG
    if data["input_size"] != 3:
        return True
    if data["input_value"] != 7:
        return True
    if data["platform"] != "qiskit":
        return True
    # END DEBUG
    print(f"Validate {file_name}")
    all_consistent = True
    for other_experiment_results in all_experiment_results:
        other_file_name = other_experiment_results["file_name"]
        other_data = other_experiment_results["data"]
        if file_name == other_file_name:
            continue
        if data["flavor"] != other_data["flavor"]:
            continue
        if data["input_size"] != other_data["input_size"]:
            continue
        if data["input_value"] != other_data["input_value"]:
            continue
        consistent = check_consistency(experiment_results, other_experiment_results)
        if consistent:
            print(f"  Compare with {other_file_name}: consistent")
        else:
            print(f"  Compare with {other_file_name}: NOT consistent")
        all_consistent = all_consistent and consistent
    return all_consistent


def check_consistency(experiment_results_1, experiment_results_2):
    """
    Check whether two experiment results are consistent with each other, i.e. whether they
    produced the same output density matrix.

    Parameters
    ----------
    experiment_results_1: The first experiment results to be compared.
    experiment_results_2: The second experiment results to be compared.

    Returns
    -------
    True if the results are consistent with each other, False if not
    """
    max_delta = 0.001
    data_1 = experiment_results_1["data"]
    data_2 = experiment_results_2["data"]
    density_matrix_1 = data_1["density_matrix"]
    density_matrix_2 = data_2["density_matrix"]
    # if data_1["platform"] != data_2["platform"]:
    #     density_matrix_2 = density_matrix_reversed_bit_order(density_matrix_2)
    # DEBUG
    print("Density matrix 1:")
    pretty_print_density_matrix(density_matrix_1)
    print("Density matrix 2:")
    pretty_print_density_matrix(density_matrix_2)
    # END DEBUG
    assert len(density_matrix_1) == len(density_matrix_2)
    for row_1, row_2 in zip(density_matrix_1, density_matrix_2):
        assert len(row_1) == len(row_2)
        for value_1, value_2 in zip(row_1, row_2):
            if abs(value_1["real"] - value_2["real"]) > max_delta:
                return False
            if abs(value_1["imag"] - value_2["imag"]) > max_delta:
                return False
    return True


def density_matrix_reversed_bit_order(density_matrix):
    """
    Produce a new density matrix by reversing the bit order of the indexes.

    Parameters
    ----------
    density_matrix: The original density matrix.

    Returns
    -------
    The new density matrix, with the bit order of the indexes reversed.
    """
    size = len(density_matrix)
    nr_bits = round(math.log2(size))
    assert 2 ** nr_bits == size
    new_density_matrix = []
    for row_index in range(size):
        new_row = []
        for col_index in range(size):
            reversed_row_index = reverse_bit_order(nr_bits, row_index)
            reversed_col_index = reverse_bit_order(nr_bits, col_index)
            value = density_matrix[reversed_row_index][reversed_col_index]
            new_row.append(value)
        new_density_matrix.append(new_row)
    return new_density_matrix


def reverse_bit_order(nr_bits, value):
    """
    Reverse the bit order.

    Parameters
    ----------
    nr_bits: The number of bits in the value to be reversed.
    value: The value to be reversed.

    Returns
    -------
    The value with the bit order reversed.
    """
    reversed_value = 0
    for _ in range(nr_bits):
        bit = value & 1
        reversed_value <<= 1
        reversed_value |= bit
        value >>= 1
    return reversed_value


def pretty_print_density_matrix(density_matrix):
    """
    Pretty print a density matrix

    Parameters
    ----------
    density_matrix: The density matrix to be printed.
    """
    for row in density_matrix:
        line = ""
        for value in row:
            real_value = value["real"]
            imaginary_value = value["imag"]
            if real_value < 0.0:
                imaginary_sign = "-"
                real_value = -real_value
            else:
                real_sign = " "
            if imaginary_value < 0.0:
                imaginary_sign = "-"
                imaginary_value = -imaginary_value
            else:
                imaginary_sign = "+"
            line += f"{real_sign}{real_value:>5.3f} {imaginary_sign} {imaginary_value:<5.3f}i    "
        print(line)


def main():
    """
    The main function.
    """
    args = parse_command_line_arguments()
    all_experiment_results = read_all_experiment_results(args.results_dir)
    all_consistent = validate_all_experiment_results(all_experiment_results)
    if all_consistent:
        print("All experimental results are consistent with each other")
    else:
        print("There is at least one inconsistency in the experimental results")


if __name__ == "__main__":
    main()
