from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection
from netqasm.sdk import Qubit


def main(app_config=None):

    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("qft starts")

    n = 4
    app_logger.log(f"{n=}")
    value = 9
    app_logger.log(f"{value=}")

    conn = NetQASMConnection("qft",
                             log_config=app_config.log_config,
                             epr_sockets=[],
                             max_qubits=n)
    with conn:

        app_logger.log(f"qft creates register of {n} qubits")
        q = {}
        for i in range(n):
            q[i] = Qubit(conn)

    app_logger.log("qft ends")

    return {
        "n": n,
        "value": value
    }
