"""
Unit tests for quantum Fourier transformation (monolithic and distributed) implemented in Qiskit.
"""
from math import sqrt
from qft import DistributedQFT, QFT
from quantum_computer import Method
from utils import state_vectors_are_same
from qiskit.quantum_info import Statevector


ONE_OVER_SQRT2 = 1.0 / sqrt(2.0)
PLUS_STATE = Statevector([ONE_OVER_SQRT2, ONE_OVER_SQRT2])
MINUS_STATE = Statevector([ONE_OVER_SQRT2, -1.0 * ONE_OVER_SQRT2])
PLUS_PLUS_STATE = PLUS_STATE.tensor(PLUS_STATE)
PLUS_PLUS_PLUS_PLUS_STATE = PLUS_PLUS_STATE.tensor(PLUS_PLUS_STATE)


def test_monolithic_qft_one_qubit():
    """
    Test monolothic (non-distributed) QFT, one qubit. A single-qubit QFT is the same as a
    Hadamard gate.
    """
    qft = QFT(total_nr_qubits=1)
    qft.run(input_number=0)
    statevector = qft.main_statevector()
    assert state_vectors_are_same(statevector, PLUS_STATE)
    qft.run(input_number=1)
    statevector = qft.main_statevector()
    assert state_vectors_are_same(statevector, MINUS_STATE)


def test_monolithic_qft_two_qubits():
    """
    Test monolothic (non-distributed) QFT, two qubits.
    """
    qft = QFT(total_nr_qubits=2)
    qft.run(input_number=0)
    statevector = qft.main_statevector()
    assert state_vectors_are_same(statevector, PLUS_PLUS_STATE)


def test_monolithic_qft_four_qubits():
    """
    Test monolothic (non-distributed) QFT, four qubits.
    """
    qft = QFT(total_nr_qubits=4)
    qft.run(input_number=0)
    statevector = qft.main_statevector()
    assert state_vectors_are_same(statevector, PLUS_PLUS_PLUS_PLUS_STATE)


def test_dqft_same_as_qft():
    """
    Test whether statevector computed by a distributed QFT is the same as the one computed by a
    monolothic QFT.
    """
    nr_processors = 2
    test_cases = [
        (Method.TELEPORT, 2, 2, 0),
        (Method.TELEPORT, 2, 2, 1),
        (Method.TELEPORT, 2, 4, 0),
        (Method.TELEPORT, 2, 4, 3),
        (Method.TELEPORT, 2, 4, 12),
        (Method.TELEPORT, 2, 4, 15),
        (Method.TELEPORT, 2, 6, 3),
        (Method.TELEPORT, 3, 6, 11),
        (Method.CAT_STATE, 2, 4, 9),
    ]
    for method, nr_processors, total_nr_qubits, input_number in test_cases:
        qft = QFT(total_nr_qubits)
        qft.run(input_number)
        qft_statevector = qft.main_statevector()
        dqft = DistributedQFT(nr_processors, total_nr_qubits, method)
        dqft.run(input_number)
        dqft_statevector = qft.main_statevector()
        assert state_vectors_are_same(qft_statevector, dqft_statevector)
