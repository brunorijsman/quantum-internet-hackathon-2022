"""
Unit tests for quantum Fourier transformation (monolithic and distributed) implemented in Qiskit.
"""
from math import sqrt
from qft import QFT
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
