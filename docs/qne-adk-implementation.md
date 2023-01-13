# The distributed quantum Fourier transformation (DQFT) implementation in QNE-ADK

In this section we describe our implementation of the distributed quantum Fourier transformation
in the Quantum Network Explorer Application Development Kit (QNE-ADK).

## What is QNE-ADK

The
[Quantum Network Explorer (QNE)](https://www.quantum-network.com/)
is a website that teaches the fundamentals of quantum networking.
It is published by
[QuTech](https://qutech.nl/),
a world-leading research institute for quantum computing and the quantum Internet
based in the Netherlands.

In addition to tutorials, QNE also offers an
[Application Development Kit (ADK)](https://www.quantum-network.com/adk/)
which allows users to develop their own quantum network applications.

QNE-ADK uses NetQASM to provide the application programming interface (API) for quantum network
application developers. NetQASM is a Python module and the applications are developed in Python.

NetQASM is based on QASM, a family of assembly-level programming languages for
quantum computers.
[OpenQASM](https://github.com/openqasm/openqasm#readme) is one example of a language in this
family.

NetQASM extends QASM by also providing quantum networking primitives in addition to
quantum computing primitives.
One example of such an extension is a primitive to create entanglement between two nodes in
the network.

You can find information about NetQASM in:

-   ArXiv paper
    [NetQASM: A low-level instruction set architecture for hybrid quantum-classical programs in a quantum internet](https://arxiv.org/abs/2111.09823)
-   [The NetQASM GitHub repository](https://github.com/QuTech-Delft/netqasm)
-   [The NetQASM read-the-docs documentation page](https://netqasm.readthedocs.io/en/latest/).

QNE-ADK also provides a suite of command line tools to:

-   Manage the life cycle of quantum network applications.
-   Run applications locally on your computer.
-   Upload applications to the QNE-ADK cloud and run them there.
-   Publish quantum network applications on the
    [Community Application Library](https://www.youtube.com/watch?v=DTONkiX1bMU)
    and make them available to other users of QNE-ADK.

These command line tools are documented in the
[QNE-ADK user guide](https://www.quantum-network.com/knowledge-base/qne-quantum-application-development-kit-adk/).

Currently, QNE-ADK uses simulated quantum networks to run the applications.

According to the
[NetSquid documentation](https://github.com/QuTech-Delft/netqasm)
it is possible to use either
[NetSquid](https://netsquid.org/)
or
[SimulaQron](http://www.simulaqron.org/)
as the simulator backend, although it seems that NetSquid is much better supported than SimulaQron.
We only used the NetSquid backend.

You can find information about NetSquid in:

-   Nature paper
    [NetSquid, a NETwork Simulator for QUantum Information using Discrete events](https://www.nature.com/articles/s42005-021-00647-8).
-   [The NetSquid website](https://netsquid.org/).
-   [The NetSquid documentation](https://docs.netsquid.org/latest-release/)
    (requires registration).

The mapping of the NetQASM API to the NetSquid simulation backend is open sourced in
GitHub repository
[QuTech-Delft/squidasm](https://github.com/QuTech-Delft/squidasm).

The
[Quantum Internet Alliance(QIA)](https://quantum-internet.team/)
is a collaboration between Europe’s leading quantum research institutes and industry actors
working to develop the quantum Internet.
They are in the process of building a metropolitan scale quantum networks containing quantum
processors and quantum repeaters.
Once that real quantum network is in place, the applications developed on QNE ADK will be able to
run on it.

The following figure shows the relationship between all of the components of QNE mentioned above:

![Components of QNE](figures/components-of-qne.png)

# Modifications to QNE-ADK

We soon found out that QNE-ADK was missing some features that we needed to implement
distributed QFT.

NetQASM was missing a controlled rotation-Z (CROTZ) gate. We filed GitHub
[issue #39](https://github.com/QuTech-Delft/netqasm/issues/39) for this
and we implemented quick and dirty patches to implement the missing CROTZ in QNE-ADK on our own
forks of the QuTech repos:

-   [This is our patch](https://github.com/QuTech-Delft/netqasm/compare/develop...brunorijsman:netqasm:issue-39-add-controlled-z-rotation-arbitrary-angle)
    on our
    [fork of the NetQASM repo](https://github.com/brunorijsman/netqasm)

-   [This is our patch](https://github.com/QuTech-Delft/squidasm/compare/develop...brunorijsman:squidasm:issue-39-add-controlled-z-rotation-arbitrary-angle)
    on our
    [fork of the SquidASM repo](https://github.com/brunorijsman/squidasm)

We plan to work with the QuTech QNE team to clean up the code for these patches and to
to submit a pull-requests to upstream them to QuTech's NetQASM repository.

NetQASM was also missing a swap gate (not to be confused with entanglement swapping).
We decided not implement a patch for this (yet).
Instead, we match the swaps at the end of the QFT optional since it is essentially just a
renumbering of the qubits.

Finally, we found that by default QNE-ADK supports a maximum of three qubits per node.
If you construct a `NetQASMConnection` and pass a value of greater than 3 to parameter
`max_qubits`, there is no immediate exception at constructor time.
However, some of the qubits will not be mapped to physical qubits and there are runtime errors
later on. As a work-around, we manually edited file `networks/nodes.json` in QNE-ADK
to set `“number_of_qubits”: 10`.

# Getting familiar with QNE-ADK

The very first thing we did was try out two very simple examples to get familiar with
QNE-ADK, namely:

1. Basic entanglement generation between two nodes.
   See the code in directory [entanglement](../qne_adk/entanglement/)

2. Teleporting a qubit from one node to another.
   See the code in directory [teleport](../qne_adk/teleport/)

We will walk you through the code and show you how to run it for the teleport example.

In the teleport example, we have two nodes: sender and receiver.

The code for the sender is in file
[`app_sender.py`](../qne_adk/teleport/src/app_sender.py):

```python
from netqasm.logging.output import get_new_app_logger
from netqasm.sdk import EPRSocket, Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox import set_qubit_state


def main(phi, theta, app_config=None):

    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("sender starts")

    app_logger.log("sender creates classical socket")
    socket = Socket("sender", "receiver", log_config=app_config.log_config)

    app_logger.log("sender creates quantum socket")
    epr_socket = EPRSocket("receiver")

    app_logger.log("sender creates qasm connection")
    sender = NetQASMConnection("sender",
                               log_config=app_config.log_config,
                               epr_sockets=[epr_socket])

    with sender:

        app_logger.log("sender creates qubit to teleport")
        q = Qubit(sender)
        set_qubit_state(q, phi, theta)
        sender.flush()

        dm = get_qubit_state(q)
        app_logger.log(f"sender density matrix of teleported qubit is {dm}")
        sender.flush()

        app_logger.log("sender creates entanglement with receiver")
        q_ent = epr_socket.create_keep()[0]

        app_logger.log("sender performs teleportation")
        q.cnot(q_ent)
        q.H()
        m1 = q.measure()
        m2 = q_ent.measure()

    correction = (int(m1), int(m2))
    app_logger.log(f"sender sends correction message {correction} to receiver")
    socket.send_structured(StructuredMessage("correction", correction))

    return "sender finishes"
```

The code for the receiver is in file
[`app_receiver.py`](../qne_adk/teleport/src/app_receiver.py):

```python
from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk import EPRSocket


def main(app_config=None):

    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("receiver starts")

    app_logger.log("receiver creates classical socket")
    socket = Socket("receiver", "sender", log_config=app_config.log_config)

    app_logger.log("receiver creates quantum socket")
    epr_socket = EPRSocket("sender")

    app_logger.log("receiver creates qasm connection")
    receiver = NetQASMConnection("receiver",
                                 log_config=app_config.log_config,
                                 epr_sockets=[epr_socket])

    with receiver:

        app_logger.log("receiver creates entanglement with sender")
        q_ent = epr_socket.recv_keep()[0]
        receiver.flush()

        m1, m2 = socket.recv_structured().payload
        app_logger.log(f"receiver receives correction ({m1}, {m2}) from sender")

        if m2 == 1:
            app_logger.log("receiver performs X correction")
            q_ent.X()
        else:
            app_logger.log("receiver does not perform X correction")
        if m1 == 1:
            app_logger.log("receiver performs Z correction")
            q_ent.Z()
        else:
            app_logger.log("receiver does not perform Z correction")
        receiver.flush()

        dm = get_qubit_state(q_ent)
        app_logger.log(f"receiver density matrix of teleported qubit is {dm}")

    return "receiver finishes"
```

In this code:

-   Sender and receiver each create a `Socket` for exchanging classical messages.

-   Sender and receiver each create an `EPRSocket` and a `NetQASMConnection` for creating
    entangled qubit pairs.

-   Sender creates a qubit `q` which will be teleported to receiver later on.
    The state is determined by the `phi` and `theta` parameters passed to the `main` function.

-   Sender creates an entangled qubit pair by calling `epr_socket.create()`.
    One of the qubits is sent to receiver and the other is stored locally in `q_ent`.

-   Receiver receives the entangled qubit from Bob by calling `epr_socket.recv()` and stores it
    in `q_ent`.

-   Sender performs gates `CNOT(q, q_ent)` and `H(q_ent)`, measures `q` and `q_ent` and sends
    the measurement results in a classical message to receiver.

-   Receiver receives the classical message and possibly performs an `X` and/or `Z` correction
    on its `q_ent` qubit, based on the received measurement results.

# Monolithic quantum Fourier transformation implementation in QNE-ADK

# Distributed quantum Fourier transformation implementation in QNE-ADK

This is just a minimal place holder so that everyone can try running a basic QNE-ADK program.

I am assuming that the environment variable `QIH_2022_ROOT` is set to the
directory where we cloned our repositories (see the
[installation instructions](docs/installation.md)
for details).

Change the directory to the `quantum-internet-hackathon-2022/qne_adk` repository directory:

```
cd $QIH_2022_ROOT/quantum-internet-hackathon-2022
```

If you have not already activated your virtual environment do so now:

```
source venv/bin/activate
```

Change into the `qne_adk` directory:

```
cd qne_adk
```

Run the `qft` application (in this case I am including the output so that you know what to expect):

<pre>
$ <b>./run.sh qft</b>
Cleaning qft...
Running qft...
qne experiment create qft_experiment qft randstad
Experiment run successfully. Check the results using command 'experiment results'
Results:
[
  {
    "app_qft": {
      "n": 3,
      "value": 1
    }
  }
]
Logs:
qft_app_log.yaml:
  LOG: qft starts
  LOG: n=3
  LOG: value=1
  LOG: qft creates register of 3 qubits
  LOG: apply qft
  LOG: apply qft value n=3 value=1
  LOG: bit 0 = 1
  LOG: X gate qubit 0
  LOG: bit 1 = 0
  LOG: bit 2 = 0
  LOG: apply qft rotations n=3
  LOG: hadamard qubit 2
  LOG: controlled phase control qubit 0 and target qubit 2 by angle pi/4
  LOG: controlled phase control qubit 1 and target qubit 2 by angle pi/2
  LOG: apply qft rotations n=2
  LOG: hadamard qubit 1
  LOG: controlled phase control qubit 0 and target qubit 1 by angle pi/2
  LOG: apply qft rotations n=1
  LOG: hadamard qubit 0
  LOG: apply qft swaps
  LOG: swap qubit 0 with qubit 2 (XXX not implemented)
  LOG: "density matrix for qubit 2 = [[ 1.25000000e-01+0.j          8.83883476e-02-0.08838835j\n
    \ -1.25000000e-01+0.j         -8.83883476e-02+0.08838835j\n   2.08166817e-17-0.125j
    \     -8.83883476e-02-0.08838835j\n  -2.08166817e-17+0.125j       8.83883476e-02+0.08838835j]\n
    [ 8.83883476e-02+0.08838835j  1.25000000e-01+0.j\n  -8.83883476e-02-0.08838835j
    -1.25000000e-01+0.j\n   8.83883476e-02-0.08838835j  2.08166817e-17-0.125j\n  -8.83883476e-02+0.08838835j
    -2.08166817e-17+0.125j     ]\n [-1.25000000e-01+0.j         -8.83883476e-02+0.08838835j\n
    \  1.25000000e-01+0.j          8.83883476e-02-0.08838835j\n  -2.08166817e-17+0.125j
    \      8.83883476e-02+0.08838835j\n   2.08166817e-17-0.125j      -8.83883476e-02-0.08838835j]\n
    [-8.83883476e-02-0.08838835j -1.25000000e-01+0.j\n   8.83883476e-02+0.08838835j
    \ 1.25000000e-01+0.j\n  -8.83883476e-02+0.08838835j -2.08166817e-17+0.125j\n   8.83883476e-02-0.08838835j
    \ 2.08166817e-17-0.125j     ]\n [ 2.08166817e-17+0.125j       8.83883476e-02+0.08838835j\n
    \ -2.08166817e-17-0.125j      -8.83883476e-02-0.08838835j\n   1.25000000e-01+0.j
    \         8.83883476e-02-0.08838835j\n  -1.25000000e-01+0.j         -8.83883476e-02+0.08838835j]\n
    [-8.83883476e-02+0.08838835j  2.08166817e-17+0.125j\n   8.83883476e-02-0.08838835j
    -2.08166817e-17-0.125j\n   8.83883476e-02+0.08838835j  1.25000000e-01+0.j\n  -8.83883476e-02-0.08838835j
    -1.25000000e-01+0.j        ]\n [-2.08166817e-17-0.125j      -8.83883476e-02-0.08838835j\n
    \  2.08166817e-17+0.125j       8.83883476e-02+0.08838835j\n  -1.25000000e-01+0.j
    \        -8.83883476e-02+0.08838835j\n   1.25000000e-01+0.j          8.83883476e-02-0.08838835j]\n
    [ 8.83883476e-02-0.08838835j -2.08166817e-17-0.125j\n  -8.83883476e-02+0.08838835j
    \ 2.08166817e-17+0.125j\n  -8.83883476e-02-0.08838835j -1.25000000e-01+0.j\n   8.83883476e-02+0.08838835j
    \ 1.25000000e-01+0.j        ]]"
  LOG: writing density matrix to qne_dm.txt
  LOG: qft ends
</pre>
