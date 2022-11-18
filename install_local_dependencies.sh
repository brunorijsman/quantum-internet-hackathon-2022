#!/bin/bash

echo "Installing squidasm dependencies from local forked repo..."
cd ~/git-personal/squidasm
pip install .

echo "Installing netqasm dependencies from local forked repo..."
cd ~/git-personal/netqasm
pip install .

cd ~/git-personal/quantum-internet-hackathon-2022
