
If you are impatient and just want to run the code, jump ahead to the
[running the code](#running-the-code) section.

# RIPE Labs Quantum Internet Hackathon 2022

The
[Réseaux IP Européens (RIPE) Network Coordination Center (NCC)](https://www.ripe.net/)
is co-organizing the
[Quantum Internet Hackathon (QIH) 2022](https://labs.ripe.net/author/karla-white/take-part-in-the-quantum-internet-hackathon-2022/)
on 1 and 2 December 2022.

# Team Q-Harmonics

Team Q-Harmonics participates in the quantum hackathon; it consists of the following members
(in alphabetical order):
| Name | LinkedIn | GitHub |
|---|---|---|
| Abdullah K | | [GitHub](https://github.com/AbdullahKazi500) |
| B Akash Reddy | | [GitHub](https://github.com/Akash6300) |
| Bruno Rijsman | [LinkedIn](https://www.linkedin.com/in/brunorijsman/) | [GitHub](https://github.com/brunorijsman) |
| Kiran Kaur | [LinkedIn](https://www.linkedin.com/in/kiran-kaur-b2922622a/) | [GitHub](https://github.com/KyranKaur) |
| Sai Ganesh Manda | [LinkedIn](https://www.linkedin.com/in/sai-ganesh-manda-bo2002/) | [GitHub](https://github.com/mvsg2) |
| Tyler Cowan | [LinkedIn](https://www.linkedin.com/in/tyler-cowan/) | |

The name of the team, Q-Harmonics (for Quantum Harmonics) was chosen because we will be working
on the quantum Fourier transformation. The Fourier transformation is also known as
[harmonic analysis](https://en.wikipedia.org/wiki/Harmonic_analysis).

We chose "_Feasible and Doable_" as the motto for our team.

# Team Project: Distributed Quantum Fourier Transformation

The team Q-Harmonics project for the QIH 2022 hackathon is to implement a distributed version of
the Quantum Fourier Transformation (QFT) on two different simulation platforms, namely Qiskit
and QNE-ADK.

# This GitHub Repository

[This GitHub repository](https://github.com/brunorijsman/quantum-internet-hackathon-2022/)
contains all code and documentation that team Q-Harmonics produced
for the hackathon.
Everything is open source (Apache 2.0 license).

# The Quantum Fourier Transformation (QFT)

The quantum Fourier transformation is an important building block in many quantum computing
algorithms including factoring prime numbers using Shor's algorithm and phase estimation.

There are numerous resources that describe the quantum Fourier transformation and its applications,
including:

 * Several sections in the [Qiskit textbook](https://qiskit.org/textbook)

   * [Section 3.5: Quantum Fourier Transformation.](https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html)

   * [Section 3.6: Quantum Phase Estimation.](https://qiskit.org/textbook/ch-algorithms/quantum-phase-estimation.html)

   * [Section 3.7: Shor's Algorithm.](https://qiskit.org/textbook/ch-algorithms/shor.html)
 
 * [The Wikipedia article on the quantum Fourier transform.](https://en.wikipedia.org/wiki/Quantum_Fourier_transform)

 * Chapter 5 "The quantum Fourier transformation and its applications" in the book
   [Quantum Computation and Quantum Information](https://www.amazon.com/Quantum-Computation-Information-10th-Anniversary/dp/1107002176).

# Distributed Quantum Computation

We are currently in the
[Noisy Intermediate Scale Quantum era (NISQ)](https://en.wikipedia.org/wiki/Noisy_intermediate-scale_quantum_era).

The circuit size that can be supported by current quantum computer technology is limited by the
number of qubit memories and by the resilience to noise due gate infidelity and memory
decoherence.

Due to these limitations existing quantum computers are not yet able to execute quantum fourier
transform based algorithms such as phase estimation and Shor's algorithm for input sizes that have
practical relevance.
For example, quantum computers are not yet powerful enough to use Shor's algorithm to break
[RSA encryption](https://en.wikipedia.org/wiki/RSA_(cryptosystem)).

Academia and industry are pursuing several different approaches to overcome this challenge:

* Improving the capabilities of hardware platforms in terms of more qubits, better gate
  fidelities, and longer memory coherence times.

* The use of 
  [Quantum Error Correction (QEC)](https://en.wikipedia.org/wiki/Quantum_error_correction)
  to recover from errors.

* The use of distributed quantum computation to implement quantum algorithms on a collection
  of smaller quantum computers that are interconnected by a quantum network (as opposed to a large
  monolithic quantum computer).

# Distributing the Quantum Fourier Transformation

The goal of this project is to implement a _distributed_ version of the quantum Fourier
transformation.

We want to compute the quantum Fourier transform on an _N_ qubit input value.

We pretend that we only have access to quantum computers that have fewer than _N_ qubits of memory.
(I say pretend because in our project we will use only small values of _N_ due to limitations
of the simulators that we will be using.)

We are going to distribute the quantum Fourier transform computation over _M_ separate smaller
quantum processors, where each quantum processor has _N/M_ qubit memories plus a few extra qubit
memories for communication with other quantum processors.

We will be using two approaches for implementing the distributed quantum Fourier transformation:

 * The fist approach is based on [teleportation](https://en.wikipedia.org/wiki/Quantum_teleportation).
   Whenever we want to perform a two-qubit gate where one qubit is located on one quantum processor
   A and the other qubit is located on another quantum processor B, we first teleport one
   qubit from A to B, then perform the gate locally on processor B, and then teleport one qubit
   back from B to A.

 * The second approach is based on [quantum cat states](https://en.wikipedia.org/wiki/Cat_state).
   This approach only works for controlled-unitary gates, which is the majority of two-qubit gates
   in the quantum Fourier transform. We first create a cat state to share the control qubit among
   two quantum processors, then we perform the controlled-unitary, and then we unshare the cat
   state.

Some existing resources that describe the distributed quantum Fourier transformation include:

 * [ArXiv paper "Distributed quantum computing: A distributed Shor algorithm" by
   Anocha Yimsiriwattana and Samuel J. Lomonaco Jr.](https://arxiv.org/abs/quant-ph/0403146)

 * [PhD thesis "Architecture of a Quantum Multicomputer Optimized for Shor's Factoring Algorithm"
   by Rodney van Meter.](https://arxiv.org/pdf/quant-ph/0607065.pdf)

Note that some of these papers discuss a distributed implementation of Shor's algorithm. This
includes as a sub-problem a distributed quantum Fourier transformation, which is the easiest
part of the problem.

We will be implementing our distributed quantum Fourier transformation on two different simulation
platforms: Qiskit and QNE-ADK (both are described in more detail below).

# Qiskit Implementation

[Qiskit](https://qiskit.org/) is an open-source software development kit (SDK) for working with
quantum computers at the level of pulses, circuits, and application modules.

One of the components in Qiskit is [Aer](https://github.com/Qiskit/qiskit-aer), which provides
high-performance quantum computing simulators with realistic noise models.

In this project we use the Qiskit SDK to develop three different implementations of the quantum
Fourier transformation:

 1. A monolithic (non-distributed) version of the quantum Fourier transformation.
    We use this as a reference to check whether the results of the distributed versions (see below)
    are correct.

 2. A distributed version of the quantum Fourier transformation based on teleportation.

 3. A distributed version of the quantum Fourier transformation based on cat states.

Read the
[viewing and running the team Q-Harmonics Qiskit related code](docs/run-qiskit-code.md)
for more details on Qiskit and for more details on the team Q-Harmonics implementation of
the distributed quantum Fourier transformation in Qiskit (including the structure of the code
and instructions on how to install and run the code).

# QNE-ADK Implementation

The [Quantum Network Explorer (QNE)](https://www.quantum-network.com/)
is a platform provided by
[QuTech](https://qutech.nl/)
where you can gain online access to our quantum internet demonstrator and learn
about its applications and capabilities.

The [QNE Application Development Kit (QNE-ADK)](https://www.quantum-network.com/adk/)
allows users to develop quantum applications that run on the quantum network explorer.

In this project we port the three implementation of the Quantum fourier transformation (see above)
from Qiskit to QNE-ADK.

# Running the code

## Installation instructions

Read the
[installation instructions](docs/installation.md)
for instructions on how to download and install the team Q-Harmonics code and its
dependencies.

## Running the Qiskit related code

Read the
[instructions for running the Qiskit related code](docs/run-qiskit-code.md)
for instructions on how to run the team Q-Harmonics code for distributed quantum Fourier
transformations implemented in Qiskit.