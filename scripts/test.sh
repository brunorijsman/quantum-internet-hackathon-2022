#!/bin/bash

TRUE=1
FALSE=0

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
REPO_ROOT_DIR=${SCRIPT_DIR}/..

TESTED_DIRS="purely_classical qiskit"
ALL_TESTS_OK=$TRUE

for DIR in $TESTED_DIRS; do

    echo "Test $DIR using pytest"
    pytest $REPO_ROOT_DIR/$DIR
    if [ "$?" -ne 0 ]; then
        ALL_TESTS_OK=$FALSE
    fi

done

if [[ $ALL_TESTS_OK == $FALSE ]]; then
    echo "At least one test failed"
    exit 1
fi

echo "All tests passed"
exit 0
