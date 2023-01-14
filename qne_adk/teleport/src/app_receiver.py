"""
Teleport an arbitrary qubit from sender to receiver; this is the receiver side.
"""

from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk import EPRSocket


def main(app_config=None):
    """
    Application main function for the receiver.
    """

    app_logger = get_new_app_logger(app_name=app_config.app_name, log_config=app_config.log_config)
    app_logger.log("receiver starts")

    app_logger.log("receiver creates classical socket")
    socket = Socket("receiver", "sender", log_config=app_config.log_config)

    app_logger.log("receiver creates quantum socket")
    epr_socket = EPRSocket("sender")

    app_logger.log("receiver creates qasm connection")
    receiver = NetQASMConnection(
        "receiver", log_config=app_config.log_config, epr_sockets=[epr_socket]
    )

    with receiver:

        app_logger.log("receiver creates entanglement with sender")
        entangled_qubit = epr_socket.recv_keep()[0]
        receiver.flush()

        measurement_1, measurement_2 = socket.recv_structured().payload
        app_logger.log(
            f"receiver receives correction ({measurement_1}, {measurement_2}) from sender"
        )

        if measurement_2 == 1:
            app_logger.log("receiver performs X correction")
            entangled_qubit.X()
        else:
            app_logger.log("receiver does not perform X correction")
        if measurement_1 == 1:
            app_logger.log("receiver performs Z correction")
            entangled_qubit.Z()
        else:
            app_logger.log("receiver does not perform Z correction")
        receiver.flush()

        density_matrix = get_qubit_state(entangled_qubit)
        app_logger.log(f"receiver density matrix of teleported qubit is {density_matrix}")

    return "receiver finishes"
