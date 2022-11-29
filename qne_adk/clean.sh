#!/bin/bash

TOP=$(git rev-parse --show-toplevel)
cd ${TOP}
for application in $(cat applications); do
    echo "Cleaning ${application}..."
    rm -rf ${application}/${application}_experiment
done
