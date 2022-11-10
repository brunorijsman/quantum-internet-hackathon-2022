from netqasm.sdk.external import NetQASMConnection
from netqasm.sdk import EPRSocket


def main(app_config=None):
    # Specify an EPR socket to Receiver
    epr_socket = EPRSocket("Receiver")

    sender = NetQASMConnection(
        "Sender",
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )
    with sender:
        # Create an entangled pair using the EPR socket to Receiver
        q_ent = epr_socket.create()[0]
        # Measure the qubit
        m = q_ent.measure()
    # Print the outcome
    print(f"Sender's outcome is: {m}")
