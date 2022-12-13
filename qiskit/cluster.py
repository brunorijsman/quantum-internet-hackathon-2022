"""
A cluster of quantum processors that can run distributed quantum algorithms.
"""

from enum import Enum
from numpy import pi
from circuit_base import CircuitBase
from qiskit import ClassicalRegister, QuantumRegister


class Method(Enum):
    """
    The method that is used to implement a two-qubit controlled-unitary gate, where the control
    qubit is on one processor and the target processor is on a different processor.
    """

    TELEPORT = 1
    """
    Implement controlled-unitary gates using teleportation: teleport the control qubit from the
    control processor to the target processor, perform the controlled-unitary gate on the target
    processor, and teleport the control qubit back to the control processor.
    """

    CAT_STATE = 2
    """
    Implement controlled-unitary gates using cat states. TODO Add reference
    """


class Processor:
    """
    A single quantum processor within a cluster of quantum processors that collectively run a
    distributed quantum computation.
    """

    def __init__(self, cluster, index, nr_qubits, method):
        """
        Constructor.

        Parameters
        ----------
        cluster: The cluster of which the processor is a member.
        index: The index of the processor within the cluster.
        nr_qubits: The number of qubits in the main register of this processor.
        method: The method that is used to implement distributed controlled-unitary gates.
        """
        self.cluster = cluster
        self.method = method
        self.qc = cluster.qc
        self.index = index
        names = ["alice", "bob", "charlie", "david", "eve", "frank", "george", "harry"]
        if index > len(names):
            self.name = str(index)
        else:
            self.name = names[index]
        self.main_reg = QuantumRegister(nr_qubits, f"{self.name}_main")
        self.qc.add_register(self.main_reg)
        self.entanglement_reg = QuantumRegister(1, f"{self.name}_entanglement")
        self.qc.add_register(self.entanglement_reg)
        self.measure_reg = ClassicalRegister(2, f"{self.name}_measure")
        self.qc.add_register(self.measure_reg)
        self.teleport_reg = QuantumRegister(1, f"{self.name}_teleport")
        self.qc.add_register(self.teleport_reg)

    def make_entanglement(self, to_processor):
        """
        Create a psi-plus entanglement between the entanglement register on this processor and the
        entanglement register on to_processor.

        Parameters
        ----------
        to_processor: The processor to create an entanglement with.
        """
        self.qc.reset(self.entanglement_reg)
        self.qc.reset(to_processor.entanglement_reg)
        self.qc.h(self.entanglement_reg)
        self.qc.cnot(self.entanglement_reg, to_processor.entanglement_reg)

    def teleport_to(self, to_processor):
        """
        Teleport the teleport register on this processor to the teleport register on to_processor.

        Parameters
        ----------
        to_processor: The processor to teleport the qubit to.
        """
        self.make_entanglement(to_processor)
        self.qc.cnot(self.teleport_reg, self.entanglement_reg)
        self.qc.h(self.teleport_reg)
        self.qc.measure(self.teleport_reg, self.measure_reg[0])
        self.qc.measure(self.entanglement_reg, self.measure_reg[1])
        self.qc.x(to_processor.entanglement_reg).c_if(self.measure_reg[1], 1)
        self.qc.z(to_processor.entanglement_reg).c_if(self.measure_reg[0], 1)
        self.qc.swap(to_processor.entanglement_reg, to_processor.teleport_reg)

    def distributed_controlled_phase(
        self, angle, control_qubit_index, target_processor, target_qubit_index
    ):
        """
        Perform a distributed controlled gate phase.

        The distributed controlled phase gate is implemented using teleportation or using cat-states
        as indicated by the method passed to the constructor.

        Parameters
        ----------
        angle: The angle (in radians) by which the target qubit needs to be rotated if the control
            qubit is one.
        control_qubit_index: The index of the qubit within the main register on this processor that
            is used as the control qubit.
        target_processor: The processor that contains the target qubit.
        target_qubit_index: The index of the qubit within the main register on target_processor that
            is used as the target qubit.
        """
        if self.method == Method.TELEPORT:
            self._distributed_controlled_phase_teleport(
                angle, control_qubit_index, target_processor, target_qubit_index
            )
        elif self.method == Method.CAT_STATE:
            self._distributed_controlled_phase_cat_state(
                angle, control_qubit_index, target_processor, target_qubit_index
            )
        else:
            assert False, "Unknown method"

    def _distributed_controlled_phase_teleport(
        self, angle, control_qubit_index, target_processor, target_qubit_index
    ):
        # Teleport local control qubit to remote processor
        self.qc.swap(self.main_reg[control_qubit_index], self.teleport_reg)
        self.teleport_to(target_processor)
        # Perform controlled phase gate on remote processor
        self.qc.cp(
            angle,
            target_processor.teleport_reg,
            target_processor.main_reg[target_qubit_index],
        )
        # Teleport remote control qubit back to local processor
        target_processor.teleport_to(self)
        self.qc.swap(self.teleport_reg, self.main_reg[control_qubit_index])

    def cat_entangle(self, target_processor, control_qubit_index):
        """
        Create an entangled cat state between control_qubit_index on this processor and the
        entanglement register on target_processor.

        Parameters
        ----------
        target_processor: The target processor to create a cat state with. The cat state is created
            with the entanglement register on the target_processor.
        control_qubit_index: The index of the control qubit within the main register on this
            processor that the cat state is created from.
        """
        self.make_entanglement(target_processor)
        self.qc.cnot(self.main_reg[control_qubit_index], self.entanglement_reg)
        self.qc.measure(self.entanglement_reg, self.measure_reg[0])
        self.qc.x(self.entanglement_reg).c_if(self.measure_reg[0], 1)
        self.qc.x(target_processor.entanglement_reg).c_if(self.measure_reg[0], 1)

    def cat_disentangle(self, target_processor, control_qubit_index):
        """
        Disentangle the cat state that was previously created by cat_entangle.

        Parameters
        ----------
        target_processor: The target processor to disentangle the cat state from. The cat state is
            stored in the entanglement register on the target_processor.
        control_qubit_index: The index of the control qubit within the main register on this
            processor that contains the cat state.
        """
        self.qc.h(target_processor.entanglement_reg)
        self.qc.measure(target_processor.entanglement_reg, target_processor.measure_reg[0])
        self.qc.z(self.main_reg[control_qubit_index]).c_if(target_processor.measure_reg[0], 1)
        self.qc.x(target_processor.entanglement_reg).c_if(target_processor.measure_reg[0], 1)

    def _distributed_controlled_phase_cat_state(
        self, angle, control_qubit_index, target_processor, target_qubit_index
    ):
        self.cat_entangle(target_processor, control_qubit_index)
        self.qc.cp(
            angle,
            target_processor.entanglement_reg,
            target_processor.main_reg[target_qubit_index],
        )
        self.cat_disentangle(target_processor, control_qubit_index)

    def distributed_swap(self, local_qubit_index, remote_processor, remote_qubit_index):
        """
        Perform a distributed swap gate.

        Distributed swap is always implemented using teleportation, even if method is set to
        CAT_STATE.

        Parameters
        ----------
        local_qubit_index: The qubit index within the main register on this processor that is being
            swapped.
        remote_processor: The remote processor that contains the other qubit that the local qubit
            is being swapped with.
        remote_qubit_index: The qubit index within the main register on the remote processor that
            contains the other qubit that the local qubit is being swapped with.
        """
        # Teleport local control qubit to remote processor
        self.qc.swap(self.main_reg[local_qubit_index], self.teleport_reg)
        self.teleport_to(remote_processor)
        # Perform swap gate on remote processor
        self.qc.swap(remote_processor.teleport_reg, remote_processor.main_reg[remote_qubit_index])
        # Teleport remote control qubit back to local processor
        remote_processor.teleport_to(self)
        self.qc.swap(self.teleport_reg, self.main_reg[local_qubit_index])

    def hadamard(self, qubit_index):
        """
        Perform a Hadamard gate.

        Parameters
        ----------
        qubit_index: The index of the qubit within the main register on this processor on which to
            apply the Hadamard gate.
        """
        self.qc.h(self.main_reg[qubit_index])

    def local_controlled_phase(self, angle, control_qubit_index, target_qubit_index):
        """
        Perform a local controlled phase gate, where the control and target qubits are both located
        on this processor.

        Parameters
        ----------
        angle: The angle (in radians) by which the target qubit needs to be rotated if the control
            qubit is one.
        control_qubit_index: The index of the qubit within the main register on this processor that
            is used as the control qubit.
        target_qubit_index: The index of the qubit within the main register on this processor that
            is used as the target qubit.
        """
        self.qc.cp(angle, self.main_reg[control_qubit_index], self.main_reg[target_qubit_index])

    def local_swap(self, qubit_index_1, qubit_index_2):
        """
        Perform a local swap gate, where both swapped qubits are located on this processor.

        Parameters
        ----------
        qubit_index_1: The index of the first qubit within the main register on this processor that
            is being swapped.
        qubit_index_2: The index of the second qubit within the main register on this processor that
            is being swapped.
        """
        self.qc.swap(self.main_reg[qubit_index_1], self.main_reg[qubit_index_2])

    def clear_ancillary(self):
        """
        Clear (reset to zero) all ancillary qubits on this processor.
        """
        # TODO: Only reset a qubit if it was used (add a used variable to keep track of this)
        # TODO: Select reset method
        self.qc.reset(self.teleport_reg)
        self.qc.reset(self.entanglement_reg)

    def measure_main(self):
        """
        Measure all qubits in the main register of this processor.
        """
        self.qc.measure(self.main_reg, self.measure_reg)


