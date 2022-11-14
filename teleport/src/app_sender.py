from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket


def main(phi, theta, app_config=None):

    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("sender starts")

    app_logger.log("sender creates classical socket")
    socket = Socket("sender", "receiver", log_config=app_config.log_config)

    app_logger.log("sender creates quantum socket")
    epr_socket = EPRSocket("receiver")

    app_logger.log("sender creates qasm connection")
    sender = NetQASMConnection("sender",
                               log_config=app_config.log_config,
                               epr_sockets=[epr_socket])

    with sender:

        app_logger.log("sender creates entanglement with receiver")
        q_ent = epr_socket.create()[0]

    return f"sender finishes"
