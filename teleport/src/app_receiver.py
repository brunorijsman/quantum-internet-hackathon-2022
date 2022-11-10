from netqasm.sdk.external import NetQASMConnection
from netqasm.sdk import EPRSocket


def main(app_config=None):
    # Specify an EPR socket to Sender
    epr_socket = EPRSocket("Sender")

    receiver = NetQASMConnection(
        "Receiver",
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )
    with receiver:
        # Receive an entangled pair using the EPR socket to Sender
        q_ent = epr_socket.recv()[0]
        # Measure the qubit
        m = q_ent.measure()
    # Print the outcome
    print(f"Receiver's outcome is: {m}")
