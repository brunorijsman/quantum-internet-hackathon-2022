"""
Send a classical message to the receiver.
"""

from netqasm.logging.output import get_new_app_logger
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket


def main(app_config=None):
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
    _sender = NetQASMConnection(
        "sender", log_config=app_config.log_config, epr_sockets=[epr_socket]
    )

    app_logger.log("sender sends 'hello' to receiver")
    socket.send("hello")

    return "sender finishes"
