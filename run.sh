#!/bin/bash

set -e

TOP=$(git rev-parse --show-toplevel)
cd ${TOP}

./clean.sh

if [[ ! -d ~/.qne ]]; then
    mkdir ~/.qne
fi
FIRST=1
echo "{" > ~/.qne/applications.json
for application in $(cat applications); do
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

for application in $(cat applications); do
    echo "Running ${application}..."
    cd ${TOP}/${application}
    qne experiment create ${application}_experiment ${application} randstad > /dev/null
    cd ${application}_experiment
    qne experiment run | gsed 's/\\n/\n/g'
    cat results/processed.json | jq '.round_result'
done
