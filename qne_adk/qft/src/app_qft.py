"""
Monolithic (non-distributed) implementation of the quantum Fourier transformation in QNE-ADK.
"""

from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.external import get_qubit_state, NetQASMConnection
from netqasm.sdk import Qubit
from common import write_density_matrix_to_log, write_density_matrix_to_file


def apply_qft(app_logger, connection, qubits, input_size, input_value):
    """
    Apply a quantum Fourier transformation.

    Parameters
    ----------
    app_logger: The application logger.
    connection: The NetQASM connection.
    qubits: A map of Qubit objects, indexed by qubit index number. After this function returns,
        these qubits contain the quantum state that is the result of the QFT.
    input_size: The number of qubits in the input value for the QFT.
    input_value: Assume that all input values for qubits are |0> or |1>, treat these qubits
        as the binary encoding of the input value as a number.
    """
    app_logger.log("apply qft")
    assert len(qubits) == input_size
    apply_qft_value(app_logger, qubits, input_size, input_value)
    apply_qft_rotations(app_logger, connection, qubits, input_size)
    apply_qft_swaps(app_logger, qubits, input_size)


def apply_qft_value(app_logger, qubits, input_size, input_value):
    """
    Apply a circuit that sets the qubits to the |0> and |1> values determined by the input_value.

    Parameters
    ----------
    app_logger: The application logger.
    qubits: A map of Qubit objects, indexed by qubit index number. After this function returns,
        these qubits are set to |0> or |1>, according to the input_value.
    input_size: The number of qubits in the input value for the QFT.
    input_value: Assume that all input values for qubits are |0> or |1>, treat these qubits
        as the binary encoding of the input value as a number.
    """
    app_logger.log(f"apply qft value {input_size=} {input_value=}")
    assert len(qubits) == input_size
    for bit_index in range(input_size):
        bit = input_value & 1
        input_value >>= 1
        app_logger.log(f"bit {bit_index} = {bit}")
        if bit:
            app_logger.log(f"X gate qubit {bit_index}")
            qubits[bit_index].X()


def apply_qft_rotations(app_logger, connection, qubits, remaining_nr_qubits):
    """
    Apply the controlled Z-rotations gates as part of the quantum Fourier transformation.

    Parameters
    ----------
    app_logger: The application logger.
    connection: The NetQASM connection.
    qubits: A map of Qubit objects, indexed by qubit index number. After this function returns,
        these qubits contain the quantum state that is the result of the QFT.
    remaining_nr_qubits: The remaining number of qubits for which to do the controlled Z-rotation.
    """
    if remaining_nr_qubits == 0:
        return
    app_logger.log(f"apply qft rotations {remaining_nr_qubits=}")
    remaining_nr_qubits -= 1
    app_logger.log(f"hadamard qubit {remaining_nr_qubits}")
    qubits[remaining_nr_qubits].H()
    for qubit_index in range(remaining_nr_qubits):
        app_logger.log(
            f"controlled phase control qubit {qubit_index} and target qubit {remaining_nr_qubits} "
            f"by angle pi/{2 ** (remaining_nr_qubits - qubit_index)}"
        )
        qubits[qubit_index].crot_Z(
            qubits[remaining_nr_qubits], n=1, d=remaining_nr_qubits - qubit_index
        )
    apply_qft_rotations(app_logger, connection, qubits, remaining_nr_qubits)


def apply_qft_swaps(app_logger, qubits, nr_qubits):
    """
    Apply the controlled Z-rotations gates as part of the quantum Fourier transformation.

    Parameters
    ----------
    app_logger: The application logger.
    connection: The NetQASM connection.
    qubits: A map of Qubit objects, indexed by qubit index number. After this function returns,
        these qubits contain the quantum state that is the result of the QFT.
    nr_qubits: The number of qubits.
    """
    app_logger.log("apply qft swaps")
    assert len(qubits) == nr_qubits
    for qubit_index_1 in range(nr_qubits // 2):
        qubit_index_2 = nr_qubits - qubit_index_1 - 1
        app_logger.log(f"swap qubit {qubit_index_1} with qubit {qubit_index_2}")
        # NetQASM does not yet natively support a SWAP gate; instead construct a SWAP gate out of
        # three CNOT gates as described here: https://algassert.com/post/1717
        # See issue #47 for details: https://github.com/QuTech-Delft/netqasm/issues/47
        qubits[qubit_index_1].cnot(qubits[qubit_index_2])
        qubits[qubit_index_2].cnot(qubits[qubit_index_1])
        qubits[qubit_index_1].cnot(qubits[qubit_index_2])


def main(app_config=None):
    """
    The application main function.
    """
    # TODO: Make input_size and input_value application parameters
    app_logger = get_new_app_logger(app_name=app_config.app_name, log_config=app_config.log_config)
    app_logger.log("qft starts")
    input_size = 3
    app_logger.log(f"{input_size=}")
    input_value = 1
    app_logger.log(f"{input_value=}")
    connection = NetQASMConnection(
        "qft", log_config=app_config.log_config, epr_sockets=[], max_qubits=input_size
    )
    with connection:
        app_logger.log(f"qft creates register of {input_size} qubits")
        qubits = {}
        for qubit_index in range(input_size):
            qubits[qubit_index] = Qubit(connection)
        apply_qft(app_logger, connection, qubits, input_size, input_value)
        connection.flush()
        density_matrix = get_qubit_state(qubits[0], reduced_dm=False)
        app_logger.log("qft output density matrix")
        write_density_matrix_to_log(app_logger, density_matrix)
        write_density_matrix_to_file(app_logger, density_matrix, input_size, input_value)
    app_logger.log("qft ends")
    return {"n": input_size, "value": input_value}
