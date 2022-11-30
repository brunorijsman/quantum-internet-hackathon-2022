# Viewing and running the team Q-Harmonics Qiskit related code

## What is Qiskit?

[Qiskit](https://qiskit.org/) is an open-source software development kit (SDK) for working with
quantum computers at the level of pulses, circuits, and application modules.
One of the components in Qiskit is [Aer](https://github.com/Qiskit/qiskit-aer), which provides
high-performance quantum computing simulators with realistic noise models.

## What do we use Qiskit for?

In this project we use the Qiskit SDK and Aer to develop three different implementations of the
quantum Fourier transformation:

 1. A non-distributed (local) version of the quantum Fourier transformation.
    We use this as a reference to check whether the results of the two distributed versions
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
| `Processor` and `Cluster` base classes for both DQFT implementations | `cluster.py` | `cluster.ipynb` |
| Distributed QFT using teleportation | `teleport_dqft.py` | `teleport_dqft.ipynb` |
| Distributed QFT using cat states | **TODO** `cat_dqft.py` | **TODO** `cat_dqft.ipynb` |

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

## The non-distributed (local) implementation of the quantum Fourier transformation

The file 
[`qft.py`](../qiskit/qft.py)
defines the class `QFT` which is our implementation of the non-distributed
(local) quantum Fourier transformation.

The `QFT` class uses the Qiskit SDK to generate the quantum circuit for the quantum Fourier
transformation and to run the generated circuit in the Qiskit Aer simulator.

The implementation of the `QFT` class is based on the example code in
[chapter 3.5: Quantum Fourier Transform](https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html)
in the
[Qiskit Textbook](https://qiskit.org/textbook/).
The main difference is that we have used a Python class instead of free-standing Python functions
to implement the functionality. This is a pattern that we also follow for the distributed
implementations.

When a `QFT` object is instantiated, the Qiskit circuit for computing the quantum Fourier
transformation is generated.
The constructor of the `QFT` class takes two arguments:

 * `n` (integer): The size of the quantum Fourier transformation, i.e. the number of input qubits,
    which is equal to the number of output qubits.

 * `swaps` (boolean, default value False): Whether or not to perform the swap gate operations at the
   end of the quantum Fourier transformation. 
   If swaps is True, we perform the swaps; if swaps is False (which is the default) we skip the
   swaps.
   It is customary to skip these final swap gates, because the same effect can be achieved by
   renumbering the qubits at the end of the algorithm.
   Also, QNE-ADK does not yet support the swap gates, we want to skip the final swap gates if we
   want to compare the Qiskit results with the QNE-ADK results.

The `run` member function of the `QFT` class executes the quantum Fourier transformation for a
specific input value. The `run` function takes two arguments:

 * `input` (integer): The input value for the quantum Fourier transformation. For example, if
   we have a 4-qubit QFT object (`n`=4) and the `input` value is 5, then the input for the quantum
   Fourier transformation is state |0101>.

 * `shots` (integer, default value 10000): How many times the Aer simulator should execute the
   QFT quantum circuit for the given input value to gather statistics for the output measurements.

Behind the scenes, the `run` method prepends some gates to the circuit to set the input qubits to
the desired values, runs the simulation the requested number of times, and stores the simulation
results in object member variables for later retrieval.

Finally, the `QFT` class provides several member functions that are intended to retrieve and
visualize the simulation results in a Jupyter notebook.

The following function can be run as soon as the `QFT` object has been instantiated, before the
`run` method has been invoked:
 
 * Function `circuit_diagram` displays a visual representation of the generated Qiskit circuit.

The following functions can be run after the `run` method has been invoked and summarize the
results of all circuit executions (all "shots"):

 * Function `density_matrix` returns the density matrix of the QFT output (averaged over all shots)
   as an array which is formatted for easy human reading.

 * Function `density_matrix_city` visualized the density matrix of the QFT output (averaged over all
   shots) as a "city diagram".

The following functions can be run after the `run` method has been invoked describe the state of
only the most recent circuit execution (shot):

 * Function `bloch_multivector` visualizes the density matrix of the QFT output as a Bloch
   multi-vector diagram
   (i.e. a group of Bloch spheres where arrows can be shorter than 1 to indicate entangled or
    mixed states).

 * Function `statevector` returns the statevector of the QFT output as a numpy array.

 * Function `statevector_latex` returns the statevector of the QFT output as a Latex vector.

If you open the Jupyter notebook `qft.ipynb` and run it (e.g. using the Microsoft Jupyter
plugin for Visual Studio Code) you will see example outputs for all of the above functions.

## Processors and Clusters

We use the following terminology when implementing distributed versions of the quantum Fourier
transformation:

* The term _processor_ refers to one individual quantum processor that participates in the
  distributed quantum Fourier transformation.

* The term _cluster_ refers  the collection of all processors that collectively perform
  the distributed quantum Fourier transformation.
   In other words, a cluster is group of processors.

Let's say we want to do a quantum Fourier transformation on an input of _N_ qubits.

 * In the non-distributed (local) implementation of the distribute quantum Fourier transformation
   we have a single processor that has _N_ input qubits and _N_ output qubits.

 * If we want to distribute the quantum Fourier transformation across _M_ processors:

   * We have a single cluster.

   * The cluster consists of _M_ processors.

   * Each processor in the cluster has _N/M_ qubits that contain the input before the circuit is
     run and that contain the output after the circuit is run. We refer to these qubits as the main
     qubits.

   * Each processor also contains two additional qubits that are used to communicate with other
     processors. We refer to these qubits as the entanglement qubit and the teleport qubit. Their
     roles are described in more detail below.

   * Finally, each processor also contains two classical bits that are used to store the measurement
     results that are part of the teleportation procedure or cat-entangle / cat-disentangle
     procedure.

In real life, the processors in a cluster would be connected using some sort of quantum network.
The quantum network is used to generate entanglement between the processors.
That entanglement is used to teleport qubits or to create cat states to implement the distributed
computation.

In our Qiskit code, we model the entire cluster as one single quantum circuit.

Within that single quantum circuit, each processor is modelled as a set of registers:

 * There is a `main` quantum register containing _N/M_ qubits.

 * There is an `entanglement` quantum register containing 1 qubit.

 * There is a `teleport` quantum register containing 1 qubit.

 * There is a `measure` classical register containing 2 classical bits.

## The cluster module

The Python module
[`cluster.py`](../qiskit/cluster.py)
defines the following base classes that are used for implementing various variations of
the distributed quantum Fourier transformation:

 * The base class `Processor` implements a single processor in a cluster.

 * The base class `Cluster` implements a cluster of processors.

## The Cluster class


The intention of the `Cluster` class is to provide all of the functionality that is necessary to
implement all of the various flavors of the distributed quantum Fourier transformation, i.e. the
teleportation-based flavor and the cat-state-based flavor.

Behind the scenes, a `Cluster` object instantiates multiple `Processor` objects to represent each
of the processors in the cluster. However, the various flavors of the distributed quantum Fourier
transformation are not expected to interact with the `Processor` objects - they only interact with
the `Cluster` object.

The constructor for the `Cluster` class takes the following arguments:

 * `nr_processors` (integer): The number of processors in the cluster.

 * `total_nr_qubits` (integer): The total number of (main) qubits in the cluster. The cluster as
   a whole will be able to compute the Fourier transformation on `total_nr_qubits` qubits. The
   computation is distributed across all `nr_processors` processors. Each processor has
   `total_nr_qubits` / `nr_processor` main qubits (plus extra two qubits and two classical bits
   for computation).

Logically speaking, the cluster has a total of `total_nr_qubits` which are index from 0 to
`total_nr_qubits` - 1. We refer to this index as the _global index_ of the qubit.

Each of these logical qubits is physically located on one of the processors. We use the term
_local index_ to refer to the index of the qubit locally on the processor where it is located.

The following table shows an example to clarify the concept. Here we have 3 processors, each with
4 qubits, for a total of 12 qubits:

| Qubit global index | Processor index | Qubit local index |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 2 | 0 | 2 |
| 3 | 0 | 3 |
| 4 | 1 | 0 |
| 5 | 1 | 1 |
| 6 | 1 | 2 |
| 7 | 1 | 3 |
| 8 | 2 | 0 |
| 9 | 2 | 1 |
| 10 | 2 | 2 |
| 11 | 2 | 3 |



## The Processor class

The constructor for the `Processor` class takes the following arguments:

 * `cluster` (Cluster): The cluster that this processor is a part of.

 * `index` (integer): The index of the processor within the cluster. The processors within a
   clustered are numbered 0 through _M-1_, where _M_ is the number of processors in the cluster.

 * `nr_qubits` (integer): The number of main qubits on this individual processor. If we have
    _M_ processors in the cluster and each processor has `nr_qubits` main qubits, then the cluster
    as a whole can perform a quantum Fourier transformation for _M_ * `nr_qubits` qubits.

When you instantiate a `Processor` object, the constructor creates the all the quantum and
classical registers for the processor and adds them to the one and only Qiskit quantum circuit
for the cluster.