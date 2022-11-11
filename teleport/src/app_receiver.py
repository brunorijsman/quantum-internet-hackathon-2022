from netqasm.sdk.external import NetQASMConnection
from netqasm.sdk import EPRSocket
import sys


def main(app_config=None):
    print("receiver main", file=sys.stderr)
    # Specify an EPR socket to sender
    epr_socket = EPRSocket("sender")

    receiver = NetQASMConnection(
        "receiver",
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )
    with receiver:
        # Receive an entangled pair using the EPR socket to sender
        q_ent = epr_socket.recv()[0]
        # Measure the qubit
        m = q_ent.measure()
    # Print the outcome
    print(f"receiver's outcome is: {m}", file=sys.stderr)
    return f"receiver measurement is: {m}"
