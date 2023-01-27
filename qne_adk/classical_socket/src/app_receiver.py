"""
Receive a classical message from the sender.
"""

from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, Socket
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
    _receiver = NetQASMConnection(
        "receiver", log_config=app_config.log_config, epr_sockets=[epr_socket]
    )

    message = socket.recv()
    app_logger.log(f"receiver receives messate {message} from sender")

    return "receiver finishes"
