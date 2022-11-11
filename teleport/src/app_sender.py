from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection
from netqasm.sdk import EPRSocket


def main(phi, theta, app_config=None):

    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("sender main")

    epr_socket = EPRSocket("receiver")

    sender = NetQASMConnection(
        "sender",
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )
    with sender:
        q_ent = epr_socket.create()[0]
        m = q_ent.measure()

    app_logger.log(f"sender outcome is {m}")

    return f"sender measurement is: {m}"
