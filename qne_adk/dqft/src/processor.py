class Processor:

    def __init__(self, nr_processors, total_nr_qubits, processor_index, logger):
        self.nr_processors = nr_processors
        self.total_nr_qubits = total_nr_qubits
        self.local_nr_qubits = total_nr_qubits // nr_processors
        self.processor_index = processor_index
        self.logger = logger
        self.name = self.processor_index_to_name(processor_index)
        self.logger.log(f"Create processor {self.name}")

    @staticmethod
    def processor_index_to_name(index):
        names = ['alice', 'bob', 'charlie', 'david', 'eve', 'frank', 'george', 'harry']
        if index > len(names):
            name = f'processor_{index}'
        else:
            name = names[index]
        return name

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