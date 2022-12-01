import processor
from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection
from netqasm.sdk import EPRSocket


def main(app_config=None):

    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("alice main")

    proc = processor.Processor(nr_processors=2, total_nr_qubits=4, processor_index=0,
                               logger=app_logger)

    epr_socket = EPRSocket("bob")

    alice = NetQASMConnection(
        "alice",
        log_config=app_config.log_config,
        epr_sockets=[epr_socket],
    )
    with alice:
        q_ent = epr_socket.recv()[0]
        m = q_ent.measure()

    app_logger.log(f"alice outcome is {m}")

    return f"alice measurement is: {m}"
