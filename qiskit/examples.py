"""
Example processors for Jupyter notebooks.
"""

from quantum_computer import ClusteredQuantumComputer, Method
from numpy import pi


class EntanglementExampleCluster(ClusteredQuantumComputer):
    """
    An example class to demonstrate which qubit registers exist in a cluster.
    """

    def __init__(self):
        ClusteredQuantumComputer.__init__(
            self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT
        )
        self.processors[0].make_entanglement(self.processors[1])


class TeleportExampleCluster(ClusteredQuantumComputer):
    """
    An example class to demonstrate the circuit that is generated to implement a single
    teleportation.
    """

    def __init__(self):
        ClusteredQuantumComputer.__init__(
            self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT
        )
        self.processors[0].teleport_to(self.processors[1])


class LocalControlledPhaseExampleCluster(ClusteredQuantumComputer):
    """
    An example class to demonstrate the circuit that is generated to implement a local
    controlled-phase gate between two qubits on the same processor in a cluster.
    """

    def __init__(self):
        ClusteredQuantumComputer.__init__(
            self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT
        )
        self.processors[0].local_controlled_phase(pi / 8, 0, 1)
