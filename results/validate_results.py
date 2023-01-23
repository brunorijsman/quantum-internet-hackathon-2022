#!/usr/bin/env python3
"""
Validate whether the result files are consistent with each other.

QNE-ADK use different numbering of qubits than Qiskit to create the density matrices. At first I
thought it was just a matter of little endian vs big endian, which would imply that reversing the
qubit order would be sufficient. This turned out not to be the case. I could not really discover the
logic in the difference in bit ordering. So, whenever I compare a QNE-ADK density matrix to a Qiskit
density matrix, I try all possible permutations of qubit indexing. If I find a match for any
permutation, I declare the density matrixes to be the same (and show the permutation that led to a
match - perhaps I can discover some pattern after all.)
"""

import argparse
import itertools
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
    print(f"Validate {file_name}")
    at_least_one_comparison = False
    all_consistent = True
    for other_experiment_results in all_experiment_results:
        other_file_name = other_experiment_results["file_name"]
        other_data = other_experiment_results["data"]
        if file_name == other_file_name:
            continue
        if data["input_size"] != other_data["input_size"]:
            continue
        if data["input_value"] != other_data["input_value"]:
            continue
        result = check_consistency(experiment_results, other_experiment_results)
        if result is True:
            print(f"  Compare with {other_file_name}: consistent")
            consistent = True
        elif result is False:
            print(f"  Compare with {other_file_name}: NOT consistent")
            consistent = False
        else:
            print(f"  Compare with {other_file_name}: consistent, using permutation {result}")
            consistent = True
        at_least_one_comparison = True
        all_consistent = all_consistent and consistent
    if not at_least_one_comparison:
        print("  Nothing to compare with")
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
    False if the results are not consistent with each other.
    True if the results are consistent without any permutation needed.
    The permutation for the density matrix in experiment_results_2 which makes the results
        consistent.
    """
    data_1 = experiment_results_1["data"]
    data_2 = experiment_results_2["data"]
    density_matrix_1 = data_1["density_matrix"]
    density_matrix_2 = data_2["density_matrix"]
    if data_1["platform"] == data_2["platform"]:
        return compare_density_matrices(density_matrix_1, density_matrix_2)
    size = len(density_matrix_1)
    nr_bits = number_of_bits(size)
    bit_indexes = range(nr_bits)
    for permutation in itertools.permutations(bit_indexes):
        permuted_density_matrix_2 = density_matrix_permuted_bit_order(density_matrix_2, permutation)
        consistent = compare_density_matrices(density_matrix_1, permuted_density_matrix_2)
        if consistent:
            return permutation
    return False


def compare_density_matrices(density_matrix_1, density_matrix_2):
    """
    Compare two density matrices for equality.

    Parameters
    ----------
    density_matrix_1: The first density matrix to be compared.
    density_matrix_2: The second density matrix to be compared.

    Returns
    -------
    True if the density matrices are the same. False if they are different.
    """
    max_delta = 0.001
    assert len(density_matrix_1) == len(density_matrix_2)
    for row_1, row_2 in zip(density_matrix_1, density_matrix_2):
        assert len(row_1) == len(row_2)
        for value_1, value_2 in zip(row_1, row_2):
            if abs(value_1["real"] - value_2["real"]) > max_delta:
                return False
            if abs(value_1["imag"] - value_2["imag"]) > max_delta:
                return False
    return True


def number_of_bits(number):
    """
    Determine the number of bits in a number, which must be a power of two.

    Parameters
    ---------
    number: An integer which must be a power of two.

    Returns
    -------
    The number of bits in the number.
    """
    nr_bits = round(math.log2(number))
    assert 2**nr_bits == number
    return nr_bits


def density_matrix_permuted_bit_order(density_matrix, permutation):
    """
    Produce a new density matrix by permuting the bit order of the indexes.

    Parameters
    ----------
    density_matrix: The original density matrix.
    permutation: The permutation.

    Returns
    -------
    The new density matrix, with the bit order of the indexes permuted.
    """
    size = len(density_matrix)
    new_density_matrix = []
    for row_index in range(size):
        new_row = []
        for col_index in range(size):
            reversed_row_index = permute_bit_order(row_index, permutation)
            reversed_col_index = permute_bit_order(col_index, permutation)
            value = density_matrix[reversed_row_index][reversed_col_index]
            new_row.append(value)
        new_density_matrix.append(new_row)
    return new_density_matrix


def permute_bit_order(number, permutation):
    """
    Permute the bit order in a given number.

    Parameters
    ----------
    number: The number whose bits need to be permuted.
    permutation: The permutation.

    Returns
    -------
    The number with the bit order permuted.
    """
    new_number = 0
    nr_bits = len(permutation)
    for old_bit_index in range(nr_bits):
        bit_value = number & 1
        number >>= 1
        if bit_value:
            new_bit_index = permutation[old_bit_index]
            bit_mask = 1 << new_bit_index
            new_number |= bit_mask
    return new_number


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
