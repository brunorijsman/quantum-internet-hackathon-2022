from datetime import datetime


def reverse_bit_order(nr_bits, value):
    reversed_value = 0
    for _ in range(nr_bits):
        bit = value & 1
        value >>= 1
        reversed_value <<= 1
        reversed_value |= bit
    return reversed_value


def density_matrix_reverse_bit_order(nr_qubits, dm):
    dm_size = nr_qubits ** 2
    reversed_dm = []
    for row_index in range(dm_size):
        row = []
        for column_index in range(dm_size):
            reversed_row_index = reverse_bit_order(nr_qubits, row_index)
            reversed_column_index = reverse_bit_order(nr_qubits, column_index)
            value = dm[reversed_row_index][reversed_column_index]
            row.append(value)
        reversed_dm.append(row)
    return reversed_dm


def density_matrix_pretty_print(density_matrix):
    nr_qubits = len(density_matrix.dims())
    for dimension in density_matrix.dims():
        assert dimension == 2, 'dimension of each subsystem must be 2'
    dm_size = 2 ** nr_qubits
    for r in range(dm_size):
        for c in range(dm_size):
            value = density_matrix.data[r][c]
            rv = value.real
            iv = value.imag
            print(f"{rv:>6.3f} {iv:>6.3f}j    ", end="")
        print()


def density_matrix_print_to_file(file_name, producer_name, nr_qubits, dm, input, swaps):
    with open(file_name, 'w') as f:
        print(producer_name, file=f)
        print(f'{datetime.now()}', file=f)
        print(f'{nr_qubits}', file=f)
        print(f'{input}', file=f)
        print(f'{swaps}', file=f)
        for r in range(nr_qubits):
            for c in range(nr_qubits):
                print(dm[r][c], file=f)
