from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, get_qubit_state
from netqasm.sdk import Qubit

from datetime import datetime


def to_qiskit_qubit_nr(nr_qubits, qne_qubit_nr):
    return nr_qubits - 1 - qne_qubit_nr


def apply_qft(app_logger, conn, qubits, nr_qubits, value):
    app_logger.log("apply qft")
    apply_qft_value(app_logger, conn, qubits, nr_qubits, value)
    apply_qft_rotations(app_logger, conn, qubits, nr_qubits, nr_qubits)
    apply_qft_swaps(app_logger, conn, qubits, nr_qubits)


def apply_qft_value(app_logger, conn, qubits, nr_qubits, value):
    app_logger.log(f"apply qft value {nr_qubits=} {value=}")
    for qne_qubit_nr in range(nr_qubits):
        bit_value = value & 1
        value >>= 1
        app_logger.log(f"bit {qne_qubit_nr} = {bit_value}")
        if bit_value:
            qiskit_qubit_nr = to_qiskit_qubit_nr(nr_qubits, qne_qubit_nr)
            app_logger.log(f"X gate qubit {qiskit_qubit_nr}")
            qubits[qiskit_qubit_nr].X()


def apply_qft_rotations(app_logger, conn, qubits, nr_qubits, remaining_nr_qubits):
    if remaining_nr_qubits == 0:
        return
    app_logger.log(f"apply qft rotations {nr_qubits=} {remaining_nr_qubits=}")
    remaining_nr_qubits -= 1
    h_qubit_nr = to_qiskit_qubit_nr(nr_qubits, remaining_nr_qubits)
    app_logger.log(f"hadamard qubit {h_qubit_nr}")
    qubits[h_qubit_nr].H()
    for i in range(remaining_nr_qubits):
        ctrl_qubit_nr = to_qiskit_qubit_nr(nr_qubits, remaining_nr_qubits)
        target_qubit_nr = to_qiskit_qubit_nr(nr_qubits, i)
        denominator = remaining_nr_qubits - i
        app_logger.log(f"controlled phase control qubit {ctrl_qubit_nr} and target qubit {target_qubit_nr} by angle pi/{2 ** denominator}")
        qubits[ctrl_qubit_nr].crot_Z(qubits[target_qubit_nr], n=1, d=denominator)
    apply_qft_rotations(app_logger, conn, qubits, nr_qubits, remaining_nr_qubits)


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
