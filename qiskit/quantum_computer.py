"""
Monolithic and clustered quantum computers.
"""

from abc import ABC, abstractmethod
from enum import Enum
from numpy import pi
from qiskit_textbook.tools import array_to_latex
from qiskit import Aer, QuantumCircuit, transpile
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_bloch_multivector, plot_state_city
from qiskit import ClassicalRegister, QuantumRegister


class QuantumComputer(ABC):
    """
    A base class for the common interface and behavior of all quantum computers, both monolithic
    and clustered.
    """

    def __init__(self, total_nr_qubits):
        """
        Constructor.

        Parameters
        ----------
        total_nr_qubits: The total number of main qubits in the processor (not including ancillary
            qubits, if any)
        """
        self.total_nr_qubits = total_nr_qubits
        self.qc = QuantumCircuit(total_nr_qubits)
        self.qc_with_input = None
        self.simulator = None
        self.result = None

    @abstractmethod
    def hadamard(self, qubit_index):
        """
        Perform a Hadamard gate.

        Parameters
        ----------
        qubit_index: The index of the qubit within the main register on this processor on which
            to apply the Hadamard gate.
        """

    @abstractmethod
    def controlled_phase(self, angle, control_qubit_index, target_qubit_index):
        """
        Perform a controlled phase gate.

        Parameters
        ----------
        angle: The angle (in radians) by which the target qubit needs to be rotated if the control
            qubit is one.
        control_qubit_index: The index of the control qubit.
        target_qubit_index: The index of the target qubit.
        """

    @abstractmethod
    def swap(self, qubit_index_1, qubit_index_2):
        """
        Perform a swap gate.

        Parameters
        ----------
        qubit_index_1: The index of the first swapped qubit.
        qubit_index_2: The index of the second swapped qubit.
        """

    def make_qft_circuit(self, final_swaps):
        """
        Make a quantum Fourier transform circuit.
        """
        self._add_rotations_to_qft_circuit(self.total_nr_qubits)
        if final_swaps:
            self._add_final_swaps_to_qft_circuit()
        # TODO move this to run self.measure_main()

    def _add_rotations_to_qft_circuit(self, remaining_nr_qubits):
        if remaining_nr_qubits == 0:
            return
        remaining_nr_qubits -= 1
        self.hadamard(remaining_nr_qubits)
        for qubit in range(remaining_nr_qubits):
            self.controlled_phase(
                pi / 2 ** (remaining_nr_qubits - qubit), qubit, remaining_nr_qubits
            )
        self._add_rotations_to_qft_circuit(remaining_nr_qubits)

    def _add_final_swaps_to_qft_circuit(self):
        for qubit in range(self.total_nr_qubits // 2):
            self.swap(qubit, self.total_nr_qubits - qubit - 1)

    def circuit_diagram(self, with_input=False):
        """
        Return a circuit diagram suitable for displaying in a Jupyter notebook.

        Parameters
        ---------
        with_input: If with_input is False, display the circuit with all input qubits initialized to
            their default value zero. If with_input is True, display the circuit with the input
            values that were specified in the call to the run function (this assumes that the run
            function was previously called; if not, this function returns None).

        Returns
        -------
        The circuit diagram that can be displayed in a Jupyter notebook.
        """
        if with_input:
            if self.qc_with_input is None:
                return None
            return self.qc_with_input.draw(fold=False, output="mpl")
        return self.qc.draw(fold=False, output="mpl")

    def statevector(self):
        """
        Returns
        -------
        The statevector of the circuit (in the form of a numpy array) resulting from the most recent
        run invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return self.result.get_statevector().data

    def statevector_latex(self):
        """
        Returns
        -------
        The statevector of the circuit (in the form of a Latex vector) resulting from the most
        recent run invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return array_to_latex(self.result.get_statevector())

    def bloch_multivector(self):
        """
        Returns
        -------
        The Block multivector diagram (that can be displayed in a Jupyter notebook) resulting from
        the most recent run invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return plot_bloch_multivector(self.result.get_statevector())

    def density_matrix(self):
        """
        Returns
        -------
        The density matrix (in the form of a numpy matrix) resulting from the most recent run
        invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return DensityMatrix(self.result.get_statevector())

    def density_matrix_city(self):
        """
        The density matrix city diagram (that can be displayed in a Jupyter notebook) resulting from
        the most recent run invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return plot_state_city(self.result.get_statevector())

    def run(self, input_value, shots=10000):
        """
        Run the quantum circuit.

        Parameters
        ----------
        input_value: An integer representing the input value for the quantum circuit. This value is
            converted to a binary value, and the bits in this binary value are used as zero or one
            initial values for the main register(s) in the cluster.
            TODO Also allow arbitrary complex initial values for each qubit.
        shots: How many times the circuit must be executed to collect statistics.
        """
        self.qc_with_input = QuantumCircuit(self.total_nr_qubits)
        # TODO: This initialization is not correct for clusters; make initialization a pure virtual
        #       function.
        bin_value = bin(input_value)[2:].zfill(self.total_nr_qubits)
        self.qc_with_input.initialize(bin_value, self.qc_with_input.qubits)
        self.qc_with_input = self.qc_with_input.compose(self.qc)
        self.simulator = Aer.get_backend("aer_simulator")
        self.qc_with_input.save_statevector()
        self.qc_with_input = transpile(self.qc_with_input, self.simulator)
        self.result = self.simulator.run(self.qc_with_input, shots=shots).result()


class MonolithicQuantumComputer(QuantumComputer):
    """
    A monolithic (non-distributed) quantum processor.
    """

    def __init__(self, total_nr_qubits):
        QuantumComputer.__init__(self, total_nr_qubits)

    def hadamard(self, qubit_index):
        self.qc.h(qubit_index)

    def controlled_phase(self, angle, control_qubit_index, target_qubit_index):
        self.qc.cp(angle, control_qubit_index, target_qubit_index)

    def swap(self, qubit_index_1, qubit_index_2):
        self.qc.swap(qubit_index_1, qubit_index_2)


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


class ProcessorInClusteredQuantumComputer:
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


class ClusteredQuantumComputer(QuantumComputer):
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
        QuantumComputer.__init__(self, total_nr_qubits)
        assert (
            total_nr_qubits % nr_processors == 0
        ), "Total nr qubits {total_nr_qubits} must be multiple of nr processors {nr_processors}"
        self.nr_processors = nr_processors
        self.method = method
        self.nr_qubits_per_processor = total_nr_qubits // nr_processors
        self.processors = {}
        for processor_index in range(nr_processors):
            self.processors[processor_index] = ProcessorInClusteredQuantumComputer(
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

    def hadamard(self, qubit_index):
        (processor_index, local_qubit_index) = self._global_to_local_index(qubit_index)
        self.processors[processor_index].hadamard(local_qubit_index)

    def controlled_phase(self, angle, control_qubit_index, target_qubit_index):
        (control_processor_index, local_control_qubit_index) = self._global_to_local_index(
            control_qubit_index
        )
        (target_processor_index, local_target_qubit_index) = self._global_to_local_index(
            target_qubit_index
        )
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

    def swap(self, qubit_index_1, qubit_index_2):
        (processor_index_1, local_qubit_index_1) = self._global_to_local_index(qubit_index_1)
        (processor_index_2, local_qubit_index_2) = self._global_to_local_index(qubit_index_2)
        if processor_index_1 == processor_index_2:
            self.processors[processor_index_1].local_swap(local_qubit_index_1, local_qubit_index_2)
        else:
            self.processors[processor_index_1].distributed_swap(
                local_qubit_index_1,
                self.processors[processor_index_2],
                local_qubit_index_2,
            )
