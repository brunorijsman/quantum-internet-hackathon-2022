#!/usr/bin/env python3
"""
Set the application input values for an experiment.
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
    parser = argparse.ArgumentParser(description="Set application input values for experiment")
    parser.add_argument("experiment", help="Experiment JSON file")
    parser.add_argument("application_meta_data", help="Application meta data JSON file")
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


def validate_experiment(experiment):
    """
    Basic checks to verify that the experiment has the expected structure.

    Parameters
    ----------
    experiment: The experiment to be validated.
    """
    if not isinstance(experiment, dict):
        fatal_error("Experiment must be a dictionary")
    if "meta" not in experiment:
        fatal_error("Experiment must have 'meta' key")
    if "asset" not in experiment:
        fatal_error("Experiment must have 'asset' key")
    if "network" not in experiment["asset"]:
        fatal_error("Experiment[asset] must have 'network' key")
    if "application" not in experiment["asset"]:
        fatal_error("Experiment[asset] must have 'application' key")
    if not isinstance(experiment["asset"]["application"], list):
        fatal_error("Experiment[asset][application] must have be a list")


def validate_application_meta_data(application_meta_data):
    """
    Basic checks to verify that the application meta data has the expected structure.

    Parameters
    ----------
    application_meta_data: The application meta data to be validated.
    """
    if not isinstance(application_meta_data, list):
        fatal_error("Application meta data must be a list")
    for node_meta_data in application_meta_data:
        if not isinstance(node_meta_data, dict):
            fatal_error("Node meta data must be a dict")
        if "roles" not in node_meta_data:
            fatal_error("Node meta data must have 'roles' key")
        if "values" not in node_meta_data:
            fatal_error("Node meta data must have 'value' key")
        for value in node_meta_data["values"]:
            if "name" not in value:
                fatal_error("Value must have 'name' key")
            if "value" not in value:
                fatal_error("Value must have 'value' key")


def replace_application_meta_data(experiment, new_application_meta_data):
    """
    Replace the application meta data in an experiment.

    Parameters
    ----------
    experiment: The experiment whose application meta data needs to be replaced.
    new_application_meta_data: The new application meta data to inject into the experiment.
    """
    experiment["asset"]["application"] = new_application_meta_data


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
            data = json.dump(data, file, indent=2)
    except (OSError, IOError) as exception:
        fatal_error(f"Could not open {description} file {file_name}: {exception}")


def main():
    """
    The main function.
    """
    args = parse_command_line_arguments()
    experiment = read_json_file(args.experiment, "experiment")
    application_meta_data = read_json_file(args.application_meta_data, "application meta data")
    validate_experiment(experiment)
    validate_application_meta_data(application_meta_data)
    replace_application_meta_data(experiment, application_meta_data)
    write_json_file(experiment, args.experiment, "experiment")


if __name__ == "__main__":
    main()
