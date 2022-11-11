#!/bin/bash

set -e

cd ~/git-personal/quantum-internet-hackathon-2022
rm -rf teleport_experiment
qne experiment create teleport_experiment teleport randstad
cd teleport_experiment
qne experiment run | gsed 's/\\n/\n/g'
cat results/processed.json | jq '.round_result'
