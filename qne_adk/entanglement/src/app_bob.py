"""
Generate entanglement between Alice and Bob; this is Bob's side.
"""

from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection
from netqasm.sdk import EPRSocket


def main(app_config=None):
    """
    Application main function for Bob.
    """

    app_logger = get_new_app_logger(app_name=app_config.app_name, log_config=app_config.log_config)
    app_logger.log("bob main")

    epr_socket = EPRSocket("alice")

    bob = NetQASMConnection(
        "bob",
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )
    with bob:
        q_ent = epr_socket.create()[0]
        measurement = q_ent.measure()

    app_logger.log(f"bob outcome is {measurement}")

    return f"bob measurement is: {measurement}"
