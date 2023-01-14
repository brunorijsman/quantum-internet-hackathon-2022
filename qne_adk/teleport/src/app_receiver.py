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
        q_ent = epr_socket.recv_keep()[0]
        receiver.flush()

        m1, m2 = socket.recv_structured().payload
        app_logger.log(f"receiver receives correction ({m1}, {m2}) from sender")

        if m2 == 1:
            app_logger.log("receiver performs X correction")
            q_ent.X()
        else:
            app_logger.log("receiver does not perform X correction")
        if m1 == 1:
            app_logger.log("receiver performs Z correction")
            q_ent.Z()
        else:
            app_logger.log("receiver does not perform Z correction")
        receiver.flush()

        dm = get_qubit_state(q_ent)
        app_logger.log(f"receiver density matrix of teleported qubit is {dm}")

    return "receiver finishes"
