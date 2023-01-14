import processor


def main(app_config=None):
    proc = processor.Processor(
        app_config=app_config, nr_processors=2, total_nr_qubits=4, processor_index=1
    )
    proc.run()
