from numpy import pi
from qiskit import Aer, ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_bloch_multivector, plot_state_city
from qiskit_textbook.tools import array_to_latex


class NaiveDQFTProcessor:

    def __init__(self, qc, name, nr_qubits):
        self.qc = qc
        self.name = name
        self.main_reg = QuantumRegister(nr_qubits, f'{name}_main')
        qc.add_register(self.main_reg)
        self.teleport_reg = QuantumRegister(1, f'{name}_teleport')
        qc.add_register(self.teleport_reg)
        self.entanglement_reg = QuantumRegister(1, f'{name}_entanglement')
        qc.add_register(self.entanglement_reg)
        self.measure_reg = ClassicalRegister(2, f'{name}_measure')
        qc.add_register(self.measure_reg)

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
        # Teleport local control qubit to remote processor
        self.qc.swap(self.main_reg[control_qubit_index], self.teleport_reg)
        self.teleport_to(target_processor)
        # Perform controlled phase gate on remote processor
        self.qc.cp(angle, target_processor.teleport_reg,
                   target_processor.main_reg[target_qubit_index])
        # Teleport remote control qubit back to local processor
        target_processor.teleport_to(self)
        self.qc.swap(self.teleport_reg, self.main_reg[control_qubit_index])

    def distributed_swap(self, local_qubit_index, remote_processor, remote_qubit_index):
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
        self.qc.reset(self.teleport_reg)
        self.qc.reset(self.entanglement_reg)

    def final_measure(self):
        self.qc.measure(self.main_reg, self.measure_reg)


class NaiveDQFT:

    NR_PROCESSORS = 2

    def __init__(self, n, swaps=True):
        assert n % self.NR_PROCESSORS == 0, 'n must be divisible by ${self.NR_PROCESSORS}'
        self.n = n
        self.qubits_per_processor = n // self.NR_PROCESSORS
        self.swaps = swaps
        self.qc = QuantumCircuit()
        self.qc_with_input = None
        self.processors = {}
        self.processors[0] = NaiveDQFTProcessor(self.qc, 'alice', self.qubits_per_processor)
        self.processors[1] = NaiveDQFTProcessor(self.qc, 'bob', self.qubits_per_processor)
        self.make_qft()

    def make_qft(self):
        self.add_qft_rotations(self.n)
        if self.swaps:
            self.add_qft_swaps()
        self.clear_ancillary()
        # TODO self.final_measure()

    def add_qft_rotations(self, n):
        if n == 0:
            return
        n -= 1
        self.global_hadamard(n)
        for qubit in range(n):
            self.global_controlled_phase(pi/2 ** (n - qubit), qubit, n)
        self.add_qft_rotations(n)

    def add_qft_swaps(self):
        for qubit in range(self.n // 2):
            self.global_swap(qubit, self.n - qubit - 1)

    def clear_ancillary(self):
        for processor in self.processors.values():
            processor.clear_ancillary()

    def final_measure(self):
        for processor in self.processors.values():
            processor.final_measure()

    def global_to_local_index(self, global_qubit_index):
        processor_index = global_qubit_index // self.qubits_per_processor
        local_qubit_index = global_qubit_index % self.qubits_per_processor
        return (processor_index, local_qubit_index)

    def global_hadamard(self, global_qubit_index):
        (processor_index, local_qubit_index) = self.global_to_local_index(global_qubit_index)
        self.processors[processor_index].local_hadamard(local_qubit_index)

    def global_controlled_phase(self, angle, global_control_qubit_index, global_target_qubit_index):
        (control_processor_index, local_control_qubit_index) = \
            self.global_to_local_index(global_control_qubit_index)
        (target_processor_index, local_target_qubit_index) = \
            self.global_to_local_index(global_target_qubit_index)
        if control_processor_index == target_processor_index:
            self.processors[control_processor_index].local_controlled_phase(
                angle, local_control_qubit_index, local_target_qubit_index)
        else:
            self.processors[control_processor_index].distributed_controlled_phase(
                angle, local_control_qubit_index, self.processors[target_processor_index],
                local_target_qubit_index)

    def global_swap(self, global_qubit_index_1, global_qubit_index_2):
        (processor_index_1, local_qubit_index_1) = self.global_to_local_index(global_qubit_index_1)
        (processor_index_2, local_qubit_index_2) = self.global_to_local_index(global_qubit_index_2)
        if processor_index_1 == processor_index_2:
            self.processors[processor_index_1].local_swap(local_qubit_index_1, local_qubit_index_2)
        else:
            self.processors[processor_index_1].distributed_swap(
                local_qubit_index_1, self.processors[processor_index_2], local_qubit_index_2)

    def circuit_diagram(self, with_input=False):
        if with_input:
            if self.qc_with_input is None:
                return None
            return self.qc_with_input.draw(fold=False)
        return self.qc.draw(fold=False)

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
        self.qc_with_input = QuantumCircuit(self.n)
        bin_value = bin(input)[2:].zfill(self.n)
        self.qc_with_input.initialize(bin_value, self.qc_with_input.qubits)
        self.qc_with_input = self.qc_with_input.compose(self.qc)
        self.simulator = Aer.get_backend('aer_simulator')
        self.qc_with_input.save_statevector()
        self.qc_with_input = transpile(self.qc_with_input, self.simulator)
        self.result = self.simulator.run(self.qc_with_input, shots=shots).result()