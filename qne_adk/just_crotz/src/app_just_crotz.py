"""
Apply a control rotation-Z gate (CROTZ) gate.
"""
from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import NetQASMConnection, get_qubit_state
from netqasm.sdk import Qubit


def apply_crotz(app_logger, control_qubit, target_qubit, rotation_pi_fraction):
    """
    Apply a CROTZ gate.

    Parameters
    ----------
    app_logger: The application logger.
    control_qubit: The control qubit.
    target_qubit: The target qubit.
    rotation_pi_fraction: The rotation angle, as a fraction of pi.
    """
    app_logger.log("apply crotz")
    app_logger.log(
        f"controlled phase control qubit 0 and target qubit 1 "
        f"by angle pi/{rotation_pi_fraction}"
    )
    control_qubit.crot_Z(target_qubit, n=1, d=rotation_pi_fraction)


def main(app_config=None):
    """
    The application main function.
    """
    app_logger = get_new_app_logger(app_name=app_config.app_name, log_config=app_config.log_config)
    app_logger.log("just crotz starts")
    conn = NetQASMConnection(
        "just_crotz", log_config=app_config.log_config, epr_sockets=[], max_qubits=2
    )
    with conn:
        app_logger.log("just_crotz creates register of 2 qubits")
        qubits = {}
        qubits[0] = Qubit(conn)
        qubits[1] = Qubit(conn)
        app_logger.log("Initialize control qubit 0")
        qubits[0].X()  # |1>
        app_logger.log("Initialize target qubit 1")
        qubits[1].H()  # |+>
        app_logger.log("Initialize pi_fraction")
        pi_fraction = 3  # 2 ** 3 = 8
        apply_crotz(app_logger, qubits[0], qubits[1], pi_fraction)
        conn.flush()
        density_matrix = get_qubit_state(qubits[0], reduced_dm=False)
        app_logger.log("Density matrix:")
        size = 2
        for row_nr in range(size * size):
            line = ""
            for col_nr in range(size * size):
                value = density_matrix[row_nr][col_nr]
                line += f"{value.real:>6.3f} {value.imag:>6.3f}j    "
            app_logger.log(line)
