"""
Teleport an arbitrary qubit from sender to receiver; this is the sender side.
"""

from netqasm.logging.output import get_new_app_logger
from netqasm.sdk import EPRSocket, Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox import set_qubit_state


def main(phi, theta, app_config=None):
    """
    Application main function for the sender.
    """

    app_logger = get_new_app_logger(app_name=app_config.app_name, log_config=app_config.log_config)
    app_logger.log("sender starts")

    app_logger.log("sender creates classical socket")
    socket = Socket("sender", "receiver", log_config=app_config.log_config)

    app_logger.log("sender creates quantum socket")
    epr_socket = EPRSocket("receiver")

    app_logger.log("sender creates qasm connection")
    sender = NetQASMConnection("sender", log_config=app_config.log_config, epr_sockets=[epr_socket])

    with sender:

        app_logger.log("sender creates qubit to teleport")
        q = Qubit(sender)
        set_qubit_state(q, phi, theta)
        sender.flush()

        dm = get_qubit_state(q)
        app_logger.log(f"sender density matrix of teleported qubit is {dm}")
        sender.flush()

        app_logger.log("sender creates entanglement with receiver")
        q_ent = epr_socket.create_keep()[0]

        app_logger.log("sender performs teleportation")
        q.cnot(q_ent)
        q.H()
        m1 = q.measure()
        m2 = q_ent.measure()

    correction = (int(m1), int(m2))
    app_logger.log(f"sender sends correction message {correction} to receiver")
    socket.send_structured(StructuredMessage("correction", correction))

    return "sender finishes"
