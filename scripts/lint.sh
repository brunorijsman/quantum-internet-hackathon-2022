#!/bin/bash

TRUE=1
FALSE=0

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
REPO_ROOT_DIR=${SCRIPT_DIR}/..

LINTED_DIRS="purely_classical"
LINTED_DIRS+=" qiskit"
LINTED_DIRS+=" qne_adk"
LINTED_DIRS+=" qne_adk/entanglement/src"
LINTED_DIRS+=" qne_adk/teleport/src"
LINTED_DIRS+=" qne_adk/just_crotz/src"
LINTED_DIRS+=" qne_adk/qft/src"
LINTED_DIRS+=" qne_adk/qft2/src"
ALL_LINTS_OK=$TRUE

for DIR in $LINTED_DIRS; do

    echo "Lint $DIR using pylint"
    pylint --rcfile $REPO_ROOT_DIR/.pylintrc $REPO_ROOT_DIR/$DIR/*.py
    if [ "$?" -ne 0 ]; then
        ALL_LINTS_OK=$FALSE
    fi

    echo "Lint $DIR using black"
    black --check $REPO_ROOT_DIR/$DIR
    if [ "$?" -ne 0 ]; then
        ALL_LINTS_OK=$FALSE
    fi

done

if [[ $ALL_LINTS_OK == $FALSE ]]; then
    echo "At least one lint failed"
    exit 1
fi

echo "All lint checks passed"
exit 0
