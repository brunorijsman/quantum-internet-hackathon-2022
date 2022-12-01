#!/bin/bash

TOP=$(git rev-parse --show-toplevel)/qne_adk
cd ${TOP}
for application in $(cat applications); do
    echo "Cleaning ${application}..."
    rm -rf ${application}/${application}_experiment
done
