from qiskit import Aer, ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_bloch_multivector, plot_state_city
from qiskit_textbook.tools import array_to_latex
from numpy import pi
from enum import Enum


class Method(Enum):
    TELEPORT = 1
    CAT_STATE = 2


class Processor:

    def __init__(self, cluster, index, nr_qubits, method):
        self.cluster = cluster
        self.method = method
        self.qc = cluster.qc
        self.index = index
        names = ['alice', 'bob', 'charlie', 'david', 'eve', 'frank', 'george', 'harry']
        if index > len(names):
            self.name = str(index)
        else:
            self.name = names[index]
        self.main_reg = QuantumRegister(nr_qubits, f'{self.name}_main')
        self.qc.add_register(self.main_reg)
        self.entanglement_reg = QuantumRegister(1, f'{self.name}_entanglement')
        self.qc.add_register(self.entanglement_reg)
        self.measure_reg = ClassicalRegister(2, f'{self.name}_measure')
        self.qc.add_register(self.measure_reg)
        if method == Method.TELEPORT:
            self.teleport_reg = QuantumRegister(1, f'{self.name}_teleport')
            self.qc.add_register(self.teleport_reg)

    def make_entanglement(self, to_processor):
        self.qc.reset(self.entanglement_reg)
        self.qc.reset(to_processor.entanglement_reg)
        self.qc.h(self.entanglement_reg)
        self.qc.cnot(self.entanglement_reg, to_processor.entanglement_reg)

    def teleport_to(self, to_processor):
        self.make_entanglement(to_processor)
        self.qc.cnot(self.teleport_reg, self.entanglement_reg)
        self.qc.h(self.teleport_reg)
        self.qc.measure(self.teleport_reg, self.measure_reg[0])
        self.qc.measure(self.entanglement_reg, self.measure_reg[1])
        self.qc.x(to_processor.entanglement_reg).c_if(self.measure_reg[1], 1)
        self.qc.z(to_processor.entanglement_reg).c_if(self.measure_reg[0], 1)
        self.qc.swap(to_processor.entanglement_reg, to_processor.teleport_reg)

    def distributed_controlled_phase(self, angle, control_qubit_index, target_processor,
                                     target_qubit_index):
        if self.method == Method.TELEPORT:
            self.distributed_controlled_phase_teleport(angle, control_qubit_index, 
                                                       target_processor, target_qubit_index)
        elif self.method == Method.CAT_STATE:
            self.distributed_controlled_phase_cat_state(angle, control_qubit_index,
                                                        target_processor, target_qubit_index)
        else:
            assert False, "Unknown method"

    def distributed_controlled_phase_teleport(self, angle, control_qubit_index, target_processor,
                                              target_qubit_index):
        # Teleport local control qubit to remote processor
        self.qc.swap(self.main_reg[control_qubit_index], self.teleport_reg)
        self.teleport_to(target_processor)
        # Perform controlled phase gate on remote processor
        self.qc.cp(angle, target_processor.teleport_reg,
                   target_processor.main_reg[target_qubit_index])
        # Teleport remote control qubit back to local processor
        target_processor.teleport_to(self)
        self.qc.swap(self.teleport_reg, self.main_reg[control_qubit_index])

    def cat_entangle(self, target_processor, control_qubit_index):
        # Create an entangled cat state between control_qubit_index on the local processor and the
        # entanglement register on to_processor.
        # TODO: Add a reference to a figure in a paper
        self.make_entanglement(target_processor)
        self.qc.cnot(self.main_reg[control_qubit_index], self.entanglement_reg)
        self.qc.measure(self.entanglement_reg, self.measure_reg[0])
        self.qc.x(self.entanglement_reg).c_if(self.measure_reg[0], 1)
        self.qc.x(target_processor.entanglement_reg).c_if(self.measure_reg[0], 1)
        # TODO: Do we really need a barrier here?
        self.qc.barrier()

    def cat_disentangle(self, target_processor, control_qubit_index):
        # Disentangle the cat state that was created by cat_entangle.
        self.qc.h(target_processor.entanglement_reg)
        self.qc.measure(target_processor.entanglement_reg, target_processor.measure_reg[0])
        self.qc.z(self.main_reg[control_qubit_index]).c_if(target_processor.measure_reg[0], 1)
        self.qc.x(target_processor.entanglement_reg).c_if(target_processor.measure_reg[0], 1)
        # TODO: Do we really need a barrier here?
        self.qc.barrier()

    def distributed_controlled_phase_cat_state(self, angle, control_qubit_index, target_processor,
                                               target_qubit_index):
        # Create a cat state to entangle the teleport register on the target_processor with the
        # control qubit on this processor.
        self.cat_entangle(target_processor, control_qubit_index)
        # Perform the controlled phase gate on the target processor.
        self.qc.cp(angle, target_processor.entanglement_reg,
                   target_processor.main_reg[target_qubit_index])
        # TODO: Do we really need a barrier here?
        self.qc.barrier()
        # Disentangle the cat state.
        self.cat_disentangle(target_processor, control_qubit_index)

    def distributed_swap(self, local_qubit_index, remote_processor, remote_qubit_index):
        # Distributed swap is always implemented using teleportation, even if controlled-phase is
        # implemented using cat states.
        # Teleport local control qubit to remote processor
        self.qc.swap(self.main_reg[local_qubit_index], self.teleport_reg)
        self.teleport_to(remote_processor)
        # Perform swap gate on remote processor
        self.qc.swap(remote_processor.teleport_reg, remote_processor.main_reg[remote_qubit_index])
        # Teleport remote control qubit back to local processor
        remote_processor.teleport_to(self)
        self.qc.swap(self.teleport_reg, self.main_reg[local_qubit_index])

    def local_hadamard(self, qubit_index):
        self.qc.h(self.main_reg[qubit_index])

    def local_controlled_phase(self, angle, control_qubit_index, target_qubit_index):
        self.qc.cp(angle, self.main_reg[control_qubit_index], self.main_reg[target_qubit_index])

    def local_swap(self, qubit_index_1, qubit_index_2):
        self.qc.swap(self.main_reg[qubit_index_1], self.main_reg[qubit_index_2])

    def clear_ancillary(self):
        if self.method == Method.TELEPORT:
            self.qc.reset(self.teleport_reg)
        self.qc.reset(self.entanglement_reg)

    def final_measure(self):
        self.qc.measure(self.main_reg, self.measure_reg)


