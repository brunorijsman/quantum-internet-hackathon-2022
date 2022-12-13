"""
A base class for common behavior between local and distributed circuits.
"""

from qiskit_textbook.tools import array_to_latex
from qiskit import Aer, QuantumCircuit, transpile
from qiskit.quantum_info import DensityMatrix
from qiskit.visualization import plot_bloch_multivector, plot_state_city


class CircuitBase:
    """
    A base class for common behavior between local and distributed circuits.
    """

    def __init__(self, total_nr_qubits):
        """
        Constructor.

        Parameters
        ----------
        total_nr_qubits: The total number of main qubits in the circuit (not including ancillary
            qubits, if any)
        """
        self.total_nr_qubits = total_nr_qubits
        self.qc = QuantumCircuit()
        self.qc_with_input = None
        self.simulator = None
        self.result = None

    def circuit_diagram(self, with_input=False):
        """
        Return a circuit diagram suitable for displaying in a Jupyter notebook.

        Parameters
        ---------
        with_input: If with_input is False, display the circuit with all input qubits initialized to
            their default value zero. If with_input is True, display the circuit with the input
            values that were specified in the call to the run function (this assumes that the run
            function was previously called; if not, this function returns None).

        Returns
        -------
        The circuit diagram that can be displayed in a Jupyter notebook.
        """
        if with_input:
            if self.qc_with_input is None:
                return None
            return self.qc_with_input.draw(fold=False, output="mpl")
        return self.qc.draw(fold=False, output="mpl")

    def statevector(self):
        """
        Returns
        -------
        The statevector of the circuit (in the form of a numpy array) resulting from the most recent
        run invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return self.result.get_statevector().data

    def statevector_latex(self):
        """
        Returns
        -------
        The statevector of the circuit (in the form of a Latex vector) resulting from the most
        recent run invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return array_to_latex(self.result.get_statevector())

    def bloch_multivector(self):
        """
        Returns
        -------
        The Block multivector diagram (that can be displayed in a Jupyter notebook) resulting from
        the most recent run invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return plot_bloch_multivector(self.result.get_statevector())

    def density_matrix(self):
        """
        Returns
        -------
        The density matrix (in the form of a numpy matrix) resulting from the most recent run
        invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return DensityMatrix(self.result.get_statevector())

    def density_matrix_city(self):
        """
        The density matrix city diagram (that can be displayed in a Jupyter notebook) resulting from
        the most recent run invocation, or None if run was never invoked.
        """
        if self.result is None:
            return None
        return plot_state_city(self.result.get_statevector())

    def run(self, input_value, shots=10000):
        """
        Run the quantum circuit.

        Parameters
        ----------
        input_value: An integer representing the input value for the quantum circuit. This value is
            converted to a binary value, and the bits in this binary value are used as zero or one
            initial values for the main register(s) in the cluster.
            TODO Also allow arbitrary complex initial values for each qubit.
        shots: How many times the circuit must be executed to collect statistics.
        """
        self.qc_with_input = QuantumCircuit(self.total_nr_qubits)
        # TODO: This initialization is not correct for clusters
        bin_value = bin(input_value)[2:].zfill(self.total_nr_qubits)
        self.qc_with_input.initialize(bin_value, self.qc_with_input.qubits)
        self.qc_with_input = self.qc_with_input.compose(self.qc)
        self.simulator = Aer.get_backend("aer_simulator")
        self.qc_with_input.save_statevector()
        self.qc_with_input = transpile(self.qc_with_input, self.simulator)
        self.result = self.simulator.run(self.qc_with_input, shots=shots).result()
