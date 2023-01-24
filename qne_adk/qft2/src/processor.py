"""
Quantum processor for QNE-ADK.
"""

from time import sleep
from netqasm.logging.output import get_new_app_logger
from netqasm.sdk import EPRSocket
from netqasm.sdk import Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import NetQASMConnection, Socket


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
        self.name = self._processor_index_to_name(processor_index)
        self.logger.log(f"{self.name}: Create processor index {self.processor_index}")
        self.epr_socket = {}
        self.classical_socket = {}
        self.main_qubit = {}
        self.conn = NetQASMConnection(
            self.name,
            log_config=self.app_config.log_config,
            epr_sockets=list(self.epr_socket.values()),
        )
        self._create_qubits()
        self._create_epr_sockets_to_other_processors()
        self._create_classical_sockets_to_other_processors()
        self._wait_until_classical_sockets_connected()

    def agent_processor_main(self):
        """
        The main entry point for an agent processor. Listen for incoming commands from the
        coordinator processor (over the classical channel) and execute them.
        """
        self.logger.log(
            f"{self.name}: Agent processor waits for instructions from coordinator processor"
        )
        socket = self.classical_socket[0]
        # message = coordinator_socket.recv_structured()
        message = socket.recv()
        socket.send("response")
        #     self.logger.log(f"Receive {message=}")
        # command = message.header
        # arguments = message.payload
        # TODO

    @staticmethod
    def _processor_index_to_name(index):
        return f"processor{index}"

    def _am_coordinator_processor(self):
        return self.processor_index == 0

    def _create_qubits(self):
        for index in range(self.local_nr_qubits):
            self.main_qubit[index] = Qubit(self.conn)
        # TODO teleport qubit
        # TODO entanglement qubit

    def _create_epr_sockets_to_other_processors(self):
        for remote_processor_index in range(self.nr_processors):
            if remote_processor_index != self.processor_index:
                remote_name = self._processor_index_to_name(remote_processor_index)
                self.logger.log(f"{self.name}: Create EPR socket {remote_processor_index=}")
                self.epr_socket[remote_processor_index] = EPRSocket(remote_name)

    def _create_classical_sockets_to_other_processors(self):
        for remote_processor_index in range(self.nr_processors):
            if remote_processor_index != self.processor_index:
                local_name = self.name
                remote_name = self._processor_index_to_name(remote_processor_index)
                self.logger.log(
                    f"{self.name}: Create classical socket {remote_processor_index=} "
                    f"{local_name=} {remote_name=}"
                )
                self.classical_socket[remote_processor_index] = Socket(
                    local_name, remote_name, log_config=self.app_config.log_config
                )

    def _wait_until_classical_sockets_connected(self):
        # TODO: We used to try to send a message over a socket soon after creating it. This caused
        #       an exception ConnectionError("Socket is not connected so cannot send")
        #       This function is an attempt to wait until the sockets are connected before
        #       proceeding. For reasons unknown to me, it doesn't work: now we just get a
        #       TimeoutExpired exception. I asked for help on the QNE-ADK Slack channel.
        while True:
            all_connected = True
            for remote_processor_index in range(self.nr_processors):
                if remote_processor_index != self.processor_index:
                    socket = self.classical_socket[remote_processor_index]
                    if not socket.connected:
                        all_connected = False
                        break
            if all_connected:
                self.logger.log("All classical sockets are connected")
                return
            self.logger.log("At least one classical socket is not yet connected")
            sleep(1.0)

    def hadamard(self, global_qubit_index):
        """
        Perform a hadamard gate. This function can only be called on the coordinator processor.

        Parameters
        ----------
        global_qubit_index: The global index of the qubit on which to perform the hadamard gate.
        """
        assert self._am_coordinator_processor()
        self.logger.log(f"{self.name}: Global hadamard {global_qubit_index=}")
        (processor_index, local_qubit_index) = self._global_to_local_index(global_qubit_index)
        if processor_index == self.processor_index:
            self._local_hadamard(local_qubit_index)
        else:
            self._remote_hadamard(processor_index, local_qubit_index)

    def _local_hadamard(self, local_qubit_index):
        self.logger.log(f"{self.name}: Local hadamard {local_qubit_index=}")
        self.main_qubit[local_qubit_index].H()

    def _remote_hadamard(self, processor_index, local_qubit_index):
        self.logger.log(f"{self.name}: Remote hadamard {processor_index=} {local_qubit_index=}")
        message = StructuredMessage("hadamard", str(local_qubit_index))
        self.logger.log(f"{self.name}: Send {message=} {processor_index=}")
        # self.classical_socket[processor_index].send_structured(message)
        # socket = self.classical_socket[processor_index]
        # socket.send("command")
        # response = socket.recv()

    def controlled_phase(self, _angle, global_control_qubit_index, global_target_qubit_index):
        """
        Perform a (global) controlled phase gate. This function can only be called on the
        coordinator processor.

        Parameters
        ----------
        angle: The rotation angle.
        global_control_qubit_index: The global index of the control qubit.
        global_target_qubit_index: The global index of the target qubit.
        """
        assert self._am_coordinator_processor()
        (control_processor_index, control_local_qubit_index) = self._global_to_local_index(
            global_control_qubit_index
        )
        (target_processor_index, target_local_qubit_index) = self._global_to_local_index(
            global_target_qubit_index
        )
        if control_processor_index == self.processor_index:
            if target_processor_index == self.processor_index:
                self._local_controlled_phase(control_local_qubit_index, target_local_qubit_index)
            else:
                self._distributed_controlled_phase(
                    control_local_qubit_index,
                    target_processor_index,
                    target_local_qubit_index,
                    True,
                )
        else:
            if target_processor_index == self.processor_index:
                self._distributed_controlled_phase(
                    target_local_qubit_index,
                    control_processor_index,
                    control_local_qubit_index,
                    False,
                )
            else:
                pass  # both control and target qubit are remote

    def _local_controlled_phase(self, local_control_qubit_index, local_target_qubit_index):
        self.logger.log(
            f"{self.name}: Local controlled phase "
            f"{local_control_qubit_index=} "
            f"{local_target_qubit_index=}"
        )
        # TODO

    def _distributed_controlled_phase(
        self,
        local_qubit_index,
        remote_processor_index,
        remote_local_qubit_index,
        am_teleport_receiver,
    ):
        self.logger.log(
            f"{self.name}: Distributed controlled phase "
            f"{local_qubit_index=} "
            f"{remote_processor_index=} "
            f"{remote_local_qubit_index=} "
            f"{am_teleport_receiver=}"
        )
        if am_teleport_receiver:
            self._distributed_controlled_phase_here(
                local_qubit_index,
                remote_processor_index,
                remote_local_qubit_index,
                am_teleport_receiver,
            )
        else:
            self._distributed_controlled_phase_there(
                local_qubit_index,
                remote_processor_index,
                remote_local_qubit_index,
                am_teleport_receiver,
            )

    def _distributed_controlled_phase_here(
        self,
        local_qubit_index,
        remote_processor_index,
        remote_local_qubit_index,
        am_teleport_receiver,
    ):
        # TODO receive teleport
        # TODO do local
        # TODO send teleport back
        pass

    def _distributed_controlled_phase_there(
        self,
        local_qubit_index,
        remote_processor_index,
        remote_local_qubit_index,
        am_teleport_receiver,
    ):
        # TODO send teleport
        # TODO receive teleport back
        pass

    def _global_to_local_index(self, global_qubit_index):
        processor_index = global_qubit_index // self.local_nr_qubits
        local_qubit_index = global_qubit_index % self.local_nr_qubits
        return (processor_index, local_qubit_index)
