from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, get_qubit_state
from netqasm.sdk import Qubit

from datetime import datetime


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
        app_logger.log(f"controlled phase control qubit {i} and target qubit {n} by angle pi/{2 ** (n - i)}")
        qubits[i].crot_Z(qubits[n], n=1, d=n-i)
    apply_qft_rotations(app_logger, conn, qubits, n)


def apply_qft_swaps(app_logger, conn, qubits, n):
    app_logger.log("apply qft swaps")
    for i1 in range(n//2):
        i2 = n - i1 - 1
        app_logger.log(f"swap qubit {i1} with qubit {i2} (XXX not implemented)")
        # TODO


def main(app_config=None):
    app_logger = get_new_app_logger(app_name=app_config.app_name,
                                    log_config=app_config.log_config)
    app_logger.log("qft starts")
    n = 3
    app_logger.log(f"{n=}")
    value = 1
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
        conn.flush()
        density_matrix = get_qubit_state(qubits[0], reduced_dm=False)
        app_logger.log(f"density matrix for qubit {i} = {density_matrix}")
        app_logger.log("writing density matrix to qne_dm.txt")
        dir = "/Users/brunorijsman/git-personal/quantum-internet-hackathon-2022"
        with open(f"{dir}/qne_dm.txt", "w") as f:
            print(f"QNE-ADM density matrix", file=f)
            print(f"{datetime.now()}", file=f)
            print(f"{n}", file=f)
            print(f"{value}", file=f)
            print("False", file=f)
            for r in range(n):
                for c in range(n):
                    print(density_matrix[r][c], file=f)
    app_logger.log("qft ends")
    return {
        "n": n,
        "value": value
    }