class Cluster(CircuitBase):
    """
    A cluster of quantum processors that collectively run a distributed quantum computation.
    """

    def __init__(self, nr_processors, total_nr_qubits, method):
        """
        Constructor.

        Parameters
        ----------
        nr_processors: The number of quantum processors in the cluster.
        total_nr_qubits: The total number of main qubits in the cluster. This must be a multiple of
            nr_processors. The qubits in the cluster have a global index ranging from 0 through
            total_nr_qubits-1.
        method: The method that is used to implement distributed controlled-unitary gates.
        """
        CircuitBase.__init__(self, total_nr_qubits)
        assert (
            total_nr_qubits % nr_processors == 0
        ), "Total nr qubits {total_nr_qubits} must be multiple of nr processors {nr_processors}"
        self.nr_processors = nr_processors
        self.method = method
        self.nr_qubits_per_processor = total_nr_qubits // nr_processors
        self.processors = {}
        for processor_index in range(nr_processors):
            self.processors[processor_index] = Processor(
                self, processor_index, self.nr_qubits_per_processor, method
            )

    def clear_ancillary(self):
        """
        Clear (reset to zero) all ancillary qubits on all processor in the cluster.
        """
        for processor in self.processors.values():
            processor.clear_ancillary()

    def measure_main(self):
        """
        Measure all qubits in the main registers of all processors in the cluster.
        """
        for processor in self.processors.values():
            processor.measure_main()

    def _global_to_local_index(self, global_qubit_index):
        processor_index = global_qubit_index // self.nr_qubits_per_processor
        local_qubit_index = global_qubit_index % self.nr_qubits_per_processor
        return (processor_index, local_qubit_index)

    def hadamard(self, global_qubit_index):
        """
        Perform a Hadamard gate.

        Parameters
        ----------
        global_qubit_index: The global index of the qubit to perform the Hadamard gate on.
        """
        (processor_index, local_qubit_index) = self._global_to_local_index(global_qubit_index)
        self.processors[processor_index].hadamard(local_qubit_index)

    def controlled_phase(self, angle, global_control_qubit_index, global_target_qubit_index):
        """
        Perform a controlled phase gate.

        If the control and target qubits are located on the same processor, this performs a local
        controlled phase gate on that processor. If the control and target qubits are located on
        different processors, this performs a distributed controlled phase gate, using the method
        specified in the cluster constructor.

        Parameters
        ----------
        angle: The angle (in radians) by which the target qubit needs to be rotated if the control
            qubit is one.
        global_control_qubit_index: The global index of the control qubit.
        global_target_qubit_index: The global index of the target qubit.
        """
        (
            control_processor_index,
            local_control_qubit_index,
        ) = self._global_to_local_index(global_control_qubit_index)
        (
            target_processor_index,
            local_target_qubit_index,
        ) = self._global_to_local_index(global_target_qubit_index)
        if control_processor_index == target_processor_index:
            self.processors[control_processor_index].local_controlled_phase(
                angle, local_control_qubit_index, local_target_qubit_index
            )
        else:
            self.processors[control_processor_index].distributed_controlled_phase(
                angle,
                local_control_qubit_index,
                self.processors[target_processor_index],
                local_target_qubit_index,
            )

    def swap(self, global_qubit_index_1, global_qubit_index_2):
        """
        Perform a swap gate.

        If the two swapped qubits are both located on the same processor, this performs a local
        swap gate on that processor. If they are located on different processors, this performs a
        distributed swap gate. Distributed swap gates are always implemented using teleportation,
        regardless of what method was specified in the cluster constructor.

        Parameters
        ----------
        global_qubit_index_1: The global index of the first swapped qubit.
        global_qubit_index_2: The global index of the second swapped qubit.
        """
        (processor_index_1, local_qubit_index_1) = self._global_to_local_index(global_qubit_index_1)
        (processor_index_2, local_qubit_index_2) = self._global_to_local_index(global_qubit_index_2)
        if processor_index_1 == processor_index_2:
            self.processors[processor_index_1].local_swap(local_qubit_index_1, local_qubit_index_2)
        else:
            self.processors[processor_index_1].distributed_swap(
                local_qubit_index_1,
                self.processors[processor_index_2],
                local_qubit_index_2,
            )


class EntanglementExampleCluster(Cluster):
    """
    An example class to demonstrate which qubit registers exist in a cluster.
    """

    def __init__(self):
        Cluster.__init__(self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT)
        self.processors[0].make_entanglement(self.processors[1])


class TeleportExampleCluster(Cluster):
    """
    An example class to demonstrate the circuit that is generated to implement a single
    teleportation.
    """

    def __init__(self):
        Cluster.__init__(self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT)
        self.processors[0].teleport_to(self.processors[1])


class LocalControlledPhaseExampleCluster(Cluster):
    """
    An example class to demonstrate the circuit that is generated to implement a local
    controlled-phase gate between two qubits on the same processor in a cluster.
    """

    def __init__(self):
        Cluster.__init__(self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT)
        self.processors[0].local_controlled_phase(pi / 8, 0, 1)
