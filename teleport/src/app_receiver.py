from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket


def main(app_config=None):

    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("receiver starts")

    app_logger.log("receiver creates classical socket")
    socket = Socket("receiver", "sender", log_config=app_config.log_config)

    app_logger.log("receiver creates quantum socket")
    epr_socket = EPRSocket("sender")

    app_logger.log("receiver creates qasm connection")
    receiver = NetQASMConnection("receiver",
                                 log_config=app_config.log_config,
                                 epr_sockets=[epr_socket])

    with receiver:

        app_logger.log("receiver creates entanglement with sender")
        q_ent = epr_socket.recv()[0]

    return f"receiver finishes"
