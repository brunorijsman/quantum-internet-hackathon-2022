#!/bin/bash

set -e

TOP=$(git rev-parse --show-toplevel)/qne_adk
cd ${TOP}

if [[ "$#" -eq 0 ]]; then
    applications=$(cat ${TOP}/applications)
else
    applications=""
    while [[ "$#" -gt 0 ]]; do
        applications="$applications $1"
        shift
    done
fi

if [[ ! -d ~/.qne ]]; then
    mkdir ~/.qne
fi
FIRST=1
echo "{" > ~/.qne/applications.json
for application in $applications; do
    if [[ ${FIRST} == 0 ]]; then 
        echo "  ," >> ~/.qne/applications.json
    else
        FIRST=0
    fi
    echo "  \"${application}\": {" >> ~/.qne/applications.json
    echo "    \"path\": \"${TOP}/${application}/\"" >> ~/.qne/applications.json
    echo "  }" >> ~/.qne/applications.json
done
echo "}" >> ~/.qne/applications.json

for application in $applications; do

    echo "Cleaning ${application}..."
    rm -rf ${application}/${application}_experiment

    echo "Creating ${application}_experiment..."
    cd ${TOP}/${application}
    echo qne experiment create ${application}_experiment ${application} randstad
    qne experiment create ${application}_experiment ${application} randstad > /dev/null

    for f in src/*.py; do
        f=$(basename $f)
        if [[ ! -e ${application}_experiment/input/$f ]]; then
            echo "Copy common file ${f}..."
            cp src/$f ${application}_experiment/input
        fi
    done

    echo "Running ${application}_experiment..."
    cd ${application}_experiment
    qne experiment run | gsed 's/\\n/\n/g'

    echo "Results:"
    cat results/processed.json | jq '.round_result'

    echo "Logs:"
    for log_file in ${TOP}/${application}/${application}_experiment/raw_output/LAST/*_app_log.yaml; do
        base=$(basename ${log_file})
        echo "${base}:"
        egrep -v '(HFL|HLN|WCT)' ${log_file}
    done

done
