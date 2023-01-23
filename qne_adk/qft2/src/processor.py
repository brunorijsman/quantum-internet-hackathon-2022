"""
Quantum processor for QNE-ADK.
"""

from netqasm.logging.output import get_new_app_logger
from netqasm.sdk import EPRSocket
from netqasm.sdk import Qubit
from netqasm.sdk.external import NetQASMConnection
from numpy import pi


class Processor:
    """
    A single quantum processor within a cluster of quantum processors that collectively run a
    distributed quantum computation. Unlike the Qiskit implementation, the QNE-ADK processor class
    is not (yet) able to run any arbitrary quantum algorithm; it is (currently) hard-coded to run
    a distributed quantum Fourier transformation.
    """

    def __init__(self, app_config, nr_processors, total_nr_qubits, processor_index):
        """
        Constructor

        Parameters
        ----------
        app_config: The QNE-ADK application configuration.
        nr_processors: The total number of processors in the cluster.
        total_nr_qubits: The total number of main qubits in the cluster. These are equally divided
            across all processors. This does not include the anillary qubits used for communication.
        processor_index: The zero-based index of this processor within the cluster.
        """
        self.app_config = app_config
        self.nr_processors = nr_processors
        self.total_nr_qubits = total_nr_qubits
        self.local_nr_qubits = total_nr_qubits // nr_processors
        self.processor_index = processor_index
        self.logger = get_new_app_logger(
            app_name=app_config.app_name, log_config=app_config.log_config
        )
        self.name = self.processor_index_to_name(processor_index)
        self.logger.log(f"{self.name}: Create processor index {self.processor_index}")
        self.epr_socket = {}
        self.main_qubit = {}
        self.conn = None

    @staticmethod
    def processor_index_to_name(index):
        """
        Convert a processor index to a processor name.

        Parameters
        ----------
        index: The zero-based processor index.

        Returns
        -------
        The processor name.
        """
        return f"processor{index}"

    def run(self):
        """
        The main run function for the processor.
        """
        self.connect_to_netqasm()
        self.create_qubits()
        self.create_epr_sockets_to_other_processors()
        self.quantum_fourier_transform()

    def connect_to_netqasm(self):
        """
        Connect to NetQASM.
        """
        self.logger.log(f"{self.name}: Connect to NetQASM")
        self.conn = NetQASMConnection(
            self.name,
            log_config=self.app_config.log_config,
            epr_sockets=list(self.epr_socket.values()),
        )

    def create_qubits(self):
        """
        Create all qubits for the processor.
        """
        for index in range(self.local_nr_qubits):
            self.main_qubit[index] = Qubit(self.conn)
        # TODO teleport qubit
        # TODO entanglement qubit

    def create_epr_sockets_to_other_processors(self):
        """
        Create EPR sockets for producing entanglements with remote processors.
        """
        for remote_processor_index in range(self.nr_processors):
            if remote_processor_index != self.processor_index:
                remote_name = self.processor_index_to_name(remote_processor_index)
                self.logger.log(f"{self.name}: Create EPR socket {remote_processor_index=}")
                self.epr_socket[remote_processor_index] = EPRSocket(remote_name)

    def quantum_fourier_transform(self):
        """
        Perform a (distributed) quantum Fourier transformation.
        """
        self.add_qft_rotations(self.total_nr_qubits)

    def add_qft_rotations(self, remaining_nr_qubits):
        """
        Perform the controlled rotations part of the distributed quantum Fourier transformation.

        Parameters
        ----------
        remaining_nr_qubits: The remaining number of qubits for which controlled rotations need
            to be performed.
        """
        if remaining_nr_qubits == 0:
            return
        remaining_nr_qubits -= 1
        self.hadamard(remaining_nr_qubits)
        for qubit in range(remaining_nr_qubits):
            self.controlled_phase(
                pi / 2 ** (remaining_nr_qubits - qubit), qubit, remaining_nr_qubits
            )
        self.add_qft_rotations(remaining_nr_qubits)

    def hadamard(self, global_qubit_index):
        """
        Perform a (global) hadamard gate. The qubit is allowed to be on any processor.

        Parameters
        ----------
        global_qubit_index: The global index of the qubit on which to perform the hadamard gate.
        """
        (processor_index, local_qubit_index) = self.global_to_local_index(global_qubit_index)
        if processor_index != self.processor_index:
            return
        self.logger.log(f"{self.name}: Local hadamard {local_qubit_index=}")
        self.main_qubit[local_qubit_index].H()

    def controlled_phase(self, _angle, global_control_qubit_index, global_target_qubit_index):
        """
        Perform a (global) controlled phase gate. The control qubit and the target qubit are
        allowed to be on any processor.

        Parameters
        ----------
        angle: The rotation angle.
        global_control_qubit_index: The global index of the control qubit.
        global_target_qubit_index: The global index of the target qubit.
        """
        (control_processor_index, control_local_qubit_index) = self.global_to_local_index(
            global_control_qubit_index
        )
        (target_processor_index, target_local_qubit_index) = self.global_to_local_index(
            global_target_qubit_index
        )
        if control_processor_index == self.processor_index:
            if target_processor_index == self.processor_index:
                self.local_controlled_phase(control_local_qubit_index, target_local_qubit_index)
            else:
                self.distributed_controlled_phase(
                    control_local_qubit_index,
                    target_processor_index,
                    target_local_qubit_index,
                    True,
                )
        else:
            if target_processor_index == self.processor_index:
                self.distributed_controlled_phase(
                    target_local_qubit_index,
                    control_processor_index,
                    control_local_qubit_index,
                    False,
                )
            else:
                pass  # both control and target qubit are remote

    def local_controlled_phase(self, local_control_qubit_index, local_target_qubit_index):
        """
        Perform a local controlled phase gate. The control qubit and the target qubit must both
        be on this processor.

        Parameters
        ----------
        local_control_qubit_index: The local index of the control qubit.
        local_target_qubit_index: The local index of the target qubit.
        """
        self.logger.log(
            f"{self.name}: Local controlled phase "
            f"{local_control_qubit_index=} "
            f"{local_target_qubit_index=}"
        )
        # TODO

    def distributed_controlled_phase(
        self,
        local_qubit_index,
        remote_processor_index,
        remote_local_qubit_index,
        am_teleport_receiver,
    ):
        """
        Perform a distributed controlled phase gate. TODO
        """
        self.logger.log(
            f"{self.name}: Distributed controlled phase "
            f"{local_qubit_index=} "
            f"{remote_processor_index=} "
            f"{remote_local_qubit_index=} "
            f"{am_teleport_receiver=}"
        )
        if am_teleport_receiver:
            self.distributed_controlled_phase_here(
                local_qubit_index,
                remote_processor_index,
                remote_local_qubit_index,
                am_teleport_receiver,
            )
        else:
            self.distributed_controlled_phase_there(
                local_qubit_index,
                remote_processor_index,
                remote_local_qubit_index,
                am_teleport_receiver,
            )

    def distributed_controlled_phase_here(
        self,
        local_qubit_index,
        remote_processor_index,
        remote_local_qubit_index,
        am_teleport_receiver,
    ):
        """
        Perform a distributed controlled phase gate. TODO
        """
        # TODO receive teleport
        # TODO do local
        # TODO send teleport back

    def distributed_controlled_phase_there(
        self,
        local_qubit_index,
        remote_processor_index,
        remote_local_qubit_index,
        am_teleport_receiver,
    ):
        """
        Perform a distributed controlled phase gate. TODO
        """
        # TODO send teleport
        # TODO receive teleport back

    def global_to_local_index(self, global_qubit_index):
        """
        Convert a global qubit index to a processor-local qubit index.

        Parameters
        ----------
        global_qubit_index: The global qubit index.

        Returns
        -------
        The local qubit index in the form of a tuple (processor_index, local_qubit_index).
        """
        processor_index = global_qubit_index // self.local_nr_qubits
        local_qubit_index = global_qubit_index % self.local_nr_qubits
        return (processor_index, local_qubit_index)
