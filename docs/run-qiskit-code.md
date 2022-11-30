# Viewing and running the team Q-Harmonics Qiskit related code

## What is Qiskit?

[Qiskit](https://qiskit.org/) is an open-source software development kit (SDK) for working with
quantum computers at the level of pulses, circuits, and application modules.

One of the components in Qiskit is [Aer](https://github.com/Qiskit/qiskit-aer), which provides
high-performance quantum computing simulators with realistic noise models.

## What do we use Qiskit for?

In this project we use the Qiskit SDK to develop three different implementations of the quantum
Fourier transformation:

 1. A monolithic (non-distributed) version of the quantum Fourier transformation.
    We use this as a reference to check whether the results of the distributed versions (see below)
    are correct.

 2. A distributed version of the quantum Fourier transformation based on teleportation.

 3. A distributed version of the quantum Fourier transformation based on cat states.

## Installation instructions

Follow 
[these installation instructions](installation.md)
to install team Q-Harmonics Qiskit related code, Qiskit itself, and other dependencies.

## Directory structure

All Qiskit related code is stored in the [`qiskit`](../qiskit/) subdirectory.

As shown in the following table, we have three Qiskit implementations of the quantum Fourier
transformation:

| Implementation | Python files | Jupyter notebook files |
|---|---|---|
| Non-distributed (local) QFT | `qft.py` | `qft.ipynb` |
| Distributed QFT using teleportation | `teleport_dqft.py` | `teleport_dqft.ipynb` |
| Distributed QFT using cat states | **TODO** `cat_dqft.py` | **TODO** `cat_dqft.ipynb` |
| Base classes for both DQFT implementations | `multi_processor.py` | `multi_processor.ipynb` |

In each case, the implementation takes the form of a Python module containing classes that generate
the quantum circuit to compute the quantum Fourier transform, and a corresponding Jupyter notebook
to execute the circuit and visualize the results.

The [`qiskit`](../qiskit/) subdirectory also contains some files that were implemented to
gain a better understanding of the the quantum Fourier transformation and its applications
using Qiskit:

 *  File `find_period.ipynb` contains a Jupyter notebook demonstrating how to use the quantum
    Fourier transformation to find the period of function (this is a key step in Shor's factoring
    algorithm).

 * File `just_crotz.ipynb` contains a Jupyter notebook that applies the controlled Z-rotation
   (CROTZ) gate on a well-defined input state and shows the resulting density matrix in several
   representations. The purpose of this file is to validate whether our implementation of CROTZ
   in QNE-ADK is correct (see **TODO** add reference).

(See also the
[run purely classical code](run-purely-classical.md)
chapter for some additional purely classical algorithms that help understand the QFT and it's
applications.)



We have also started implementing Python code to view, analyze, and compare density matrices
for the output states that are produced by the Qiskit QFT implementations.
To goal is to use these density matrices to verify that the Qiskit and QNE-ADK implementations
actually produce the same results.
The related code is in files `density_matrices.ipynb` and `utils.py`.
**TODO** This is still a work in progress.


## Modeling multiple quantum processors in Qiskit

In the Qiskit implementation, we still have one single quantum circuit that simulates all quantum
processors. This single large circuit is composed of several quantum registers, where each quantum
register is understood to be owned by a specific quantum processor. Each processor has a _main_
register which represents the local working memory as well as two extra registers
(_entanglement_ and _teleport_) that are used for communications with other quantum processors.