class Cluster:

    def __init__(self, nr_processors, total_nr_qubits, method):
        assert total_nr_qubits % nr_processors == 0, \
            'Total nr qubits {total_nr_qubits} must be multiple of nr processors {nr_processors}'
        self.nr_processors = nr_processors
        self.total_nr_qubits = total_nr_qubits
        self.method = method
        self.nr_qubits_per_processor = total_nr_qubits // nr_processors
        self.qc = QuantumCircuit()
        self.qc_with_input = None
        self.processors = {}
        for processor_index in range(nr_processors):
            self.processors[processor_index] = Processor(self, processor_index, 
                                                         self.nr_qubits_per_processor, method)

    def clear_ancillary(self):
        for processor in self.processors.values():
            processor.clear_ancillary()

    def final_measure(self):
        for processor in self.processors.values():
            processor.final_measure()

    def _global_to_local_index(self, global_qubit_index):
        processor_index = global_qubit_index // self.nr_qubits_per_processor
        local_qubit_index = global_qubit_index % self.nr_qubits_per_processor
        return (processor_index, local_qubit_index)

    def hadamard(self, global_qubit_index):
        (processor_index, local_qubit_index) = self._global_to_local_index(global_qubit_index)
        self.processors[processor_index].local_hadamard(local_qubit_index)

    def controlled_phase(self, angle, global_control_qubit_index, global_target_qubit_index):
        (control_processor_index, local_control_qubit_index) = \
            self._global_to_local_index(global_control_qubit_index)
        (target_processor_index, local_target_qubit_index) = \
            self._global_to_local_index(global_target_qubit_index)
        if control_processor_index == target_processor_index:
            self.processors[control_processor_index].local_controlled_phase(
                angle, local_control_qubit_index, local_target_qubit_index)
        else:
            self.processors[control_processor_index].distributed_controlled_phase(
                angle, local_control_qubit_index, self.processors[target_processor_index],
                local_target_qubit_index)

    def swap(self, global_qubit_index_1, global_qubit_index_2, flag):
        (processor_index_1, local_qubit_index_1) = self._global_to_local_index(global_qubit_index_1)
        (processor_index_2, local_qubit_index_2) = self._global_to_local_index(global_qubit_index_2)
        if processor_index_1 == processor_index_2:
            self.processors[processor_index_1].local_swap(local_qubit_index_1, local_qubit_index_2)
        else:
            self.processors[processor_index_1].distributed_swap(local_qubit_index_1,
                self.processors[processor_index_2], local_qubit_index_2)

    def circuit_diagram(self, with_input=False):
        if with_input:
            if self.qc_with_input is None:
                return None
            return self.qc_with_input.draw(fold=False, output="mpl")
        return self.qc.draw(fold=False, output="mpl" )

    def statevector(self):
        if self.result is None:
            return None
        return self.result.get_statevector().data

    def statevector_latex(self):
        if self.result is None:
            return None
        return array_to_latex(self.result.get_statevector())

    def bloch_multivector(self):
        if self.result is None:
            return None
        return plot_bloch_multivector(self.result.get_statevector())

    def density_matrix(self):
        if self.result is None:
            return None
        return DensityMatrix(self.result.get_statevector())

    def density_matrix_city(self):
        if self.result is None:
            return None
        return plot_state_city(self.result.get_statevector())

    def run(self, input, shots=10000):
        self.qc_with_input = QuantumCircuit(self.total_nr_qubits)
        bin_value = bin(input)[2:].zfill(self.qubits_per_processor)
        self.qc_with_input.initialize(bin_value, self.qc_with_input.qubits)
        self.qc_with_input = self.qc_with_input.compose(self.qc)
        self.simulator = Aer.get_backend('aer_simulator')
        self.qc_with_input.save_statevector()
        self.qc_with_input = transpile(self.qc_with_input, self.simulator)
        self.result = self.simulator.run(self.qc_with_input, shots=shots).result()


class EntanglementExampleCluster(Cluster):

    def __init__(self):
        Cluster.__init__(self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT)
        self.processors[0].make_entanglement(self.processors[1])


class TeleportExampleCluster(Cluster):

    def __init__(self):
        Cluster.__init__(self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT)
        self.processors[0].teleport_to(self.processors[1])


class LocalControlledPhaseExampleCluster(Cluster):

    def __init__(self):
        Cluster.__init__(self, nr_processors=2, total_nr_qubits=4, method=Method.TELEPORT)
        self.processors[0].local_controlled_phase(pi/8, 0, 1)
