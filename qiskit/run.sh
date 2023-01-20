#!/bin/bash

./run_experiment.py monolithic 2 0 ../results
./run_experiment.py monolithic 2 1 ../results
./run_experiment.py monolithic 2 2 ../results
./run_experiment.py monolithic 2 3 ../results
./run_experiment.py monolithic 3 0 ../results
./run_experiment.py monolithic 3 4 ../results
./run_experiment.py monolithic 3 7 ../results
./run_experiment.py monolithic 4 0 ../results
./run_experiment.py monolithic 4 7 ../results
./run_experiment.py monolithic 4 15 ../results

./run_experiment.py distributed 2 0 ../results
./run_experiment.py distributed 2 1 ../results
./run_experiment.py distributed 2 2 ../results
./run_experiment.py distributed 2 3 ../results
./run_experiment.py distributed 4 0 ../results
./run_experiment.py distributed 4 7 ../results
./run_experiment.py distributed 4 15 ../results
