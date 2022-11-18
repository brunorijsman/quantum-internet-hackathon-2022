from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, get_qubit_state
from netqasm.sdk import Qubit


def apply_qft(app_logger, conn, qubits, n, value):
    app_logger.log("apply qft")
    apply_qft_value(app_logger, conn, qubits, n, value)
    apply_qft_rotations(app_logger, conn, qubits, n)
    apply_qft_swaps(app_logger, conn, qubits, n)


def apply_qft_value(app_logger, conn, qubits, n, value):
    app_logger.log(f"apply qft value {n=} {value=}")
    for i in range(n):
        bit = value & 1
        value >>= 1
        app_logger.log(f"bit {i} = {bit}")
        if bit:
            app_logger.log(f"X gate qubit {i}")
            qubits[i].X()


def apply_qft_rotations(app_logger, conn, qubits, n):
    if n == 0:
        return
    app_logger.log(f"apply qft rotations {n=}")
    n -= 1
    app_logger.log(f"hadamard qubit {n}")
    qubits[n].H()
    for i in range(n):
        app_logger.log(f"controlled phase qubits {i} and {n} by angle pi/{2 ** (n - i)}")
        qubits[i].crot_Z(qubits[n], n=1, d=n-i)
    apply_qft_rotations(app_logger, conn, qubits, n)


def apply_qft_swaps(app_logger, conn, qubits, n):
    app_logger.log("apply qft swaps")
    for i1 in range(n//2):
        i2 = n - i1 - 1
        app_logger.log(f"swap qubit {i1} with qubit {i2}")
        # TODO


def main(app_config=None):
    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("qft starts")
    n = 2
    app_logger.log(f"{n=}")
    value = 3
    app_logger.log(f"{value=}")
    conn = NetQASMConnection("qft",
                             log_config=app_config.log_config,
                             epr_sockets=[],
                             max_qubits=n)
    with conn:
        app_logger.log(f"qft creates register of {n} qubits")
        qubits = {}
        for i in range(n):
            qubits[i] = Qubit(conn)
        apply_qft(app_logger, conn, qubits, n, value)
        # qubits[0].H()
        # qubits[1].H()
        conn.flush()
        for i in range(n):
            state = get_qubit_state(qubits[i], reduced_dm=False)
            app_logger.log(f"density matrix for qubit {i} = {state}")
    app_logger.log("qft ends")
    return {
        "n": n,
        "value": value
    }
