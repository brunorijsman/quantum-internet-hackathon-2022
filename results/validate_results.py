#!/usr/bin/env python3
"""
Validate whether the result files are consistent with each other.
"""

import argparse
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
    """
    for experiment_results in all_experiment_results:
        validate_one_experiment_results(experiment_results, all_experiment_results)


def validate_one_experiment_results(experiment_results, all_experiment_results):
    """
    Validate one experiment results against the other experiment results for consistency.
    """
    file_name = experiment_results["file_name"]
    data = experiment_results["data"]
    print(f"Validate {file_name}")
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
        print(f"  Compare with {other_file_name}")



def main():
    """
    The main function.
    """
    args = parse_command_line_arguments()
    all_experiment_results = read_all_experiment_results(args.results_dir)
    validate_all_experiment_results(all_experiment_results)


if __name__ == "__main__":
    main()
