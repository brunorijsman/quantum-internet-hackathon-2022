"""
QNE-ADK application distributed quantum Fourier transformation on two processors.
This is the program for the second of two processors.
"""

import processor


def main(app_config=None):
    """
    Main function for the QNE-ADK quantum Fourier transformation running on the first of two
    processors.
    """
    agent_processor = processor.Processor(
        app_config=app_config, nr_processors=2, total_nr_qubits=4, processor_index=1
    )
    agent_processor.agent_processor_main()
