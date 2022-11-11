from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection
from netqasm.sdk import EPRSocket


def main(app_config=None):

    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("receiver main")

    epr_socket = EPRSocket("sender")

    receiver = NetQASMConnection(
        "receiver",
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )
    with receiver:
        q_ent = epr_socket.recv()[0]
        m = q_ent.measure()

    app_logger.log(f"receiver outcome is {m}")

    return f"receiver measurement is: {m}"
