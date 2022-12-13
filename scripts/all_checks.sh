#!/bin/bash

# set -e

TRUE=1
FALSE=0

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")

COMMIT_OK=$TRUE

echo "Perform lint checks"
$SCRIPT_DIR/lint.sh
if [ "$?" -ne 0 ]; then
    COMMIT_OK=$FALSE
fi

if [[ $COMMIT_OK == $FALSE ]]; then
    echo "Not OK to commit"
    exit 1
fi

echo "OK to commit"
exit 0