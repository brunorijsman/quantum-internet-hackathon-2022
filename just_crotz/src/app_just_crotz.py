from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, get_qubit_state
from netqasm.sdk import Qubit

from datetime import datetime


def apply_crotz(app_logger, conn, qubits, pi_fraction):
    app_logger.log("apply crotz")
    app_logger.log(f"controlled phase control qubit 0 and target qubit 1 "
                   f"by angle pi/{pi_fraction}")
    qubits[0].crot_Z(qubits[1], n=1, d=pi_fraction)


def main(app_config=None):
    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("just crotz starts")
    conn = NetQASMConnection("just_crotz",
                             log_config=app_config.log_config,
                             epr_sockets=[],
                             max_qubits=2)
    with conn:
        app_logger.log("just_crotz creates register of 2 qubits")
        qubits = {}
        qubits[0] = Qubit(conn)
        qubits[1] = Qubit(conn)
        app_logger.log("Initialize control qubit 0")
        qubits[0].X()   # |1>
        app_logger.log("Initialize target qubit 1")
        qubits[1].H()   # |+>
        app_logger.log("Initialize pi_fraction")
        pi_fraction = 3    # 2 ** 3 = 8
        apply_crotz(app_logger, conn, qubits, pi_fraction)
        conn.flush()
        density_matrix = get_qubit_state(qubits[0], reduced_dm=False)
        app_logger.log("Density matrix:")
        n = 2
        for r in range(n*n):
            line = ""
            for c in range(n*n):
                value = density_matrix[r][c]
                rv = value.real
                iv = value.imag
                line += f"{rv:>6.3f} {iv:>6.3f}j    "
            app_logger.log(line)
