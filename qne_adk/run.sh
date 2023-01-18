#!/bin/bash

NORMAL=$(tput sgr0)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
MAGENTA=$(tput setaf 5)
BEEP=$(tput bel)

FALSE=0
TRUE=1

TOP=""
SKIP_CREATE_EXPERIMENTS=${FALSE}
APPLICATIONS=""

fatal_error ()
{
    local message="$1"

    echo "${RED}Error:${NORMAL} ${message}" >&2
    exit 1
}

progress ()
{
    local message="$1"

    echo "${NORMAL}${message}"
}

function run_command ()
{
    local command="$1"
    local failure_msg="$2"

    output=$(${command} 2>&1)
    if [ $? -ne 0 ] ; then
        echo "${RED}Error:${NORMAL} $failure_msg:"
        echo "The following command failed:"
        echo "${MAGENTA}${command}${NORMAL}"
        echo "The output of the command was:"
        echo "${MAGENTA}${output}${NORMAL}"
        exit 1
    fi
}

determine_top_directory ()
{
    run_command "git --version" "Git is not installed"
    TOP=$(git rev-parse --show-toplevel)/qne_adk
    progress "Directory containing QNE-ADK applications is ${TOP}"
}

help ()
{
    echo
    echo "SYNOPSIS"
    echo
    echo "    run.sh [OPTION]... [APPLICATION]..."
    echo
    echo "OPTIONS"
    echo
    echo "    -?, -h, --help"
    echo "      Print this help and exit"
    echo
    echo "    -s, --skip-create-experiments"
    echo "      Skip the create expirement steps. Just run the experiments that were"
    echo "      already created in a previous run."
    echo
    echo "APPLICATIONS"
    echo
    echo "    List of directory names, each containing an QNE-ADK application to run."
    echo
    exit 0
}

parse_command_line_options ()
{
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -\?|-h|--help)
                help
                ;;
            -s|--skip-create-experiments)
                SKIP_CREATE_EXPERIMENTS=${TRUE}
                ;;
            *)
                APPLICATIONS="${APPLICATIONS} $1"
                ;;
        esac
        shift
    done
}

run_all_applications ()
{
    create_fresh_dot_qne_directory
    for application in ${APPLICATIONS}; do
        run_one_application ${application}
    done
}

create_fresh_dot_qne_directory ()
{
    progress "Creating fresh .qne directory in home directory..."
    if [[ ! -d ~/.qne ]]; then
        run_command "mkdir ~/.qne"
    fi
    first=$TRUE
    echo "{" > ~/.qne/applications.json
    for application in $APPLICATIONS; do
        if [[ ${first} == $FALSE ]]; then 
            echo "  ," >> ~/.qne/applications.json
        else
            first=$FALSE
        fi
        echo "  \"${application}\": {" >> ~/.qne/applications.json
        echo "    \"path\": \"${TOP}/${application}/\"" >> ~/.qne/applications.json
        echo "  }" >> ~/.qne/applications.json
    done
    echo "}" >> ~/.qne/applications.json
}

run_one_application ()
{
    local application="$1"

    check_application_exists $application
    if [[ $SKIP_CREATE_EXPERIMENTS == $FALSE ]]; then
        create_fresh_experiment_directory $application
    fi
    run_all_experiments_for_application $application
}

check_application_exists ()
{
    local application="$1"

    if [[ ! -d $TOP/$application ]]; then
        fatal_error "Application directory $application not found"
    fi
}

create_fresh_experiment_directory ()
{
    local application="$1"

    progress "Creating fresh ${application}_experiment directory..."
    cd ${TOP}/${application}
    run_command "rm -rf ${application}_experiment"
    run_command "qne experiment create ${application}_experiment ${application} randstad"
    
    for f in src/*.py; do
        f=$(basename $f)
        if [[ ! -e ${application}_experiment/input/$f ]]; then
            progress "Copying source file ${f}..."
            run_command "cp src/$f ${application}_experiment/input"
        fi
    done
}

#@@@
run_all_experiments_for_application ()
{
    local application="$1"

    if [[ -d ${TOP}/${application}/experiment_values ]]; then
        for values_file in ${TOP}/${application}/experiment_values/*; do
            run_one_experiment_for_application "$application" "$values_file"
        done
    else
        run_one_experiment_for_application "$application" ""
    fi
}

run_one_experiment_for_application ()
{
    local application="$1"
    local values_file="$2"

}

run_one_experiment_for_application ()
{
    local application="$1"
    local values_file="$2"

    cd ${TOP}/${application}/${application}_experiment

    if [[ -z "$values_file" ]]; then
        progress "Running ${application}_experiment using default values..."
    else
        value_file_base_name=$(basename ${values_file})
        progress "Running ${application}_experiment using values file ${value_file_base_name}..."
        ${TOP}/set_experiment_values.py experiment.json "$values_file"
    fi

    output=$(qne experiment run)
    if [[ "$output" == Error* ]]; then
        echo "${RED}Error${NORMAL} while running the script"
        echo "${MAGENTA}${output}${MAGENTA}" | gsed 's/\\n/\n/g'
    fi

    show_results $application
    show_logs $application
}

show_results ()
{
    local application="$1"

    progress "Results:"
    cd ${TOP}/${application}/${application}_experiment
    cat results/processed.json | jq '.round_result'
}

show_logs ()
{
    local application="$1"

    progress "Logs:"
    for log_file in ${TOP}/${application}/${application}_experiment/raw_output/LAST/*_app_log.yaml; do
        base=$(basename ${log_file})
        echo "${base}:"
        egrep -v '(HFL|HLN|WCT)' ${log_file}
    done
}

parse_command_line_options "$@"
determine_top_directory
if [ -z "${APPLICATIONS}" ]; then
    APPLICATIONS=$(cat ${TOP}/applications)
fi
run_all_applications
