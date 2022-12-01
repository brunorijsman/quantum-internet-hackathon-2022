from netqasm.logging.output import get_new_app_logger
from netqasm.sdk import EPRSocket
from netqasm.sdk import Qubit
from netqasm.sdk.external import NetQASMConnection
from numpy import pi


class Processor:

    def __init__(self, app_config, nr_processors, total_nr_qubits, processor_index):
        self.app_config = app_config
        self.nr_processors = nr_processors
        self.total_nr_qubits = total_nr_qubits
        self.local_nr_qubits = total_nr_qubits // nr_processors
        self.processor_index = processor_index
        self.logger = get_new_app_logger(app_name=app_config.app_name,
                                         log_config=app_config.log_config)
        self.name = self.processor_index_to_name(processor_index)
        self.logger.log(f"{self.name}: Create processor index {self.processor_index}")
        self.epr_socket = {}
        self.main_qubit = {}
        self.conn = None

    @staticmethod
    def processor_index_to_name(index):
        names = ['alice', 'bob', 'charlie', 'david', 'eve', 'frank', 'george', 'harry']
        if index > len(names):
            name = f'processor_{index}'
        else:
            name = names[index]
        return name

    def run(self):
        self.connect_to_netqasm()
        self.create_qubits()
        self.create_epr_sockets_to_other_processors()
        self.quantum_fourier_transform()

    def connect_to_netqasm(self):
        self.logger.log(f"{self.name}: Connect to NetQASM")
        self.conn = NetQASMConnection(self.name,
                                      log_config=self.app_config.log_config,
                                      epr_sockets=list(self.epr_socket.values()))

    def create_qubits(self):
        for index in range(self.local_nr_qubits):
            self.main_qubit[index] = Qubit(self.conn)
        # TODO teleport qubit
        # TODO entanglement qubit

    def create_epr_sockets_to_other_processors(self):
        for remote_processor_index in range(self.nr_processors):
            if remote_processor_index != self.processor_index:
                remote_name = self.processor_index_to_name(remote_processor_index)
                self.logger.log(f"{self.name}: Create EPR socket {remote_processor_index=}")
                self.epr_socket[remote_processor_index] = EPRSocket(remote_name)

    def quantum_fourier_transform(self):
        self.add_qft_rotations(self.total_nr_qubits)

    def add_qft_rotations(self, n):
        if n == 0:
            return
        n -= 1
        self.hadamard(n)
        for qubit in range(n):
            self.controlled_phase(pi/2 ** (n - qubit), qubit, n)
        self.add_qft_rotations(n)

    def hadamard(self, global_qubit_index):
        (processor_index, local_qubit_index) = self.global_to_local_index(global_qubit_index)
        if processor_index != self.processor_index:
            return
        self.logger.log(f"{self.name}: Local hadamard {local_qubit_index=}")
        self.main_qubit[local_qubit_index].H()

    def controlled_phase(self, angle, global_control_qubit_index, global_target_qubit_index):
        (control_processor_index, control_local_qubit_index) = \
            self.global_to_local_index(global_control_qubit_index)
        (target_processor_index, target_local_qubit_index) = \
            self.global_to_local_index(global_target_qubit_index)
        if control_processor_index == self.processor_index:
            if target_processor_index == self.processor_index:
                self.local_controlled_phase(control_local_qubit_index, target_local_qubit_index)
            else:
                self.distributed_controlled_phase(control_local_qubit_index,
                                                  target_processor_index,
                                                  target_local_qubit_index,
                                                  True)
        else:
            if target_processor_index == self.processor_index:
                self.distributed_controlled_phase(target_local_qubit_index,
                                                  control_processor_index,
                                                  control_local_qubit_index,
                                                  False)
            else:
                pass  # both control and target qubit are remote

    def local_controlled_phase(self, local_control_qubit_index, target_local_qubit_index):
        self.logger.log(f"{self.name}: Local controlled phase "
                        f"{local_control_qubit_index=} "
                        f"{target_local_qubit_index=}")
        # TODO

    def distributed_controlled_phase(self, local_qubit_index, remote_processor_index,
                                     remote_local_qubit_index, am_teleport_receiver):
        self.logger.log(f"{self.name}: Distributed controlled phase "
                        f"{local_qubit_index=} "
                        f"{remote_processor_index=} "
                        f"{remote_local_qubit_index=} "
                        f"{am_teleport_receiver=}")
        if am_teleport_receiver:
            self.distributed_controlled_phase_here(local_qubit_index, remote_processor_index,
                                                   remote_local_qubit_index, am_teleport_receiver)
        else:
            self.distributed_controlled_phase_there(local_qubit_index, remote_processor_index,
                                                    remote_local_qubit_index, am_teleport_receiver)

    def distributed_controlled_phase_here(self, local_qubit_index, remote_processor_index,
                                          remote_local_qubit_index, am_teleport_receiver):
        # TODO receive teleport
        # TODO do local
        # TODO send teleport back
        pass

    def distributed_controlled_phase_there(self, local_qubit_index, remote_processor_index,
                                           remote_local_qubit_index, am_teleport_receiver):
        # TODO send teleport
        # TODO receive teleport back
        pass

    def global_to_local_index(self, global_qubit_index):
        processor_index = global_qubit_index // self.local_nr_qubits
        local_qubit_index = global_qubit_index % self.local_nr_qubits
        return (processor_index, local_qubit_index)
