from netqasm.logging.output import get_new_app_logger
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection


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
        self.conn = None
        self.create_epr_sockets_to_other_processors()

    @staticmethod
    def processor_index_to_name(index):
        names = ['alice', 'bob', 'charlie', 'david', 'eve', 'frank', 'george', 'harry']
        if index > len(names):
            name = f'processor_{index}'
        else:
            name = names[index]
        return name

    def create_epr_sockets_to_other_processors(self):
        for remote_processor_index in range(self.nr_processors):
            if remote_processor_index != self.processor_index:
                remote_name = self.processor_index_to_name(remote_processor_index)
                self.logger.log(f"{self.name}: Create EPR socket to remote processor "
                                f"index {remote_processor_index}")
                self.epr_socket[remote_processor_index] = EPRSocket(remote_name)

    def run(self):
        self.connect_to_netqasm()
        
    def connect_to_netqasm(self):
        self.logger.log(f"{self.name}: Connect to NetQASM")
        self.conn = NetQASMConnection(self.name,
                                      log_config=self.app_config.log_config,
                                      epr_sockets=list(self.epr_socket.values()))

    #####

    def make_entanglement(self, to_processor_index):
        # TODO
        pass

    def teleport_to(self, to_processor):
        # TODO
        pass

    def distributed_controlled_phase(self, angle, control_qubit_index, target_processor,
                                     target_qubit_index):
        # TODO
        pass

    def distributed_swap(self, local_qubit_index, remote_processor, remote_qubit_index):
        # TODO
        pass

    def local_hadamard(self, qubit_index):
        # TODO
        pass

    def local_controlled_phase(self, angle, control_qubit_index, target_qubit_index):
        # TODO
        pass

    def local_swap(self, qubit_index_1, qubit_index_2):
        # TODO
        pass

    def clear_ancillary(self):
        # TODO
        pass