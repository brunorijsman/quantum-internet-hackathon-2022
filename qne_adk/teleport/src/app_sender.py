"""
Teleport an arbitrary qubit from sender to receiver; this is the sender side.
"""

from netqasm.logging.output import get_new_app_logger
from netqasm.sdk import EPRSocket, Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox import set_qubit_state
from common import write_density_matrix_to_log


def main(phi, theta, app_config=None):
    """
    Application main function for the sender.
    """

    app_logger = get_new_app_logger(app_name=app_config.app_name, log_config=app_config.log_config)
    app_logger.log("sender starts")
    app_logger.log(f"phi = {phi}")
    app_logger.log(f"theta = {theta}")

    app_logger.log("sender creates classical socket")
    socket = Socket("sender", "receiver", log_config=app_config.log_config)

    app_logger.log("sender creates quantum socket")
    epr_socket = EPRSocket("receiver")

    app_logger.log("sender creates qasm connection")
    sender = NetQASMConnection("sender", log_config=app_config.log_config, epr_sockets=[epr_socket])

    with sender:

        app_logger.log("sender creates qubit to teleport")
        teleported_qubit = Qubit(sender)
        set_qubit_state(teleported_qubit, phi, theta)
        sender.flush()

        app_logger.log("sender density matrix of teleported qubit")
        density_matrix = get_qubit_state(teleported_qubit)
        write_density_matrix_to_log(app_logger, density_matrix)

        app_logger.log("sender creates entanglement with receiver")
        entangled_qubit = epr_socket.create_keep()[0]

        app_logger.log("sender performs teleportation")
        teleported_qubit.cnot(entangled_qubit)
        teleported_qubit.H()
        measurement_1 = teleported_qubit.measure()
        measurement_2 = entangled_qubit.measure()

    correction = (int(measurement_1), int(measurement_2))
    app_logger.log(f"sender sends correction message {correction} to receiver")
    socket.send_structured(StructuredMessage("correction", correction))

    return "sender finishes"
